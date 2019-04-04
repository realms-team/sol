#!/usr/bin/python
"""
Code taken from SmartMeshSDK. The origin code was modified.

Copyright (c) 2012, Dust Networks
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Dust Networks nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL DUST NETWORKS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import struct
import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
log = logging.getLogger('HrParser')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

HR_ID_DEVICE                  = 0x80
HR_ID_NEIGHBORS               = 0x81
HR_ID_DISCOVERED              = 0x82
HR_ID_EXTENDED                = 0x91
HR_ID_ALL                     = [
    HR_ID_DEVICE,
    HR_ID_NEIGHBORS,
    HR_ID_DISCOVERED,
    HR_ID_EXTENDED,
]
HR_ID_EXTENDED_RSSI           = 1

HR_DESC_DEVICE = [
    ('charge',                'I'),
    ('queueOcc',              'B'),
    ('temperature',           'b'),
    ('batteryVoltage',        'H'),
    ('numTxOk',               'H'),
    ('numTxFail',             'H'),
    ('numRxOk',               'H'),
    ('numRxLost',             'H'),
    ('numMacDropped',         'B'),
    ('numTxBad',              'B'),
    ('badLinkFrameId',        'B'),
    ('badLinkSlot',           'I'),
    ('badLinkOffset',         'B'),
    ('numNetMicErr',          'B'),
    ('numMacMicErr',          'B'),
    ('numMacCrcErr',          'B'),
]

HR_DESC_NEIGHBORS = [
    ('numItems',              'B'),
]
HR_DESC_NEIGHBOR_DATA = [
    ('neighborId',            'H'),
    ('neighborFlag',          'B'),
    ('rssi',                  'b'),
    ('numTxPackets',          'H'),
    ('numTxFailures',         'H'),
    ('numRxPackets',          'H'),
]

HR_DESC_DISCOVERED = [
    ('numJoinParents',        'B'),
    ('numItems',              'B'),
]
HR_DESC_DISCOVERED_DATA = [
    ('neighborId',            'H'),
    ('rssi',                  'b'),
    ('numRx',                 'B'),
]

HR_DESC_EXTENDED = [
    ('extType',               'B'),
    ('extLength',             'B'),
]

HR_DESC_EXTENDED_RSSI_DATA = [
    ('idleRssi',              'b'),
    ('txUnicastAttempts',     'H'),
    ('txUnicastFailures',     'H'),
]

# ======================= public ==============================================

def parseHr(hr):
    """
    Parse a byte list representing a received HR.

    :returns: The parsed HR, of the following format:
    {
        'Device': {
            <fieldName>: <fieldVal>,
            ...
        }
        'Neighbors': {
            <fieldName>: <fieldVal>,
            ...,
            'neighbors': [
                {
                    <fieldName>: <fieldVal>,
                    ...
                }
            ]
        }
        'Discovered': {
            <fieldName>: <fieldVal>,
            ...,
            'discoveredNeighbors': [
                {
                    <fieldName>: <fieldVal>,
                    ...
                }
            ]
        }
    }
    """
    returnVal = {}

    while hr:
        if len(hr) < 2:
            raise ValueError("Less than 2 bytes in HR")
        hr_id      = hr[0]
        length     = hr[1]
        payload    = hr[2:2+length]

        # parse current HR
        if   hr_id == HR_ID_DEVICE:
            returnVal['Device']         = _parseDevice(payload)
        elif hr_id == HR_ID_NEIGHBORS:
            returnVal['Neighbors']      = _parseNeighbors(payload)
        elif hr_id == HR_ID_DISCOVERED:
            returnVal['Discovered']     = _parseDiscovered(payload)
        elif hr_id == HR_ID_EXTENDED:
            returnVal['Extended']       = _parseExtended(payload)
        else:
            raise ValueError("unknown HR id {0}".format(hr_id))

        # remove current HR
        hr = hr[2+length:]

    return returnVal

def formatHr(hr):
    return _formatHr_recursive(hr, 0)

# ======================= private =============================================

def _formatHr_recursive(e, lvl):
    output  = []
    indent  = ' '*(4*lvl)
    if   type(e) in [str, int]:
        output     += [str(e)]
    elif type(e) == dict:
        for k in sorted(e.keys()):
            if type(e[k]) in [dict, list]:
                formatString = '{0}- {1}:\n{2}'
            else:
                formatString = '{0}- {1:<20}: {2}'
            output += [formatString.format(indent, k, _formatHr_recursive(e[k], lvl+1))]
    elif type(e) == list:
        for idx, v in enumerate(e):
            if type(v) in [dict, list]:
                output += ['{0}-item {1}\n{2}'.format(
                        indent,
                        idx,
                        _formatHr_recursive(v, lvl+1)
                    )
                ]
            else:
                output += ['{0}- {1}'.format(
                        indent,
                        _formatHr_recursive(v, lvl+1)
                    )
                ]
    else:
        raise SystemError("unexpected type {0}".format(type(e)))
    output = '\n'.join(output)
    return output

def _parseDevice(payload):
    (remainder, fields) = _parseAs(
        desc    = HR_DESC_DEVICE,
        payload = payload,
    )
    assert not remainder
    return fields

def _parseNeighbors(payload):

    # parse the header
    (payload, fields) = _parseAs(
        desc    = HR_DESC_NEIGHBORS,
        payload = payload,
    )

    # parse the neighbors
    fields['neighbors'] = []
    for _ in range(fields['numItems']):
        (payload, newItem) = _parseAs(
            desc    = HR_DESC_NEIGHBOR_DATA,
            payload = payload,
        )
        fields['neighbors'] += [newItem]

    return fields

def _parseDiscovered(payload):

    # parse the header
    (payload, fields) = _parseAs(
        desc    = HR_DESC_DISCOVERED,
        payload = payload,
    )

    # parse the discoveredNeighbors
    fields['discoveredNeighbors'] = []
    for _ in range(fields['numItems']):
        (payload, newItem) = _parseAs(
            desc    = HR_DESC_DISCOVERED_DATA,
            payload = payload,
        )
        fields['discoveredNeighbors'] += [newItem]

    return fields

def _parseExtended(payload):

    # parse the header
    (payload, fields) = _parseAs(
        desc    = HR_DESC_EXTENDED,
        payload = payload,
    )

    if fields['extLength'] != len(payload):
        raise ValueError("extLength={0} while len(extended HR payload)={1}"
                         .format(fields['extLength'], len(payload)))

    returnVal = {}
    if fields['extType'] == HR_ID_EXTENDED_RSSI:
        returnVal['RSSI']   = _parseExtendedRSSI(payload)
    else:
        raise ValueError("unknown extended HR extType {0}".format(fields['extType']))

    return returnVal

def _parseExtendedRSSI(payload):

    if len(payload) != 75:
        raise ValueError("RSSI HR should be of length 75, not {0}".format(len(payload)))

    returnVal = []

    while payload:
        (payload, fields) = _parseAs(
            desc    = HR_DESC_EXTENDED_RSSI_DATA,
            payload = payload,
        )
        returnVal += [fields]

    return returnVal

# ======================= helpers =============================================

def _parseAs(desc, payload):

    returnVal            = {}

    # assemble the format string
    fmt                  = '>'
    numFields            = 0
    while True:
        fmt             += desc[numFields][1]
        numBytes         = struct.calcsize(fmt)
        if numBytes == len(payload):
            break
        numFields       += 1
        if len(desc) == numFields:
            break

    # verify enough bytes
    if len(payload) < numBytes:
        raise ValueError("not enough bytes for HR")

    # separate string to parse from remainder
    hrstring             = bytes(payload[:numBytes])
    remainder            = payload[numBytes:]

    # apply the format string
    fields               = struct.unpack(fmt, hrstring)

    for (d, v) in zip(desc, fields):
        returnVal[d[0]]  = v

    return remainder, returnVal
