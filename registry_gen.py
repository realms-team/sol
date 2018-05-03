"""
This file is used to generate the registry.md file
It reads the SolDefines.py file to generate a readable list of SOL Types
"""

import sys
import os

# =========================== adjust path =====================================

sys.path.insert(0, os.getcwd())
from sensorobjectlibrary import SolDefines

# =========================== output file constants ===========================

REGISTRY_FILE   = "registry.md"
INTRO_SEC       = \
"""When a sensor is associated a well-known length, the `L` (length) field MAY be omitted from its binary representation.
When the well-known length is the table below is \"None\", the `L` (length) MUST be present in the object's binary representation.
"""
TAB_HEADER      = \
"""
| value    |     name                                                                    |
|---------:|-----------------------------------------------------------------------------|
|   `0x00` | _reserved_                                                                  |
"""
TAB_BOTTOM      = \
"""|   `0xff` | _reserved_                                                                  |
| `0xffff` | _reserved_                                                                  |
"""
TAB_VAL_SIZE    = 10
TAB_NAME_SIZE   = 77

# =========================== helpers =========================================

def pystruct_to_human(pystruct):
    human_struct = []
    struct_map = {
        "b": "INT8",
        "B": "INT8U",
        "h": "INT16",
        "H": "INT16U",
        "i": "INT32",
        "I": "INT32U",
        "l": "INT32",
        "L": "INT32U",
        "q": "INT64",
        "Q": "INT64U",
        "f": "INT32",
        "p": "INT8",
    }
    for i in range(0,len(pystruct)):
        if struct_map.has_key(pystruct[i]):
            human_struct.append(struct_map[pystruct[i]])
        elif pystruct[i].isdigit():
            human_struct.append(
                    "".join([
                        pystruct[i],
                        struct_map[pystruct[i+1]]
                        ])
                    )
            i+=1
        i+=1
    return human_struct

# =========================== output file generation ==========================

with open(REGISTRY_FILE, 'w') as reg_file:

    # write file head

    reg_file.write(INTRO_SEC)
    reg_file.write(TAB_HEADER)

    # get the SOL Types

    dict_types = {}
    for sol_type in dir(SolDefines):
        if sol_type.startswith('SOL_TYPE_'):
            dict_types[getattr(SolDefines,sol_type)] = sol_type

    # write SOL Types

    for key, value in dict_types.iteritems():
        short_type = value[len("SOL_TYPE_"):]
        reg_file.write("|{0}|{1}|\n".format(
            "".join(["`",format(key, '#04x'),"` "]).rjust(TAB_VAL_SIZE),
            "".join([" [`",short_type,"`](#",short_type.lower(),")"]).ljust(TAB_NAME_SIZE)
            ))

    # write Tab bottom

    reg_file.write(TAB_BOTTOM)

    # write types details

    for item in SolDefines.sol_types:
        fields_lines    = ""
        scores_lines    = ""
        struct_lines    = ""

        # prepare equally sized columns

        for i in range(0, len(item["fields"])):
            field   = item["fields"][i]
            if len(item["structure"]) < 2:
                continue
            struct  = pystruct_to_human(item["structure"][1:])[i]
            max_len = max(len(field), len(struct))

            fields_lines += "| {0} ".format(field.rjust(max_len))
            scores_lines += "|{0}".format("-"*((max_len)+2))
            struct_lines += "| {0} ".format(struct.rjust(max_len))

        # write columns

        reg_file.write("\n#### {0}\n\n{1}|\n{2}|\n{3}|\n".format(
            SolDefines.sol_type_to_type_name(item["type"])[len("SOL_TYPE_"):],
            fields_lines,
            scores_lines,
            struct_lines,
            ))

