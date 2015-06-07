from __future__ import print_function

import sys
import json
import base64
import os.path
import settings
from io_to_json import translate as trans


def _translate(break_submission, break_file_name):
    inp = []
    outp = []
    for command in break_submission['commands']:
        formated_command = {}
        arguments = ' '.join(command['args'])
        formated_command['input'] = command['program'] + ' ' + arguments
        formated_command['outputdict'] = {}
        formated_command['outputdict']['output'] = command['oracle_out']
        formated_command['outputdict']['error'] = command['oracle_err']
        formated_command['outputdict']['exit'] = command['oracle_ret']
        if break_submission.get('batch'):
            raise ValueError()
            # formated_command['batch'] = break_submission['batch']
            # trans(formated_command['input'], formated_command['outputdict'], break_file_name, batch=formated_command['batch'])
        else:
            inp.append(formated_command['input'])
            outp.append(formated_command['outputdict'])

    trans(inp, outp, break_file_name)


def translate(break_file_name=sys.stdout):
    with open(os.path.join(settings.BREAKS, break_file_name), 'r') as break_file:
        try:
            break_submission = json.load(break_file)
        except ValueError:
            print("malformed json")
            print(break_file_name)
        else:
            _translate(break_submission, break_file_name)


translate("873_team129usedotlog.json")