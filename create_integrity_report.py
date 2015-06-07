from __future__ import print_function

import sys
import json
import base64
import os.path
import settings


def _translate(input_, team, logfile, replacement, open_file):
    def put(string, indentation=0, end='\n'):
        print('  '*indentation + string, end=end, file=open_file)

    put('{')
    put('"target_team": ' + str(team), 1, '')
    put(',')
    put('"type": "integrity",', 1)
    put('"commands": [', 1, '')
    input_ = input_.split("\n")[1:]
    for n, io in enumerate(input_):
        if not io:
            continue
        input_string = io.split(' ')
        if n != 0:
            put(',')
        else:
            put('')
        put('{', 2)
        put('"program": "logread"', 3, '')
        put(',')
        comm = ''
        for n, item in enumerate(input_string):
            if n == 0:
                comm = '"' + item + '"'
            else:
                comm = comm + ', "' + item + '"'
        put('"args": [' + comm + ']', 3, '')
        put('')
        put('}', 2, '')
    put('')
    put('],', 1)
    put('"logfile": "' + logfile + '",', 1)
    with open(replacement, 'r') as open_replacement:
        encoded_replacement = base64.b64encode(open_replacement.read())
    put('"replacement": "' + encoded_replacement + '"', 1)
    put('}')


def translate(input_, team, logfile, replacement, filename=sys.stdout):
    if isinstance(filename, file):
        _translate(input_, team, logfile, replacement, filename)
    else:
        with open(os.path.join(settings.REPORTS_FOLDER, filename), 'w') as open_file:
            _translate(input_, team, logfile, replacement, open_file)
        text_filename = filename.replace("json", "txt")
        os.system("touch {}".format(os.path.join(settings.REPORTS_FOLDER, text_filename)))
    with open(os.path.join(settings.REPORTS_FOLDER, filename), 'r') as open_file:
        try:
            json.load(open_file)
        except ValueError:
            print("malformed json")
            sys.exit(1)
        else:
            sys.exit(0)

'''
Sample:

team = 129
submission = 1
report = "{team}_{submission}.json".format(team=team, submission=submission)
logfile = 'log_file'
replacement = 'replacement_file'
input_ = """
-R -E Fred
"""

translate(input_, team, logfile, replacement, report)
'''
