import pytest
import json

from   SmartMeshSDK.IpMgrConnectorMux  import IpMgrConnectorMux

#============================ defines ===============================

MACMANAGER = [3,3,3,3,3,3,3,3]
TIMESTAMP   = 0x05050505

#============================ fixtures ==============================

SOL_CHAIN_EXAMPLE = [
    # SOL_TYPE_DUST_NOTIF_DATA_RAW
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
                "timestamp"  : TIMESTAMP,
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
                0x05,0x05,0x05,0x05,                       # timestamp
                0x0e,                                      # type
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # value
            ],
        "http":
            '{                                             \
                "v" : 0,                                   \
                "o" : [                                    \
                    "EwECAwQFBgcIBQUFBQ4BAgMEBQYHCA=="     \
                ]                                          \
            }',
        "influxdb":
            {
                "timestamp"  : TIMESTAMP,
                "tag"        : {
                    'mac'    : '01-02-03-04-05-06-07-08',
                },
                "measurement": 'SOL_TYPE_DUST_NOTIFDATA',
                "fields"     : {
                    'srcPort': 0x0102,
                    'dstPort': 0x0304,
                    'data'   : '05-06-07-08',
                },
            },
    },
    # SOL_TYPE_DUST_NOTIF_HR_DEVICE
    # TODO
    # SOL_TYPE_DUST_NOTIF_HR_NEIGHBORS
    # TODO
    # SOL_TYPE_DUST_NOTIF_HR_DISCOVERED
    # TODO
    # SOL_TYPE_DUST_EVENTPATHCREATE
    {
        "dust":
            "IpMgrConnectorMux.IpMgrConnectorMux.Tuple_eventPathCreate(   \
                eventId      = 0x11223344,                                \
                source       = [1,1,1,1,1,1,1,1],                         \
                dest         = [2,2,2,2,2,2,2,2],                         \
                direction    = 3,                                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x14,
                "value"      : {
                    'source'      : [1,1,1,1,1,1,1,1],
                    'dest'        : [2,2,2,2,2,2,2,2],
                    'direction'   : 3,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x14,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
                0x03,
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRQBAQEBAQEBAQICAgICAgICAw=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "timestamp"  : TIMESTAMP,
                "tag"        : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTPATHCREATE',
                "fields"     : {
                    'source'      : '01-01-01-01-01-01-01-01',
                    'dest'        : '02-02-02-02-02-02-02-02',
                    'direction'   : 3,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTPATHDELETE
    {
        "dust":
            "IpMgrConnectorMux.IpMgrConnectorMux.Tuple_eventPathDelete(   \
                eventId      = 0x11223344,                                \
                source       = [1,1,1,1,1,1,1,1],                         \
                dest         = [2,2,2,2,2,2,2,2],                         \
                direction    = 3,                                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x15,
                "value"      : {
                    'source'      : [1,1,1,1,1,1,1,1],
                    'dest'        : [2,2,2,2,2,2,2,2],
                    'direction'   : 3,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x15,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
                0x03,
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRUBAQEBAQEBAQICAgICAgICAw=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "timestamp"  : TIMESTAMP,
                "tag"        : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTPATHDELETE',
                "fields"     : {
                    'source'      : '01-01-01-01-01-01-01-01',
                    'dest'        : '02-02-02-02-02-02-02-02',
                    'direction'   : 3,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTEJOIN
    {
        "dust":
            "IpMgrConnectorMux.IpMgrConnectorMux.Tuple_eventMoteJoin(     \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x19,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x19,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRkBAQEBAQEBAQ=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "timestamp"  : TIMESTAMP,
                "tag"        : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTEJOIN',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTECREATE
    {
        "dust":
            "IpMgrConnectorMux.IpMgrConnectorMux.Tuple_eventMoteCreate(   \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
                moteId       = 0x0202,                                    \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x1a,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                    'moteId'      : 0x0202,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x1a,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                0x02,0x02,
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRoBAQEBAQEBAQIC"   \
                ]                                                    \
            }',
        "influxdb":
            {
                "timestamp"  : TIMESTAMP,
                "tag"        : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTECREATE',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                    'moteId'      : 0x0202,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTEDELETE
    {
        "dust":
            "IpMgrConnectorMux.IpMgrConnectorMux.Tuple_eventMoteDelete(   \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
                moteId       = 0x0202,                                    \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x1b,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                    'moteId'      : 0x0202,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x1b,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                0x02,0x02,
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRsBAQEBAQEBAQIC"   \
                ]                                                    \
            }',
        "influxdb":
            {
                "timestamp"  : TIMESTAMP,
                "tag"        : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTEDELETE',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                    'moteId'      : 0x0202,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTELOST
    {
        "dust":
            "IpMgrConnectorMux.IpMgrConnectorMux.Tuple_eventMoteLost(     \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x1c,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x1c,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRwBAQEBAQEBAQ=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "timestamp"  : TIMESTAMP,
                "tag"        : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTELOST',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTEOPERATIONAL
    {
        "dust":
            "IpMgrConnectorMux.IpMgrConnectorMux.Tuple_eventMoteOperational(     \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x1d,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x1d,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBR0BAQEBAQEBAQ=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "timestamp"  : TIMESTAMP,
                "tag"        : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTEOPERATIONAL',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                },
            },
    },
    # SOL_TYPE_DUST_OAP_TEMPSAMPLE
    # TODO
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
    sol_json  = sol.dust_to_json(
       eval(sol_chain_example["dust"]),
       macManager  = MACMANAGER,
       timestamp   = TIMESTAMP,
    )
    print sol_json
    print sol_chain_example["json"]
    assert sol_json==sol_chain_example["json"]
    
    # json->bin
    sol_bin   = sol.json_to_bin(sol_json)
    print sol_bin
    print sol_chain_example["bin"]
    assert sol_bin==sol_chain_example["bin"]
    
    # bin->http
    sol_http  = sol.bin_to_http([sol_bin])
    print sol_http
    print sol_chain_example["http"]
    assert json.loads(sol_http)==json.loads(sol_chain_example["http"])
    
    # http->bin
    sol_binl  = sol.http_to_bin(sol_http)
    assert len(sol_binl)==1
    sol_bin = sol_binl[0]
    print sol_bin
    print sol_chain_example["bin"]
    assert sol_bin==sol_chain_example["bin"]
    
    # bin->json
    sol_json  = sol.bin_to_json(sol_bin)
    print sol_json
    print sol_chain_example["json"]
    assert sol_json==sol_chain_example["json"]
    
    # json->influxbd
    sol_influxdb  = sol.json_to_influxdb(sol_json)
    print sol_influxdb
    print sol_chain_example["influxdb"]
    assert sol_influxdb==sol_chain_example["influxdb"]
