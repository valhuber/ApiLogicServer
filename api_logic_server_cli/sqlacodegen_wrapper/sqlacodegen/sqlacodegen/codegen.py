"""Contains the code generation logic and helper functions."""
from __future__ import unicode_literals, division, print_function, absolute_import

import inspect
import re
import sys
from collections import defaultdict
from importlib import import_module
from inspect import ArgSpec
from keyword import iskeyword

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy import (
    Enum, ForeignKeyConstraint, PrimaryKeyConstraint, CheckConstraint, UniqueConstraint, Table,
    Column, Float)
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.types import Boolean, String
from sqlalchemy.util import OrderedDict

# The generic ARRAY type was introduced in SQLAlchemy 1.1
from api_logic_server_cli.create_from_model.model_creation_services import Resource, ResourceRelationship, \
    ResourceAttribute

try:
    from sqlalchemy import ARRAY
except ImportError:
    from sqlalchemy.dialects.postgresql import ARRAY

# SQLAlchemy 1.3.11+
try:
    from sqlalchemy import Computed
except ImportError:
    Computed = None

# Conditionally import Geoalchemy2 to enable reflection support
try:
    import geoalchemy2  # noqa: F401
except ImportError:
    pass

_re_boolean_check_constraint = re.compile(r"(?:(?:.*?)\.)?(.*?) IN \(0, 1\)")
_re_column_name = re.compile(r'(?:(["`]?)(?:.*)\1\.)?(["`]?)(.*)\2')
_re_enum_check_constraint = re.compile(r"(?:(?:.*?)\.)?(.*?) IN \((.+)\)")
_re_enum_item = re.compile(r"'(.*?)(?<!\\)'")
_re_invalid_identifier = re.compile(r'[^a-zA-Z0-9_]' if sys.version_info[0] < 3 else r'(?u)\W')


class _DummyInflectEngine(object):
    @staticmethod
    def singular_noun(noun):
        return noun


# In SQLAlchemy 0.x, constraint.columns is sometimes a list, on 1.x onwards, always a
# ColumnCollection
def _get_column_names(constraint):
    if isinstance(constraint.columns, list):
        return constraint.columns
    return list(constraint.columns.keys())


def _get_constraint_sort_key(constraint):
    if isinstance(constraint, CheckConstraint):
        return 'C{0}'.format(constraint.sqltext)
    return constraint.__class__.__name__[0] + repr(_get_column_names(constraint))


class ImportCollector(OrderedDict):
    def add_import(self, obj):
        type_ = type(obj) if not isinstance(obj, type) else obj
        pkgname = type_.__module__

        # The column types have already been adapted towards generic types if possible, so if this
        # is still a vendor specific type (e.g., MySQL INTEGER) be sure to use that rather than the
        # generic sqlalchemy type as it might have different constructor parameters.
        if pkgname.startswith('sqlalchemy.dialects.'):
            dialect_pkgname = '.'.join(pkgname.split('.')[0:3])
            dialect_pkg = import_module(dialect_pkgname)

            if type_.__name__ in dialect_pkg.__all__:
                pkgname = dialect_pkgname
        else:
            pkgname = 'sqlalchemy' if type_.__name__ in sqlalchemy.__all__ else type_.__module__
        self.add_literal_import(pkgname, type_.__name__)

    def add_literal_import(self, pkgname, name):
        names = self.setdefault(pkgname, set())
        names.add(name)


class Model(object):
    def __init__(self, table):
        super(Model, self).__init__()
        self.table = table
        self.schema = table.schema

        # Adapt column types to the most reasonable generic types (ie. VARCHAR -> String)
        for column in table.columns:
            try:
                column.type = self._get_adapted_type(column.type, column.table.bind)
            except:
                # print('Failed to get col type for {}, {}'.format(column, column.type))
                if "sqlite_sequence" not in format(column):
                    print("#Failed to get col type for {}".format(column))

    def __str__(self):
        return f'Model for table: {self.table} (in schema: {self.schema})'

    def _get_adapted_type(self, coltype, bind):
        compiled_type = coltype.compile(bind.dialect)
        for supercls in coltype.__class__.__mro__:
            if not supercls.__name__.startswith('_') and hasattr(supercls, '__visit_name__'):
                # Hack to fix adaptation of the Enum class which is broken since SQLAlchemy 1.2
                kw = {}
                if supercls is Enum:
                    kw['name'] = coltype.name

                try:
                    new_coltype = coltype.adapt(supercls)
                except TypeError:
                    # If the adaptation fails, don't try again
                    break

                for key, value in kw.items():
                    setattr(new_coltype, key, value)

                if isinstance(coltype, ARRAY):
                    new_coltype.item_type = self._get_adapted_type(new_coltype.item_type, bind)

                try:
                    # If the adapted column type does not render the same as the original, don't
                    # substitute it
                    if new_coltype.compile(bind.dialect) != compiled_type:
                        # Make an exception to the rule for Float and arrays of Float, since at
                        # least on PostgreSQL, Float can accurately represent both REAL and
                        # DOUBLE_PRECISION
                        if not isinstance(new_coltype, Float) and \
                           not (isinstance(new_coltype, ARRAY) and
                                isinstance(new_coltype.item_type, Float)):
                            break
                except sqlalchemy.exc.CompileError:
                    # If the adapted column type can't be compiled, don't substitute it
                    break

                # Stop on the first valid non-uppercase column type class
                coltype = new_coltype
                if supercls.__name__ != supercls.__name__.upper():
                    break

        return coltype

    def add_imports(self, collector):
        if self.table.columns:
            collector.add_import(Column)

        for column in self.table.columns:
            collector.add_import(column.type)
            if column.server_default:
                if Computed and isinstance(column.server_default, Computed):
                    collector.add_literal_import('sqlalchemy', 'Computed')
                else:
                    collector.add_literal_import('sqlalchemy', 'text')

            if isinstance(column.type, ARRAY):
                collector.add_import(column.type.item_type.__class__)

        for constraint in sorted(self.table.constraints, key=_get_constraint_sort_key):
            if isinstance(constraint, ForeignKeyConstraint):
                if len(constraint.columns) > 1:
                    collector.add_literal_import('sqlalchemy', 'ForeignKeyConstraint')
                else:
                    collector.add_literal_import('sqlalchemy', 'ForeignKey')
            elif isinstance(constraint, UniqueConstraint):
                if len(constraint.columns) > 1:
                    collector.add_literal_import('sqlalchemy', 'UniqueConstraint')
            elif not isinstance(constraint, PrimaryKeyConstraint):
                collector.add_import(constraint)

        for index in self.table.indexes:
            if len(index.columns) > 1:
                collector.add_import(index)

    @staticmethod
    def _convert_to_valid_identifier(name):
        assert name, 'Identifier cannot be empty'
        if name[0].isdigit() or iskeyword(name):
            name = '_' + name
        elif name == 'metadata':
            name = 'metadata_'
        name = name.replace("$", "_S_")   # ApiLogicServer valid name fixes for superclass version (why override?)
        name = name.replace(" ", "_")
        name = name.replace("+", "_")
        name = name.replace("-", "_")

        result = _re_invalid_identifier.sub('_', name)
        return result


class ModelTable(Model):
    def __init__(self, table):
        super(ModelTable, self).__init__(table)
        self.name = self._convert_to_valid_identifier(table.name)

    def add_imports(self, collector):
        super(ModelTable, self).add_imports(collector)
        try:
            collector.add_import(Table)
        except Exception as exc:
            print("Failed to add imports {}".format(collector))


class ModelClass(Model):
    parent_name = 'Base'

    def __init__(self, table, association_tables, inflect_engine, detect_joined):
        super(ModelClass, self).__init__(table)
        self.name = self._tablename_to_classname(table.name, inflect_engine)
        self.children = []
        self.attributes = OrderedDict()
        self.foreign_key_relationships = list()
        self.rendered_model = ""                # ApiLogicServer
        self.rendered_model_relationships = ""  # appended at end ( render() )

        # Assign attribute names for columns
        for column in table.columns:
            self._add_attribute(column.name, column)

        # Add many-to-one relationships
        pk_column_names = set(col.name for col in table.primary_key.columns)
        for constraint in sorted(table.constraints, key=_get_constraint_sort_key):
            if isinstance(constraint, ForeignKeyConstraint):
                target_cls = self._tablename_to_classname(constraint.elements[0].column.table.name,
                                                          inflect_engine)
                if (detect_joined and self.parent_name == 'Base' and
                        set(_get_column_names(constraint)) == pk_column_names):
                    self.parent_name = target_cls
                else:
                    relationship_ = ManyToOneRelationship(self.name, target_cls, constraint,
                                                          inflect_engine)
                    self._add_attribute(relationship_.preferred_name, relationship_)

        # Add many-to-many relationships
        for association_table in association_tables:
            fk_constraints = [c for c in association_table.constraints
                              if isinstance(c, ForeignKeyConstraint)]
            fk_constraints.sort(key=_get_constraint_sort_key)
            target_cls = self._tablename_to_classname(
                fk_constraints[1].elements[0].column.table.name, inflect_engine)
            relationship_ = ManyToManyRelationship(self.name, target_cls, association_table)
            self._add_attribute(relationship_.preferred_name, relationship_)

    @classmethod
    def _tablename_to_classname(cls, tablename, inflect_engine):
        """
        camel-case and singlularize, with provisions for reserved word (Date) and collisions (Dates & _Dates)
        """
        tablename = cls._convert_to_valid_identifier(tablename)
        if tablename in ["Dates"]:  # ApiLogicServer
            tablename = tablename + "Classs"
        camel_case_name = ''.join(part[:1].upper() + part[1:] for part in tablename.split('_'))
        if camel_case_name in ["Dates"]:
            camel_case_name = camel_case_name + "_Classs"
        result = inflect_engine.singular_noun(camel_case_name) or camel_case_name
        if result == "CategoryTableNameTest":  # ApiLogicServer
            result = "Category"
        return result

    @staticmethod
    def _convert_to_valid_identifier(name):  # TODO review
        assert name, "Identifier cannot be empty"
        if name[0].isdigit() or iskeyword(name):
            name = "_" + name
        elif name == "metadata":
            name = "metadata_"
        name = name.replace("$", "_S_")   # ApiLogicServer valid name fixes, ModelClass version
        name = name.replace(" ", "_")
        name = name.replace("+", "_")
        name = name.replace("-", "_")

        result = _re_invalid_identifier.sub("_", name)
        return result

    def _add_attribute(self, attrname, value):
        """ add table column/relationship to attributes

        disambiguate relationship accessor names (append tablename with 1, 2...)
        """
        attrname = tempname = self._convert_to_valid_identifier(attrname)
        counter = 1
        while tempname in self.attributes:
            tempname = attrname + str(counter)
            counter += 1

        self.attributes[tempname] = value
        return tempname

    def add_imports(self, collector):
        super(ModelClass, self).add_imports(collector)

        if any(isinstance(value, Relationship) for value in self.attributes.values()):
            collector.add_literal_import('sqlalchemy.orm', 'relationship')

        for child in self.children:
            child.add_imports(collector)


class Relationship(object):
    def __init__(self, source_cls, target_cls):
        super(Relationship, self).__init__()
        self.source_cls = source_cls
        self.target_cls = target_cls
        self.kwargs = OrderedDict()


class ManyToOneRelationship(Relationship):
    def __init__(self, source_cls, target_cls, constraint, inflect_engine):
        super(ManyToOneRelationship, self).__init__(source_cls, target_cls)

        column_names = _get_column_names(constraint)
        colname = column_names[0]
        tablename = constraint.elements[0].column.table.name
        self.foreign_key_constraint = constraint
        if not colname.endswith('_id'):
            self.preferred_name = inflect_engine.singular_noun(tablename) or tablename
        else:
            self.preferred_name = colname[:-3]

        # Add uselist=False to One-to-One relationships
        if any(isinstance(c, (PrimaryKeyConstraint, UniqueConstraint)) and
               set(col.name for col in c.columns) == set(column_names)
               for c in constraint.table.constraints):
            self.kwargs['uselist'] = 'False'

        # Handle self referential relationships
        if source_cls == target_cls:
            # self.preferred_name = 'parent' if not colname.endswith('_id') else colname[:-3]
            if colname.endswith("id") or colname.endswith("Id"):
                self.preferred_name = colname[:-2]
            else:
                self.preferred_name = "parent"  # hmm, why not just table name
            pk_col_names = [col.name for col in constraint.table.primary_key]
            self.kwargs['remote_side'] = '[{0}]'.format(', '.join(pk_col_names))

        # If the two tables share more than one foreign key constraint,
        # SQLAlchemy needs an explicit primaryjoin to figure out which column(s) to join with
        common_fk_constraints = self.get_common_fk_constraints(
            constraint.table, constraint.elements[0].column.table)
        if len(common_fk_constraints) > 1:
            self.kwargs['primaryjoin'] = "'{0}.{1} == {2}.{3}'".format(
                source_cls, column_names[0], target_cls, constraint.elements[0].column.name)

    @staticmethod
    def get_common_fk_constraints(table1, table2):
        """Returns a set of foreign key constraints the two tables have against each other."""
        c1 = set(c for c in table1.constraints if isinstance(c, ForeignKeyConstraint) and
                 c.elements[0].column.table == table2)
        c2 = set(c for c in table2.constraints if isinstance(c, ForeignKeyConstraint) and
                 c.elements[0].column.table == table1)
        return c1.union(c2)


class ManyToManyRelationship(Relationship):
    def __init__(self, source_cls, target_cls, assocation_table):
        super(ManyToManyRelationship, self).__init__(source_cls, target_cls)

        prefix = (assocation_table.schema + '.') if assocation_table.schema else ''
        self.kwargs['secondary'] = repr(prefix + assocation_table.name)
        constraints = [c for c in assocation_table.constraints
                       if isinstance(c, ForeignKeyConstraint)]
        constraints.sort(key=_get_constraint_sort_key)
        colname = _get_column_names(constraints[1])[0]
        tablename = constraints[1].elements[0].column.table.name
        self.preferred_name = tablename if not colname.endswith('_id') else colname[:-3] + 's'

        # Handle self referential relationships
        if source_cls == target_cls:
            self.preferred_name = 'parents' if not colname.endswith('_id') else colname[:-3] + 's'
            pri_pairs = zip(_get_column_names(constraints[0]), constraints[0].elements)
            sec_pairs = zip(_get_column_names(constraints[1]), constraints[1].elements)
            pri_joins = ['{0}.{1} == {2}.c.{3}'.format(source_cls, elem.column.name,
                                                       assocation_table.name, col)
                         for col, elem in pri_pairs]
            sec_joins = ['{0}.{1} == {2}.c.{3}'.format(target_cls, elem.column.name,
                                                       assocation_table.name, col)
                         for col, elem in sec_pairs]
            self.kwargs['primaryjoin'] = (
                repr('and_({0})'.format(', '.join(pri_joins)))
                if len(pri_joins) > 1 else repr(pri_joins[0]))
            self.kwargs['secondaryjoin'] = (
                repr('and_({0})'.format(', '.join(sec_joins)))
                if len(sec_joins) > 1 else repr(sec_joins[0]))


class CodeGenerator(object):
    template = """\
# coding: utf-8
{imports}

{metadata_declarations}


{models}"""
    do_model_creation_services_hack = False  # fixme remove

    def __init__(self, metadata, noindexes=False, noconstraints=False, nojoined=False,
                 noinflect=False, noclasses=False, model_creation_services = None,
                 indentation='    ', model_separator='\n\n',
                 ignored_tables=('alembic_version', 'migrate_version'), table_model=ModelTable,
                 class_model=ModelClass,  template=None, nocomments=False):
        super(CodeGenerator, self).__init__()
        self.metadata = metadata
        self.noindexes = noindexes
        self.noconstraints = noconstraints
        self.nojoined = nojoined
        self.noinflect = noinflect
        self.noclasses = noclasses
        self.model_creation_services = model_creation_services  # ApiLogicServer
        self.generate_relationships_on = "parent"  # "child"
        self.indentation = indentation
        self.model_separator = model_separator
        self.ignored_tables = ignored_tables
        self.table_model = table_model
        self.class_model = class_model
        self.nocomments = nocomments
        self.children_map = dict()
        """ key is table name, value is list of (parent-role-name, child-role-name, relationship) ApiLogicServer """
        self.parents_map = dict()
        """ key is table name, value is list of (parent-role-name, child-role-name, relationship) ApiLogicServer """
        self.inflect_engine = self.create_inflect_engine()
        if template:
            self.template = template

        # Pick association tables from the metadata into their own set, don't process them normally
        links = defaultdict(lambda: [])
        association_tables = set()
        skip_association_table = True
        for table in metadata.tables.values():
            # Link tables have exactly two foreign key constraints and all columns are involved in
            # them
            fk_constraints = [constr for constr in table.constraints
                              if isinstance(constr, ForeignKeyConstraint)]
            if len(fk_constraints) == 2 and all(col.foreign_keys for col in table.columns):
                if skip_association_table:  # Chinook playlist tracks, SqlSvr, Postgres Emp Territories
                    debug_str = f'skipping associate table: {table.name}'
                    debug_str += "... treated as normal table, with automatic joins"
                else:
                    association_tables.add(table.name)
                    tablename = sorted(
                        fk_constraints, key=_get_constraint_sort_key)[0].elements[0].column.table.name
                    links[tablename].append(table)

        # Iterate through the tables and create model classes when possible
        self.models = []
        self.collector = ImportCollector()
        self.classes = {}
        for table in metadata.sorted_tables:
            # Support for Alembic and sqlalchemy-migrate -- never expose the schema version tables
            if table.name in self.ignored_tables:
                continue

            if noindexes:
                table.indexes.clear()

            if noconstraints:
                table.constraints = {table.primary_key}
                table.foreign_keys.clear()
                for col in table.columns:
                    col.foreign_keys.clear()
            else:
                # Detect check constraints for boolean and enum columns
                for constraint in table.constraints.copy():
                    if isinstance(constraint, CheckConstraint):
                        sqltext = self._get_compiled_expression(constraint.sqltext)

                        # Turn any integer-like column with a CheckConstraint like
                        # "column IN (0, 1)" into a Boolean
                        match = _re_boolean_check_constraint.match(sqltext)
                        if match:
                            colname = _re_column_name.match(match.group(1)).group(3)
                            table.constraints.remove(constraint)
                            table.c[colname].type = Boolean()
                            continue

                        # Turn any string-type column with a CheckConstraint like
                        # "column IN (...)" into an Enum
                        match = _re_enum_check_constraint.match(sqltext)
                        if match:
                            colname = _re_column_name.match(match.group(1)).group(3)
                            items = match.group(2)
                            if isinstance(table.c[colname].type, String):
                                table.constraints.remove(constraint)
                                if not isinstance(table.c[colname].type, Enum):
                                    options = _re_enum_item.findall(items)
                                    table.c[colname].type = Enum(*options, native_enum=False)
                                continue

            # Tables vs. Classes ********
            # Only form model classes for tables that have a primary key and are not association
            # tables
            if "productvariantsoh-20190423" in (table.name + "") or "unique_no_key" in (table.name + ""):
                debug_str = "target table located"
            """ create classes iff unique col - CAUTION: fails to run """
            has_unique_constraint = False
            if not table.primary_key:
                for each_constraint in table.constraints:
                    if isinstance(each_constraint, sqlalchemy.sql.schema.UniqueConstraint):
                        has_unique_constraint = True
                        print(f'\n*** ApiLogicServer -- {table.name} has unique constraint, no primary_key')
                #  print(f'\nTEST *** {table.name} not table.primary_key = {not table.primary_key}, has_unique_constraint = {has_unique_constraint}')
            unique_constraint_class = model_creation_services.infer_primary_key and has_unique_constraint
            if unique_constraint_class == False and (noclasses or not table.primary_key or table.name in association_tables):
                model = self.table_model(table)
            else:
                model = self.class_model(table, links[table.name], self.inflect_engine, not nojoined)  # computes attrs (+ roles)
                self.classes[model.name] = model

            self.models.append(model)
            model.add_imports(self.collector)

        # Nest inherited classes in their superclasses to ensure proper ordering
        for model in self.classes.values():
            if model.parent_name != 'Base':
                self.classes[model.parent_name].children.append(model)
                self.models.remove(model)

        # Add either the MetaData or declarative_base import depending on whether there are mapped
        # classes or not
        if not any(isinstance(model, self.class_model) for model in self.models):
            self.collector.add_literal_import('sqlalchemy', 'MetaData')
        else:
            self.collector.add_literal_import('sqlalchemy.ext.declarative', 'declarative_base')

    def create_inflect_engine(self):
        if self.noinflect:
            return _DummyInflectEngine()
        else:
            import inflect
            return inflect.engine()

    def render_imports(self):
        return '\n'.join('from {0} import {1}'.format(package, ', '.join(sorted(names)))
                         for package, names in self.collector.items())

    def render_metadata_declarations(self):
        api_logic_server_imports = """
########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://valhuber.github.io/ApiLogicServer/Project-Rebuild/#rebuilding

from safrs import SAFRSBase

import safrs

Base = declarative_base()
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.mysql import *
########################################################################################################################
"""
        if "sqlalchemy.ext.declarative" in self.collector:  # Manually Added for safrs (ApiLogicServer)
            dialect_name = self.metadata.bind.engine.dialect.name  # sqlite , mysql , postgresql , oracle , or mssql
            if dialect_name in ["firebird", "mssql", "oracle", "postgresql", "sqlite", "sybase"]:
                rtn_api_logic_server_imports = api_logic_server_imports.replace("mysql", dialect_name)
            else:
                rtn_api_logic_server_imports = api_logic_server_imports
                print(".. .. ..Warning - unknown sql dialect, defaulting to msql - check database/models.py")
            return rtn_api_logic_server_imports
        return "metadata = MetaData()"

    def _get_compiled_expression(self, statement):
        """Return the statement in a form where any placeholders have been filled in."""
        return str(statement.compile(
            self.metadata.bind, compile_kwargs={"literal_binds": True}))

    @staticmethod
    def _getargspec_init(method):
        try:
            if hasattr(inspect, 'getfullargspec'):
                return inspect.getfullargspec(method)
            else:
                return inspect.getargspec(method)
        except TypeError:
            if method is object.__init__:
                return ArgSpec(['self'], None, None, None)
            else:
                return ArgSpec(['self'], 'args', 'kwargs', None)

    @classmethod
    def render_column_type(cls, coltype):
        args = []
        kwargs = OrderedDict()
        argspec = cls._getargspec_init(coltype.__class__.__init__)
        defaults = dict(zip(argspec.args[-len(argspec.defaults or ()):],
                            argspec.defaults or ()))
        missing = object()
        use_kwargs = False
        for attr in argspec.args[1:]:
            # Remove annoyances like _warn_on_bytestring
            if attr.startswith('_'):
                continue

            value = getattr(coltype, attr, missing)
            default = defaults.get(attr, missing)
            if value is missing or value == default:
                use_kwargs = True
            elif use_kwargs:
                kwargs[attr] = repr(value)
            else:
                args.append(repr(value))

        if argspec.varargs and hasattr(coltype, argspec.varargs):
            varargs_repr = [repr(arg) for arg in getattr(coltype, argspec.varargs)]
            args.extend(varargs_repr)

        if isinstance(coltype, Enum) and coltype.name is not None:
            kwargs['name'] = repr(coltype.name)

        for key, value in kwargs.items():
            args.append('{}={}'.format(key, value))

        rendered = coltype.__class__.__name__
        if args:
            rendered += '({0})'.format(', '.join(args))
        if rendered.startswith("CHAR("):  # temp fix for non-double byte chars
            rendered = rendered.replace("CHAR(", "String(")
        return rendered

    def render_constraint(self, constraint):
        def render_fk_options(*opts):
            opts = [repr(opt) for opt in opts]
            for attr in 'ondelete', 'onupdate', 'deferrable', 'initially', 'match':
                value = getattr(constraint, attr, None)
                if value:
                    opts.append('{0}={1!r}'.format(attr, value))

            return ', '.join(opts)

        if isinstance(constraint, ForeignKey):
            remote_column = '{0}.{1}'.format(constraint.column.table.fullname,
                                             constraint.column.name)
            return 'ForeignKey({0})'.format(render_fk_options(remote_column))
        elif isinstance(constraint, ForeignKeyConstraint):
            local_columns = _get_column_names(constraint)
            remote_columns = ['{0}.{1}'.format(fk.column.table.fullname, fk.column.name)
                              for fk in constraint.elements]
            return 'ForeignKeyConstraint({0})'.format(
                render_fk_options(local_columns, remote_columns))
        elif isinstance(constraint, CheckConstraint):
            return 'CheckConstraint({0!r})'.format(
                self._get_compiled_expression(constraint.sqltext))
        elif isinstance(constraint, UniqueConstraint):
            columns = [repr(col.name) for col in constraint.columns]
            return 'UniqueConstraint({0})'.format(', '.join(columns))

    @staticmethod
    def render_index(index):
        extra_args = [repr(col.name) for col in index.columns]
        if index.unique:
            extra_args.append('unique=True')
        return 'Index({0!r}, {1})'.format(index.name, ', '.join(extra_args))

    def render_column(self, column, show_name):
        kwarg = []
        is_sole_pk = column.primary_key and len(column.table.primary_key) == 1
        dedicated_fks = [c for c in column.foreign_keys if len(c.constraint.columns) == 1]
        is_unique = any(isinstance(c, UniqueConstraint) and set(c.columns) == {column}
                        for c in column.table.constraints)
        is_unique = is_unique or any(i.unique and set(i.columns) == {column}
                                     for i in column.table.indexes)
        has_index = any(set(i.columns) == {column} for i in column.table.indexes)
        server_default = None

        # Render the column type if there are no foreign keys on it or any of them points back to
        # itself
        render_coltype = not dedicated_fks or any(fk.column is column for fk in dedicated_fks)
        if 'DataTypes.char_type DEBUG ONLY' == str(column):
            print("Debug Stop: Column")  # char_type = Column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'))

        if column.key != column.name:
            kwarg.append('key')
        if column.primary_key:
            kwarg.append('primary_key')
        if not column.nullable and not is_sole_pk:
            kwarg.append('nullable')
        if is_unique:
            column.unique = True
            kwarg.append('unique')
            if self.model_creation_services.infer_primary_key:
                # print(f'ApiLogicServer infer_primary_key for {column.table.name}.{column.name}')
                column.primary_key = True
                kwarg.append('primary_key')
        elif has_index:
            column.index = True
            kwarg.append('index')

        if Computed and isinstance(column.server_default, Computed):
            expression = self._get_compiled_expression(column.server_default.sqltext)

            persist_arg = ''
            if column.server_default.persisted is not None:
                persist_arg = ', persisted={}'.format(column.server_default.persisted)

            server_default = 'Computed({!r}{})'.format(expression, persist_arg)

        elif column.server_default:
            # The quote escaping does not cover pathological cases but should mostly work FIXME SqlSvr no .arg
            # not used for postgres/mysql; for sqlite, text is '0'
            if not hasattr( column.server_default, 'arg' ):
                server_default = 'server_default=text("{0}")'.format('0')
            else:
                default_expr = self._get_compiled_expression(column.server_default.arg)
                if '\n' in default_expr:
                    server_default = 'server_default=text("""\\\n{0}""")'.format(default_expr)
                else:
                    default_expr = default_expr.replace('"', '\\"')
                    server_default = 'server_default=text("{0}")'.format(default_expr)

        comment = getattr(column, 'comment', None)
        if (column.name + "") == "debug_column_name":
            db = 'Column({0})'.format(', '.join(
            ([repr(column.name)] if show_name else []) +
            ([self.render_column_type(column.type)] if render_coltype else []) +
            [self.render_constraint(x) for x in dedicated_fks] +
            [repr(x) for x in column.constraints] +
            ([server_default] if server_default else []) +
            ['{0}={1}'.format(k, repr(getattr(column, k))) for k in kwarg] +
            (['comment={!r}'.format(comment)] if comment and not self.nocomments else [])
            ))
            print("Debug Stop")  # ApiLogicServer fix for putting this at end:  index=True
        return 'Column({0})'.format(', '.join(
            ([repr(column.name)] if show_name else []) +
            ([self.render_column_type(column.type)] if render_coltype else []) +
            [self.render_constraint(x) for x in dedicated_fks] +
            [repr(x) for x in column.constraints] +
            ([server_default] if server_default else []) +
            ['{0}={1}'.format(k, repr(getattr(column, k))) for k in kwarg] +
            (['comment={!r}'.format(comment)] if comment and not self.nocomments else [])
        ))

    def render_relationship(self, relationship) -> str:
        ''' returns string like: Department = relationship(\'Department\', remote_side=[Id])
        '''
        rendered = 'relationship('
        args = [repr(relationship.target_cls)]

        if 'secondaryjoin' in relationship.kwargs:
            rendered += '\n{0}{0}'.format(self.indentation)
            delimiter, end = (',\n{0}{0}'.format(self.indentation),
                              '\n{0})'.format(self.indentation))
        else:
            delimiter, end = ', ', ')'

        args.extend([key + '=' + value for key, value in relationship.kwargs.items()])
        return rendered + delimiter.join(args) + end

    def render_relationship_on_parent(self, relationship) -> str:
        ''' returns string like: Department = relationship(\'Department\', remote_side=[Id])
        '''
        rendered = 'relationship('
        args = [repr(relationship.source_cls)]

        if 'secondaryjoin' in relationship.kwargs:
            rendered += '\n{0}{0}'.format(self.indentation)
            delimiter, end = (',\n{0}{0}'.format(self.indentation),
                              '\n{0})'.format(self.indentation))
        else:
            delimiter, end = ', ', ')'

        args.extend([key + '=' + value for key, value in relationship.kwargs.items()])
        return rendered + delimiter.join(args) + end

    def render_table(self, model):
        # Manual edit:
        # replace invalid chars for views etc  TODO review ApiLogicServer -- using model.name vs model.table.name
        table_name = model.name
        bad_chars = r"$-+ "
        if any(elem in table_name for elem in bad_chars):
            print("sys error")

        table_name = table_name.replace("$", "_S_")
        table_name = table_name.replace(" ", "_")
        table_name = table_name.replace("+", "_")
        if model.table.name == "Plus+Table":
            print("Debug Stop on table")
        rendered = "t_{0} = Table(\n{1}{0!r}, metadata,\n".format(table_name, self.indentation)

        for column in model.table.columns:
            if column.name == "char_type DEBUG ONLY":
                print("Debug Stop - column")
            rendered += '{0}{1},\n'.format(self.indentation, self.render_column(column, True))

        for constraint in sorted(model.table.constraints, key=_get_constraint_sort_key):
            if isinstance(constraint, PrimaryKeyConstraint):
                continue
            if (isinstance(constraint, (ForeignKeyConstraint, UniqueConstraint)) and
                    len(constraint.columns) == 1):
                continue
            rendered += '{0}{1},\n'.format(self.indentation, self.render_constraint(constraint))

        for index in model.table.indexes:
            if len(index.columns) > 1:
                rendered += '{0}{1},\n'.format(self.indentation, self.render_index(index))

        if model.schema:
            rendered += "{0}schema='{1}',\n".format(self.indentation, model.schema)

        table_comment = getattr(model.table, 'comment', None)
        if table_comment:
            quoted_comment = table_comment.replace("'", "\\'").replace('"', '\\"')
            rendered += "{0}comment='{1}',\n".format(self.indentation, quoted_comment)

        return rendered.rstrip('\n,') + '\n)\n'

    def render_class(self, model):
        # print("# Render", model.name)
        rendered = 'class {0}(SAFRSBase, {1}):\n'.format(model.name, model.parent_name)   # ApiLogicServer
        rendered += '{0}__tablename__ = {1!r}\n'.format(self.indentation, model.table.name)
        rendered += '{0}_s_collection_name = {1!r}\n'.format(self.indentation, model.name)

        if self.do_model_creation_services_hack and not self.model_creation_services.resource_list_complete:
            resource_list = self.model_creation_services.resource_list
            resource = Resource(name=model.name)
            for each_attr, each_column in model.attributes.items():
                if isinstance(each_column, Column):
                    resource_attribute = ResourceAttribute(name=str(each_column.name))
                    resource.attributes.append(resource_attribute)
            resource_list[model.name] = resource
            if not str(model.table.name).startswith("ab_"):
                self.model_creation_services.table_to_class_map_update(
                    table_name=model.table.name, class_name=model.name)

        # Render constraints and indexes as __table_args__
        autonum_col = False
        table_args = []
        for constraint in sorted(model.table.constraints, key=_get_constraint_sort_key):
            if isinstance(constraint, PrimaryKeyConstraint):
                if constraint._autoincrement_column is not None:
                    autonum_col = True
                continue
            if (isinstance(constraint, (ForeignKeyConstraint, UniqueConstraint)) and
                    len(constraint.columns) == 1):
                continue
            table_args.append(self.render_constraint(constraint))
        for index in model.table.indexes:
            if len(index.columns) > 1:
                table_args.append(self.render_index(index))

        table_kwargs = {}
        if model.schema:
            table_kwargs['schema'] = model.schema

        table_comment = getattr(model.table, 'comment', None)
        if table_comment:
            table_kwargs['comment'] = table_comment

        kwargs_items = ', '.join('{0!r}: {1!r}'.format(key, table_kwargs[key])
                                 for key in table_kwargs)
        kwargs_items = '{{{0}}}'.format(kwargs_items) if kwargs_items else None
        if table_kwargs and not table_args:
            rendered += '{0}__table_args__ = {1}\n'.format(self.indentation, kwargs_items)
        elif table_args:
            if kwargs_items:
                table_args.append(kwargs_items)
            if len(table_args) == 1:
                table_args[0] += ','
            table_args_joined = ',\n{0}{0}'.format(self.indentation).join(table_args)
            rendered += '{0}__table_args__ = (\n{0}{0}{1}\n{0})\n'.format(
                self.indentation, table_args_joined)

        # Render columns
        rendered += '\n'
        for attr, column in model.attributes.items():
            if isinstance(column, Column):
                show_name = attr != column.name
                rendered += '{0}{1} = {2}\n'.format(
                    self.indentation, attr, self.render_column(column, show_name))
        if not autonum_col:
            rendered += '{0}{1}'.format(self.indentation, "allow_client_generated_ids = True\n")


        # Render relationships (declared in parent class, backref to child)
        if any(isinstance(value, Relationship) for value in model.attributes.values()):
            rendered += '\n'
        backrefs = {}
        for attr, relationship in model.attributes.items():
            if isinstance(relationship, Relationship):  # ApiLogicServer changed to insert backref
                attr_to_render = attr
                if self.generate_relationships_on != "child":
                    attr_to_render = "# see backref on parent: " + attr  # relns not created on child; comment out
                rel_render = "{0}{1} = {2}\n".format(self.indentation, attr_to_render, self.render_relationship(relationship))
                rel_parts = rel_render.split(")")  # eg, Department = relationship(\'Department\', remote_side=[Id]
                backref_name = model.name + "List"
                """ disambiguate multi-relns, eg, in the Employee child class, 2 relns to Department:
                        Department =  relationship('Department', primaryjoin='Employee.OnLoanDepartmentId == Department.Id', cascade_backrefs=True, backref='EmployeeList')
                        Department1 = relationship('Department', primaryjoin='Employee.WorksForDepartmentId == Department.Id', cascade_backrefs=True, backref='EmployeeList_Department1')
                    cascade_backrefs=True, backref='EmployeeList_Department1'   <== need to append that "1"
                """
                unique_name = relationship.target_cls + '.' + backref_name
                if unique_name in backrefs:  # disambiguate
                    backref_name += "_" + attr
                back_ref = f', cascade_backrefs=True, backref=\'{backref_name}\''
                rel_render_with_backref = rel_parts[0] + \
                                          back_ref + \
                                          ")" + rel_parts[1]
                # rendered += "{0}{1} = {2}\n".format(self.indentation, attr, self.render_relationship(relationship))

                """ disambiguate multi-relns, eg, in the Department parent class, 2 relns to Employee:
                        EmployeeList =  relationship('Employee', primaryjoin='Employee.OnLoanDepartmentId == Department.Id', cascade_backrefs=True, backref='Department')
                        EmployeeList1 = relationship('Employee', primaryjoin='Employee.WorksForDepartmentId == Department.Id', cascade_backrefs=True, backref='Department1')
                    cascade_backrefs=True, backref='EmployeeList_Department1'   <== need to append that "1"
                """
                if relationship.target_cls not in self.classes:
                    print(f'.. .. ..ERROR - {model.name} -- missing parent class: {relationship.target_cls}')
                    print(f'.. .. .. .. Parent Class may be missing Primary Key and Unique Column')
                    print(f'.. .. .. .. Attempting to continue - you may need to repair model, or address database design')
                    continue
                parent_model = self.classes[relationship.target_cls]  # eg, Department
                parent_relationship_def = self.render_relationship_on_parent(relationship)
                parent_relationship_def = parent_relationship_def[:-1]
                # eg, for Dept: relationship('Employee', primaryjoin='Employee.OnLoanDepartmentId == Department.Id')
                child_role_name = model.name + "List"
                parent_role_name = attr
                if unique_name in backrefs:  # disambiguate
                    child_role_name += '1'  # FIXME - fails for 3 relns
                if model.name != parent_model.name:
                    parent_relationship = f'{child_role_name} = {parent_relationship_def}, cascade_backrefs=True, backref=\'{parent_role_name}\')'
                else:  # work-around for self relns
                    """
                    special case self relns:
                        not DepartmentList = relationship('Department', remote_side=[Id], cascade_backrefs=True, backref='Department')
                        but Department     = relationship('Department', remote_side=[Id], cascade_backrefs=True, backref='DepartmentList')
                    """
                    parent_relationship = f'{parent_role_name} = {parent_relationship_def}, cascade_backrefs=True, backref=\'{child_role_name}\')'
                    parent_relationship += "  # special handling for self-relationships"
                if self.generate_relationships_on != "parent":  # relns not created on parent; comment out
                    parent_relationship = "# see backref on child: " + parent_relationship
                parent_model.rendered_model_relationships += "    " + parent_relationship + "\n"
                if model.name == "OrderDetail":
                    debug_str = "nice breakpoint"
                rendered += rel_render_with_backref
                backrefs[unique_name] = backref_name
                if relationship.source_cls.startswith("Ab"):
                    pass
                elif isinstance(relationship, ManyToManyRelationship):  # eg, chinook:PlayList->PlayListTrack
                    print(f'many to many should not occur on: {model.name}.{unique_name}')
                elif not self.do_model_creation_services_hack:
                    pass
                else:  # fixme dump all this, right?
                    use_old_code = False  # so you can elide this
                    if use_old_code:
                        resource = self.model_creation_services.resource_list[relationship.source_cls]
                        resource_relationship = ResourceRelationship(parent_role_name = attr,
                                                                     child_role_name = backref_name)
                        resource_relationship.child_resource = relationship.source_cls
                        resource_relationship.parent_resource = relationship.target_cls
                        # gen key pairs
                        for each_pair in relationship.foreign_key_constraint.elements:
                            pair = ( str(each_pair.column.name), str(each_pair.parent.name) )
                            resource_relationship.parent_child_key_pairs.append(pair)

                            resource.parents.append(resource_relationship)
                            parent_resource = self.model_creation_services.resource_list[relationship.target_cls]
                            parent_resource.children.append(resource_relationship)
                            if use_old_code:
                                if relationship.source_cls not in self.parents_map:   # todo old code remove
                                    self.parents_map[relationship.source_cls] = list()
                                self.parents_map[relationship.source_cls].append(
                                    (
                                        attr,          # to parent, eg, Department, Department1
                                        backref_name,  # to children, eg, EmployeeList, EmployeeList_Department1
                                        relationship.foreign_key_constraint
                                    ) )
                                if relationship.target_cls not in self.children_map:
                                    self.children_map[relationship.target_cls] = list()
                                self.children_map[relationship.target_cls].append(
                                    (
                                        attr,          # to parent, eg, Department, Department1
                                        backref_name,  # to children, eg, EmployeeList, EmployeeList_Department1
                                        relationship.foreign_key_constraint
                                    ) )
                pass

        # Render subclasses
        for child_class in model.children:
            rendered += self.model_separator + self.render_class(child_class)
        # rendered += "\n    # END RENDERED CLASS\n"  # useful for debug, as required
        return rendered

    def render(self, outfile=sys.stdout):
        """ create model from db, and write models.py file to in-memory buffer (outfile)
            relns created from not-yet-seen children, so save *all* class info, then append rendered_model_relationships
        """
        for model in self.models:
            if isinstance(model, self.class_model):
                # rendered_models.append(self.render_class(model))
                model.rendered_model = self.render_class(model)  # also sets parent_model.rendered_model_relationships

        rendered_models = []  # now append the rendered_model + rendered_model_relationships
        for model in self.models:
            if isinstance(model, self.class_model):
                # rendered_models.append(self.render_class(model))
                if model.rendered_model_relationships != "":
                    model.rendered_model_relationships = "\n" + model.rendered_model_relationships
                rendered_models.append(model.rendered_model + model.rendered_model_relationships)
            elif isinstance(model, self.table_model):  # eg, views, database id generators, etc
                rendered_models.append(self.render_table(model))

        output = self.template.format(
            imports=self.render_imports(),
            metadata_declarations=self.render_metadata_declarations(),
            models=self.model_separator.join(rendered_models).rstrip('\n'))
        print(output, file=outfile)
