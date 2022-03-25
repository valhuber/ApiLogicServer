#!/usr/bin/env python

# -*- coding: utf-8 -*-
# ASSUMPTION: behave is installed.

# shoutout: https://github.com/behave/behave/issues/709

import sys
import datetime
from behave.__main__ import main as behave_main  # behave is pip'd...

if __name__ == "__main__":
    # sys.exit(behave_main())
    behave_result = behave_main()
    date_time = str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S"))
    sys.stdout.write(f'\nCompleted at {date_time}')
    sys.stderr.write(f'\ndebug_behave exit at {date_time}\n\n')
    sys.exit(behave_result)