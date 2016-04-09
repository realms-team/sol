import pytest
import json

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
                srcPort      = 0x0102,                               \
                dstPort      = 0x0304,                               \
                data         = (0x05,0x06,0x07,0x08),                \
            )",
        "json":
            {
                "timestamp"  : 0x11223344,
                "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                "type"       : 0x0e,
                "value"      : {
                    'srcPort': 0x0102,
                    'dstPort': 0x0304,
                    'data'   : [0x05,0x06,0x07,0x08],
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x11,0x22,0x33,0x44,                       # timestamp
                0x0e,                                      # type
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # value
            ],
        "http":
            '{                                             \
                "v" : 0,                                   \
                "o" : [                                    \
                    "EwECAwQFBgcIESIzRA4BAgMEBQYHCA=="     \
                ]                                          \
            }',
        "influxdb":
            {
                "timestamp"  : 0x11223344,
                "tag"        : {
                    'mac'    : '01-02-03-04-05-06-07-08',
                },
                "measurement": 'SOL_TYPE_DUST_NOTIF_DATA_RAW',
                "fields"     : {
                    'srcPort': 0x0102,
                    'dstPort': 0x0304,
                    'data'   : '05-06-07-08',
                },
            },
    },
]

@pytest.fixture(params=SOL_CHAIN_EXAMPLE)
def sol_chain_example(request):
    return json.dumps(request.param)

#============================ helpers ===============================

#============================ tests =================================

def test_chain(sol_chain_example):
    sol_chain_example = json.loads(sol_chain_example)

    import Sol
    sol = Sol.Sol()

    # dust->json
    sol_json  = sol.dust_to_json(eval(sol_chain_example["dust"]),timestamp=0x11223344)
    assert sol_json==sol_chain_example["json"]
    
    # json->bin
    sol_bin   = sol.json_to_bin(sol_json)
    assert sol_bin==sol_chain_example["bin"]
    
    # bin->http
    sol_http  = sol.bin_to_http([sol_bin])
    assert json.loads(sol_http)==json.loads(sol_chain_example["http"])
    
    # http->bin
    sol_binl  = sol.http_to_bin(sol_http)
    assert len(sol_binl)==1
    sol_bin = sol_binl[0]
    assert sol_bin==sol_chain_example["bin"]
    
    # bin->json
    sol_json  = sol.bin_to_json(sol_bin)
    assert sol_json==sol_chain_example["json"]
    
    # json->influxbd
    sol_influxdb  = sol.json_to_influxdb(sol_json)
    assert sol_influxdb==sol_chain_example["influxdb"]
