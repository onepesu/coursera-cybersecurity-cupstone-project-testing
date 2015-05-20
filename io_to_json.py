from __future__ import print_function

import sys

start = '    '


def _translate(input_, output, open_file=sys.stdout):
    print('{', file=open_file)
    print(start + '"tests": [', end='', file=open_file)
    for n, io in enumerate(zip(input_, output)):
        input_string, output_dict = io
        if n != 0:
            print(',', file=open_file)
        else:
            print('', file=open_file)
        print(2*start + '{', file=open_file)
        print(3*start + '"input": "' + input_string, end='"', file=open_file)
        if output_dict.get('output'):
            print(',', file=open_file)
            print(3*start + '"output": "' + repr(output_dict['output'])[1:-1],
                  end='"', file=open_file)
        if output_dict.get('exit'):
            print(',', file=open_file)
            print(3*start + '"exit": ' + str(output_dict['exit']), end='',
                  file=open_file)
        print('', file=open_file)
        print(2*start + '}', end='', file=open_file)

    print('', file=open_file)
    print(start + ']', file=open_file)
    print('}', file=open_file)


def translate(input_, output, filename=None):
    if filename is None:
        _translate(input_, output)
    else:
        with open(filename, 'w') as open_file:
            _translate(input_, output, open_file)
