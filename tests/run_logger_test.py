import logging
import sys

'''
no logger output when run via  subprocess.check_output (fine when run directly)
'''


def setup_safrs_logger():
    log = logging.getLogger("safrs_logger")
    if log.level == logging.NOTSET:
        output = sys.stderr
        print(f'setup_safrs_logger on: {output}')
        handler = logging.StreamHandler(output)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)
        print(f'.. sys.stdout: {str(output)}')   # sys.stdout: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
        print(f'.. str(log.handlers): {str(log.handlers)}')


def setup_logic_logger():
    setup_logic_logger = True
    if setup_logic_logger:
        output = sys.stdout
        print(f'setup_logic_logger on: {output}')
        logic_logger = logging.getLogger('logic_logger')
        logic_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(output)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        logic_logger.addHandler(handler)
        logic_logger.propagate = True
        print(f'.. sys.stdout: {str(output)}')   # sys.stdout: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
        print(f'.. str(logic_logger.handlers): {str(logic_logger.handlers)}')


print("\nrun_logger_test running")
setup_safrs_logger()
setup_logic_logger()

test_std_logger = False
if test_std_logger:
    print("\ntest std logger")
    logger = logging.getLogger()
    logger.debug("regular logger")

print("\ntest logic_logger")
my_logic_logger = logging.getLogger('logic_logger')
my_logic_logger.debug("===> logic_logger here")

print("\ntest safrs_logger")
safrs_logger = logging.getLogger('safrs_logger')
safrs_logger.debug("===> safrs_logger")

print(f'\n Handlers')
print(f'\nstr(my_logic_logger.handlers): {str(my_logic_logger.handlers)}')
print(f'str(safrs_logger.handlers): {str(safrs_logger.handlers)}')
