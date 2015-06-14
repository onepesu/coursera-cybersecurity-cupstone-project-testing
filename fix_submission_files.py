from __future__ import print_function

import sys
import json
import os.path
import settings


def write_submission(open_file, commit_hash, teams):
    def put(string, indentation=0, end='\n'):
        print('  '*indentation + string, end=end, file=open_file)

    put('{')
    put('"commit": "' + commit_hash + '",', 1)
    put('"breaks": [' + ', '.join(teams) + ']', 1)
    put('}')


def make_files(filename, commit_hash, teams, justification):
    submission_name = filename + '.json'
    submission_file = os.path.join(settings.SUBMISSION_JSON_FILES, submission_name)
    txt_file = filename + '.txt'
    txt_file = os.path.join(settings.SUBMISSION_JUSTIFICATION_FILES, txt_file)

    with open(txt_file, 'w') as justify:
        justify.write(justification)

    with open(submission_file, 'w') as submission:
        write_submission(submission, commit_hash, teams)

    with open(submission_file, 'r') as submission:
        try:
            json.load(submission)
        except ValueError:
            print("The json file wasn't writen correctly")
            sys.exit(1)


def make_files_from_folder(folder_name, commit_hash, justification):
    folder = settings.BREAK_TESTS + '/' + folder_name
    submission_id_list = []
    for bug_report in os.listdir(folder):
        if bug_report[-5:] != '.json':
            continue
        else:
            submission_id_list.append(bug_report.split('_')[0])
    submission_id_list.sort(key=lambda x: int(x))
    if submission_id_list:
        justification = justification[1:]
        make_files(folder_name, commit_hash, submission_id_list, justification)
        print(len(submission_id_list))
    else:
        print("There is nothing in this folder")

'''
Sample:

folder_name = "sorted_i"

commit_hash = "1a23456"

justification = """
nothing
"""

make_files_from_folder(folder_name, commit_hash, justification)
'''
