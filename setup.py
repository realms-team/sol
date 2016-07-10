from distutils.core import setup

import solobjectlib.SolVersion as ver

setup(
  name = 'solobjectlib',
  packages = ['solobjectlib'], # this must be the same as the name above
  version = '.'.join(str(i) for i in ver.VERSION),
  description = 'The Sensor Object Library',
  author = 'Thomas Watteyne, Keoma Brun, Sami Malek, Ziran Zhang',
  author_email = 'keoma.brun@inria.fr',
  url = 'https://github.com/realms-team/sol', # use the URL to the github repo
  download_url = 'https://github.com/realms-team/sol/releases/tag/REL-0.0.5',
  keywords = ['wireless', 'sensor', 'network'], # arbitrary keywords
  classifiers = [],
)
