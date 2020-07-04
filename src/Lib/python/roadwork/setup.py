# -*- coding: utf-8 -*-

"""
Copyright (c) Xavier Geerinck.
Licensed under the MIT License.
"""

import os

from setuptools import setup
from subprocess import check_output as run

# Load version in dapr package.
exec(open('roadwork/version.py').read())
version = __version__

name = 'roadwork'
description = 'The official release of Roadwork Python SDK'
long_description = '''
Roadwork is a client server framework that allows developers and data scientists to easily 
run distributed reinforcement learning applications on multi-sim clusters over HTTP.
Roadwork utilizes the Dapr framework underlying as its stable infrastructure layer, with
libraries put on top to provide an abstracted way to interact in a OpenAI Gym kind of way.
'''.lstrip()

# Get build number from GITHUB_RUN_NUMBER environment variable
build_number = os.environ.get('GITHUB_RUN_NUMBER', '0')

version = f'{__version__}'
description = 'The developmental release for Roadwork Python SDK.'
long_description = 'This is the developmental release for Roadwork Python SDK.'

print(f'package name: {name}, version: {version}', flush=True)


setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
)