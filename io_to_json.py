import json


def translate(input_, output):
    out = {'test': []}
    for input_string, output_dict in zip(input_, output):
        output_dict.update({'input': input_string})
        out['test'].append(output_dict)

    return json.dumps(out)
