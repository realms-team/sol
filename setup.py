from distutils.core import setup

import sensorobjectlibrary.Sol as sol

with open('README.md') as f:
    readme = f.read()

with open('license.txt') as f:
    license = f.read()

setup(
    name = 'sensorobjectlibrary',
    packages = ['sensorobjectlibrary'],
    version = '.'.join(str(i) for i in sol.VERSION),
    description = 'The Sensor Object Library',
    long_description=readme,
    author = 'Thomas Watteyne, Keoma Brun, Sami Malek, Ziran Zhang',
    author_email = 'keoma.brun@inria.fr',
    url = 'https://github.com/realms-team/sol',
    keywords = ['wireless', 'sensor', 'network'],
    licence=license
)
