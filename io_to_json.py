from __future__ import print_function

start = '    '


def translate(input_, output):
    print('{')
    print(start + '"tests": [')
    for n, io in enumerate(zip(input_, output)):
        input_string, output_dict = io
        if n != 0:
            print(',')
        else:
            print('')
        print(2*start + '{')
        print(3*start + '"input": "' + input_string, end='"')
        if output_dict.get('exit'):
            print(',')
            print(3*start + '"exit": "' + str(output_dict['exit']), end='"')
        if output_dict.get('output'):
            print(',')
            print(3*start + '"output": "' + repr(output_dict['output'])[1:-1],
                  end='"')
        print('')
        print(2*start + '}', end='')

    print('')
    print(start + ']')
    print('}')
