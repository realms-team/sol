from .context import Sol
import pytest
import json
import pprint

from SmartMeshSDK.IpMgrConnectorSerial  import IpMgrConnectorSerial

#============================ defines ===============================

MACMANAGER   = [3,3,3,3,3,3,3,3]
TIMESTAMP    = 0x05050505
TAGS_DEFAULT = { "mac" : "03-03-03-03-03-03-03-03"}
TAGS         = {
    "mac"       : "01-02-03-04-05-06-07-08",
    "site"      : "super_site",
    "latitude"  : 55.5555,
    "longitude" : -44.4444,
}

#============================ fixtures ==============================

SOL_CHAIN_EXAMPLE = [
    # SOL_TYPE_DUST_NOTIF_DATA_RAW
    {
        "dust": {
            "notif"     :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifData(    \
                    utcSecs      = 1111,                                 \
                    utcUsecs     = 222,                                  \
                    macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],             \
                    srcPort      = 0x0102,                               \
                    dstPort      = 0x0304,                               \
                    data         = (0x05,0x06,0x07,0x08),                \
                )",
            "notif_name": IpMgrConnectorSerial.IpMgrConnectorSerial.NOTIFDATA,
            },
        "objects": [
            {
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
                        "time"          : TIMESTAMP*1000000000,
                        "tags"          : {
                            'mac'       : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement"   : 'SOL_TYPE_DUST_NOTIFDATA',
                        "fields"        : {
                            'srcPort'   : 0x0102,
                            'dstPort'   : 0x0304,
                            'data:0'    : 0x05,
                            'data:1'    : 0x06,
                            'data:2'    : 0x07,
                            'data:3'    : 0x08,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_NOTIF_HRDEVICE
    {
        "dust": {
            "notif":
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifHealthReport( \
                    macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                    payload      = [128, 24, 0, 0, 0, 40, 49, 25, 11,119, 0, 26, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],            \
                )",
            "notif_name": IpMgrConnectorSerial.IpMgrConnectorSerial.NOTIFHEALTHREPORT,
            },
        "objects": [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                        "type"       : 0x10,
                        "value"      : {
                            'charge':             40,
                            'queueOcc':           49,
                            'temperature':        25,
                            'batteryVoltage':     2935,
                            'numTxOk':            26,
                            'numTxFail':          0,
                            'numRxOk':            9,
                            'numRxLost':          0,
                            'numMacDropped':      0,
                            'numTxBad':           0,
                            'badLinkFrameId':     0,
                            'badLinkSlot':        0,
                            'badLinkOffset':      0,
                        },
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x10,                                      # type
                        0, 0, 0, 40, 49, 25, 11,119, 0, 26, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,   # value
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBRAAAAAoMRkLdwAaAAAACQAAAAAAAAAAAAA="     \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_DUST_NOTIF_HRDEVICE',
                        "fields"     : {
                            'charge':             40,
                            'queueOcc':           49,
                            'temperature':        25,
                            'batteryVoltage':     2935,
                            'numTxOk':            26,
                            'numTxFail':          0,
                            'numRxOk':            9,
                            'numRxLost':          0,
                            'numMacDropped':      0,
                            'numTxBad':           0,
                            'badLinkFrameId':     0,
                            'badLinkSlot':        0,
                            'badLinkOffset':      0,
                        },
                    },
                }
        ]
    },
    # SOL_TYPE_DUST_NOTIF_HRNEIGHBORS
    {
        "dust": {
            "notif"     :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifHealthReport( \
                    macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                    payload      = [129, 31, 3, 0, 3, 0, 223, 0, 0, 0, 0, 0, 47, 0, 1, 0, 209, 0, 76, 0, 1, 0, 2, 0, 4, 0, 211, 0, 30, 0, 0, 0, 1],            \
                )",
            "notif_name": IpMgrConnectorSerial.IpMgrConnectorSerial.NOTIFHEALTHREPORT,
            },
        "objects" : [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                        "type"       : 0x11,
                        "value"      : {
                            'numItems': 3,
                            'neighbors': [
                                {
                                    'neighborId':       3,
                                    'neighborFlag':     0,
                                    'rssi':             -33,
                                    'numTxPackets':     0,
                                    'numTxFailures':    0,
                                    'numRxPackets':     47,
                                },
                                {
                                    'neighborId':       1,
                                    'neighborFlag':     0,
                                    'rssi':             -47,
                                    'numTxPackets':     76,
                                    'numTxFailures':    1,
                                    'numRxPackets':     2,
                                },
                                {
                                    'neighborId':      4,
                                    'neighborFlag':    0,
                                    'rssi':            -45,
                                    'numTxPackets':    30,
                                    'numTxFailures':   0,
                                    'numRxPackets':    1,
                                },
                            ]
                        },
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x11,                                      # type
                        3, 0, 3, 0, 223, 0, 0, 0, 0, 0, 47, 0, 1, 0, 209, 0, 76, 0, 1, 0, 2, 0, 4, 0, 211, 0, 30, 0, 0, 0, 1,   # value
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBREDAAMA3wAAAAAALwABANEATAABAAIABADTAB4AAAAB"     \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_DUST_NOTIF_HRNEIGHBORS',
                        "fields"     : {
                            'neighbors:3:neighborId':           3,
                            'neighbors:3:neighborFlag':       0,
                            'neighbors:3:rssi':               -33,
                            'neighbors:3:numTxPackets':       0,
                            'neighbors:3:numTxFailures':      0,
                            'neighbors:3:numRxPackets':       47,
                            'neighbors:1:neighborId':         1,
                            'neighbors:1:neighborFlag':       0,
                            'neighbors:1:rssi':               -47,
                            'neighbors:1:numTxPackets':       76,
                            'neighbors:1:numTxFailures':      1,
                            'neighbors:1:numRxPackets':       2,
                            'neighbors:4:neighborId':         4,
                            'neighbors:4:neighborFlag':       0,
                            'neighbors:4:rssi':               -45,
                            'neighbors:4:numTxPackets':       30,
                            'neighbors:4:numTxFailures':      0,
                            'neighbors:4:numRxPackets':       1,
                            'numItems':             3,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_NOTIF_HRDISCOVERED
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifHealthReport( \
                    macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                    payload      = [130, 14, 3, 3, 0, 6, 178, 2, 0, 5, 169, 1, 0, 7, 185, 1],            \
                )",
            "notif_name": IpMgrConnectorSerial.IpMgrConnectorSerial.NOTIFHEALTHREPORT,
            },
        "objects": [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                        "type"       : 0x12,
                        "value"      : {
                            'numJoinParents': 3,
                            'numItems': 3,
                            'discoveredNeighbors': [
                                {
                                    'neighborId': 6,
                                    'rssi': -78,
                                    'numRx': 2,
                                },
                                {
                                    'neighborId': 5,
                                    'rssi': -87,
                                    'numRx': 1,
                                },
                                {
                                    'neighborId': 7,
                                    'rssi': -71,
                                    'numRx': 1,
                                },
                            ]
                        },
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x12,                                      # type
                        3, 3, 0, 6, 178, 2, 0, 5, 169, 1, 0, 7, 185, 1,   # value
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBRIDAwAGsgIABakBAAe5AQ=="     \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_DUST_NOTIF_HRDISCOVERED',
                        "fields"     : {
                            'discoveredNeighbors:0:neighborId':    6,
                            'discoveredNeighbors:0:numRx':         2,
                            'discoveredNeighbors:0:rssi':          -78,
                            'discoveredNeighbors:1:neighborId':    5,
                            'discoveredNeighbors:1:numRx':         1,
                            'discoveredNeighbors:1:rssi':          -87,
                            'discoveredNeighbors:2:neighborId':    7,
                            'discoveredNeighbors:2:numRx':         1,
                            'discoveredNeighbors:2:rssi':          -71,
                            'numItems':                            3,
                            'numJoinParents':                      3,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_EVENTPATHCREATE
    {
        "dust": {
            "notif":
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventPathCreate(   \
                    eventId      = 0x11223344,                                \
                    source       = [1,1,1,1,1,1,1,1],                         \
                    dest         = [2,2,2,2,2,2,2,2],                         \
                    direction    = 3,                                         \
                )",
            "notif_name": IpMgrConnectorSerial.IpMgrConnectorSerial.EVENTPATHCREATE,
            },
        "objects":[
            {
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
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '03-03-03-03-03-03-03-03',
                        },
                        "measurement": 'SOL_TYPE_DUST_EVENTPATHCREATE',
                        "fields"     : {
                            'source'      : '01-01-01-01-01-01-01-01',
                            'dest'        : '02-02-02-02-02-02-02-02',
                            'direction'   : 3,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_EVENTPATHDELETE
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventPathDelete(   \
                    eventId      = 0x11223344,                                \
                    source       = [1,1,1,1,1,1,1,1],                         \
                    dest         = [2,2,2,2,2,2,2,2],                         \
                    direction    = 3,                                         \
                )",
            "notif_name": IpMgrConnectorSerial.IpMgrConnectorSerial.EVENTPATHDELETE,
            },
        "objects": [
            {
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
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '03-03-03-03-03-03-03-03',
                        },
                        "measurement": 'SOL_TYPE_DUST_EVENTPATHDELETE',
                        "fields"     : {
                            'source'      : '01-01-01-01-01-01-01-01',
                            'dest'        : '02-02-02-02-02-02-02-02',
                            'direction'   : 3,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_EVENTMOTEJOIN
    {
        "dust":{
            "notif":
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteJoin(     \
                    eventId      = 0x11223344,                                \
                    macAddress   = [1,1,1,1,1,1,1,1],                         \
                )",
            "notif_name":IpMgrConnectorSerial.IpMgrConnectorSerial.EVENTMOTEJOIN,
            },
        "objects":[
            {
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
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '03-03-03-03-03-03-03-03',
                        },
                        "measurement": 'SOL_TYPE_DUST_EVENTMOTEJOIN',
                        "fields"     : {
                            'macAddress'  : '01-01-01-01-01-01-01-01',
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_EVENTMOTECREATE
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteCreate(   \
                    eventId      = 0x11223344,                                \
                    macAddress   = [1,1,1,1,1,1,1,1],                         \
                    moteId       = 0x0202,                                    \
                )",
            "notif_name" : IpMgrConnectorSerial.IpMgrConnectorSerial.EVENTMOTECREATE,
            },
        "objects": [
            {
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
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '03-03-03-03-03-03-03-03',
                        },
                        "measurement": 'SOL_TYPE_DUST_EVENTMOTECREATE',
                        "fields"     : {
                            'macAddress'  : '01-01-01-01-01-01-01-01',
                            'moteId'      : 0x0202,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_EVENTMOTEDELETE
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteDelete(   \
                    eventId      = 0x11223344,                                \
                    macAddress   = [1,1,1,1,1,1,1,1],                         \
                    moteId       = 0x0202,                                    \
                )",
            "notif_name" : IpMgrConnectorSerial.IpMgrConnectorSerial.EVENTMOTEDELETE,
            },
        "objects": [
            {
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
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '03-03-03-03-03-03-03-03',
                        },
                        "measurement": 'SOL_TYPE_DUST_EVENTMOTEDELETE',
                        "fields"     : {
                            'macAddress'  : '01-01-01-01-01-01-01-01',
                            'moteId'      : 0x0202,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_EVENTMOTELOST
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteLost(     \
                    eventId      = 0x11223344,                                \
                    macAddress   = [1,1,1,1,1,1,1,1],                         \
                )",
            "notif_name" : IpMgrConnectorSerial.IpMgrConnectorSerial.EVENTMOTELOST,
            },
        "objects": [
            {
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
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '03-03-03-03-03-03-03-03',
                        },
                        "measurement": 'SOL_TYPE_DUST_EVENTMOTELOST',
                        "fields"     : {
                            'macAddress'  : '01-01-01-01-01-01-01-01',
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_EVENTMOTEOPERATIONAL
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteOperational(     \
                    eventId      = 0x11223344,                                \
                    macAddress   = [1,1,1,1,1,1,1,1],                         \
                )",
            "notif_name" : IpMgrConnectorSerial.IpMgrConnectorSerial.EVENTMOTEOPERATIONAL,
            },
        "objects": [
            {
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
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '03-03-03-03-03-03-03-03',
                        },
                        "measurement": 'SOL_TYPE_DUST_EVENTMOTEOPERATIONAL',
                        "fields"     : {
                            'macAddress'  : '01-01-01-01-01-01-01-01',
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_OAP_TEMPSAMPLE (with positive temperature value)
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifData(         \
                    utcSecs      = 1111,                                      \
                    utcUsecs     = 222,                                       \
                    macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                    srcPort      = 0xf0b9,                                    \
                    dstPort      = 0xf0b9,                                    \
                    data         = (  0,   0,   5,   0, 255,   1,   5,   0,   \
                                      0,   0,   0,  61,  34, 107,  74,   0,   \
                                     13, 104, 164,   0,   0, 117,  48,   1,   \
                                     16,0x0a,0x33                             \
                                   ),                                         \
                )",
            "notif_name":IpMgrConnectorSerial.IpMgrConnectorSerial.NOTIFDATA,
            },
        "objects": [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                        "type"       : 0x27,
                        "value"      : {
                            'temperature': 0x0a33,
                        },
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x27,                                      # type
                        0x0a,0x33,                                 # value
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBScKMw=="             \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_DUST_OAP_TEMPSAMPLE',
                        "fields"     : {
                            'temperature': 0x0a33,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_OAP_TEMPSAMPLE (with negative temperature value)
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifData(         \
                    utcSecs      = 1111,                                      \
                    utcUsecs     = 222,                                       \
                    macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                    srcPort      = 0xf0b9,                                    \
                    dstPort      = 0xf0b9,                                    \
                    data         = (  0,   0,   5,   0, 255,   1,   5,   0,   \
                                      0,   0,   0,  61,  34, 107,  74,   0,   \
                                     13, 104, 164,   0,   0, 117,  48,   1,   \
                                     16,0xff,0xff                             \
                                   ),                                         \
                )",
            "notif_name" : IpMgrConnectorSerial.IpMgrConnectorSerial.NOTIFDATA,
            },
        "objects" : [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                        "type"       : 0x27,
                        "value"      : {
                            'temperature': -1,
                        },
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x27,                                      # type
                        0xff,0xff,                                 # value
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBSf//w=="             \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_DUST_OAP_TEMPSAMPLE',
                        "fields"     : {
                            'temperature': -1,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_JUDD_DTYPE_T2D2R1N1,
    {
        "objects": [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                        "type"       : 0x22,
                        "value"      : {
                            'temperature': 0x0a33,
                            'depth': 0x0b44,
                            'numReadings': 0x01,
                            'stdDev': 0x0203,
                            'retries': 0x04,
                        },
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,    # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,    # mac
                        0x05,0x05,0x05,0x05,                        # timestamp
                        0x22,                                       # type
                        0x0a,0x33,                                  # value_temperature
                        0x0b,0x44,                                  # value_depth
                        0x01,                                       # value_numReadings
                        0x02,0x03,                                  # value_stdDev
                        0x04,                                       # value_retries
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBSIKMwtEAQIDBA=="     \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_JUDD_DTYPE_T2D2R1N1',
                        "fields"     : {
                            'temperature': 0x0a33,
                            'depth': 0x0b44,
                            'numReadings': 0x01,
                            'stdDev': 0x0203,
                            'retries': 0x04,
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_DUST_SNAPSHOT
    {
        "objects": [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : MACMANAGER,
                        "type"       : 0x20,
                        "value"      : [
                            {   'macAddress':          [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08],
                                'moteId':              0x090a,      # INT16U  H
                                'isAP':                0x0b,        # BOOL    B
                                'state':               0x0c,        # INT8U   B
                                'isRouting':           0x0d,        # BOOL    B
                                'numNbrs':             0x0e,        # INT8U   B
                                'numGoodNbrs':         0x0f,        # INT8U   B
                                'requestedBw':         0x10111213,  # INT32U  I
                                'totalNeededBw':       0x14151617,  # INT32U  I
                                'assignedBw':          0x18191a1b,  # INT32U  I
                                'packetsReceived':     0x1c1d1e1f,  # INT32U  I
                                'packetsLost':         0x20212223,  # INT32U  I
                                'avgLatency':          0x24252627,  # INT32U  I
                                'paths': [
                                    {
                                        'macAddress':   [0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18],
                                        'direction':    0x2c,       # INT8U   B
                                        'numLinks':     0x2d,       # INT8U   B
                                        'quality':      0x2e,       # INT8U   B
                                        'rssiSrcDest':  -1,         # INT8    b
                                        'rssiDestSrc':  -2,         # INT8    b
                                    },
                                    {
                                        'macAddress':   [0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28],
                                        'direction':    0x2c,       # INT8U  B
                                        'numLinks':     0x2d,       # INT8U  B
                                        'quality':      0x2e,       # INT8U  B
                                        'rssiSrcDest':  -1,         # INT8   b
                                        'rssiDestSrc':  -2,         # INT8   b
                                    },
                                ],
                            },
                            {
                                'macAddress':           [0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38],
                                'moteId':               0x090a,     # INT16U
                                'isAP':                 0x0b,       # BOOL
                                'state':                0x0c,       # INT8U
                                'isRouting':            0x0d,       # BOOL
                                'numNbrs':              0x0e,       # INT8U
                                'numGoodNbrs':          0x0f,       # INT8U
                                'requestedBw':          0x10111213, # INT32U
                                'totalNeededBw':        0x14151617, # INT32U
                                'assignedBw':           0x18191a1b, # INT32U
                                'packetsReceived':      0x1c1d1e1f, # INT32U
                                'packetsLost':          0x20212223, # INT32U
                                'avgLatency':           0x24252627, # INT32U
                                'paths': [
                                    {
                                        'macAddress':   [0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48],
                                        'direction':    0x2c,       # INT8U
                                        'numLinks':     0x2d,       # INT8U
                                        'quality':      0x2e,       # INT8U
                                        'rssiSrcDest':  -1,         # INT8
                                        'rssiDestSrc':  -2,         # INT8
                                    },
                                ],
                            },
                        ]
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,        # header
                        0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,        # mac
                        0x05,0x05,0x05,0x05,                            # timestamp
                        0x20,                                           # type

                        # value
                        0x02,                                           # number of motes
                        # -- first mote
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,        # value_macAddr
                        0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,             # --
                        0x10,0x11,0x12,0x13,                            # value_requestedBw
                        0x14,0x15,0x16,0x17,                            # value_totalNeededBw
                        0x18,0x19,0x1a,0x1b,                            # value_assignedBw
                        0x1c,0x1d,0x1e,0x1f,                            # value_packetsReceived
                        0x20,0x21,0x22,0x23,                            # value_packetsLost
                        0x24,0x25,0x26,0x27,                            # value_avgLatency
                        0x02,                                           # number of paths
                        0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,        # value_path_macAddr
                        0x2c,0x2d,0x2e,0xff,0xfe,                       # --
                        0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,        # value_path_macAddr
                        0x2c,0x2d,0x2e,0xff,0xfe,                       # --
                        # -- second mote
                        0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,        # value_macAddr
                        0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,             # --
                        0x10,0x11,0x12,0x13,                            # value_requestedBw
                        0x14,0x15,0x16,0x17,                            # value_totalNeededBw
                        0x18,0x19,0x1a,0x1b,                            # value_assignedBw
                        0x1c,0x1d,0x1e,0x1f,                            # value_packetsReceived
                        0x20,0x21,0x22,0x23,                            # value_packetsLost
                        0x24,0x25,0x26,0x27,                            # value_avgLatency
                        0x01,                                           # number of paths
                        0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,        # value_paths_macAddr
                        0x2c,0x2d,0x2e,0xff,0xfe,                       # --
                    ],
                "http":
                    '{                                              \
                        "v" : 0,                                    \
                        "o" : [                                     \
                        "EwMDAwMDAwMDBQUFBSACAQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRobHB0eHyAhIiMkJSYnAhESExQVFhcYLC0u//4hIiMkJSYnKCwtLv/+MTIzNDU2NzgJCgsMDQ4PEBESExQVFhcYGRobHB0eHyAhIiMkJSYnAUFCQ0RFRkdILC0u//4="\
                        ]                                           \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '03-03-03-03-03-03-03-03',
                            },
                        "measurement": 'SOL_TYPE_DUST_SNAPSHOT',
                        "fields"     : {
                            'mote:0:macAddress':            '01-02-03-04-05-06-07-08',
                            'mote:0:moteId':                0x090a,      # INT16U  H
                            'mote:0:isAP':                  0x0b,        # BOOL    B
                            'mote:0:state':                 0x0c,        # INT8U   B
                            'mote:0:isRouting':             0x0d,        # BOOL    B
                            'mote:0:numNbrs':               0x0e,        # INT8U   B
                            'mote:0:numGoodNbrs':           0x0f,        # INT8U   B
                            'mote:0:requestedBw':           0x10111213,  # INT32U  I
                            'mote:0:totalNeededBw':         0x14151617,  # INT32U  I
                            'mote:0:assignedBw':            0x18191a1b,  # INT32U  I
                            'mote:0:packetsReceived':       0x1c1d1e1f,  # INT32U  I
                            'mote:0:packetsLost':           0x20212223,  # INT32U  I
                            'mote:0:avgLatency':            0x24252627,  # INT32U  I
                            'mote:0:paths:0:macAddress':    '11-12-13-14-15-16-17-18',
                            'mote:0:paths:0:direction':     0x2c,       # INT8U   B
                            'mote:0:paths:0:numLinks':      0x2d,       # INT8U   B
                            'mote:0:paths:0:quality':       0x2e,       # INT8U   B
                            'mote:0:paths:0:rssiSrcDest':   -1,         # INT8    b
                            'mote:0:paths:0:rssiDestSrc':   -2,         # INT8    b
                            'mote:0:paths:1:macAddress':    '21-22-23-24-25-26-27-28',
                            'mote:0:paths:1:direction':     0x2c,       # INT8U  B
                            'mote:0:paths:1:numLinks':      0x2d,       # INT8U  B
                            'mote:0:paths:1:quality':       0x2e,       # INT8U  B
                            'mote:0:paths:1:rssiSrcDest':   -1,         # INT8   b
                            'mote:0:paths:1:rssiDestSrc':   -2,         # INT8   b

                            'mote:1:macAddress':            '31-32-33-34-35-36-37-38',
                            'mote:1:moteId':                0x090a,     # INT16U
                            'mote:1:isAP':                  0x0b,       # BOOL
                            'mote:1:state':                 0x0c,       # INT8U
                            'mote:1:isRouting':             0x0d,       # BOOL
                            'mote:1:numNbrs':               0x0e,       # INT8U
                            'mote:1:numGoodNbrs':           0x0f,       # INT8U
                            'mote:1:requestedBw':           0x10111213, # INT32U
                            'mote:1:totalNeededBw':         0x14151617, # INT32U
                            'mote:1:assignedBw':            0x18191a1b, # INT32U
                            'mote:1:packetsReceived':       0x1c1d1e1f, # INT32U
                            'mote:1:packetsLost':           0x20212223, # INT32U
                            'mote:1:avgLatency':            0x24252627, # INT32U
                            'mote:1:paths:0:macAddress':    '41-42-43-44-45-46-47-48',
                            'mote:1:paths:0:direction':     0x2c,       # INT8U
                            'mote:1:paths:0:numLinks':      0x2d,       # INT8U
                            'mote:1:paths:0:quality':       0x2e,       # INT8U
                            'mote:1:paths:0:rssiSrcDest':   -1,         # INT8
                            'mote:1:paths:0:rssiDestSrc':   -2,         # INT8
                    }
                },
            }
        ]
    },
    # SOL_TYPE_SOLMANAGER_STATS
    {
        "objects": [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                        "type"       : 0x28,
                        "value"      : {
                            "sol_version"           : [1,2,3,4],
                            "solmanager_version"    : [5,6,7,8],
                            "sdk_version"           : [9,1,2,3],
                        },
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x28,                                      # type
                        0x01,0x02,0x03,0x04,                       # value_solversion
                        0x05,0x06,0x07,0x08,                       # value_solmanagerversion
                        0x09,0x01,0x02,0x03,                       # value_sdkversion
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBSgBAgMEBQYHCAkBAgM=" \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_SOLMANAGER_STATS',
                        "fields"     : {
                            "sol_version"           : "1.2.3.4",
                            "solmanager_version"    : "5.6.7.8",
                            "sdk_version"           : "9.1.2.3",
                        },
                    },
            }
        ]
    },
    # SOL_TYPE_SENS_SHT25_T2N1H2N1 with apply function
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifData(     \
                    utcSecs      = 1111,                                        \
                    utcUsecs     = 222,                                         \
                    macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                    \
                    srcPort      = 0xf0ba,                                      \
                    dstPort      = 0xf0ba,                                      \
                    data         = (0x00, 0x50, 0x7b, 0x41, 0x3e,               \
                                    0x31, 0x3c, 0x65, 0x01, 0xa2, 0x67, 0x01,"  + # SENS_SHT25_T2N1H2N1
                                    "                                           \
                                   ),                                           \
                )",
            "notif_name":IpMgrConnectorSerial.IpMgrConnectorSerial.NOTIFDATA,
            },
        "objects": [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                        "type"       : 0x31,
                        "value"      : {
                            "temp_raw"      : 0x653c,
                            "t_Nval"      : 0x01,
                            "rh_raw"        : 0x67a2,
                            "rh_Nval"       : 0x01,
                        },
                    },
                "bin":
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x31,                                      # type
                        0x3c,0x65,                                 # value--temp_raw
                        0x01,                                      # value--t_Nval
                        0xa2,0x67,                                 # value--rh_raw
                        0x01,                                      # value--rh_Nval
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBTE8ZQGiZwE="         \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_SENS_SHT25_T2N1H2N1',
                        "fields"     : {
                            "temp_raw"      : 0x653c,
                            "t_Nval"        : 0x01,
                            "rh_raw"        : 0x67a2,
                            "rh_Nval"       : 0x01,
                            "rh_phys"       : 44.601959228515625,
                            "temp_phys"     : 22.63790771484374,
                        },
                    },
            }
        ]
    },
    # MULTI-TTLV (VBAT_DTYPE_V2N1, SENS_SHT25_T2N1H2N1, SENS_GS3_I1D4T4E4N1, SENS_MB7363_D2S2N1L1G1)
    {
        "dust": {
            "notif" :
                "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifData(     \
                    utcSecs      = 1111,                                        \
                    utcUsecs     = 222,                                         \
                    macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                    \
                    srcPort      = 0xf0ba,                                      \
                    dstPort      = 0xf0ba,                                      \
                    data         = ( 0x20,"                                     + # multi TTLV 0100 0000
                                    "0x50, 0x7b, 0x41, 0x3e,"                   + # epoch
                                    "0x04,"                                     + # 5 objects
                                    "0x32, 0x00, 0x00, 0x01,"                   + # 1. VBAT_DTYPE_V2N1
                                    "0x31, 0x3c, 0x65, 0x01, 0xa2, 0x67, 0x01," + # 2. SENS_SHT25_T2N1H2N1
                                    "0x30, 0x00, 0x0a, 0xd7, 0x23, 0x40, 0x66," + # 3. SENS_GS3_I1D4T4E4N1
                                    "0x66, 0xb2, 0x41, 0x00, 0x00, 0x80, 0x3f," +
                                    "0x01,"                                     +
                                    "0x29, 0x1b, 0x02, 0x01, 0x00, 0x1b, 0x54," + # 4. SENS_MB7363_D2S2N1L1G1
                                    "0x55                                       \
                                   ),                                           \
                )",
            "notif_name": IpMgrConnectorSerial.IpMgrConnectorSerial.NOTIFDATA,
            },
        "objects": [
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                    "type"       : 0x32,
                    "value"      : {
                        "voltage"       : 0,
                        "N"             : 1,
                    },
                },
                "bin" :
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x32,                                      # type
                        0x00,0x00,                                 # value--voltage
                        0x01,                                      # value--numReadings
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBTIAAAE=" \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_SENS_NEOVBAT_V2N1',
                        "fields"     : {
                            "voltage"       : 0,
                            "vol_phys"      : 0,
                            "N"             : 1,
                        },
                    },
            },
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                    "type"       : 0x31,
                    "value"      : {
                        "temp_raw"      : 0x653c,
                        "t_Nval"        : 0x01,
                        "rh_raw"        : 0x67a2,
                        "rh_Nval"       : 0x01,
                    },
                },
                "bin" :
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x31,                                      # type
                        0x3c,0x65,                                 # value--temp_raw
                        0x01,                                      # value--t_Nval
                        0xa2,0x67,                                 # value--rh_raw
                        0x01,                                      # value--rh_Nval
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBTE8ZQGiZwE=" \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_SENS_SHT25_T2N1H2N1',
                        "fields"     : {
                            "temp_raw"      : 0x653c,
                            "t_Nval"        : 0x01,
                            "rh_raw"        : 0x67a2,
                            "rh_Nval"       : 0x01,
                            "rh_phys"       : 44.601959228515625,
                            "temp_phys"     : 22.63790771484374,
                        },
                    },
            },
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                    "type"       : 0x30,
                    "value"      : {
                        "sub_id"        : 0x00,
                        "dielect"       : 2.559999942779541,
                        "temp"          : 22.299999237060547,
                        "eleCond"       : 1.0,
                        "Nval"          : 0x01,
                    },
                },
                "bin" :
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x30,                                      # type
                        0x00,                                      # value--id
                        0x0a,0xd7,0x23,0x40,                       # value--dielect
                        0x66,0x66,0xb2,0x41,                       # value--temp
                        0x00,0x00,0x80,0x3f,                       # value--eleCond
                        0x01,                                      # value--Nval
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBTAACtcjQGZmskEAAIA/AQ==" \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_SENS_GS3_I1D4T4E4N1',
                        "fields"     : {
                            "sub_id"        : 0x00,
                            "dielect"       : 2.559999942779541,
                            "temp"          : 22.299999237060547,
                            "eleCond"       : 1.0,
                            "Nval"          : 0x01,
                        },
                    },
            },
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                    "type"       : 0x29,
                    "value"      : {
                        "mean_d2g"      : 0x021b,
                        "stdev"         : 0x0001,
                        "Nval"          : 0x1b,
                        "Nltm"          : 0x54,
                        "NgtM"          : 0x55,
                    },
                },
                "bin" :
                    [
                        #ver   type   MAC    ts    typelen length
                        0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                        0x05,0x05,0x05,0x05,                       # timestamp
                        0x29,                                      # type
                        0x1b, 0x02,                                # value--mean_d2g
                        0x01, 0x00,                                # value--stdDev
                        0x1b,                                      # value--Nval
                        0x54,                                      # value--Nltm
                        0x55,                                      # value--NgtM
                    ],
                "http":
                    '{                                             \
                        "v" : 0,                                   \
                        "o" : [                                    \
                            "EwECAwQFBgcIBQUFBSkbAgEAG1RV" \
                        ]                                          \
                    }',
                "influxdb":
                    {
                        "time"       : TIMESTAMP*1000000000,
                        "tags"       : {
                            'mac'    : '01-02-03-04-05-06-07-08',
                            'site'      : 'super_site',
                            'latitude'  : 55.5555,
                            'longitude' : -44.4444,
                        },
                        "measurement": 'SOL_TYPE_SENS_MB7363_D2S2N1L1G1',
                        "fields"     : {
                            "mean_d2g"      : 0x021b,
                            "stdev"         : 0x0001,
                            "Nval"          : 0x1b,
                            "Nltm"          : 0x54,
                            "NgtM"          : 0x55,
                        },
                    }
            }
        ]
    }
]

@pytest.fixture(params=SOL_CHAIN_EXAMPLE)
def sol_chain_example(request):
    return json.dumps(request.param)

#============================ helpers ===============================

pp = pprint.PrettyPrinter(indent=4)

#============================ tests =================================

def test_chain(sol_chain_example):
    sol_chain_example = json.loads(sol_chain_example)

    sol = Sol.Sol()

    sol_json = None
    if "dust" in sol_chain_example:
        # dust->json
        sol_jsonl  = sol.dust_to_json(
           sol_chain_example["dust"]["notif_name"],
           eval(sol_chain_example["dust"]["notif"]),
           macManager  = MACMANAGER,
           timestamp   = TIMESTAMP,
        )
    else:
        sol_jsonl = [sol_chain_example["objects"][0]["json"]]

    assert len(sol_jsonl) == len(sol_chain_example["objects"])
    for (sol_json, example) in zip(sol_jsonl,sol_chain_example["objects"]):
        assert sol_json==example["json"]
        print '=====\ndust->json'
        print sol_json
        print example["json"]

        # json->bin
        sol_bin   = sol.json_to_bin(sol_json)
        print '=====\njson->bin'
        print sol_bin
        print example["bin"]
        assert sol_bin==example["bin"]

        # bin->http
        sol_http  = sol.bin_to_http([sol_bin])
        print '=====\nbin->http'
        print sol_http
        print example["http"]
        assert json.loads(sol_http)==json.loads(example["http"])

        # http->bin
        sol_binl  = sol.http_to_bin(sol_http)
        assert len(sol_binl)==1
        sol_bin = sol_binl[0]
        print '=====\nhttp->bin'
        print sol_bin
        print example["bin"]
        assert sol_bin==example["bin"]

        # bin->json
        sol_json  = sol.bin_to_json(sol_bin)
        print '=====\nbin->json'
        print sol_json
        print example["json"]
        assert sol_json==example["json"]

        # json->influxdb
        sol_influxdb = None
        if MACMANAGER == sol_json['mac']:
            sol_influxdb = sol.json_to_influxdb(sol_json,TAGS_DEFAULT)
        else:
            sol_influxdb = sol.json_to_influxdb(sol_json,TAGS)
        print '=====\njson->influxdb'
        pp.pprint(sol_influxdb)
        print example["influxdb"]
        assert sol_influxdb==example["influxdb"]
