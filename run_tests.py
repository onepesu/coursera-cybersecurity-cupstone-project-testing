#!/usr/bin/env python
from __future__ import print_function

import re
import os
import os.path
import argparse

from settings import BUILD_PATH

json_re = re.compile('.*\.json$')

current_dir = os.getcwd()
test_dir = os.path.join(current_dir, 'tests')
test_list = [os.path.join(path, filename) for path, _, files
             in os.walk(test_dir) for filename in files
             if re.search(json_re, filename)]

test_prefix = ("python check_test.py --prefix {}/ --test ".format(BUILD_PATH))

to_keep = ('run_tests.py', 'check_test.py', 'settings.template',
           'settings.py', '.gitignore')
log_files = 'clean_test_log', 'test_log'


def clean_folder(extra_files=()):
    file_list = [f for f in os.listdir(current_dir)
                 if os.path.isfile(os.path.join(current_dir, f))]
    for f in file_list:
        if f not in to_keep + extra_files:
            os.system('rm {}'.format(f))

parser = argparse.ArgumentParser()
parser.add_argument('test', nargs='+')
args = parser.parse_args()

clean_folder()
os.system('touch test_log')

if args.test[0] == 'all':
    custom_list = test_list
else:
    custom_list = [test_name for test_name in test_list
                   if re.search(args.test[0], test_name)]

for test_name in custom_list:
    clean_folder(log_files)
    print(re.sub('^' + current_dir + os.sep, '', test_name), end='\t')
    os.system('echo {} >> test_log'.format(test_name))
    os.system(test_prefix + test_name + ' >> test_log')
    with open('test_log', 'r') as test_log:
        test_result = test_log.readlines()[-1]
        if test_result == 'Test passed\n':
            print('\033[92m[OK]\033[0m')
        else:
            print('\033[91m[FAIL]\033[0m')

with open('test_log', 'r') as source:
    with open('clean_test_log', 'w') as target:
        for line in source.readlines():
            if 'running command' not in line and line != 'start_testing\n':
                target.write(line)

clean_folder(log_files)
