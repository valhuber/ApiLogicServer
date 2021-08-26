import logging
import shutil
import sys
import os
from pathlib import Path
from typing import NewType, List
from sqlalchemy import MetaData
import create_from_model.model_creation_services as create_from_model

log = logging.getLogger(__name__)

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)


class ReactCreator(object):
    """
    Iterate over model

    Create ui/basic_web_app/views.py and api/expose_api_models.py
    """

    # result_views = ""

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

    _indent = "   "
    '''
    tables_visited = set()  # to address "generate children first"
    """ table names of all visited views """
    tables_generated = set()  # to address "generate children first"
    """ table names of all fully generated views """
    '''

    num_pages_generated = 0
    num_related = 0

    def __init__(self,
                 mod_gen: create_from_model.CreateFromModel,
                 host: str = "localhost",
                 port: str = "5000",
                 not_exposed: str = 'ProductDetails_V',
                 favorite_names: str = "name description",
                 non_favorite_names: str = "id"):
        self.mod_gen = mod_gen
        self.host = host
        self.port = port
        self.not_exposed = not_exposed
        self.favorite_names = favorite_names
        self.non_favorite_name = non_favorite_names

        # TODO REMOVE self.table_to_class_map = {}
        """ keys are table[.column], values are class / attribute """
        self.metadata = None
        self.engine = None
        self.session = None
        self.connection = None
        self.app = None

        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()

    def create_components(self, version="TBD"):
        """ create react_admin/src/components file for each table """

        cwd = os.getcwd()
        sys.path.append(cwd)  # for banking Command Line test  TODO drop??

        self.mod_gen.find_meta_data(cwd)  # sets self.metadata
        meta_tables = self.mod_gen.metadata.tables

        for each_table in meta_tables.items():
            each_result = self.create_each_component(each_table[1])
        return

    def create_each_component(self, a_table_def: MetaDataTable):
        """
            create react_admin/src/components file for given table.

            Parameters
                argument1 a_table_def - TableModelInstance
        """
        result = ""
        table_name = a_table_def.name
        log.debug("process_each_table: " + table_name)
        if "TRANSFERFUNDx" in table_name:
            log.debug("special table")  # debug stop here
        if table_name + " " in self.not_exposed:
            return "# not_exposed: api.expose_object(models.{table_name})"
        if "ProductDetails_V" in table_name:
            log.debug("special table")  # should not occur (--noviews)
        if table_name.startswith("ab_"):
            return "# skip admin table: " + table_name + "\n"
        elif 'sqlite_sequence' in table_name:
            return "# skip sqlite_sequence table: " + table_name + "\n"
        else:
            class_name = self.mod_gen.get_class_for_table(table_name)
            if class_name is None:
                return "# skip view: " + table_name

            self.num_pages_generated += 1
            component_file_name = self.create_component_file(class_name=class_name)
            with open(component_file_name) as component_file:
                component_code_str = component_file.read().replace("ApiLogicServer_component", class_name)
            with open(component_file_name, 'w') as component_file:
                component_file.write(component_code_str)

            component_file = open(component_file_name)
            # component_code_lines = component_file.readlines()  # lines is list of lines, each element '...\n'
            with open(component_file_name) as component_file:
                component_code_lines = component_file.readlines()

            component_file = open(component_file_name, 'w')
            self.insert_list_lines(a_table_def=a_table_def, component_code_lines=component_code_lines)
            self.insert_show_lines(a_table_def=a_table_def, component_code_lines=component_code_lines)
            self.insert_edit_lines(a_table_def=a_table_def, component_code_lines=component_code_lines)
            self.insert_add_lines(a_table_def=a_table_def, component_code_lines=component_code_lines)
            self.insert_related_lines(a_table_def=a_table_def, component_code_lines=component_code_lines)
            with open(component_file_name, 'w') as component_file:
                component_file.writelines(component_code_lines)
            pass

    def create_component_file(self, class_name: str) -> str:
        """ copy react_admin_templates/component_template.js -> class_name.js

        :param class_name name of component class
        :return name of created component file
        """
        component_template_file = str(self.get_create_from_model_dir())
        if "\\" in component_template_file:
            component_template_file = component_template_file +\
                                      "\\create_from_model\\templates\\react_admin_component.js"
        else:
            component_template_file = component_template_file +\
                                      "/create_from_model/templates/react_admin_component.js"

        to_component = self.mod_gen.project_directory
        if "\\" in to_component:
            to_component = to_component + f'\\ui\\react_admin\\src\\components\\{class_name}.js'
        else:
            to_component = to_component + f'/ui/react_admin/src/components/{class_name}.js'
        # print(f'>> >> >> copy prototype react-admin component {component_template_file} -> {to_component}')
        shutil.copy(component_template_file, to_component)
        return to_component

    def insert_list_lines(self, a_table_def: MetaDataTable, component_code_lines: List[str]):
        """
        find "// ApiLogicServer_list_columns", and insert lines like: <TextField source="ContactName" />
        """
        columns = self.mod_gen.get_list_columns(a_table_def)
        insert_point = self.find_line(lines = component_code_lines, at = "// ApiLogicServer_list_columns")
        for each_column in columns:
            component_code_lines.insert(insert_point, f'            <TextField source="{each_column}"/>\n')
            insert_point += 1
        pass

    def insert_show_lines(self, a_table_def: MetaDataTable, component_code_lines: List[str]):
        columns = self.mod_gen.get_show_columns(a_table_def)
        insert_point = self.find_line(lines = component_code_lines, at = "// ApiLogicServer_show_columns")
        insert_point -= 1
        del component_code_lines[insert_point]
        for each_column in columns:
            component_code_lines.insert(insert_point, f'                <ShowField source="{each_column}"/>\n')
            insert_point += 1
        pass

    def insert_edit_lines(self, a_table_def: MetaDataTable, component_code_lines: List[str]):
        columns = self.mod_gen.get_edit_columns(a_table_def)
        insert_point = self.find_line(lines = component_code_lines, at = "// ApiLogicServer_edit_columns")
        insert_point -= 1
        del component_code_lines[insert_point]
        for each_column in columns:
            component_code_lines.insert(insert_point, f'            <TextInput source="{each_column}"/>\n')
            insert_point += 1
        pass

    def insert_add_lines(self, a_table_def: MetaDataTable, component_code_lines: List[str]):
        columns = self.mod_gen.get_add_columns(a_table_def)
        insert_point = self.find_line(lines = component_code_lines, at = "// ApiLogicServer_add_columns")
        insert_point -= 1
        del component_code_lines[insert_point]
        for each_column in columns:
            component_code_lines.insert(insert_point, f'            <TextField source="{each_column}"/>\n')
            insert_point += 1
        pass

    def insert_related_lines(self, a_table_def: MetaDataTable, component_code_lines: List[str]):
        insert_point = self.find_line(lines = component_code_lines, at = "// ApiLogicServer_related")
        insert_point -= 1
        del component_code_lines[insert_point]

        related_count = 0
        child_list = self.mod_gen.find_child_list(a_table_def)
        if a_table_def.fullname == "store":
            log.debug(f'related_views for {a_table_def.fullname}')
        for each_child in child_list:
            class_name = self.mod_gen.get_class_for_table(each_child.fullname)
            if class_name is None:
                print(f'.. .. .. Warning - Skipping {self.mod_gen.model_name(each_child)}->'
                      f'{each_child.fullname} - no database/models.py class')
                related_count -= 1
            else:
                related_count += 1
                if related_count == 1:
                    child_header = ['<hr style={{ margin: "30px 0px 30px" }}/>\n',
                                    '\t<TabbedShowLayout>\n']
                    component_code_lines[insert_point:insert_point] = child_header
                    insert_point += len(child_header)

                component_code_lines.insert(insert_point,
                                            f'<Tab label="{each_child.fullname} List">\n')
                insert_point += 1

                ref_many = f'<ReferenceManyField reference = "{each_child.fullname}"' \
                           f'target = "{a_table_def.fullname}Id"' \
                           'addLabel = {false}>\n'
                component_code_lines.insert(insert_point, ref_many)
                insert_point += 1

                component_code_lines.insert(insert_point, f'<Datagrid rowClick="show">\n')
                insert_point += 1

                columns = self.mod_gen.get_list_columns(each_child)  # TODO - no join for master
                for each_column in columns:
                    component_code_lines.insert(insert_point, f'            <TextField source="{each_column}"/>\n')
                    insert_point += 1

                component_code_lines.insert(insert_point, "<EditButton />\n")
                insert_point += 1

                component_code_lines.insert(insert_point, "</Datagrid>\n")
                insert_point += 1

                component_code_lines.insert(insert_point, "</ReferenceManyField>\n")
                insert_point += 1

                component_code_lines.insert(insert_point, "</Tab>\n")
                insert_point += 1
        if related_count > 0:
            component_code_lines.insert(insert_point, f'</TabbedShowLayout>\n')
            insert_point += 1
        self.num_related += related_count
        pass  # TODO - tab + child grids

    @staticmethod
    def find_line(lines: List[str], at: str) -> int:
        """ returns line_number after one that contains <at> in <lines>
        """
        find_line_result = 0
        found = False
        for each_line in lines:
            if at in each_line:
                found = True
                break
            find_line_result += 1
        if not found:
            raise Exception(f'Internal error - unable to find insert: {at}')
        return find_line_result + 1

    def app_info_lines(self) -> str:
        """
            returns the last few lines

            comments - # tables etc
        """
        meta_tables = self.mod_gen.metadata.tables
        result = (
            "\n//  "
            + str(len(meta_tables))
            + " table(s) in model; generated "
            + str(self.num_pages_generated)
            + " page(s), including "
            + str(self.num_related)
            + " related_view(s).\n\n"
        )
        if self.num_related == 0:
            result += "//  Warning - no related_views,"
            result += " since foreign keys missing\n"
            result += "//  .. add them to your models.py (see nw example)\n"
            result += "//  .. or better, add them to your database"
            print(".. ..WARNING - no relationships detected - add them to your database or model")
            print(".. ..  See https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design")
        return result

    def get_create_from_model_dir(self) -> str:
        """
        :return: create_from_model dir, eg, /Users/val/dev/ApiLogicServer/create_from_model
        """
        path = Path(__file__)
        parent_path = path.parent
        parent_path = parent_path.parent
        return parent_path

    def fixup_app_js(self):
        app_file_name = self.mod_gen.project_directory
        if "\\" in app_file_name:
            app_file_name = app_file_name + f'\\ui\\react_admin\\src\\App.js'
        else:
            app_file_name = app_file_name + f'/ui/react_admin/src/App.js'

        with open(app_file_name) as app_file:
            server_loc = f'http://{self.mod_gen.host}:{self.mod_gen.port}'
            app_code_str = app_file.read().replace("ApiLogicServer_server_url", server_loc)
        with open(app_file_name, 'w') as app_file:
            app_file.write(app_code_str)

        meta_tables = self.mod_gen.metadata.tables
        with open(app_file_name) as app_file:
            app_file_lines = app_file.readlines()

        import_lines_loc = self.find_line(lines=app_file_lines, at="ApiLogicServer_server_imports")
        import_lines = []
        for each_table in meta_tables.items():
            class_name = self.mod_gen.get_class_for_table(each_table[1].name)
            if class_name:
                imports = f'{class_name}List, {class_name}Edit, {class_name}Show'
                import_line = "import {" + imports + "} from './components/" + class_name + "';\n"
                import_lines.append(import_line)
        app_file_lines[import_lines_loc:import_lines_loc] = import_lines

        resource_lines_loc = self.find_line(lines=app_file_lines, at="<Admin loginPage")
        resource_lines = []
        for each_table in meta_tables.items():
            class_name = self.mod_gen.get_class_for_table(each_table[1].name)
            if class_name:
                resource_line = f'<Resource name="{class_name}" show={{{class_name}Show}} ' \
                                f'edit={{{class_name}Edit}} list={{{class_name}List}} icon={{ContactsIcon}} />\n'
                resource_lines.append(resource_line)
        app_file_lines[resource_lines_loc:resource_lines_loc] = resource_lines

        info_lines_loc = self.find_line(lines=app_file_lines, at="export default App")
        app_file_lines[info_lines_loc:info_lines_loc] = self.app_info_lines()


        # component_file = open(component_file_name, 'w')
        with open(app_file_name, 'w') as app_file:
            app_file.writelines(app_file_lines)
        pass

    def create_react_admin_app(self, msg: str = "", from_git: str = ""):
        """
        deep copy ApiLogicServer/create_from_model/react_admin -> project_directory/ui/react_admin

        :param msg: console log
        :param from_git: git url for source - override ApiLogicServer/create_from_model/react_admin (not impl)
        """
        from_proto_dir = from_git
        if from_proto_dir == "":
            code_loc = str(self.get_create_from_model_dir())
            if "\\" in code_loc:
                from_proto_dir = code_loc + "\\create_from_model\\react_admin"
            else:
                from_proto_dir = code_loc + "/create_from_model/react_admin"

        to_project_dir = self.mod_gen.project_directory
        if "\\" in to_project_dir:
            to_project_dir = to_project_dir + "\\ui\\react_admin"
        else:
            to_project_dir = to_project_dir + "/ui/react_admin"

        print(f'{msg} copy prototype react-admin project {from_proto_dir} -> {to_project_dir}')
        shutil.copytree(from_proto_dir, to_project_dir)

    def create_react_admin_application(self):
        self.create_react_admin_app(msg=".. ..Create ui/react_admin")
        self.create_components(version="")
        self.fixup_app_js()
        pass


def create(model_creation_services: create_from_model.CreateFromModel):
    """ called by ApiLogicServer CLI -- creates ui/react_admin application
    """
    if model_creation_services.react_admin:
        fab_creator = ReactCreator(model_creation_services,
                                   host=model_creation_services.host, port=model_creation_services.port,
                                   not_exposed=model_creation_services.not_exposed + " ",
                                   favorite_names=model_creation_services.favorite_names,
                                   non_favorite_names=model_creation_services.non_favorite_names)
        fab_creator.create_react_admin_application()
    else:
        print("4. ui/react_admin creation declined")

