from __future__ import print_function

import sys
import json
import base64
import os.path
import settings

from io_to_json import translate as trans


def _translate(submission, break_file_name):
    inp = []
    outp = []
    for command in submission['commands']:
        formated_command = {}
        arguments = ' '.join(command['args'])
        formated_command['input'] = command['program'] + ' ' + arguments
        formated_command['outputdict'] = {}
        formated_command['outputdict']['output'] = base64.b64decode(command['oracle_out'])
        formated_command['outputdict']['error'] = base64.b64decode(command['oracle_err'])
        formated_command['outputdict']['exit'] = command['oracle_ret']
        inp.append(formated_command['input'])
        outp.append(formated_command['outputdict'])
    if submission.get('batch'):
        trans(inp, outp, submission['batch'], break_file_name)
        return submission['batch']
    else:
        trans(inp, outp, filename=break_file_name)


def translate(break_file_name):
    with open(os.path.join(settings.READ_TESTS, break_file_name + '.json'), 'r') as break_file:
        submission = json.load(break_file)
        batch = _translate(submission, break_file_name + '.json')
    with open(os.path.join(settings.READ_TESTS, break_file_name + '.txt'), 'r') as in_txt:
        with open(os.path.join(settings.WRITE_TESTS, break_file_name + '.txt'), 'w') as out_txt:
            out_txt.write(in_txt.read())
    if batch:
        with open(os.path.join(settings.WRITE_TESTS, break_file_name + '.batch.txt'), 'w') as batch_file:
            batch_file.write(base64.b64decode(batch))
