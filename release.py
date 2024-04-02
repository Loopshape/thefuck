#!/usr/bin/env python
from subprocess import call
import os
import re


version = None


def get_new_setup_py_lines():
    global version
    with open('setup.py', 'r') as sf:
        current_setup = sf.readlines()
    for line in current_setup:
        if line.startswith('VERSION = '):
            major, minor = re.findall(r"VERSION = '(\d+)\.(\d+)'", line)[0]
            version = "{}.{}".format(major, int(minor) + 1)
            yield "VERSION = '{}'\n".format(version)
        else:
            yield line


lines = list(get_new_setup_py_lines())
with open('setup.py', 'w') as sf:
    sf.writelines(lines)

call('git pull', shell=False)
call('git commit -am "Bump to {}"'.format(version), shell=False)
call('git tag {}'.format(version), shell=False)
call('git push', shell=False)
call('git push --tags', shell=False)

env = os.environ
env['CONVERT_README'] = 'true'
call('python setup.py sdist bdist_wheel upload', shell=False, env=env)
