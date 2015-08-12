import re

SOL_VERSION = {}

KEYS = ['SOL_VERSION_MAJOR','SOL_VERSION_MINOR','SOL_VERSION_PATCH','SOL_VERSION_BUILD']

with open('sol-version.h') as f:
    lines = f.readlines()
    for k in KEYS:
        for line in lines:
            m = re.search('{0}\s*(\w)'.format(k), line)
            if m:
                SOL_VERSION[k] = int(m.group(1))

for k in KEYS:
    assert SOL_VERSION[k] != None

if __name__=="__main__":
    for k in KEYS:
        print '{0}: {1}'.format(k,SOL_VERSION[k])
    raw_input("Press Enter to close.")