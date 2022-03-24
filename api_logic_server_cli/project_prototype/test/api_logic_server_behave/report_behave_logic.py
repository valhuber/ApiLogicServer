import requests
from pathlib import Path
import os
import ast
import sys

"""
Creates wiki file from test/behave/behave.log, with rule use.

Tips
* use 2 spaces (at end) for newline
* for tab: & emsp;

"""

tab = "&emsp;"
debug_info = "# features"
wiki_data = []
debug_scenario = "Custom Service: add_order - good"
logic_logs_dir = "scenario_logic_logs"

scenario_doc_strings = {}
""" dict of scenario_name, array of strings """


def remove_trailer(line: str) -> str:
    """ remove everything after the ## """
    end_here = line.find("\t\t##")
    result = line[0:end_here]
    return result

def line_spacer():
    wiki_data.append("\n")
    wiki_data.append("&nbsp;")
    wiki_data.append("&nbsp;")
    wiki_data.append("\n")


def get_current_readme():
    """ initialize wiki_data with readme up to 'TDD Report' """
    TDD_report_name = "TDD Report"
    readme_file_name = '../../readme.md'
    with open(readme_file_name) as readme:
        readme_lines = readme.readlines()
    for each_readme_line in readme_lines:
        if '# ' + TDD_report_name in each_readme_line:
            break
        wiki_data.append(each_readme_line[0:-1])
    line_spacer()
    wiki_data.append("# TDD Report")

def get_truncated_scenario_name(scenario_name: str) -> str:
    """ address max file length (chop at 26), illegal characters """
    scenario_trunc = scenario_name
    if scenario_trunc is not None and len(scenario_trunc) >= 26:
        scenario_trunc = scenario_name[0:25]
    scenario_trunc = f'{str(scenario_trunc).replace(" ", "_")}'
    return scenario_trunc


def show_logic(scenario: str):
    """ insert s{logic_logs_dir}/scenario.log into wiki_data as disclosure area """
    scenario_trunc = get_truncated_scenario_name(scenario)
    logic_file_name = f'{logic_logs_dir}/{scenario_trunc}.log'
    logic_file_name_path = Path(logic_file_name)
    if not logic_file_name_path.is_file():  # debug code
        # wiki_data.append(f'unable to find Logic Log file: {logic_file_name}')
        if scenario == debug_scenario:
            print(f'RELATIVE: {logic_file_name} in {os.getcwd()}')
            full_name = f'{os.getcwd()}/{logic_file_name}'
            print(f'..FULL: {os.getcwd()}/{logic_file_name}')
            logic_file_name = '{logic_logs_dir}/test.log'
            with open(logic_file_name) as logic:
                logic_lines = logic.readlines()
            # finder:  /Users/val/dev/TDD/test/api_logic_server_behave/{logic_logs_dir}
            # seeking: /Users/val/dev/TDD/test/api_logic_server_behave/{logic_logs_dir}/Custom Service: add_order - good.log
    else:
        logic_log = []
        rules_used = []
        wiki_data.append("<details>")
        wiki_data.append("<summary>Tests - and their logic - are transparent.. click to see Logic</summary>")
        line_spacer()
        scenario_trunc = get_truncated_scenario_name(scenario)
        if scenario_trunc in scenario_doc_strings:
            wiki_data.append(f'**Logic Doc** for scenario: {scenario}')
            wiki_data.append("   ")
            for each_doc_string_line in scenario_doc_strings[scenario_trunc]:
                wiki_data.append(each_doc_string_line[0: -1])
            line_spacer()
        wiki_data.append(f'**Rules Used** in Scenario: {scenario}')
        wiki_data.append("```")
        with open(logic_file_name) as logic:
            logic_lines = logic.readlines()
        is_logic_log = True
        for each_logic_line in logic_lines:
            each_logic_line = remove_trailer(each_logic_line)
            if is_logic_log:
                if "Rules Fired" in each_logic_line:
                    is_logic_log = False
                    continue
                else:
                    logic_log.append(each_logic_line)
            else:
                if 'logic_logger - INFO' in each_logic_line:
                    pass
                    break
                wiki_data.append(each_logic_line + "  ")
        wiki_data.append("```")
        wiki_data.append(f'**Logic Log** in Scenario: {scenario}')
        wiki_data.append("```")
        for each_logic_log in logic_log:
            each_line = remove_trailer(each_logic_log)
            wiki_data.append(each_line)
        wiki_data.append("```")
        wiki_data.append("</details>")


def get_docStrings(steps_dir: str):
    steps_dir_files = os.listdir(steps_dir)
    indent = 4  # skip leading blanks
    for each_steps_dir_file in steps_dir_files:
        each_steps_dir_file_path = Path(steps_dir).joinpath(each_steps_dir_file)
        if each_steps_dir_file_path.is_file():
            with open(each_steps_dir_file_path) as f:
                step_code = f.readlines()
            # print(f'Found File: {str(each_steps_dir_file_path)}')
            for index, each_step_code_line in enumerate(step_code):
                if each_step_code_line.startswith('@when'):
                    comment_start = index + 2
                    if '"""' in step_code[comment_start]:
                        # print(".. found doc string")
                        doc_string_line = comment_start+1
                        doc_string = []
                        while (True):
                            if '"""' in step_code[doc_string_line]:
                                break
                            doc_string.append(step_code[doc_string_line][indent:])
                            doc_string_line += 1
                        scenario_line = doc_string_line+1
                        if 'scenario_name' not in step_code[scenario_line]:
                            print(f'\n** Warning - scenario_name not found '\
                                f'in file {str(each_steps_dir_file_path)}, '\
                                f'after line {scenario_line} -- skipped')
                        else:
                            scenario_code_line = step_code[scenario_line]
                            scenario_name_start = scenario_code_line.find("'") + 1
                            scenario_name_end = scenario_code_line[scenario_name_start+1:].find("'")
                            scenario_name = scenario_code_line[scenario_name_start: 
                                scenario_name_end + scenario_name_start+1]
                            scenario_trunc = get_truncated_scenario_name(scenario_name)
                            # print(f'.... truncated scenario_name: {scenario_trunc} in {scenario_code_line}')
                            scenario_doc_strings[scenario_trunc] = doc_string
    # print("that's all, folks")


def main(behave_log: str):
    get_docStrings(steps_dir="features/steps")

    get_current_readme()

    contents = None
    with open(behave_log) as f:
        contents = f.readlines()

    just_saw_then = False
    current_scenario = ""
    for each_line in contents:
        if just_saw_then and each_line == "\n":
            show_logic(current_scenario)
        just_saw_then = False
        if each_line.startswith("Feature"):
            wiki_data.append("&nbsp;")
            wiki_data.append("&nbsp;")
            each_line = "## " + each_line
        if each_line.startswith("  Scenario"):
            each_line = tab + each_line
        if each_line.startswith("    Given") or \
                each_line.startswith("    When") or \
                each_line.startswith("    Then"):
            if each_line.startswith("    Then"):
                just_saw_then = True
            each_line = tab + tab + each_line

        each_line = each_line[:-1]
        debug_loc = each_line.find(debug_info)
        if debug_loc > 0:
            each_line = each_line[0 : debug_loc]
        each_line = each_line.rstrip()
        if "Scenario" in each_line:
            current_scenario = each_line[18:]
            wiki_data.append("&nbsp;")
            wiki_data.append("&nbsp;")
            wiki_data.append("### " + each_line[8:])

        each_line = each_line + "  "  # wiki for "new line"
        
        wiki_data.append(each_line)

    report_name = 'report_behave_logic.md'
    with open(report_name, 'w') as rpt:
        rpt.write('\n'.join(wiki_data))
    print(f'* Output: {report_name}\n***\n\n')

if __name__ == "__main__":
    print(f'\n***\n* Begin:  starting Behave Logic Report.py, at {os.getcwd()}')
    main(behave_log = 'behave.log')
