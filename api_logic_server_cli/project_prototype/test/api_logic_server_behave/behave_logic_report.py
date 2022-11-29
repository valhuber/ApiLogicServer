import requests
from pathlib import Path
import os
import ast
import sys
import click

"""
Creates wiki file from test/behave/behave.log, with rule use.

Tips
* use 2 spaces (at end) for newline
* for tab: & emsp;

"""

tab = "&emsp;"
behave_debug_info = " # "
wiki_data = []
debug_scenario = "XXGood Order Custom Service"

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


def get_current_readme(prepend_wiki: str):
    """ initialize wiki_data with readme up to {report_name} """
    report_name = "Behave Logic Report"
    with open(prepend_wiki) as readme:
        readme_lines = readme.readlines()
    need_spacer = True
    for each_readme_line in readme_lines:
        if '# ' + report_name in each_readme_line:
            need_spacer = False
            break
        wiki_data.append(each_readme_line[0:-1])
    if need_spacer:
        line_spacer()
    wiki_data.append(f'# {report_name}')

def get_truncated_scenario_name(scenario_name: str) -> str:
    """ address max file length (chop at 26), illegal characters """
    scenario_trunc = scenario_name
    if scenario_trunc is not None and len(scenario_trunc) >= 26:
        scenario_trunc = scenario_name[0:25]
    scenario_trunc = f'{str(scenario_trunc).replace(" ", "_")}'
    return scenario_trunc


def show_logic(scenario: str, logic_logs_dir: str):
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
    else:
        logic_log = []
        rules_used = []
        wiki_data.append("<details markdown>")
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
                            if scenario_name == debug_scenario:
                                print(f'got {debug_scenario}')
                            scenario_trunc = get_truncated_scenario_name(scenario_name)
                            # print(f'.... truncated scenario_name: {scenario_trunc} in {scenario_code_line}')
                            scenario_doc_strings[scenario_trunc] = doc_string
    # print("that's all, folks")


def main(behave_log: str, scenario_logs: str, wiki: str, prepend_wiki: str):
    """ main driver """
    get_docStrings(steps_dir="features/steps")

    get_current_readme(prepend_wiki=prepend_wiki)

    contents = None
    with open(behave_log) as f:
        contents = f.readlines()

    just_saw_then = False
    current_scenario = ""
    for each_line in contents:
        if just_saw_then and each_line == "\n":
            show_logic(scenario=current_scenario, logic_logs_dir=scenario_logs)
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
        debug_loc = each_line.find(behave_debug_info)
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

    with open(wiki, 'w') as rpt:
        rpt.write('\n'.join(wiki_data))
    wiki_full_path = Path(wiki).absolute()
    print(f'Wiki Output: {wiki_full_path}\n\n')



def print_args(args, msg):
    print(msg)
    for each_arg in args:
        print(f'  {each_arg}')
    print(" ")


@click.group()
@click.pass_context
def cli(ctx):
    """
    Combine behave.log and scenario_logic_logs to create Behave Logic Report

    """
    pass


@cli.command("run")
@click.pass_context
@click.option('--behave_log',
              default=f'logs/behave.log',  # cwd set to test/api_logic_server_behave
              # prompt="Log from behave test suite run [behave.log]",
              help="Help")
@click.option('--scenario_logs',
              default=f'logs/scenario_logic_logs',
              # prompt="Logic Log directory from ",
              help="Help")
@click.option('--wiki',
              default=f'reports/Behave Logic Report.md',
              # prompt="Log from behave test suite run [api_logic_server_behave]",
              help="Help")
@click.option('--prepend_wiki',
              default=f'reports/Behave Logic Report Intro micro.md',
              # prompt="Log from behave test suite run [Behave Logic Report Intro]",
              help="Help")
def run(ctx, behave_log: str, scenario_logs: str, wiki: str, prepend_wiki: str):
    main(behave_log = behave_log, scenario_logs = scenario_logs, wiki = wiki, prepend_wiki = prepend_wiki)


if __name__ == '__main__':  # debugger & python command line start here
    # eg: python api_logic_server_cli/cli.py create --project_name=~/Desktop/test_project
    # unix: python api_logic_server_cli/cli.py create --project_name=/home/ApiLogicProject

    print(f'\nBehave Logic Report 1.1, started at {os.getcwd()}')
    commands = sys.argv
    if len(sys.argv) > 1:
        print_args(commands, f'\n\nCommand Line Arguments:')
    cli()
