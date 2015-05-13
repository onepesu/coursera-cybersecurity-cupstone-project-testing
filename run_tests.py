#!/usr/bin/env python
import os
import os.path
import argparse

from settings import BUILD_PATH

test_list = [
    "",
    "perf/size/1.json",
    "perf/size/2.json",
    "perf/size/3.json",
    "perf/speed/4.json",
    "perf/speed/5.json",
    "perf/speed/6.json",
    "core/doesitwork/7.json",
    "core/doesitwork/8.json",
    "core/doesitwork/9.json",
    "core/doesitwork/10.json",
    "core/edge/badargs/11.json",
    "core/edge/badargs/12.json",
    "core/edge/badstate/13.json",
    "core/edge/badstate/14.json",
    "core/features/summary/15.json",
    "core/features/summary/16.json",
    "core/features/rooms/17.json",
    "core/features/rooms/18.json",
    "core/batch/19.json",
    "core/batch/20.json",
    "optional/roomhistory/21.json",
    "optional/roomhistory/22.json",
    "optional/time/23.json",
    "optional/time/24.json",
    "perf/size/25.json",
    "perf/size/26.json",
    "perf/speed/27.json",
    "perf/speed/28.json",
    "optional/roomhistory/29.json",
    "optional/roomhistory/30.json",
    "optional/roomhistory/31.json",
    "optional/time/32.json",
    "optional/time/33.json",
    "optional/time/34.json"
]

test_prefix = ("python check_test.py --prefix {}/ --test tests/".format(BUILD_PATH))

current_dir = os.getcwd()
to_keep = 'run_tests.py', 'check_test.py', 'settings.template', 'settings.py', '.gitignore'
log_files = 'clean_test_log', 'test_log'

def clean_folder(extra_files=()):
    files = [f for f in os.listdir(current_dir)
             if os.path.isfile(os.path.join(current_dir, f))]
    for f in files:
        if f not in to_keep + extra_files:
            os.system('rm {}'.format(f))

parser = argparse.ArgumentParser()
parser.add_argument('test', nargs='+')
args = parser.parse_args()

clean_folder()

if args.test[0] == 'all':
    os.system('echo start_testing > test_log')
    for n, test_name in enumerate(test_list):
        clean_folder(log_files)
        if test_name:
            os.system('echo {} >> test_log'.format(n))
            os.system(test_prefix + test_name + ' >> test_log')
    with open('test_log', 'r') as source:
        with open('clean_test_log', 'w') as target:
            for line in source.readlines():
                if 'running command' not in line and line != 'start_testing\n':
                    target.write(line)
else:
    for arg in args.test:
        clean_folder(log_files)
        os.system('echo {} >> test_log'.format(arg))
        os.system(test_prefix + test_list[int(arg)] + ' >> test_log')
    with open('test_log', 'r') as source:
        with open('clean_test_log', 'w') as target:
            for line in source.readlines():
                if 'running command' not in line and line != 'start_testing\n':
                    target.write(line)

clean_folder(log_files)

