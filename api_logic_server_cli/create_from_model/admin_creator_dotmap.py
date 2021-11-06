import logging
import shutil
import sys
import os
from pathlib import Path
from typing import NewType, List

import sqlalchemy
import yaml
from sqlalchemy import MetaData
import datetime
import create_from_model.model_creation_services as create_from_model
from dotmap import DotMap

log = logging.getLogger(__name__)

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)


class AdminCreator(object):
    """
    Iterate over model

    Create ui/admin/admin.yaml
    """

    _favorite_names_list = []  #: ["name", "description"]
    """
        array of substrings used to find favorite column name

        command line option to override per language, db conventions

        eg,
            name in English
            nom in French
    """
    _non_favorite_names_list = []
    non_favorite_names = "id"

    num_pages_generated = 0
    num_related = 0

    def __init__(self,
                 mod_gen: create_from_model.CreateFromModel,
                 host: str = "localhost",
                 port: str = "5656",
                 not_exposed: str = 'ProductDetails_V',
                 favorite_names: str = "name description",
                 non_favorite_names: str = "id"):
        self.mod_gen = mod_gen
        self.host = host
        self.port = port
        self.not_exposed = not_exposed
        self.favorite_names = favorite_names
        self.non_favorite_name = non_favorite_names
        self.multi_reln_exceptions = list()

        self.metadata = None
        self.engine = None
        self.session = None
        self.connection = None
        self.app = None
        self.admin_yaml = DotMap()
        self.max_list_columns = 7  # maybe make this a param

        self.first_resource = True
        self.first_column = True
        self.first_object = True
        self.first_object_list = True

        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()

    def create_admin_application(self):
        """ main driver - loop through resources, write admin.yaml - with backup, nw customization
        """
        self.create_admin_app(msg=".. .. ..Create ui/admin")

        cwd = os.getcwd()
        sys.path.append(cwd)  # for banking Command Line test  TODO drop??
        self.mod_gen.find_meta_data(cwd)  # sets self.metadata
        meta_tables = self.mod_gen.metadata.tables

        self.admin_yaml.resources = {}
        for each_table in meta_tables.items():
            each_table_def = each_table[1]
            each_resource = self.create_each_resource(each_table_def)
            if each_resource is not None:
                self.admin_yaml.resources[str(each_table_def.name)] = each_resource.toDict()

        self.create_about()
        self.create_info()
        self.create_settings()

        admin_yaml_dict = self.admin_yaml.toDict()
        admin_yaml_dump = yaml.dump(admin_yaml_dict)
        self.write_yaml_files(admin_yaml_dump)

    def create_each_resource(self, a_table_def: MetaDataTable) -> (None, DotMap):
        """ create resource DotMap for given table
        """
        table_name = a_table_def.name
        class_name = self.mod_gen.get_class_for_table(table_name)
        log.debug("process_each_table: " + table_name)
        if "Employee" == table_name:
            log.debug("special table")  # debug stop here
        if table_name + " " in self.not_exposed:
            return None  # not_exposed: api.expose_object(models.{table_name})
        if "ProductDetails_V" in table_name:
            log.debug("special table")  # should not occur (--noviews)
        if table_name.startswith("ab_"):
            return None  # skip admin table: " + table_name + "\n
        elif 'sqlite_sequence' in table_name:
            return None  # skip sqlite_sequence table: " + table_name + "\n
        elif class_name is None:
            return None  # no class (view): " + table_name + "\n
        else:
            each_resource = self.new_resource(a_table_def)
            each_resource.columns = []
            columns = self.mod_gen.get_show_columns(a_table_def)
            for each_column in columns:
                if "." not in each_column:
                    column = DotMap()
                    column.name = each_column
                    each_resource.columns.append(column)
                else:
                    relationship = self.new_relationship_to_parent(a_table_def, each_column, None)
                    if relationship is not None:  # skip redundant master join
                        rel = DotMap()
                        parent_role_name = each_column.split('.')[0]
                        rel[parent_role_name] = relationship.toDict()
                        each_resource.columns.append(rel)
                self.create_first_column()
            child_tabs = self.create_child_tabs(a_table_def)
            if child_tabs:
                each_resource.tab_groups = child_tabs
            self.admin_yaml.resources[str(a_table_def.name)] = each_resource
            return each_resource

    def new_resource(self, a_table_def) -> DotMap:
        # resource_header[self.mod_gen.get_class_for_table(a_table_def.name)] = DotMap()
        resource = DotMap()
        self.num_pages_generated += 1
        class_name = self.mod_gen.get_class_for_table(a_table_def.name)
        resource.type = str(a_table_def.name)
        resource.user_key = str(self.mod_gen.favorite_column_name(a_table_def))
        self.create_first_resource()
        return resource

    def new_relationship_to_parent(self, a_child_table_def, parent_column_reference,
                                   a_master_parent_table_def) -> (None, DotMap):
        """
        given a_child_table_def.parent_column_reference, create object: attrs, fKeys (for *js* client (no meta))

        :param a_child_table_def: a child table (not class), eg, Employees
        :param parent_column_reference: parent ref, eg, Department1.DepartmentName
        :param a_master_parent_table_def: the master of master/detail - skip joins for this
        """
        parent_role_name = parent_column_reference.split('.')[0]  # careful - is role (class) name, not table name
        if a_master_parent_table_def != None and parent_role_name == a_master_parent_table_def.name:
            skipped = f'avoid redundant master join - {a_child_table_def}.{parent_column_reference}'
            # self.yaml_lines.append(f'#{tabs(num_tabs)} - {skipped}')  # uncomment for debug
            log.debug(f'master object detected - {skipped}')
            return None
        relationship = DotMap()
        if self.mod_gen.my_parents_list is not None:   # almost always, use_model false (we create)
            class_name = self.mod_gen.get_class_for_table(a_child_table_def.name)
            my_parents_list = self.mod_gen.my_parents_list[class_name]
            found_role=False
            for each_parent_role, each_child_role, each_fkey_constraint in my_parents_list:
                if each_parent_role == parent_role_name:
                    found_role = True
                    break
            if not found_role:
                msg = f'Unable to find role for: {parent_column_reference}'
                # self.yaml_lines.append(f'#{tabs(num_tabs)} -- {msg}')  FIXME error diagnostic
                if parent_role_name not in self.multi_reln_exceptions:
                    self.multi_reln_exceptions.append(parent_role_name)
                    log.warning(f'Error - please search ui/admin/admin.yaml for: {msg}')
            relationship.type = str(each_fkey_constraint.referred_table.fullname)
            relationship.show_attributes = []
            relationship.key_attributes = []
            if class_name == "Employee":
                log.debug("Parents for special table - debug")
                pass
            for each_column in each_fkey_constraint.column_keys:
                key_column = DotMap()
                key_column.name = str(each_column)
                relationship.key_attributes.append(str(each_column))
            # todo - verify fullname is table name (e.g, multiple relns - emp.worksFor/onLoan)
        else:  # rarely used - only when use_model (we did not generated models.py)
            fkeys = a_child_table_def.foreign_key_constraints
            if a_child_table_def.name == "Employee":  # table Employees, class/role employee
                log.debug("Debug stop")
            found_fkey = False
            checked_keys = ""
            for each_fkey in fkeys:  # find fkey for parent_role_name
                referred_table: str = each_fkey.referred_table.key  # table name, eg, Employees
                referred_table = referred_table.lower()
                checked_keys += referred_table + " "
                if referred_table.startswith(parent_role_name.lower()):
                    # self.yaml_lines.append(f'{tabs(num_tabs)}  - object:')
                    # todo - verify fullname is table name (e.g, multiple relns - emp.worksFor/onLoan)
                    # self.yaml_lines.append(f'{tabs(num_tabs)}    - type: {each_fkey.referred_table.fullname}')
                    # self.yaml_lines.append(f'{tabs(num_tabs)}    - show_attributes:')
                    # self.yaml_lines.append(f'{tabs(num_tabs)}    - key_attributes:')
                    log.debug(f'got each_fkey: {str(each_fkey)}')
                    for each_column in each_fkey.column_keys:
                        # self.yaml_lines.append(f'{tabs(num_tabs)}      - name: {each_column}')
                        pass
                    found_fkey = True
            if not found_fkey:
                parent_table_name = parent_role_name
                if parent_table_name.endswith("1"):
                    parent_table_name = parent_table_name[:-1]
                    pass
                msg = f'Please specify references to {parent_table_name}'
                # self.yaml_lines.append(f'#{tabs(num_tabs)} - Multiple relationships detected -- {msg}')  FIXME
                if parent_role_name not in self.multi_reln_exceptions:
                    self.multi_reln_exceptions.append(parent_role_name)
                    log.warning(f'Alert - please search ui/admin/admin.yaml for: {msg}')
                # raise Exception(msg)
        return relationship

    def create_child_tabs(self, a_table_def) -> DotMap:
        """
        build tab for any table with fkey to a_table_def (brute force search)
        """
        first_child = True
        if self.mod_gen.my_parents_list is not None:   # almost always, use_model false (we create)
            class_name = self.mod_gen.get_class_for_table(a_table_def.name)
            if class_name not in self.mod_gen.my_children_list:
                return None  # it's ok to have no children
            my_children_list = self.mod_gen.my_children_list[class_name]
            children_seen = set()
            tab_group = DotMap()
            for each_parent_role, each_child_role, each_fkey_constraint in my_children_list:
                each_tab = DotMap()
                self.num_related += 1
                each_child = each_fkey_constraint.table
                if each_child.name in children_seen:
                    pass
                    # FIXME self.yaml_lines.append(f'        label: {each_child.name}1')
                children_seen.add(each_child.name)
                for each_pair in each_fkey_constraint.elements:
                    key_pair = DotMap()
                    key_pair.target = str(each_pair.parent.name)
                    key_pair.source_delete_me = str(each_pair.column.name)
                    each_tab.fkeys = key_pair

                each_tab.resource = str(each_child.name)
                tab_name = each_child_role

                columns = self.mod_gen.get_show_columns(each_child)
                each_tab.columns = []
                for each_column in columns:
                    if "." not in each_column:
                        column = DotMap()
                        column.name = each_column
                        each_tab.columns.append(column)
                    else:
                        relationship = self.new_relationship_to_parent(each_child, each_column, a_table_def)
                        if relationship is not None:  # skip redundant master join
                            rel = DotMap()
                            parent_role_name = each_column.split('.')[0]
                            rel[parent_role_name] = relationship.toDict()
                            each_tab.columns.append(rel)

                tab_group[tab_name] = each_tab
            return tab_group
        else:  # rarely used (use_model)
            all_tables = a_table_def.metadata.tables
            for each_possible_child_tuple in all_tables.items():
                each_possible_child = each_possible_child_tuple[1]
                parents = each_possible_child.foreign_keys
                if (a_table_def.name == "Customer" and
                        each_possible_child.name == "Order"):
                    log.debug(a_table_def)
                for each_parent in parents:
                    each_parent_name = each_parent.target_fullname
                    loc_dot = each_parent_name.index(".")
                    each_parent_name = each_parent_name[0:loc_dot]
                    if each_parent_name == a_table_def.name:
                        if first_child:
                            # self.yaml_lines.append(f'    tab_group:')  FIXME
                            first_child = False
                            self.create_first_tab()
                        self.num_related += 1
                        # self.yaml_lines.append(f'      - tab: {each_possible_child.name} List')
                        # self.yaml_lines.append(f'        resource: {each_possible_child.name}')
                        # self.yaml_lines.append(f'          fkeys:')
                        for each_foreign_key in each_parent.parent.foreign_keys:
                            for each_element in each_foreign_key.constraint.elements:
                                # self.yaml_lines.append(f'          - target: {each_element.column.key}')
                                child_table_name = each_element.parent.table.name
                                # self.yaml_lines.append(f'            source: {each_element.parent.name}')
                        # self.yaml_lines.append(f'          columns:')
                        columns = columns = self.mod_gen.get_show_columns(each_possible_child)
                        col_count = 0
                        for each_column in columns:
                            col_count += 1
                            if col_count > self.max_list_columns:
                                break
                            if "." not in each_column:
                                # self.yaml_lines.append(f'          - name: {each_column}')
                                pass
                            else:
                                pass
                                # self.create_object_reference(each_possible_child, each_column, 4, a_table_def)

    def get_create_from_model_dir(self) -> Path:
        """
        :return: create_from_model dir, eg, /Users/val/dev/ApiLogicServer/create_from_model
        """
        path = Path(__file__)
        parent_path = path.parent
        parent_path = parent_path.parent
        return parent_path

    def create_first_resource(self):
        if self.first_resource:
            pass  # FIXME - approach?
            """
            self.yaml_lines.append(f'#{tabs(num_tabs)}  menu: False | name')
            self.yaml_lines.append(f'#{tabs(num_tabs)}  info: |')
            self.yaml_lines.append(f'#{tabs(num_tabs)}    {{long html text')
            self.yaml_lines.append(f'#{tabs(num_tabs)}    for user info}}')
            self.yaml_lines.append(f'#{tabs(num_tabs)}  allow_update: False')
            self.yaml_lines.append(f'#{tabs(num_tabs)}  allow_insert: False')
            self.yaml_lines.append(f'#{tabs(num_tabs)}  allow_delete: False')
            """
        self.first_resource = False

    def create_first_column(self):
        if self.first_column:
            pass
            """
            self.yaml_lines.append(f'#{tabs(num_tabs)}   label: text')
            self.yaml_lines.append(f'#{tabs(num_tabs)}   hidden: <exp>')
            self.yaml_lines.append(f'#{tabs(num_tabs)}   group: name')
            self.yaml_lines.append(f'#{tabs(num_tabs)}   component: name')
            self.yaml_lines.append(f'#{tabs(num_tabs)}   style:')
            self.yaml_lines.append(f'#{tabs(num_tabs)}     font-weight: 20')
            self.yaml_lines.append(f'#{tabs(num_tabs)}     color: blue')
            """
        self.first_column = False

    def create_first_tab(self):
        if self.first_column:
            pass
            """
            self.yaml_lines.append(f'#     label: text')
            self.yaml_lines.append(f'#     lookup: False')
            """

        self.first_column = False

    def write_yaml_files(self, admin_yaml):

        yaml_file_name = self.mod_gen.fix_win_path(self.mod_gen.project_directory + f'/ui/admin/admin_dotmap.yaml')
        with open(yaml_file_name, 'w') as yaml_file:
            yaml_file.write(admin_yaml)
        yaml_backup_file_name = yaml_file_name.replace("admin_dotmap", "admin_dotmap_backup")
        with open(yaml_backup_file_name, 'w') as yaml_backup_file:
            yaml_backup_file.write(admin_yaml)


        if self.mod_gen.nw_db_status in ["nw", "nw-"]:
            admin_custom_nw_file = open(
                os.path.dirname(os.path.realpath(__file__)) + "/templates/admin_custom_nw.yaml")
            admin_custom_nw = admin_custom_nw_file.read()
            dev_temp_do_not_overwrite = True  # fixme remove this when the files are stable
            if not dev_temp_do_not_overwrite:
                admin_file = open(yaml_file_name, 'w')
                admin_file.write(admin_custom_nw)
                admin_file.close()

                nw_backup_file_name = yaml_file_name.replace("admin.yaml", "admin_custom_nw_backup.yaml")
                admin_file = open(nw_backup_file_name, 'w')
                admin_file.write(admin_custom_nw)
                admin_file.close()

    def create_settings(self):
        self.admin_yaml.settings = DotMap()
        self.admin_yaml.settings.max_list_columns = str(self.max_list_columns)
        return

    def create_about(self):
        self.admin_yaml.about = DotMap()
        self.admin_yaml.about.date = f'{str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S"))}'
        self.admin_yaml.about.version = self.mod_gen.version
        self.admin_yaml.about.recent_changes = "much to say"
        return

    def create_info(self):
        """
            info block - # tables, relns, [no-relns warning]
        """
        meta_tables = self.mod_gen.metadata.tables
        self.admin_yaml.info = DotMap()
        self.admin_yaml.info.number_tables = self.num_pages_generated
        self.admin_yaml.info.number_relationships = self.num_related
        if self.num_related == 0:
            # FIXME what to do self.yaml_lines.append(f'  warning: no_related_view')
            print(".. .. ..WARNING - no relationships detected - add them to your database or model")
            print(".. .. ..  See https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design")

    def create_admin_app(self, msg: str = "", from_git: str = ""):
        """
        deep copy ApiLogicServer/create_from_model/admin -> project_directory/ui/admin

        :param msg: console log
        :param from_git: git url for source - override ApiLogicServer/create_from_model/admin (not impl)
        """
        from_proto_dir = from_git
        if from_proto_dir == "":
            from_proto_dir = self.mod_gen.fix_win_path(str(self.get_create_from_model_dir()) +
                                                       "/create_from_model/admin")
        to_project_dir = self.mod_gen.fix_win_path(self.mod_gen.project_directory + "/ui/admin")
        print(f'{msg} copy prototype admin project {from_proto_dir} -> {to_project_dir}')
        # self.mod_gen.recursive_overwrite(from_proto_dir, to_project_dir)
        shutil.copytree(from_proto_dir, to_project_dir)


def create(model_creation_services: create_from_model.CreateFromModel):
    """ called by ApiLogicServer CLI -- creates ui/react_admin application
    """
    admin_creator = AdminCreator(model_creation_services,
                                   host=model_creation_services.host, port=model_creation_services.port,
                                   not_exposed=model_creation_services.not_exposed + " ",
                                   favorite_names=model_creation_services.favorite_names,
                                   non_favorite_names=model_creation_services.non_favorite_names)
    admin_creator.create_admin_application()

