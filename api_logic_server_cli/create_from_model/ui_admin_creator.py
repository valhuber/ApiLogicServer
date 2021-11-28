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

from api_logic_server_cli.create_from_model.model_creation_services import Resource

log = logging.getLogger(__file__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter(f'%(name)s: %(message)s')     # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate = True

# temp hacks for admin app migration to attributes
admin_col_is_active = True
admin_col_is_join_active = False
admin_col_tab_columns = False
admin_user_key_is_active = True  # resource property, in lieu of admin_col_tab_columns
admin_relationships_with_parents = True

# have to monkey patch to work with WSL as workaround for https://bugs.python.org/issue38633
import errno, shutil
orig_copyxattr = shutil._copyxattr


def patched_copyxattr(src, dst, *, follow_symlinks=True):
    try:
        orig_copyxattr(src, dst, follow_symlinks=follow_symlinks)
    except OSError as ex:
        if ex.errno != errno.EACCES: raise


shutil._copyxattr = patched_copyxattr



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
        self.admin_yaml_col = DotMap()
        self.max_list_columns = 7  # maybe make this a param

        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()

    def create_admin_application(self) -> str:
        """ main driver - loop through resources, write admin.yaml - with backup, nw customization
        """
        if self.mod_gen.command == "create-ui" or self.mod_gen.command.startswith("rebuild"):
            if self.mod_gen.command.startswith("rebuild"):
                print(".. .. ..Use existing ui/admin")
        else:
            self.create_admin_app(msg=".. .. ..Create ui/admin")

        cwd = os.getcwd()
        sys.path.append(cwd)

        self.admin_yaml.api_root = "http://localhost:5656/api"
        self.admin_yaml_col.api_root = "http://localhost:5656/api"
        self.admin_yaml.resources = {}
        for each_resource_name in self.mod_gen.resource_list:
            each_resource = self.mod_gen.resource_list[each_resource_name]
            self.create_resource_in_admin(each_resource)
            if admin_col_is_active:
                self.create_resource_in_admin_col(each_resource)

        self.create_about()
        self.create_info()
        self.create_settings()
        self.doc_properties()

        admin_yaml_dict = self.admin_yaml.toDict()
        admin_yaml_dump = yaml.dump(admin_yaml_dict)
        admin_yaml_dict_col = self.admin_yaml_col.toDict()
        admin_yaml_dump_col = yaml.dump(admin_yaml_dict_col)
        if self.mod_gen.command != "create-ui":
            self.write_yaml_files(admin_yaml_dump, admin_yaml_dump_col)
        return admin_yaml_dump

    def create_resource_in_admin(self, resource: Resource):
        """ self.admin_yaml.resources += resource DotMap for given resource
        """
        resource_name = resource.name
        if self.do_process_resource(resource_name):
            new_resource = DotMap()
            self.num_pages_generated += 1
            new_resource.type = str(resource.name)
            if admin_user_key_is_active:
                new_resource.user_key = str(self.mod_gen.favorite_attribute_name(resource))

            self.create_attributes_in_owner(new_resource, resource, None)
            child_tabs = self.create_child_tabs(resource)
            if child_tabs:
                new_resource.tab_groups = child_tabs
            self.admin_yaml.resources[resource.table_name] = new_resource.toDict()

    def create_attributes_in_owner(self, owner: DotMap, resource: Resource, owner_resource: (None, Resource)):
        """ create attribute in owner (DotMap - of resource or tab)

          Customer:
            attributes:
            - CompanyName
            - ContactName
        """
        owner.attributes = []
        attributes = set()
        if admin_col_tab_columns:
            attributes = self.mod_gen.get_show_attributes(resource)
        else:
            attributes = self.mod_gen.get_attributes(resource)
        for each_attribute in attributes:
            if "." not in each_attribute:
                if each_attribute == self.mod_gen.favorite_attribute_name(resource):
                    attribute_with_search = DotMap()
                    search = DotMap()
                    search.search = True
                    search.label = f'{each_attribute}*'  # adding space causes newline, so omit for now
                    attribute_with_search[each_attribute] = search
                    owner.attributes.append(attribute_with_search)
                else:
                    owner.attributes.append(each_attribute)
            else:
                relationship = self.new_relationship_to_parent(resource, each_attribute, owner_resource)
                if relationship is not None:  # skip redundant master join
                    rel = DotMap()
                    parent_role_name = each_attribute.split('.')[0]
                    rel[parent_role_name] = relationship.toDict()
                    owner.attributes.append(rel)

    def create_resource_in_admin_col(self, resource: Resource):
        """ self.admin_yaml.resources += resource DotMap for given resource
        """
        resource_name = resource.name
        if self.do_process_resource(resource_name):
            new_resource = DotMap()
            self.num_pages_generated += 1
            new_resource.type = str(resource.name)
            new_resource.label = resource.name + " - label"
            if admin_user_key_is_active:
                new_resource.user_key = str(self.mod_gen.favorite_attribute_name(resource))

            self.create_columns_in_owner(new_resource, resource, None)
            child_tabs = self.create_child_tabs_col(resource)
            new_resource.relationships = child_tabs

            self.admin_yaml_col.resources[resource_name] = new_resource.toDict()

    def create_columns_in_owner(self, owner: DotMap, resource: Resource, owner_resource: (None, Resource)):
        """ create columns in owner (DotMap - of resource or tab)
        """
        owner.columns = []
        attributes = set()
        if admin_col_tab_columns:
            attributes = self.mod_gen.get_show_attributes(resource)
        else:
            attributes = self.mod_gen.get_attributes(resource)
        for each_attribute in attributes:
            if "." not in each_attribute:
                col_def = DotMap()
                col_def.name = each_attribute
                owner.columns.append(col_def)
            elif admin_col_is_join_active:
                relationship = self.new_relationship_to_parent(resource, each_attribute, owner_resource)
                if relationship is not None:  # skip redundant master join
                    rel = DotMap()
                    parent_role_name = each_attribute.split('.')[0]
                    rel[parent_role_name] = relationship.toDict()
                    owner.columns.append(rel)
            else:
                log.debug(f'column skipped since admin_col_is_join_active is false: '
                          f'{resource.name}.{each_attribute} ')

    def new_relationship_to_parent(self, a_child_resource: Resource, parent_attribute_reference,
                                   a_master_parent_resource) -> (None, DotMap):
        """
        given a_child_table_def.parent_column_reference, create relationship: attrs, fKeys (for *js* client (no meta))

          Order:
            attributes:
            - ShipName
            - Location:
                fks:
                - City
                - Country
                show_attributes: []
                type: Location

        :param a_child_resource: a child table (not class), eg, Employees
        :param parent_attribute_reference: parent ref, eg, Department1.DepartmentName
        :param a_master_parent_resource: the master of master/detail - skip joins for this
        """
        parent_role_name = parent_attribute_reference.split('.')[0]  # careful - is role (class) name, not table name
        if a_master_parent_resource is not None and parent_role_name == a_master_parent_resource.name:
            skipped = f'avoid redundant master join - {a_child_resource}.{parent_attribute_reference}'
            log.debug(f'master object detected - {skipped}')
            return None
        relationship = DotMap()
        if len(self.mod_gen.resource_list) == 0:   # RARELY used - use_model is true (expose_existing not called)
            return self.new_relationship_to_parent_no_model(a_child_resource,
                                                            parent_attribute_reference, a_master_parent_resource)
        my_parents_list = a_child_resource.parents
        parent_relationship = None
        for each_parent_relationship in my_parents_list:
            if each_parent_relationship.parent_role_name == parent_role_name:
                parent_relationship = each_parent_relationship
                break
        if not parent_relationship:
            msg = f'Unable to find role for: {parent_attribute_reference}'
            relationship.error_unable_to_find_role = msg
            if parent_role_name not in self.multi_reln_exceptions:
                self.multi_reln_exceptions.append(parent_role_name)
                log.warning(f'Error - please search ui/admin/admin.yaml for: Unable to find role')
        relationship.type = str(parent_relationship.parent_resource)
        relationship.show_attributes = []
        relationship.fks = []
        if a_child_resource.name == "Employee":
            log.debug("Parents for special table - debug")
        for each_column in parent_relationship.parent_child_key_pairs:  # XXX FIXME
            # key_column = DotMap()
            # key_column.name = str(each_column)
            relationship.fks.append(str(each_column[1]))
        # todo - verify fullname is table name (e.g, multiple relns - emp.worksFor/onLoan)
        return relationship

    def create_child_tabs(self, resource: Resource) -> DotMap:
        """
        build tabs for related children

            tab_groups:
              CustomerCustomerDemoList:
                attributes:
                - Id
                - CustomerTypeId
                fkeys:
                  source_delete_me: '?'
                  target: CustomerTypeId
                resource: CustomerCustomerDemo
        """
        if len(self.mod_gen.resource_list) == 0:   # almost always, use_model false (we create)
            return self.create_child_tabs_no_model(resource)

        children_seen = set()
        tab_group = DotMap()
        for each_resource_relationship in resource.children:
            each_resource_tab = DotMap()
            self.num_related += 1
            each_child = each_resource_relationship.child_resource
            if each_child in children_seen:
                pass  # it's ok, we are using the child_role_name now
            children_seen.add(each_child)
            each_resource_tab.fks = []
            for each_pair in each_resource_relationship.parent_child_key_pairs:
                each_resource_tab.fks.append(each_pair[1])
                """
                key_pair = DotMap()
                key_pair.target = each_pair[1]
                key_pair.source_delete_me = each_pair[0]
                each_resource_tab.fks = key_pair
                """

            each_resource_tab.resource = str(each_child)
            each_resource_tab.direction = "tomany"
            tab_name = each_resource_relationship.child_role_name

            each_child_resource = self.mod_gen.resource_list[each_child]
            if admin_col_tab_columns:
                self.create_attributes_in_owner(each_resource_tab, each_child_resource, resource)
            tab_group[tab_name] = each_resource_tab  # disambiguate multi-relns, eg Employee OnLoan/WorksForDept
        if admin_relationships_with_parents:
            for each_resource_relationship in resource.parents:
                each_resource_tab = DotMap()
                each_resource_tab.name = each_resource_relationship.parent_role_name
                each_parent = each_resource_relationship.parent_resource
                each_resource_tab.target = str(each_parent)
                each_resource_tab.direction = "toone"
                each_resource_tab.fks = []
                for each_pair in each_resource_relationship.parent_child_key_pairs:
                    each_resource_tab.fks.append(each_pair[1])
                tab_name = each_resource_relationship.parent_role_name

                # tab_group[tab_name] = each_resource_tab  # disambiguate multi-relns, eg Employee OnLoan/WorksForDept
                tab_group[tab_name] = each_resource_tab
        return tab_group

    def create_child_tabs_col(self, resource: Resource) -> DotMap:
        """
        build tabs for all related children, col style
        """
        if len(self.mod_gen.resource_list) == 0:   # almost always, use_model false (we create)
            return self.create_child_tabs_no_model(resource)

        children_seen = set()
        tab_group = []  # ??  DotMap()
        for each_resource_relationship in resource.children:
            each_resource_tab = DotMap()
            each_resource_tab.name = each_resource_relationship.child_role_name
            self.num_related += 1
            each_child = each_resource_relationship.child_resource
            if each_child in children_seen:
                pass  # it's ok, we are using the child_role_name now
            each_resource_tab.target = str(each_child)
            each_resource_tab.direction = "tomany"
            children_seen.add(each_child)
            each_resource_tab.fks = []
            for each_pair in each_resource_relationship.parent_child_key_pairs:
                each_resource_tab.fks.append(each_pair[1])
            tab_name = each_resource_relationship.child_role_name

            each_child_resource = self.mod_gen.resource_list[each_child]
            if admin_col_tab_columns:
                self.create_columns_in_owner(each_resource_tab, each_child_resource, resource)

            # tab_group[tab_name] = each_resource_tab  # disambiguate multi-relns, eg Employee OnLoan/WorksForDept
            tab_group.append(each_resource_tab)
        if admin_relationships_with_parents:
            for each_resource_relationship in resource.parents:
                each_resource_tab = DotMap()
                each_resource_tab.name = each_resource_relationship.parent_role_name
                each_parent = each_resource_relationship.parent_resource
                each_resource_tab.target = str(each_parent)
                each_resource_tab.direction = "toone"
                each_resource_tab.fks = []
                for each_pair in each_resource_relationship.parent_child_key_pairs:
                    each_resource_tab.fks.append(each_pair[1])
                tab_name = each_resource_relationship.parent_role_name

                # tab_group[tab_name] = each_resource_tab  # disambiguate multi-relns, eg Employee OnLoan/WorksForDept
                tab_group.append(each_resource_tab)
        return tab_group

    def do_process_resource(self, resource_name: str)-> bool:
        """ filter out resources that are skipped by user, start with ab etc
        """
        if resource_name + " " in self.not_exposed:
            return False  # not_exposed: api.expose_object(models.{table_name})
        if "ProductDetails_V" in resource_name:
            log.debug("special table")  # should not occur (--noviews)
        if resource_name.startswith("ab_"):
            return False  # skip admin table: " + table_name + "\n
        elif 'sqlite_sequence' in resource_name:
            return False  # skip sqlite_sequence table: " + table_name + "\n
        elif resource_name is None:
            return False  # no class (view): " + table_name + "\n
        elif resource_name.startswith("Ab"):
            return False
        return True

    def create_child_tabs_no_model(self, a_table_def: MetaDataTable) -> DotMap:
        """
        Rarely used, now broken.  Ignore for now

        This approach is for cases where use_model specifies an existing model.

        In such cases, self.mod_gen.my_children_list is  None, so we need to get relns from db, inferring role names
        """
        all_tables = a_table_def.metadata.tables
        tab_group = DotMap()
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
        return tab_group

    def new_relationship_to_parent_no_model(self, a_child_table_def: MetaDataTable, parent_column_reference,
                                   a_master_parent_table_def) -> (None, DotMap):
        """
        Rarely used, now broken.  Ignore for now.

        This approach is for cases where use_model specifies an existing model.

        In such cases, self.mod_gen.my_children_list is  None, so we need to get relns from db, inferring role names
        """
        parent_role_name = parent_column_reference.split('.')[0]  # careful - is role (class) name, not table name
        relationship = DotMap()
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

    def get_create_from_model_dir(self) -> Path:
        """
        :return: create_from_model dir, eg, /Users/val/dev/ApiLogicServer/create_from_model
        """
        path = Path(__file__)
        parent_path = path.parent
        parent_path = parent_path.parent
        return parent_path

    def write_yaml_files(self, admin_yaml, admin_yaml_col):
        """ write admin.yaml, with backup, with additional nw customized backup
        """
        yaml_file_name = self.mod_gen.fix_win_path(self.mod_gen.project_directory + f'/ui/admin/admin.yaml')
        if not self.mod_gen.command.startswith("rebuild"):
            with open(yaml_file_name, 'w') as yaml_file:
                yaml_file.write(admin_yaml)
            if admin_col_is_active:
                yaml_file_name_col = self.mod_gen.fix_win_path(
                    self.mod_gen.project_directory + f'/ui/admin/admin-col.yaml')
                print(f'.. .. .. ..Creating temp {yaml_file_name_col}')
                with open(yaml_file_name_col, 'w') as yaml_file_col:
                    yaml_file_col.write(admin_yaml_col)

        yaml_created_file_name = \
            self.mod_gen.fix_win_path(self.mod_gen.project_directory + f'/ui/admin/admin-created.yaml')
        with open(yaml_created_file_name, 'w') as yaml_copy_file:
            yaml_copy_file.write(admin_yaml)

        if self.mod_gen.nw_db_status in ["nw", "nw-"]:
            admin_custom_nw_file = open(
                os.path.dirname(os.path.realpath(__file__)) + "/templates/admin_custom_nw.yaml")
            admin_custom_nw = admin_custom_nw_file.read()
            nw_backup_file_name = \
                self.mod_gen.fix_win_path(self.mod_gen.project_directory + f'/ui/admin/admin_custom_nw.yaml')
            admin_file = open(nw_backup_file_name, 'w')
            admin_file.write(admin_custom_nw)
            admin_file.close()
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
        self.admin_yaml.about.recent_changes = "works with modified safrs-react-admin"
        return

    def create_info(self):
        """
            info block - # tables, relns, [no-relns warning]
        """
        self.admin_yaml.info = DotMap()
        self.admin_yaml.info.number_tables = self.num_pages_generated
        self.admin_yaml.info.number_relationships = self.num_related
        if self.num_related == 0:
            # FIXME what to do self.yaml_lines.append(f'  warning: no_related_view')
            print(".. .. ..WARNING - no relationships detected - add them to your database or model")
            print(".. .. ..  See https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design")

    def doc_properties(self):
        """ show non-automated properties in yaml, for users' quick reference
        """
        resource_props = DotMap()
        resource_props.menu = "False | name"
        resource_props.info = "long html / rich text"
        resource_props.allow_insert = "exp"
        resource_props.allow_update = "exp"
        resource_props.allow_delete = "exp"
        self.admin_yaml.properties_ref.resource = resource_props

        attr_props = DotMap()
        attr_props.search = "true | false"
        attr_props.label = "caption for display"
        attr_props.hidden = "exp"
        attr_props.group = "name"
        style_props = DotMap()
        style_props.font_weight = 0
        style_props.color = "blue"
        attr_props.style = style_props
        self.admin_yaml.properties_ref.attribute = attr_props

        tab_props = DotMap()
        tab_props.label = "text"
        tab_props.lookup = "boolean"
        self.admin_yaml.properties_ref.tab = tab_props

    def create_admin_app(self, msg: str = "", from_git: str = ""):
        """
        deep copy ApiLogicServer/create_from_model/admin -> project_directory/ui/admin

        :param msg: console log
        :param from_git: git url for source - override ApiLogicServer/create_from_model/admin (not impl)
        """
        from_proto_dir = from_git
        if from_proto_dir == "":
            from_proto_dir = self.mod_gen.fix_win_path(str(self.get_create_from_model_dir()) +
                                                       "/create_from_model/safrs-react-admin-npm-build")
        to_project_dir = self.mod_gen.fix_win_path(self.mod_gen.project_directory + "/ui/admin")
        print(f'{msg} copy prototype admin project {from_proto_dir} -> {to_project_dir}')
        # self.mod_gen.recursive_overwrite(from_proto_dir, to_project_dir)
        shutil.copytree(from_proto_dir, to_project_dir)


def create(model_creation_services: create_from_model.CreateFromModel):
    """ called by ApiLogicServer CLI -- creates ui/admin application (ui/admin folder, admin.yaml)
    """
    admin_creator = AdminCreator(model_creation_services,
                                 host=model_creation_services.host, port=model_creation_services.port,
                                 not_exposed=model_creation_services.not_exposed + " ",
                                 favorite_names=model_creation_services.favorite_names,
                                 non_favorite_names=model_creation_services.non_favorite_names)
    return admin_creator.create_admin_application()

