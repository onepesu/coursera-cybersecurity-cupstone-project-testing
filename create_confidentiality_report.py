from __future__ import print_function

import sys
import os.path
import settings


def _translate(input_, team, logfile, output_, open_file):
    def put(string, indentation=0, end='\n'):
        print('    '*indentation + string, end=end, file=open_file)

    output = 0
    put('{')
    put('"target_team": ' + str(team), 1, '')
    put(',')
    put('"type": "confidentiality",', 1)
    put('"logfile": "' + logfile + '",', 1)
    put('"commands": [', 1)
    put('{', 2)
    input_ = input_.replace("running command ", '')
    input_ = input_.replace("\n", '')
    input_ = input_.split(" ")
    put('"program": "logread",', 2)
    comm = ''
    for n, item in enumerate(input_[1:]):
        if n == 0:
            comm = '"' + item + '"'
        else:
            comm = comm + ', "' + item + '"'
    put('"args": [' + comm + '],', 2)
    put('"output": "' + str(output_) + '"', 2)
    put('}', 2)
    put(']', 1)
    put('}')


def translate(input_, team, logfile, output_, filename=sys.stdout):
    if isinstance(filename, file):
        _translate(input_, team, logfile, output_, filename)
    else:
        with open(os.path.join(settings.REPORTS_FOLDER, filename), 'w') as open_file:
            _translate(input_, team, logfile, output_, open_file)
        text_filename = filename.replace("json", "txt")
        os.system("touch {}".format(os.path.join(settings.REPORTS_FOLDER, text_filename)))

'''
Sample:

input_ = """
running command logread -S -K token1 log1
"""

team = 129

delete_this = "delete_this.json"

logfile = 'yeah'

replacement = 15

translate(input_, team, logfile, replacement, delete_this)
'''

