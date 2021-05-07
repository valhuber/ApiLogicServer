import subprocess


def run_command(cmd: str, msg: str = "") -> str:
    """ run shell command """
    print(f'\n{msg}...\n')
    result_b = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    result = result_b.decode("utf-8")
    print(f'subprocess.check_output("{cmd}", shell=True)  ...result: {result}')


run_command("python run_logger_test.py localhost",
            msg="\nRun - observe no logic_logger output")