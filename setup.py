import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(HERE, 'README.md'), 'r') as f:
    long_description = f.read()

# Get the license from the LICENSE file
with open(os.path.join(HERE, 'LICENSE'), 'r') as f:
    license = f.read()

# Get the long description from the README file
version = {}
with open(os.path.join(HERE, 'sensorobjectlibrary', '__version__.py'), 'r') as f:
    exec (f.read(), version)

setup(
    name='sensorobjectlibrary',
    packages=['sensorobjectlibrary'],
    version=version['__version__'],
    description='The Sensor Object Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Thomas Watteyne, Keoma Brun, Sami Malek, Ziran Zhang',
    author_email='keoma.brun@inria.fr',
    url='https://github.com/realms-team/sol',
    keywords=['wireless', 'sensor', 'network'],
    install_requires=[
        'pyserial>=3.4'
    ],
    package_data={'': ['LICENSE']},
    license=license
)
