from __future__ import print_function

import sys
import os.path
import settings


def _translate(input_, team, type_, batch, open_file):
    def put(string, indentation=0, end='\n'):
        print('    '*indentation + string, end=end, file=open_file)

    output = 0
    put('{')
    put('"target_team": ' + str(team), 1, '')
    put(',')
    put('"type": "' + type_ + '",', 1)
    put('"commands": [', 1, '')
    input_ = input_.replace("running command ", '')
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
        put('"program": "' + input_string[0], 3, '"')
        put(',')
        comm = ''
        for n, item in enumerate(input_string[1:]):
            if n == 0:
                comm = '"' + item + '"'
            else:
                comm = comm + ', "' + item + '"'
        put('"args": [' + comm + ']', 3, '')
        put('')
        put('}', 2, '')
    put('')
    put('],', 1)
    if batch:
        put('"batch": "' + batch + '"', 1, '')
    put('}')


def translate(input_, team, filename=sys.stdout, type_="correctness", batch=''):
    if isinstance(filename, file):
        _translate(input_, team, type_, batch, filename)
    else:
        with open(os.path.join(settings.REPORTS_FOLDER, filename), 'w') as open_file:
            _translate(input_, team, type_, batch, open_file)
        text_filename = filename.replace("json", "txt")
        os.system("touch {}".format(os.path.join(settings.REPORTS_FOLDER, text_filename)))

'''
Sample:

input_ = """
running command logappend -T 1 -K secret -A -E Fred log1
running command logappend -T 2 -K secret -A -E Fred -R 1 log1
running command logappend -T 3 -K secret -L -E Fred -R 2 log1
"""

team = 129

delete_this = "delete_this.json"

batch = 'yeah'

translate(input_, team, delete_this, batch=batch)
'''
