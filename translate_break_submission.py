from __future__ import print_function

import sys
import json
import os.path
import settings
from io_to_json import translate as trans


def _translate(in_submission, out_submission, break_file_name):
    inp = []
    outp = []
    for in_command, out_command in zip(in_submission['commands'], out_submission['commands']):
        formated_command = {}
        arguments = ' '.join(in_command['args'])
        formated_command['input'] = in_command['program'] + ' ' + arguments
        formated_command['outputdict'] = {}
        formated_command['outputdict']['output'] = out_command['oracle_out']
        formated_command['outputdict']['error'] = out_command['oracle_err']
        formated_command['outputdict']['exit'] = out_command['oracle_ret']
        inp.append(formated_command['input'])
        outp.append(formated_command['outputdict'])
    if in_submission.get('batch'):
        trans(inp, outp, in_submission['batch'], break_file_name)
    else:
        trans(inp, outp, filename=break_file_name)


def translate(break_file_name=sys.stdout):
    with open(os.path.join(settings.BREAKS_NO_ORACLE, break_file_name), 'r') as in_break_file:
        try:
            in_submission = json.load(in_break_file)
        except ValueError:
            print("malformed json")
            print(in_submission)
        else:
            with open(os.path.join(settings.BREAKS, break_file_name), 'r') as out_break_file:
                try:
                    out_submission = json.load(out_break_file)
                except ValueError:
                    pass
                else:
                    _translate(in_submission, out_submission, break_file_name)
