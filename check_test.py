#!/usr/bin/env python
from __future__ import print_function

import os
import argparse
import subprocess
import base64
import json


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def main(testin, prefix):
    t = json.load(file(testin, 'r'))
    # write out the batch file, if present
    if 'batch' in t:
        buf = t['batch']
        buf = base64.b64decode(buf)
        bufout = file('batch', 'w')
        bufout.write(buf)
        bufout.close()
    # run all of the commands and test their outputs
    cmds = t['tests']
    passed = True
    for i in cmds:
        inpt = i['input']
        args = inpt.split(" ")
        cmd = prefix + args[0]
        args[0] = cmd
        print("running command {}".format(inpt))
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        ret = p.returncode
        # check and see if out,err,ret match what is in this test
        expectedout = ""
        expectederr = ""
        expectedret = 0
        if 'output' in i:
            expectedout = i['output']
        if 'error' in i:
            expectederr = i['error']
        if 'exit' in i:
            expectedret = i['exit']
        truncated_out = out.replace("\n", "").replace("\r", "").replace(" ", "")
        truncated_error = err.replace("\n", "").replace("\r", "").replace(" ", "")
        truncated_expected_out = expectedout.replace("\n", "").replace("\r", "").replace(" ", "")
        truncated_expected_error = expectederr.replace("\n", "").replace("\r", "").replace(" ", "")
        if truncated_out != truncated_expected_out:
            print("got:\n{}expected:\n{}".format(out, expectedout), end='')
            passed = False
        if truncated_error != truncated_expected_error:
            print("got:\n{}expected:\n{}".format(err, expectederr), end='')
            passed = False
        if ret != expectedret:
            print("got:\n{}expected:\n{}".format(ret, expectedret), end='')
            passed = False
    if passed is True:
        print("Test passed")
    else:
        print("Test failed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test executor')
    parser.add_argument('--prefix', dest='prefix', type=str, default=".",
                        help='program prefix')
    parser.add_argument('--test', dest='test', type=str, default="test.json", required=True,
                        help='test input')

    args = parser.parse_args()
    main(args.test, args.prefix)
