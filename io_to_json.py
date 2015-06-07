from __future__ import print_function

import sys
import os.path
import settings


def _translate(input_, output, batch, open_file):
    def put(string, indentation=0, end='\n'):
        print('  '*indentation + string, end=end, file=open_file)

    put('{')
    put('"tests": [', 1, '')
    for n, io in enumerate(zip(input_, output)):
        input_string, output_dict = io
        if n != 0:
            put(',')
        else:
            put('')
        put('{', 2)
        put('"input": "' + input_string, 3, '"')
        if output_dict.get('output'):
            put(',')
            put('"output": "' + repr(output_dict['output'])[1:-1], 3, '"')
        if output_dict.get('error'):
            put(',')
            put('"error": "' + repr(output_dict['error'])[1:-1], 3, '"')
        if output_dict.get('exit'):
            put(',')
            put('"exit": ' + str(output_dict['exit']), 3, '')
        put('')
        put('}', 2, '')

    put('')
    if batch is None:
        put(']', 1)
    else:
        put('],', 1)
        put('"batch": "{batch}"'.format(batch=batch), 1)
    put('}')


def translate(input_, output, batch=None, filename=sys.stdout):
    if isinstance(filename, file):
        _translate(input_, output, batch, filename)
    else:
        with open(os.path.join(settings.TEST_FOLDER, filename), 'w') as open_file:
            _translate(input_, output, batch, open_file)
