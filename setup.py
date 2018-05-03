import os
from setuptools import setup

import sensorobjectlibrary.Sol as sol

HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(HERE, 'README.md'), 'r') as f:
    long_description = f.read()

# Get the long description from the README file
with open(os.path.join(HERE, 'license.txt'), 'r') as f:
    license = f.read()

setup(
    name = 'sensorobjectlibrary',
    packages = ['sensorobjectlibrary'],
    version = '.'.join(str(i) for i in sol.VERSION),
    description = 'The Sensor Object Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Thomas Watteyne, Keoma Brun, Sami Malek, Ziran Zhang',
    author_email = 'keoma.brun@inria.fr',
    url = 'https://github.com/realms-team/sol',
    keywords = ['wireless', 'sensor', 'network'],
    package_data = {'': ['license.txt']},
    license=license
)
