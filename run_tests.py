#!/usr/bin/env python
from __future__ import print_function

import re
import os
import os.path
import argparse
import subprocess

import settings

OK = '\033[92m[OK]\033[0m'
FAIL = '\033[91m[FAIL]\033[0m'
json_re = re.compile('.*\.json$')

current_dir = os.getcwd()
test_dir = os.path.join(current_dir, 'tests')
test_list = [
    os.path.join(path, filename) for path, _, files in os.walk(test_dir)
    for filename in files if re.search(json_re, filename)
]

to_keep = (
    'run_tests.py', 'check_test.py', 'settings.template', 'settings.py',
    '.gitignore', 'io_to_json.py', 'create_integrity_report.py',
    'create_confidentiality_report', 'create_correctness_or_crash_report.py'
)
log_files = 'failed_test_log', 'test_log'


def clean_folder(extra_files=()):
    file_list = [f for f in os.listdir(current_dir)
                 if os.path.isfile(os.path.join(current_dir, f))]
    for f in file_list:
        if f not in to_keep + extra_files:
            os.system('rm ./{}'.format(f))

parser = argparse.ArgumentParser()
parser.add_argument('test', nargs='*')
parser.add_argument('--team', nargs='?')
args = parser.parse_args()

clean_folder()
os.system('touch test_log')
os.system('touch failed_test_log')

if args.test:
    custom_list = [
        test_name for test_name in test_list
        if re.search(
            args.test[0], re.sub('^' + test_dir + os.sep, '', test_name)
        )
    ]
else:
    custom_list = test_list

if args.team:
    path_to_build = settings.ALTERNATIVE_BUILD_PATH.format(args.team)
    os.system('echo Testing team {}'.format(args.team))
else:
    path_to_build = settings.BUILD_PATH

if path_to_build[-1] != '/':
    path_to_build += '/'

test_prefix = 'check_test.py --prefix {} --test '.format(path_to_build)

n = max([len(test_name) for test_name in custom_list])
failures = False

for i, test_name in enumerate(custom_list):
    clean_folder(log_files)
    short_test_name = re.sub('^' + test_dir + os.sep, '', test_name)
    print(short_test_name, end=' '*(n-len(test_name)) + '\t')
    arguments = (test_prefix + test_name).split(' ')
    process = subprocess.Popen(
        arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    try:
        test_result = out.split('\n')[-2]
    except IndexError:
        test_result = 'Test crashed'
    if err:
        test_result = 'Test crashed'
    start = '\n' if i else ''
    with open('test_log', 'a') as test_log:
        test_log.write(start + short_test_name + '\n')
        test_log.write(test_result + '\n')
        test_log.write(out)
        if err:
            test_log.write('CRASH:\n')
            test_log.write(err)
    if test_result == 'Test passed':
        print(OK)
    else:
        print(FAIL)
        start = '\n' if failures else ''
        failures = True
        with open('failed_test_log', 'a') as failed_test_log:
            failed_test_log.write(start + short_test_name + '\n')
            failed_test_log.write(test_result + '\n')
            failed_test_log.write(out)
            if err:
                failed_test_log.write('CRASH:\n')
                failed_test_log.write(err)

clean_folder(log_files)
