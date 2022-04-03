#!/usr/bin/env python

# -*- coding: utf-8 -*-
# ASSUMPTION: behave is installed.

# shoutout: https://github.com/behave/behave/issues/709

import sys, os
import datetime
from behave.__main__ import main as behave_main  # behave is pip'd...

if __name__ == "__main__":
    print("\nbehave_run started at:", os.getcwd())

    behave_result = behave_main()

    log_file_name = None
    n = len(sys.argv)
    for i in range(1, n):
        arg = sys.argv[i]
        if sys.argv[i].startswith("--outfile"):
            log_file_name = sys.argv[i][10:]
        
    date_time = str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S"))
    if log_file_name is None:
        sys.stdout.write(f'\nCompleted at {date_time}')
    else:
        with open(log_file_name, 'a') as log_file:
            log_file.write(f'')
            log_file.write(f'&nbsp;&nbsp;')
            log_file.write(f'')
            log_file.write(f'\nCompleted at {date_time}')
    print(f'\ndebug_behave exit at {date_time}\n\n')
    sys.exit(behave_result)