from .context import Sol
import pytest
import json
import pprint

from SmartMeshSDK.IpMgrConnectorSerial  import IpMgrConnectorSerial

#============================ defines ===============================

MACMANAGER   = "03-03-03-03-03-03-03-03"
TIMESTAMP    = 0x12131415
TAGS_DEFAULT = { "mac" : "03-03-03-03-03-03-03-03"}
TAGS         = {
    "mac"       : "01-02-03-04-05-06-07-08",
    "site"      : "super_site",
    "latitude"  : 55.5555,
    "longitude" : -44.4444,
}

#============================ fixtures ==============================

SOL_CHAIN_EXAMPLE = [
    # SOL_TYPE_DUST_NOTIF_DATA_NOT_OAP
    {
        "dust": {
            'name':     'notifData',
            'manager':  'COM6',
            'fields' : {
                'utcSecs':    0x11111111,
                'utcUsecs':   0x22222222,
                'macAddress': '01-02-03-04-05-06-07-08',
                'srcPort':    0x0102,
                'dstPort':    0x0304,
                'data':       [0x05,0x06,0x07,0x08],
            },
        },
        "objects": [
            {
                "json":
                    {
                        "timestamp"  : TIMESTAMP,
                        "mac"        : '01-02-03-04-05-06-07-08',
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
                        0x12,0x13,0x14,0x15,                       # timestamp
                        0x0e,                                      # type
                        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # value
                    ],
                "http":
                    {
                        "v" : 0,
                        "o" : [
                            "EwECAwQFBgcIEhMUFQ4BAgMEBQYHCA=="
                        ]
                    },
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
            },
        ],
    },
    # SOL_TYPE_DUST_NOTIF_DATA_OAP
    {
        "dust": {
            'name':     'notifData',
            'manager':  'COM6',
            'fields' : {
                'utcSecs':    0x11111111,
                'utcUsecs':   0x22222222,
                'macAddress': '01-02-03-04-05-06-07-08',
                'srcPort':    0xf0b9,
                'dstPort':    0xf0b9,
                'data':       [0x05,0x06,0x07,0x08],
            },
        },
        "objects": [],
    },
    # SOL_TYPE_DUST_NOTIF_HRDEVICE (24 bytes, old version)
    {
        "dust": {
            'hr': {
                'Device': {
                    'badLinkFrameId':  0,
                    'badLinkOffset':   0,
                    'badLinkSlot':     0,
                    'batteryVoltage':  2949,
                    'charge':          377,
                    'numMacDropped':   0,
                    'numRxLost':       0,
                    'numRxOk':         5,
                    'numTxBad':        0,
                    'numTxFail':       0,
                    'numTxOk':         58,
                    'queueOcc':        49,
                    'temperature':     21,
                },
            },
            'mac': u'01-02-03-04-05-06-07-08',
            'name': u'hr',
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x10,
                    "value"      : {
                        'badLinkFrameId':  0,
                        'badLinkOffset':   0,
                        'badLinkSlot':     0,
                        'batteryVoltage':  2949,
                        'charge':          377,
                        'numMacDropped':   0,
                        'numRxLost':       0,
                        'numRxOk':         5,
                        'numTxBad':        0,
                        'numTxFail':       0,
                        'numTxOk':         58,
                        'queueOcc':        49,
                        'temperature':     21,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,    # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,    # mac
                    0x12,0x13,0x14,0x15,                        # timestamp
                    0x10,                                       # type
                    0, 0, 1, 121, 49, 21, 11, 133, 0, 58, 0, 0, # value
                    0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0          # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFRAAAAF5MRULhQA6AAAABQAAAAAAAAAAAAA="
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                    },
                    "measurement": 'SOL_TYPE_DUST_NOTIF_HRDEVICE',
                    "fields"     : {
                        'badLinkFrameId':  0,
                        'badLinkOffset':   0,
                        'badLinkSlot':     0,
                        'batteryVoltage':  2949,
                        'charge':          377,
                        'numMacDropped':   0,
                        'numRxLost':       0,
                        'numRxOk':         5,
                        'numTxBad':        0,
                        'numTxFail':       0,
                        'numTxOk':         58,
                        'queueOcc':        49,
                        'temperature':     21,
                    },
                },
            },
        ],
    },
    # SOL_TYPE_DUST_NOTIF_HRDEVICE (27 bytes, new version)
    {
        "dust": {
            'hr': {
                'Device': {
                    'badLinkFrameId': 0,
                    'badLinkOffset': 0,
                    'badLinkSlot': 0,
                    'batteryVoltage': 2949,
                    'charge': 377,
                    'numMacCrcErr': 1,
                    'numMacDropped': 0,
                    'numMacMicErr': 0,
                    'numNetMicErr': 0,
                    'numRxLost': 0,
                    'numRxOk': 5,
                    'numTxBad': 0,
                    'numTxFail': 0,
                    'numTxOk': 58,
                    'queueOcc': 49,
                    'temperature': 21,
                },
            },
            'mac': u'01-02-03-04-05-06-07-08',
            'name': u'hr',
        },
        "objects": [
            {
                "json": {
                    "timestamp": TIMESTAMP,
                    "mac": '01-02-03-04-05-06-07-08',
                    "type": 0x10,
                    "value": {
                        'badLinkFrameId': 0,
                        'badLinkOffset': 0,
                        'badLinkSlot': 0,
                        'batteryVoltage': 2949,
                        'charge': 377,
                        'numMacCrcErr': 1,
                        'numMacDropped': 0,
                        'numMacMicErr': 0,
                        'numNetMicErr': 0,
                        'numRxLost': 0,
                        'numRxOk': 5,
                        'numTxBad': 0,
                        'numTxFail': 0,
                        'numTxOk': 58,
                        'queueOcc': 49,
                        'temperature': 21,
                    },
                },
                "bin": [
                    # ver    type     MAC      ts      typelen   length
                    0 << 6 | 0 << 5 | 1 << 4 | 0 << 3 | 0 << 2 | 3 << 0,# header
                    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,     # mac
                    0x12, 0x13, 0x14, 0x15,                             # timestamp
                    0x10,                                               # type
                    0, 0, 1, 121, 49, 21, 11, 133, 0, 58, 0, 0, 0, 5,   # value
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1               # value
                ],
                "http": {
                    "v": 0,
                    "o": [
                        "EwECAwQFBgcIEhMUFRAAAAF5MRULhQA6AAAABQAAAAAAAAAAAAAAAAE="
                    ]
                },
                "influxdb": {
                    "time": TIMESTAMP * 1000000000,
                    "tags": {
                        'mac': '01-02-03-04-05-06-07-08',
                        'site': 'super_site',
                        'latitude': 55.5555,
                        'longitude': -44.4444,
                    },
                    "measurement": 'SOL_TYPE_DUST_NOTIF_HRDEVICE',
                    "fields": {
                        'badLinkFrameId': 0,
                        'badLinkOffset': 0,
                        'badLinkSlot': 0,
                        'batteryVoltage': 2949,
                        'charge': 377,
                        'numMacCrcErr': 1,
                        'numMacDropped': 0,
                        'numMacMicErr': 0,
                        'numNetMicErr': 0,
                        'numRxLost': 0,
                        'numRxOk': 5,
                        'numTxBad': 0,
                        'numTxFail': 0,
                        'numTxOk': 58,
                        'queueOcc': 49,
                        'temperature': 21,
                    },
                },
            },
        ],
    },
    # SOL_TYPE_DUST_NOTIF_HRDEVICE+SOL_TYPE_DUST_NOTIF_HRDISCOVERED
    {
        "dust": {
            'hr': {
                'Device': {
                    'badLinkFrameId':  0,
                    'badLinkOffset':   0,
                    'badLinkSlot':     0,
                    'batteryVoltage':  2949,
                    'charge':          377,
                    'numMacCrcErr':    1,
                    'numMacDropped':   0,
                    'numMacMicErr':    0,
                    'numNetMicErr':    0,
                    'numRxLost':       0,
                    'numRxOk':         5,
                    'numTxBad':        0,
                    'numTxFail':       0,
                    'numTxOk':         58,
                    'queueOcc':        49,
                    'temperature':     21,
                },
               'Discovered': {
                    'discoveredNeighbors': [
                        {
                            u'neighborId': 3,
                            u'numRx': 2,
                            u'rssi': -37,
                        },
                        {
                            u'neighborId': 7,
                            u'numRx': 1,
                            u'rssi': -62
                        },
                        {
                            u'neighborId': 10,
                            u'numRx': 3,
                            u'rssi': -38
                        },
                        {
                            u'neighborId': 12,
                            u'numRx': 1,
                            u'rssi': -36
                        },
                        {
                            u'neighborId': 5,
                            u'numRx': 1,
                            u'rssi': -35,
                        },
                        {
                            u'neighborId': 8,
                            u'numRx': 1,
                            u'rssi': -39,
                        },
                        {
                            u'neighborId': 9,
                            u'numRx': 1,
                            u'rssi': -44,
                        },
                        {
                            u'neighborId': 11,
                            u'numRx': 1,
                            u'rssi': -49
                        },
                    ],
                    u'numItems': 8,
                    u'numJoinParents': 8,
                },
            },
            'mac': u'01-02-03-04-05-06-07-08',
            'name': u'hr',
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x10,
                    "value"      : {
                        'badLinkFrameId':  0,
                        'badLinkOffset':   0,
                        'badLinkSlot':     0,
                        'batteryVoltage':  2949,
                        'charge':          377,
                        'numMacCrcErr':    1,
                        'numMacDropped':   0,
                        'numMacMicErr':    0,
                        'numNetMicErr':    0,
                        'numRxLost':       0,
                        'numRxOk':         5,
                        'numTxBad':        0,
                        'numTxFail':       0,
                        'numTxOk':         58,
                        'queueOcc':        49,
                        'temperature':     21,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x10,                                      # type
                    0, 0, 1, 121, 49, 21, 11, 133, 0, 58, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1  # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFRAAAAF5MRULhQA6AAAABQAAAAAAAAAAAAAAAAE="
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                    },
                    "measurement": 'SOL_TYPE_DUST_NOTIF_HRDEVICE',
                    "fields"     : {
                        'badLinkFrameId':  0,
                        'badLinkOffset':   0,
                        'badLinkSlot':     0,
                        'batteryVoltage':  2949,
                        'charge':          377,
                        'numMacCrcErr':    1,
                        'numMacDropped':   0,
                        'numMacMicErr':    0,
                        'numNetMicErr':    0,
                        'numRxLost':       0,
                        'numRxOk':         5,
                        'numTxBad':        0,
                        'numTxFail':       0,
                        'numTxOk':         58,
                        'queueOcc':        49,
                        'temperature':     21,
                    },
                },
            },
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x12,
                    "value"      : {
                        'discoveredNeighbors': [
                            {
                                u'neighborId': 3,
                                u'numRx': 2,
                                u'rssi': -37,
                            },
                            {
                                u'neighborId': 7,
                                u'numRx': 1,
                                u'rssi': -62
                            },
                            {
                                u'neighborId': 10,
                                u'numRx': 3,
                                u'rssi': -38
                            },
                            {
                                u'neighborId': 12,
                                u'numRx': 1,
                                u'rssi': -36
                            },
                            {
                                u'neighborId': 5,
                                u'numRx': 1,
                                u'rssi': -35,
                            },
                            {
                                u'neighborId': 8,
                                u'numRx': 1,
                                u'rssi': -39,
                            },
                            {
                                u'neighborId': 9,
                                u'numRx': 1,
                                u'rssi': -44,
                            },
                            {
                                u'neighborId': 11,
                                u'numRx': 1,
                                u'rssi': -49
                            },
                        ],
                        u'numItems': 8,
                        u'numJoinParents': 8,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x12,                                      # type
                    8, 8, 0, 3, 219, 2, 0, 7, 194, 1, 0, 10, 218, 3, 0, 12, 220, 1, 0, 5, 221, 1, 0, 8, 217, 1, 0, 9, 212, 1, 0, 11, 207, 1,   # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFRIICAAD2wIAB8IBAAraAwAM3AEABd0BAAjZAQAJ1AEAC88B"
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'       : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                    },
                    "measurement": 'SOL_TYPE_DUST_NOTIF_HRDISCOVERED',
                    "fields"     : {
                        'discoveredNeighbors:0:neighborId': 3,
                        'discoveredNeighbors:0:numRx': 2,
                        'discoveredNeighbors:0:rssi': -37,
                        'discoveredNeighbors:1:neighborId': 7,
                        'discoveredNeighbors:1:numRx': 1,
                        'discoveredNeighbors:1:rssi': -62,
                        'discoveredNeighbors:2:neighborId': 10,
                        'discoveredNeighbors:2:numRx': 3,
                        'discoveredNeighbors:2:rssi': -38,
                        'discoveredNeighbors:3:neighborId': 12,
                        'discoveredNeighbors:3:numRx': 1,
                        'discoveredNeighbors:3:rssi': -36,
                        'discoveredNeighbors:4:neighborId': 5,
                        'discoveredNeighbors:4:numRx': 1,
                        'discoveredNeighbors:4:rssi': -35,
                        'discoveredNeighbors:5:neighborId': 8,
                        'discoveredNeighbors:5:numRx': 1,
                        'discoveredNeighbors:5:rssi': -39,
                        'discoveredNeighbors:6:neighborId': 9,
                        'discoveredNeighbors:6:numRx': 1,
                        'discoveredNeighbors:6:rssi': -44,
                        'discoveredNeighbors:7:neighborId': 11,
                        'discoveredNeighbors:7:numRx': 1,
                        'discoveredNeighbors:7:rssi': -49,
                        'numItems': 8,
                        'numJoinParents': 8,
                    },
                },
            },
        ],
    },
    # SOL_TYPE_DUST_NOTIF_HRNEIGHBORS
    {
        "dust": {
            'hr': {
                'Neighbors': {
                    'neighbors': [
                        {
                            'neighborFlag': 0,
                            u'neighborId': 4,
                            u'numRxPackets': 2,
                            u'numTxFailures': 0,
                            u'numTxPackets': 103,
                            u'rssi': -33,
                        },
                        {
                            u'neighborFlag': 0,
                            u'neighborId': 1,
                            u'numRxPackets': 4,
                            u'numTxFailures': 14,
                            u'numTxPackets': 193,
                            u'rssi': -60,
                        },
                        {
                            u'neighborFlag': 0,
                            u'neighborId': 6,
                            u'numRxPackets': 40,
                            u'numTxFailures': 0,
                            u'numTxPackets': 0,
                            u'rssi': -28
                        },
                        {
                            u'neighborFlag': 0,
                            u'neighborId': 7,
                            u'numRxPackets': 98,
                            u'numTxFailures': 0,
                            u'numTxPackets': 0,
                            u'rssi': -58,
                        },
                        {
                            u'neighborFlag': 0,
                            u'neighborId': 12,
                            u'numRxPackets': 97,
                            u'numTxFailures': 0,
                            u'numTxPackets': 0,
                            u'rssi': -36,
                        },
                    ],
                    u'numItems': 5,
                },
            },
            u'mac': u'01-02-03-04-05-06-07-08',
            u'name': u'hr',
        },
        "objects" : [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x11,
                    "value"      : {
                        'neighbors': [
                            {
                                'neighborFlag': 0,
                                u'neighborId': 4,
                                u'numRxPackets': 2,
                                u'numTxFailures': 0,
                                u'numTxPackets': 103,
                                u'rssi': -33,
                            },
                            {
                                u'neighborFlag': 0,
                                u'neighborId': 1,
                                u'numRxPackets': 4,
                                u'numTxFailures': 14,
                                u'numTxPackets': 193,
                                u'rssi': -60,
                            },
                            {
                                u'neighborFlag': 0,
                                u'neighborId': 6,
                                u'numRxPackets': 40,
                                u'numTxFailures': 0,
                                u'numTxPackets': 0,
                                u'rssi': -28
                            },
                            {
                                u'neighborFlag': 0,
                                u'neighborId': 7,
                                u'numRxPackets': 98,
                                u'numTxFailures': 0,
                                u'numTxPackets': 0,
                                u'rssi': -58,
                            },
                            {
                                u'neighborFlag': 0,
                                u'neighborId': 12,
                                u'numRxPackets': 97,
                                u'numTxFailures': 0,
                                u'numTxPackets': 0,
                                u'rssi': -36,
                            },
                        ],
                        u'numItems': 5,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x11,                                      # type
                    5, 0, 4, 0, 223, 0, 103, 0, 0, 0, 2, 0, 1, 0, 196, 0, 193, 0, 14, 0, 4, 0, 6, 0, 228, 0, 0, 0, 0, 0, 40, 0, 7, 0, 198, 0, 0, 0, 0, 0, 98, 0, 12, 0, 220, 0, 0, 0, 0, 0, 97   # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFREFAAQA3wBnAAAAAgABAMQAwQAOAAQABgDkAAAAAAAoAAcAxgAAAAAAYgAMANwAAAAAAGE=",
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                    },
                    "measurement": 'SOL_TYPE_DUST_NOTIF_HRNEIGHBORS',
                    "fields"     : {
                        'neighbors:4:neighborFlag': 0,
                        'neighbors:4:neighborId': 4,
                        'neighbors:4:numRxPackets': 2,
                        'neighbors:4:numTxFailures': 0,
                        'neighbors:4:numTxPackets': 103,
                        'neighbors:4:rssi': -33,
                        'neighbors:1:neighborFlag': 0,
                        'neighbors:1:neighborId': 1,
                        'neighbors:1:numRxPackets': 4,
                        'neighbors:1:numTxFailures': 14,
                        'neighbors:1:numTxPackets': 193,
                        'neighbors:1:rssi': -60,
                        'neighbors:6:neighborFlag': 0,
                        'neighbors:6:neighborId': 6,
                        'neighbors:6:numRxPackets': 40,
                        'neighbors:6:numTxFailures': 0,
                        'neighbors:6:numTxPackets': 0,
                        'neighbors:6:rssi': -28,
                        'neighbors:7:neighborFlag': 0,
                        'neighbors:7:neighborId': 7,
                        'neighbors:7:numRxPackets': 98,
                        'neighbors:7:numTxFailures': 0,
                        'neighbors:7:numTxPackets': 0,
                        'neighbors:7:rssi': -58,
                        'neighbors:12:neighborFlag': 0,
                        'neighbors:12:neighborId': 12,
                        'neighbors:12:numRxPackets': 97,
                        'neighbors:12:numTxFailures': 0,
                        'neighbors:12:numTxPackets': 0,
                        'neighbors:12:rssi': -36,
                        'numItems': 5,
                    },
                },
            }
        ]
    },
    # SOL_TYPE_DUST_NOTIF_HREXTENDED (RSSI)
    {
        "dust": {
            'hr': {
                "Extended": {
                    'RSSI': [{'txUnicastAttempts': 12, 'idleRssi': -93, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 13, 'idleRssi': -93, 'txUnicastFailures': 1},
                             {'txUnicastAttempts': 8, 'idleRssi': -89, 'txUnicastFailures': 1},
                             {'txUnicastAttempts': 11, 'idleRssi': -92, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 9, 'idleRssi': -93, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 13, 'idleRssi': -90, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 10, 'idleRssi': -93, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 15, 'idleRssi': -93, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 11, 'idleRssi': -93, 'txUnicastFailures': 1},
                             {'txUnicastAttempts': 14, 'idleRssi': -93, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 12, 'idleRssi': -90, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 15, 'idleRssi': -92, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 14, 'idleRssi': -84, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 13, 'idleRssi': -93, 'txUnicastFailures': 0},
                             {'txUnicastAttempts': 15, 'idleRssi': -93, 'txUnicastFailures': 0}],
                },
            },
            u'mac': u'01-02-03-04-05-06-07-08',
            u'name': u'hr',
        },
        "objects": [
            {
                "json": {
                    "timestamp": TIMESTAMP,
                    "mac": '01-02-03-04-05-06-07-08',
                    "type": 0x44,
                    "value": {
                        'RSSI': [{'txUnicastAttempts': 12, 'idleRssi': -93, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 13, 'idleRssi': -93, 'txUnicastFailures': 1},
                                 {'txUnicastAttempts': 8,  'idleRssi': -89, 'txUnicastFailures': 1},
                                 {'txUnicastAttempts': 11, 'idleRssi': -92, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 9,  'idleRssi': -93, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 13, 'idleRssi': -90, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 10, 'idleRssi': -93, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 15, 'idleRssi': -93, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 11, 'idleRssi': -93, 'txUnicastFailures': 1},
                                 {'txUnicastAttempts': 14, 'idleRssi': -93, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 12, 'idleRssi': -90, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 15, 'idleRssi': -92, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 14, 'idleRssi': -84, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 13, 'idleRssi': -93, 'txUnicastFailures': 0},
                                 {'txUnicastAttempts': 15, 'idleRssi': -93, 'txUnicastFailures': 0}],
                    },
                },
                "bin": [
                    # ver   type   MAC    ts    typelen length
                    0 << 6 | 0 << 5 | 1 << 4 | 0 << 3 | 0 << 2 | 3 << 0,  # header
                    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,  # mac
                    0x12, 0x13, 0x14, 0x15,  # timestamp
                    0x44,  # type
                    1, 75, # extType, extLength
                    163, 0, 12, 0, 0, # channel 11
                    163, 0, 13, 0, 1, # channel 12
                    167, 0, 8, 0, 1,  # channel 13
                    164, 0, 11, 0, 0, # channel 14
                    163, 0, 9, 0, 0,  # channel 15
                    166, 0, 13, 0, 0, # channel 16
                    163, 0, 10, 0, 0, # channel 17
                    163, 0, 15, 0, 0, # channel 18
                    163, 0, 11, 0, 1, # channel 19
                    163, 0, 14, 0, 0, # channel 20
                    166, 0, 12, 0, 0, # channel 21
                    164, 0, 15, 0, 0, # channel 22
                    172, 0, 14, 0, 0, # channel 23
                    163, 0, 13, 0, 0, # channel 24
                    163, 0, 15, 0, 0  # channel 25
                ],
                "http": {
                    "v": 0,
                    "o": [
                        "EwECAwQFBgcIEhMUFUQBS6MADAAAowANAAGnAAgAAaQACwAAowAJAACmAA0AAKMACgAAowAPAACjAAsAAaMADgAApgAMAACkAA8AAKwADgAAowANAACjAA8AAA==",
                    ]
                },
                "influxdb": {
                    "time": TIMESTAMP * 1000000000,
                    "tags": {
                        'mac': '01-02-03-04-05-06-07-08',
                        'site': 'super_site',
                        'latitude': 55.5555,
                        'longitude': -44.4444,
                    },
                    "measurement": 'SOL_TYPE_DUST_NOTIF_HREXTENDED',
                    "fields": {
                        '11:txUnicastAttempts': 12, '11:idleRssi': -93, '11:txUnicastFailures': 0,
                        '12:txUnicastAttempts': 13, '12:idleRssi': -93, '12:txUnicastFailures': 1,
                        '13:txUnicastAttempts': 8,  '13:idleRssi': -89, '13:txUnicastFailures': 1,
                        '14:txUnicastAttempts': 11, '14:idleRssi': -92, '14:txUnicastFailures': 0,
                        '15:txUnicastAttempts': 9,  '15:idleRssi': -93, '15:txUnicastFailures': 0,
                        '16:txUnicastAttempts': 13, '16:idleRssi': -90, '16:txUnicastFailures': 0,
                        '17:txUnicastAttempts': 10, '17:idleRssi': -93, '17:txUnicastFailures': 0,
                        '18:txUnicastAttempts': 15, '18:idleRssi': -93, '18:txUnicastFailures': 0,
                        '19:txUnicastAttempts': 11, '19:idleRssi': -93, '19:txUnicastFailures': 1,
                        '20:txUnicastAttempts': 14, '20:idleRssi': -93, '20:txUnicastFailures': 0,
                        '21:txUnicastAttempts': 12, '21:idleRssi': -90, '21:txUnicastFailures': 0,
                        '22:txUnicastAttempts': 15, '22:idleRssi': -92, '22:txUnicastFailures': 0,
                        '23:txUnicastAttempts': 14, '23:idleRssi': -84, '23:txUnicastFailures': 0,
                        '24:txUnicastAttempts': 13, '24:idleRssi': -93, '24:txUnicastFailures': 0,
                        '25:txUnicastAttempts': 15, '25:idleRssi': -93, '25:txUnicastFailures': 0
                    },
                },
            }
        ]
    },
    # SOL_TYPE_DUST_EVENTPATHCREATE
    {
        "dust": {
            'name': u'eventPathCreate',
            'manager': u'COM6',
            'fields': {
                'source':    '01-01-01-01-01-01-01-01',
                'dest':      '02-02-02-02-02-02-02-02',
                'direction': 3,
                'eventId':   7,
            },
        },
        "objects":[
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : MACMANAGER,
                    "type"       : 0x14,
                    "value"      : {
                        'source'      : [1,1,1,1,1,1,1,1],
                        'dest'        : [2,2,2,2,2,2,2,2],
                        'direction'   : 3,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x14,                                      # type
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                    0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
                    0x03,
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFRQBAQEBAQEBAQICAgICAgICAw=="
                    ]
                },
                "influxdb": {
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
            'name': u'eventPathDelete',
            'manager': u'COM6',
            'fields': {
                'source':    '01-01-01-01-01-01-01-01',
                'dest':      '02-02-02-02-02-02-02-02',
                'direction': 3,
                'eventId':   7,
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : MACMANAGER,
                    "type"       : 0x15,
                    "value"      : {
                        'source'      : [1,1,1,1,1,1,1,1],
                        'dest'        : [2,2,2,2,2,2,2,2],
                        'direction'   : 3,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x15,                                      # type
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                    0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
                    0x03,
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFRUBAQEBAQEBAQICAgICAgICAw==",
                    ],
                },
                "influxdb": {
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
        "dust": {
            'manager': u'COM6',
            'name': u'eventMoteJoin',
            'fields': {
                'eventId': 0x11223344,
                'macAddress': '01-01-01-01-01-01-01-01',
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : MACMANAGER,
                    "type"       : 0x19,
                    "value"      : {
                        'macAddress'  : [1,1,1,1,1,1,1,1],
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x19,                                      # type
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFRkBAQEBAQEBAQ==",
                    ]
                },
                "influxdb": {
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
            'manager': u'COM6',
            'name': u'eventMoteCreate',
            'fields': {
                'eventId': 0x11223344,
                'macAddress': '01-01-01-01-01-01-01-01',
                'moteId': 0x0202,
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : MACMANAGER,
                    "type"       : 0x1a,
                    "value"      : {
                        'macAddress'  : [1,1,1,1,1,1,1,1],
                        'moteId'      : 0x0202,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x1a,                                      # type
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                    0x02,0x02,
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFRoBAQEBAQEBAQIC",
                    ],
                },
                "influxdb": {
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
            'manager': u'COM6',
            'name': u'eventMoteDelete',
            'fields': {
                'eventId': 0x11223344,
                'macAddress': '01-01-01-01-01-01-01-01',
                'moteId': 0x0202,
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : MACMANAGER,
                    "type"       : 0x1b,
                    "value"      : {
                        'macAddress'  : [1,1,1,1,1,1,1,1],
                        'moteId'      : 0x0202,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x1b,                                      # type
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                    0x02,0x02,
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFRsBAQEBAQEBAQIC",
                    ],
                },
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
            'manager': u'COM6',
            'name': u'eventMoteLost',
            'fields': {
                'eventId': 0x11223344,
                'macAddress': '01-01-01-01-01-01-01-01',
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : MACMANAGER,
                    "type"       : 0x1c,
                    "value"      : {
                        'macAddress'  : [1,1,1,1,1,1,1,1],
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x1c,                                      # type
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFRwBAQEBAQEBAQ==",
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '03-03-03-03-03-03-03-03',
                    },
                    "measurement": 'SOL_TYPE_DUST_EVENTMOTELOST',
                    "fields"     : {
                        'macAddress'  : '01-01-01-01-01-01-01-01',
                    },
                },
            },
        ],
    },
    # SOL_TYPE_DUST_EVENTMOTEOPERATIONAL
    {
        "dust": {
            'manager': u'COM6',
            'name': u'eventMoteOperational',
            'fields': {
                'eventId': 0x11223344,
                'macAddress': '01-01-01-01-01-01-01-01',
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : MACMANAGER,
                    "type"       : 0x1d,
                    "value"      : {
                        'macAddress'  : [1,1,1,1,1,1,1,1],
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x1d,                                      # type
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFR0BAQEBAQEBAQ==",
                    ]
                },
                "influxdb": {
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
            'name': u'oap',
            'mac': u'01-02-03-04-05-06-07-08',
            'fields': {
                'channel': [5],
                'channel_str': u'temperature',
                'num_samples': 1,
                'packet_timestamp': [262570839552L, 116116480],
                'rate': 30000,
                'received_timestamp': u'2017-05-07 14:53:44.753000',
                'sample_size': 16,
                'samples': [0x0a33],
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x27,
                    "value"      : {
                        'temperature': 0x0a33,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x27,                                      # type
                    0x0a,0x33,                                 # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFScKMw==",
                    ],
                },
                "influxdb": {
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
            },
        ],
    },
    # SOL_TYPE_DUST_OAP_TEMPSAMPLE (with negative temperature value)
    {
        "dust": {
            'name': u'oap',
            'mac': u'01-02-03-04-05-06-07-08',
            'fields': {
                'channel': [5],
                'channel_str': u'temperature',
                'num_samples': 1,
                'packet_timestamp': [262570839552L, 116116480],
                'rate': 30000,
                'received_timestamp': u'2017-05-07 14:53:44.753000',
                'sample_size': 16,
                'samples': [-123],
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x27,
                    "value"      : {
                        'temperature': -123,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x27,                                      # type
                    255, 133,                                  # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFSf/hQ==",
                    ],
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                    },
                    "measurement": 'SOL_TYPE_DUST_OAP_TEMPSAMPLE',
                    "fields"     : {
                        'temperature': -123,
                    },
                },
            },
        ],
    },
    # SOL_TYPE_DUST_EVENTJOINFAILED
    {
        "dust": {
            'name': u'eventJoinFailed',
            'manager': u'COM6',
            'fields': {
                'macAddress':   '01-01-01-01-01-01-01-01',
                'reason':       1
            },
        },
        "objects":[
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : MACMANAGER,
                    "type"       : 0x3a,
                    "value"      : {
                        'macAddress'    : [1, 1, 1, 1, 1, 1, 1, 1],
                        'reason'        : 1
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x3a,                                      # type
                    0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                    0x01,
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFToBAQEBAQEBAQE="
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '03-03-03-03-03-03-03-03',
                    },
                    "measurement": 'SOL_TYPE_DUST_EVENTJOINFAILED',
                    "fields"     : {
                        'macAddress'    : '01-01-01-01-01-01-01-01',
                        'reason'        : 1
                    },
                },
            }
        ]
    },
    # SOL_TYPE_JUDD_T2D2R1N1,
    {
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x22,
                    "value"      : {
                        'temperature': 0x0a33,
                        'depth':       0x0b44,
                        'numReadings': 0x01,
                        'retries':     0x04,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,    # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,    # mac
                    0x12,0x13,0x14,0x15,                        # timestamp
                    0x22,                                       # type
                    0x0a,0x33,                                  # value_temperature
                    0x0b,0x44,                                  # value_depth
                    0x01,                                       # value_numReadings
                    0x04,                                       # value_retries
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFSIKMwtEAQQ=",
                    ],
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                    },
                    "measurement": 'SOL_TYPE_JUDD_T2D2R1N1',
                    "fields"     : {
                        'temperature': 0x0a33,
                        'depth': 0x0b44,
                        'numReadings': 0x01,
                        'retries': 0x04,
                    },
                },
            },
        ],
    },
    # SOL_TYPE_DUST_SNAPSHOT
    {
        "objects": [
            {
                "json": {
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
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,        # header
                    0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,        # mac
                    0x12,0x13,0x14,0x15,                            # timestamp
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
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwMDAwMDAwMDEhMUFSACAQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRobHB0eHyAhIiMkJSYnAhESExQVFhcYLC0u//4hIiMkJSYnKCwtLv/+MTIzNDU2NzgJCgsMDQ4PEBESExQVFhcYGRobHB0eHyAhIiMkJSYnAUFCQ0RFRkdILC0u//4=",
                    ]
                },
                "influxdb": {
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
                    },
                },
            },
        ],
    },
    # SOL_TYPE_SOLMANAGER_STATS
    {
        "objects": [
            {
                "json": {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x28,
                    "value"      : {
                        "sol_version"           : [1,2,3,4],
                        "solmanager_version"    : [5,6,7,8],
                        "sdk_version"           : [9,1,2,3],
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x28,                                      # type
                    0x01,0x02,0x03,0x04,                       # value_solversion
                    0x05,0x06,0x07,0x08,                       # value_solmanagerversion
                    0x09,0x01,0x02,0x03,                       # value_sdkversion
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFSgBAgMEBQYHCAkBAgM="
                    ]
                },
                "influxdb": {
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
            },
        ],
    },
    # SOL_TYPE_SENS_SHT25_T2N1H2N1 with apply field function
    {
        "dust": {
            'name':     'notifData',
            'manager':  'COM6',
            'fields' : {
                'utcSecs':    1111,
                'utcUsecs':   222,
                'macAddress': '01-02-03-04-05-06-07-08',
                'srcPort':    0xf0ba,
                'dstPort':    0xf0ba,
                'data':       [
                    0x00,                                      # HEADER
                    0x00, 0x0e, 0x9a, 0x57,                    # TIMESTAMP
                    0x31, 0x3c, 0x65, 0x01, 0x99, 0x88, 0x01,  # SENS_SHT25_T2N1H2N1
                ],
            },
        },
        "objects": [
            {
                "json": {
                    "timestamp"  : 0x12131415,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x31,
                    "value"      : {
                        "temp_raw"      : 0x653c,
                        "t_Nval"        : 0x01,
                        "rh_raw"        : 0x8899,
                        "rh_Nval"       : 0x01,
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x31,                                      # type
                    0x3c,0x65,                                 # value--temp_raw
                    0x01,                                      # value--t_Nval
                    0x99,0x88,                                 # value--rh_raw
                    0x01,                                      # value--rh_Nval
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFTE8ZQGZiAE=",
                    ],
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        't_Nval'    : 0x01,
                        'rh_Nval'   : 0x01,
                    },
                    "measurement": 'SOL_TYPE_SENS_SHT25_T2N1H2N1',
                    "fields"     : {
                        "temp_raw"      : 0x653c,
                        "t_Nval"        : 0x01,
                        "rh_raw"        : 0x8899,
                        "rh_Nval"       : 0x01,
                        'rh_phys': 60.69807434082031,
                        'temp_phys': 22.63790771484374,
                    },
                },
            },
        ],
    },
    # SOL_TYPE_SENS_MPS1 with apply tag function
    {
        "objects": [
            {
                "json": {
                    "timestamp"  : 0x579a0e00,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x38,
                    "value"      : {
                        "die_raw"       : 10.100000381469727,   # 0x4121999a
                        "depth"         : 15.300000190734863,   # 0x4174cccd
                    },
                },
                "bin": [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x57,0x9a,0x0e,0x00,                       # timestamp
                    0x38,                                      # type
                    0x9a,0x99,0x21,0x41,                       # value--die_raw
                    0xcd,0xcc,0x74,0x41,                       # value--depth
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIV5oOADiamSFBzcx0QQ==",
                    ],
                },
                "influxdb": {
                    "time"       : 0x579a0e00*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        'depth'     : 15.300000190734863,
                    },
                    "measurement": 'SOL_TYPE_SENS_MPS1',
                    "fields"     : {
                        "die_raw"       : 10.100000381469727,
                        "depth"         : 15.300000190734863,
                    },
                },
            },
        ],
    },
    # MULTI-TTLV
    {
        "dust": {
            'name':     'notifData',
            'manager':  'COM6',
            'fields' : {
                'utcSecs':    1111,
                'utcUsecs':   222,
                'macAddress': '01-02-03-04-05-06-07-08',
                'srcPort':    0xf0ba,
                'dstPort':    0xf0ba,
                'data':       (
                    0x20,                                     # multi TTLV 0010 0000
                    0x05, 0x05, 0x05, 0x05,                   # epoch
                    0x04,                                     # 4 objects:
                    0x32, 0x00, 0x00, 0x01,                   # - SOL_TYPE_SENS_NEOVBAT_V2N1
                    0x31, 0x3c, 0x65, 0x01, 0xa2, 0x67, 0x01, # - SOL_TYPE_SENS_SHT25_T2N1H2N1
                    0x30, 0x00, 0x0a, 0xd7, 0x23, 0x40, 0x66, # - SOL_TYPE_SENS_GS3_I1D4T4E4N1
                    0x66, 0xb2, 0x41, 0x00, 0x00, 0x80, 0x3f,
                    0x01,
                    0x29, 0x1b, 0x02, 0x01, 0x00, 0x1b, 0x54, # - SOL_TYPE_SENS_MB7363_D2S2N1L1G1
                    0x55,
                ),
            },
        },
        "objects": [
            # SOL_TYPE_SENS_NEOVBAT_V2N1
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x32,
                    "value"      : {
                        "voltage"       : 0,
                        "N"             : 1,
                    },
                },
                "bin" : [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x32,                                      # type 0x32==SOL_TYPE_SENS_NEOVBAT_V2N1
                    0x00,0x00,                                 # value--voltage
                    0x01,                                      # value--numReadings
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFTIAAAE=",
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        "N"         : 1,
                    },
                    "measurement": 'SOL_TYPE_SENS_NEOVBAT_V2N1',
                    "fields"     : {
                        "voltage"       : 0,
                        "vol_phys"      : 0,
                        "N"             : 1,
                    },
                },
            },
            # SOL_TYPE_SENS_SHT25_T2N1H2N1
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x31,
                    "value"      : {
                        "temp_raw"      : 0x653c,
                        "t_Nval"        : 0x01,
                        "rh_raw"        : 0x67a2,
                        "rh_Nval"       : 0x01,
                    },
                },
                "bin" : [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x31,                                      # type 0x31==SOL_TYPE_SENS_SHT25_T2N1H2N1
                    0x3c,0x65,                                 # value--temp_raw
                    0x01,                                      # value--t_Nval
                    0xa2,0x67,                                 # value--rh_raw
                    0x01,                                      # value--rh_Nval
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFTE8ZQGiZwE=",
                    ],
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        't_Nval'    : 0x01,
                        'rh_Nval'   : 0x01,
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
            # SOL_TYPE_SENS_GS3_I1D4T4E4N1
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x30,
                    "value"      : {
                        "sub_id"        : 0x00,
                        "dielect"       : 2.559999942779541,
                        "temp"          : 22.299999237060547,
                        "eleCond"       : 1.0,
                        "Nval"          : 0x01,
                    },
                },
                "bin" : [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x30,                                      # type 0x30==SOL_TYPE_SENS_GS3_I1D4T4E4N1
                    0x00,                                      # value--id
                    0x0a,0xd7,0x23,0x40,                       # value--dielect
                    0x66,0x66,0xb2,0x41,                       # value--temp
                    0x00,0x00,0x80,0x3f,                       # value--eleCond
                    0x01,                                      # value--Nval
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFTAACtcjQGZmskEAAIA/AQ==",
                    ],
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        'sub_id'    : 0x00,
                        'Nval'      : 0x01,
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
            # SOL_TYPE_SENS_MB7363_D2S2N1L1G1
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x29,
                    "value"      : {
                        "mean_d2g"      : 0x021b,
                        "stdev"         : 0x0001,
                        "Nval"          : 0x1b,
                        "Nltm"          : 0x54,
                        "NgtM"          : 0x55,
                    },
                },
                "bin" : [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x29,                                      # type 0x29==SOL_TYPE_SENS_MB7363_D2S2N1L1G1
                    0x1b, 0x02,                                # value--mean_d2g
                    0x01, 0x00,                                # value--stdDev
                    0x1b,                                      # value--Nval
                    0x54,                                      # value--Nltm
                    0x55,                                      # value--NgtM
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFSkbAgEAG1RV",
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        'mean_d2g'  : 0x021b,
                        'stdev'     : 0x0001,
                        'Nval'      : 0x1b,
                    },
                    "measurement": 'SOL_TYPE_SENS_MB7363_D2S2N1L1G1',
                    "fields"     : {
                        "mean_d2g"      : 0x021b,
                        "stdev"         : 0x0001,
                        "Nval"          : 0x1b,
                        "Nltm"          : 0x54,
                        "NgtM"          : 0x55,
                    },
                },
            }
        ]
    },
    # get timestamp from Dust Message (with TEMPRH_SHT31)
    {
        "dust": {
            'name':     'notifData',
            'manager':  'COM6',
            'fields' : {
                'utcSecs':    1111,
                'utcUsecs':   222,
                'macAddress': '01-02-03-04-05-06-07-08',
                'srcPort':    0xf0ba,
                'dstPort':    0xf0ba,
                'data':       [
                    0x28,              # SOL Header 0010 1000
                    0x02,              # number of objects
                    0x40,              # 1. TEMPRH_SHT31
                    0x63, 0x87,        # value--temp_raw
                    0x9d, 0x27,        # value--rh_raw
                    0x03,              # value--id
                    0x40,              # 2. TEMPRH_SHT31
                    0x63, 0x87,        # value--temp_raw
                    0x9d, 0x27,        # value--rh_raw
                    0x03,              # value--id
                ],
            },
        },
        "objects": [
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x40,
                    "value"      : {
                        "temp_raw"       : 0x6387,
                        "rh_raw"         : 0x9d27,
                        "id"             : 3,
                    },
                },
                "bin" : [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x40,                                      # type
                    0x63,0x87,                                 # value--temp_raw
                    0x9d,0x27,                                 # value--rh_raw
                    0x03                                       # value--id
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFUBjh50nAw==",
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        'id'        : 3,
                    },
                    "measurement": 'SOL_TYPE_TEMPRH_SHT31',
                    "fields"     : {
                        "temp_raw"      : 0x6387,
                        "rh_raw"        : 0x9d27,
                        "temp_phys"     : 23,
                        "rh_phys"       : 61,
                        "id"            : 3,
                    },
                },
            },
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 0x40,
                    "value"      : {
                        "temp_raw"       : 0x6387,
                        "rh_raw"         : 0x9d27,
                        "id"             : 3,
                    },
                },
                "bin" : [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    0x40,                                      # type
                    0x63,0x87,                                 # value--temp_raw
                    0x9d,0x27,                                 # value--rh_raw
                    0x03                                       # value--id
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFUBjh50nAw==",
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        'id'        : 3,
                    },
                    "measurement": 'SOL_TYPE_TEMPRH_SHT31',
                    "fields"     : {
                        "temp_raw"      : 0x6387,
                        "rh_raw"        : 0x9d27,
                        "temp_phys"     : 23,
                        "rh_phys"       : 61,
                        "id"            : 3,
                    },
                },
            },
        ],
    },

    # SOL_TYPE_SENS_INDUCTION_CURRENT_V_SOURCE
    # 140, 91, 0, 0, 220, 65, 33, 0, 252, 0, 1

    {"objects": [
            {
                "json" : {
                    "timestamp"  : TIMESTAMP,
                    "mac"        : '01-02-03-04-05-06-07-08',
                    "type"       : 73,
                    "value"      : {'accu_sum_of_squares': 2179548,
                                    'sensor_id': 4,
                                    'accu_sum': 23436,
                                    'sample_count': 252},
                },
                "bin" : [
                    #ver   type   MAC    ts    typelen length
                    0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                    0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                    0x12,0x13,0x14,0x15,                       # timestamp
                    73,                                        # type
                    140, 91, 0, 0, 220, 65, 33, 0, 252, 0, 4   # value
                ],
                "http": {
                    "v" : 0,
                    "o" : [
                        "EwECAwQFBgcIEhMUFUmMWwAA3EEhAPwABA==",
                    ]
                },
                "influxdb": {
                    "time"       : TIMESTAMP*1000000000,
                    "tags"       : {
                        'mac'    : '01-02-03-04-05-06-07-08',
                        'site'      : 'super_site',
                        'latitude'  : 55.5555,
                        'longitude' : -44.4444,
                        'id'        : 4,
                    },
                    "measurement": 'SOL_TYPE_SENS_INDUCTION_CURRENT_V_SOURCE',
                    "fields"     : {'accu_sum_of_squares': 2179548,
                                    'sensor_id': 4,
                                    'accu_sum': 23436,
                                    'sample_count': 252,
                                    'current_A': 0.0},
                },
            },
        ],
    },
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

    if "dust" in sol_chain_example:
        # dust->json
        sol_jsonl  = sol.dust_to_json(
           sol_chain_example["dust"],
           mac_manager  = MACMANAGER,
           timestamp    = TIMESTAMP,
        )
    else:
        sol_jsonl = [sol_chain_example["objects"][0]["json"]]

    print sol_chain_example["objects"]
    print sol_jsonl

    # same number of objects? (for HR)
    assert len(sol_jsonl) == len(sol_chain_example["objects"])

    for (sol_json, example) in zip(sol_jsonl,sol_chain_example["objects"]):
        # dust->json
        print '=====\ndust->json'
        print sol_json
        print example["json"]
        assert sol_json==example["json"]

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
        assert json.loads(sol_http)==example["http"]

        # http->bin
        sol_binl  = sol.http_to_bin(sol_http)
        assert len(sol_binl)==1
        sol_bin   = sol_binl[0]
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
