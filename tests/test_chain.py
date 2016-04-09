import pytest
import json


import sys
print sys.path

from   SmartMeshSDK.IpMgrConnectorMux  import IpMgrConnectorMux

#============================ defines ===============================


#============================ fixtures ==============================

SOL_CHAIN_EXAMPLE = [
    {
        "dust":
            "IpMgrConnectorMux.IpMgrConnectorMux.Tuple_notifData(    \
                utcSecs      = 1111,                                 \
                utcUsecs     = 222,                                  \
                macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],             \
                srcPort      = 0x1234,                               \
                dstPort      = 0x5678,                               \
                data         = (0x33,0x44,0x55,0x66),                \
            )",
        "json":
            {
                "timestamp"  : 0,
                "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                "type"       : 0x0e,
                "value"      : [0x12,0x34,0x56,0x78,0x33,0x44,0x55,0x66],
            },
        "bin":
            [
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<0,          # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x57,0x03,0x49,0xae,                       # timestamp
                0x27,                                      # type
                0x00, 0x00, 0x05, 0x00, 0xff, 0x01, 0x05,
                0x00, 0x00, 0x00, 0x00, 0x3d, 0x22, 0x68,
                0xee, 0x00, 0x02, 0x38, 0xa0, 0x00, 0x00,
                0x75, 0x30, 0x01, 0x10, 0x09, 0x19         # value
            ],
        "http":
            'TODO',
        "influx":
            'TODO',
    },
]

@pytest.fixture(params=SOL_CHAIN_EXAMPLE)
def sol_chain_example(request):
    return json.dumps(request.param)

#============================ helpers ===============================

#============================ tests =================================

def test_dust_json_bin_http_bin_json_influx(sol_chain_example):
    sol_chain_example = json.loads(sol_chain_example)

    import Sol
    sol = Sol.Sol()

    # dust->json
    sol_json  = sol.dust_to_json(eval(sol_chain_example["dust"]))
    assert sol_json==sol_chain_example["json"]
    '''
    # json->bin
    sol_bin   = sol.json_to_bin(sol_json)
    assert sol_bin==sol_chain_example["bin"]
    
    # bin->http
    sol_http  = sol.bin_to_http(sol_bin)
    assert sol_http==sol_chain_example["http"]
    
    # http->bin
    sol_bin   = sol.http_to_bin(sol_http)
    assert sol_bin==sol_chain_example["bin"]
    
    # bin->json
    sol_json  = sol.bin_to_json(sol_bin)
    assert sol_json==sol_chain_example["json"]
    
    # json->influx
    sol_inlux  = sol.bin_to_json(sol_json)
    assert sol_influx==sol_chain_example["influx"]
    '''
