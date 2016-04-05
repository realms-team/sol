import sys
import os

import json
import struct
import base64
import threading
import time
import array
import datetime
import pdb

import SolDefines
import SolVersion as ver
import OpenHdlc

here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(here, 'smartmeshsdk', 'libs'))
sys.path.insert(0, os.path.join(here, 'smartmeshsdk', 'external_libs'))

from SmartMeshSDK.protocols.Hr          import  HrParser

from SmartMeshSDK.protocols.oap         import  OAPMessage, \
                                                OAPNotif


class Sol(object):
    '''
    Sensor Object Library.
    '''

    def __init__(self):
        self.fileLock = threading.RLock()
        self.hdlc     = OpenHdlc.OpenHdlc()
        self.hrParser = HrParser.HrParser()

    #======================== public ==========================================

    #===== admin

    @property
    def version(self):
        return ver.SOL_VERSION

    #===== SOL Compound conversions
    @staticmethod
    def list_to_compound(obj_list):
        '''
        Converts a list of SOL Objects to a SOL Compound.
        All the Objects in the list must be in verbose fomat

        :param list obj_list: a list of SOL Objects in verbose format
        :return: A SOL Compound in JSON representation
        :rtype: dict
        '''

        sol_comp = {
            "v": SolDefines.SOL_HDR_V,
            "o": obj_list,
        }

        return sol_comp

    @staticmethod
    def compound_to_list(sol_comp):
        '''
        Converts a SOL Compound Object into a list of SOL Objects
        The returned Objects are in verbose format.

        :param dict sol_comp: A SOL Compound in JSON representation
        :return: A list of Objects in verbose format
        :rtype: list
        '''

        obj_list = sol_comp['o']

        return obj_list

    @staticmethod
    def comp_json_to_bin():
        return NotImplementedError

    @staticmethod
    def comp_bin_to_json():
        return NotImplementedError

    #===== SOL Object conversion
    def dust_to_json(self, dust_obj):
        '''
        Convert DUST messages into SOL Objects in JSON format.

        :param dict dust_obj: The DUST Object
        :return: A SOL Object in verbose format
        :rtype: dict
        '''

        # extract the important data
        #netTs      = self._calcNetTs(notifParams)
        srcPort    = dust_obj['srcPort']
        dstPort    = dust_obj['dstPort']
        data       = dust_obj['data']

        # Find SOL type by port
        obj_id = 0
        if dstPort==SolDefines.SOL_PORT:
            raise NotImplementedError()
        elif dstPort==SolDefines.OAP_PORT:
            obj_id = SolDefines.SOL_TYPE_DUST_OAP
        else:
            obj_id = SolDefines.SOL_TYPE_DUST_NOTIF_DATA_RAW

        # Create JSON Object
        json_obj = {
            "mac":          dust_obj['macAddress'],
            "timestamp":    int(time.time()),
            "type":         obj_id,
            "value":        dust_obj['data']
        }

        return json_obj

    def json_to_bin(self, json_obj):
        bin_obj = []

        # header
        h     = 0
        h    |= SolDefines.SOL_HDR_V<<SolDefines.SOL_HDR_V_OFFSET
        h    |= SolDefines.SOL_HDR_H_START<<SolDefines.SOL_HDR_H_OFFSET
        h    |= SolDefines.SOL_HDR_START_M_8BMAC<<SolDefines.SOL_HDR_START_M_OFFSET
        h    |= SolDefines.SOL_HDR_START_S_EPOCH<<SolDefines.SOL_HDR_START_S_OFFSET
        h    |= SolDefines.SOL_HDR_START_Y_1B<<SolDefines.SOL_HDR_START_Y_OFFSET
        h    |= SolDefines.SOL_HDR_START_L_WK<<SolDefines.SOL_HDR_START_L_OFFSET
        bin_obj  += [h]

        # mac
        bin_obj  += json_obj['mac']

        # timestamp
        bin_obj  += self._num_to_list(json_obj['timestamp'],4)

        # type
        bin_obj  += self._num_to_list(json_obj['type'],1)

        # value
        bin_obj  += json_obj['value']

        return bin_obj

        return json_m_obj

    def bin_to_json(self,o_bin,mac=None):
        return_val = {}

        # header

        assert len(o_bin)>=1

        h     = o_bin[0]
        h_V   = (h>>SolDefines.SOL_HDR_V_OFFSET)&0x03
        assert h_V==SolDefines.SOL_HDR_V
        h_H   = (h>>SolDefines.SOL_HDR_H_OFFSET)&0x01
        assert h_H==SolDefines.SOL_HDR_H_START
        h_M   = (h>>SolDefines.SOL_HDR_START_M_OFFSET)&0x01
        h_S   = (h>>SolDefines.SOL_HDR_START_S_OFFSET)&0x01
        assert h_S==SolDefines.SOL_HDR_START_S_EPOCH
        h_Y   = (h>>SolDefines.SOL_HDR_START_Y_OFFSET)&0x01
        assert h_Y==SolDefines.SOL_HDR_START_Y_1B
        h_L   = (h>>SolDefines.SOL_HDR_START_L_OFFSET)&0x03
        assert h_L==SolDefines.SOL_HDR_START_L_WK

        o_bin = o_bin[1:]

        # mac

        if h_M==SolDefines.SOL_HDR_START_M_NOMAC:
            assert mac is not None
            return_val['mac'] = mac
        else:
            assert len(o_bin)>=8
            return_val['mac'] = o_bin[:8]
            o_bin = o_bin[8:]

        # timestamp

        assert len(o_bin)>=4
        return_val['timestamp'] = self._list_to_num(o_bin[:4])
        o_bin = o_bin[4:]

        # type

        assert len(o_bin)>=1
        return_val['type'] = o_bin[0]
        o_bin = o_bin[1:]

        # value

        assert len(o_bin)>=0
        return_val['value'] = o_bin

        return return_val

    #===== JSON Object conversions
    def json_verb_to_min(self, verb_obj):
        '''
        Converts a JSON Object from verbose format to minimal format.

        :param dict json_obj: The JSON Object in verbose format
        :return: The JSON Object in minimal format (bytes list)
        :rtype: list
        '''
        return base64.b64encode(''.join(chr(b) for b in self.json_to_bin(verb_obj)))

    def json_min_to_verb(self, min_obj):
        bin_obj = base64.b64decode(min_obj)
        bin_obj = [ord(b) for b in bin_obj]
        return self.bin_to_json(bin_obj)

    def json_to_dicts(self,o_json):
        all_obj = json.loads(o_json)['o']

        return_val = []
        for obj in all_obj:

            if type(obj)==dict:
                # verbose

                thisDict = {
                    "mac": [int(b, 16) for b in obj['mac'].split('-')],
                    "timestamp": obj['timestamp'],
                    "type": obj['type'],
                    "value": [ord(b) for b in base64.b64decode(obj['value'])]
                }
            else:
                # minimal

                o_bin = base64.b64decode(obj)
                o_bin = [ord(b) for b in o_bin]

                thisDict = self.bin_to_dict(o_bin)
            return_val += [thisDict]

        return return_val

    #===== file manipulation

    def dumpToFile(self,dicts,file_name):

        with self.fileLock:
            with open(file_name,'ab') as f:
                for o_dict in dicts:
                    o_bin = self.dict_to_bin(o_dict)
                    o_bin = self.hdlc.hdlcify(o_bin)
                    o_bin = ''.join([chr(b) for b in o_bin])
                    f.write(o_bin)

    def loadFromFile(self,file_name,startTimestamp=None,endTimestamp=None):

        if startTimestamp is not None or endTimestamp is not None:
            assert startTimestamp is not None and endTimestamp is not None

        if startTimestamp is None:
            # retrieve all data

            with self.fileLock:
                (bins,_) = self.hdlc.dehdlcify(file_name)

            dicts = [self.bin_to_dict(b) for b in bins]

        else:

            with self.fileLock:

                #=== find startOffset

                while True:

                    startOffset = None

                    def oneObject(offset):
                        (o,idx) = self.hdlc.dehdlcify(file_name,fileOffset=offset,maxNum=1)
                        o = o[0]
                        o = self.bin_to_dict(o)
                        return o, idx

                    def oneTimestamp(offset):
                        (o,idx) = oneObject(offset)
                        return o['timestamp'], idx

                    #=== get boundaries

                    left_offset_start = 0
                    try:
                        (left_timestamp,left_offset_stop) = oneTimestamp(left_offset_start)
                    except IndexError:
                        # complete file is corrupted
                        return []
                    with open(file_name,'rb') as f:
                        f.seek(0,os.SEEK_END)
                        right_offset_start = f.tell()
                    while True:
                        right_offset_start = self._backUpUntilStartFrame(file_name,right_offset_start)
                        try:
                           (right_timestamp,right_offset_stop) = oneTimestamp(right_offset_start)
                        except IndexError:
                            right_offset_start -= 1
                        else:
                            break

                    if left_timestamp>startTimestamp:
                        startOffset = left_timestamp
                        break
                    if right_timestamp<startTimestamp:
                        startOffset = right_timestamp
                        break

                    #=== binary search

                    while left_offset_stop<right_offset_start-1:

                        cur_offset_start = int((right_offset_start-left_offset_start)/2+left_offset_start)
                        (cur_timestamp,cur_offset_stop) = oneTimestamp(cur_offset_start)

                        if cur_timestamp==startTimestamp:
                            startOffset = cur_offset_start
                            break
                        elif cur_timestamp>startTimestamp:
                            right_offset_start = cur_offset_start
                            right_offset_stop  = cur_offset_stop
                            right_timestamp    = cur_timestamp
                        elif cur_timestamp<startTimestamp:
                            left_offset_start  = cur_offset_start
                            left_offset_stop   = cur_offset_stop
                            left_timestamp     = cur_timestamp

                    if startOffset is None:
                        startOffset = left_offset_start

                    break

                #=== read objects

                dicts = []

                curOffset = startOffset
                while True:
                    try:
                        (o,curOffset) = oneObject(curOffset)
                    except IndexError:
                        # we have passed the end of the file
                        break
                    if o['timestamp']>endTimestamp:
                        break
                    dicts += [o]

        return dicts

    #===== create value

    def create_value_SOL_TYPE_DUST_NOTIF_EVENT_NETWORKTIME(self,uptime,utcSecs,utcUsecs,asn,asnOffset):
        return self._num_to_list(uptime,4)+      \
               self._num_to_list(utcSecs,4)+     \
               self._num_to_list(utcUsecs,4)+    \
               list(asn)+                        \
               self._num_to_list(asnOffset,2)

    def create_value_SOL_TYPE_DUST_NOTIF_EVENT_NETWORKRESET(self):
        return []

    def create_value_SOL_TYPE_DUST_NOTIF_HR_DEVICE(self,hr):
        '''
        {
            'charge':             0x090a0b0c,    # INT32U
            'queueOcc':           0x0d,          # INT8U
            'temperature':        -1,            # INT8
            'batteryVoltage':     0x0e0f,        # INT16U
            'numTxOk':            0x1011,        # INT16U
            'numTxFail':          0x1213,        # INT16U
            'numRxOk':            0x1415,        # INT16U
            'numRxLost':          0x1617,        # INT16U
            'numMacDropped':      0x18,          # INT8U
            'numTxBad':           0x19,          # INT8U
            'badLinkFrameId':     0x1a,          # INT8U
            'badLinkSlot':        0x1b1c1d1e,    # INT32U
            'badLinkOffset':      0x1f,          # INT8U
        }
        '''

        return_val  = []
        return_val += [struct.pack(
            '>IBbHHHHHBBBIB',
            hr['charge'],         # INT32U  I
            hr['queueOcc'],       # INT8U   B
            hr['temperature'],    # INT8    b
            hr['batteryVoltage'], # INT16U  H
            hr['numTxOk'],        # INT16U  H
            hr['numTxFail'],      # INT16U  H
            hr['numRxOk'],        # INT16U  H
            hr['numRxLost'],      # INT16U  H
            hr['numMacDropped'],  # INT8U   B
            hr['numTxBad'],       # INT8U   B
            hr['badLinkFrameId'], # INT8U   B
            hr['badLinkSlot'],    # INT32U  I
            hr['badLinkOffset'],  # INT8U   B
        )]
        return_val  = ''.join(return_val)
        return_val  = [ord(c) for c in return_val]

        return return_val

    def create_value_SOL_TYPE_DUST_NOTIF_HR_NEIGHBORS(self,hr):
        '''
        {
            'numItems': 2,
            'neighbors': [
                {
                    'neighborId':         0x0102,     # INT16U
                    'neighborFlag':       0x03,       # INT8U
                    'rssi':               -1,         # INT8
                    'numTxPackets':       0x0405,     # INT16U
                    'numTxFailures':      0x0607,     # INT16U
                    'numRxPackets':       0x0809,     # INT16U
                },
                {
                    'neighborId':         0x1112,     # INT16U
                    'neighborFlag':       0x13,       # INT8U
                    'rssi':               -1,         # INT8
                    'numTxPackets':       0x1415,     # INT16U
                    'numTxFailures':      0x1617,     # INT16U
                    'numRxPackets':       0x1819,     # INT16U
                },
            ],
        }
        '''
        return_val  = []
        return_val += [chr(len(hr['neighbors']))] # num_neighbors
        for n in hr['neighbors']:
            return_val += [struct.pack(
                '>HBbHHH',
                n['neighborId'],       # INT16U  H
                n['neighborFlag'],     # INT8U   B
                n['rssi'],             # INT8    b
                n['numTxPackets'],     # INT16U  H
                n['numTxFailures'],    # INT16U  H
                n['numRxPackets'],     # INT16U  H
            )]
        return_val  = ''.join(return_val)
        return_val  = [ord(c) for c in return_val]

        return return_val

    def create_value_SOL_TYPE_DUST_NOTIF_HR_DISCOVERED(self,hr):
        '''
        {
            'numJoinParents': 0x55,              # INT8U
            'numItems':       2,
            'discoveredNeighbors': [
                {
                    'neighborId':     0x0102,    # INT16U
                    'rssi':           -1,        # INT8
                    'numRx':          0x03,      # INT8U
                },
                {
                    'neighborId':     0x1112,    # INT16U
                    'rssi':           -1,        # INT8
                    'numRx':          0x13,      # INT8U
                },
            ],
        }
        '''
        return_val  = []
        return_val += [chr(hr['numJoinParents'])] # numJoinParents
        return_val += [chr(len(hr['discoveredNeighbors']))] # num_neighbors
        for n in hr['discoveredNeighbors']:
            return_val += [struct.pack(
                '>HbB',
                n['neighborId'],       # INT16U  H
                n['rssi'],             # INT8    b
                n['numRx'],            # INT8U   B

            )]
        return_val  = ''.join(return_val)
        return_val  = [ord(c) for c in return_val]

        return return_val

    def create_value_SOL_TYPE_DUST_SNAPSHOT(self,summary):
        '''
        [
            {
                'macAddress':          (0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08),
                'moteId':              0x090a,        # INT16U  H
                'isAP':                0x0b,          # BOOL    B
                'state':               0x0c,          # INT8U   B
                'isRouting':           0x0d,          # BOOL    B
                'numNbrs':             0x0e,          # INT8U   B
                'numGoodNbrs':         0x0f,          # INT8U   B
                'requestedBw':         0x10111213,    # INT32U  I
                'totalNeededBw':       0x14151617,    # INT32U  I
                'assignedBw':          0x18191a1b,    # INT32U  I
                'packetsReceived':     0x1c1d1e1f,    # INT32U  I
                'packetsLost':         0x20212223,    # INT32U  I
                'avgLatency':          0x24252627,    # INT32U  I
                'stateTime':           0x28292a2b,    # INT32U  I
                'paths': [
                    {
                        'dest':        (0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18),
                        'direction':   0x2c,          # INT8U   B
                        'numLinks':    0x2d,          # INT8U   B
                        'quality':     0x2e,          # INT8U   B
                        'rssiSrcDest': -1,            # INT8    b
                        'rssiDestSrc': -2,            # INT8    b
                    },
                    {
                        'dest':        (0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28),
                        'direction':   0x2c,          # INT8U  B
                        'numLinks':    0x2d,          # INT8U  B
                        'quality':     0x2e,          # INT8U  B
                        'rssiSrcDest': -1,            # INT8   b
                        'rssiDestSrc': -2,            # INT8   b
                    },
                ],
            },
            {
                'macAddress':          (0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38),
                'moteId':              0x090a,        # INT16U
                'isAP':                0x0b,          # BOOL
                'state':               0x0c,          # INT8U
                'isRouting':           0x0d,          # BOOL
                'numNbrs':             0x0e,          # INT8U
                'numGoodNbrs':         0x0f,          # INT8U
                'requestedBw':         0x10111213,    # INT32U
                'totalNeededBw':       0x14151617,    # INT32U
                'assignedBw':          0x18191a1b,    # INT32U
                'packetsReceived':     0x1c1d1e1f,    # INT32U
                'packetsLost':         0x20212223,    # INT32U
                'avgLatency':          0x24252627,    # INT32U
                'stateTime':           0x28292a2b,    # INT32U
                'paths': [
                    {
                        'dest':        (0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48),
                        'direction':   0x2c,          # INT8U
                        'numLinks':    0x2d,          # INT8U
                        'quality':     0x2e,          # INT8U
                        'rssiSrcDest': -1,            # INT8
                        'rssiDestSrc': -2,            # INT8
                    },
                ],
            },
        ]
        '''
        return_val  = []
        return_val += [chr(len(summary))] # num_motes
        for m in summary:
            return_val += [''.join([chr(b) for b in m['macAddress']])] # macAddress
            return_val += [struct.pack(
                '>HBBBBBIIIIII',
                m['moteId'],           # INT16U  H
                m['isAP'],             # BOOL    B
                m['state'],            # INT8U   B
                m['isRouting'],        # BOOL    B
                m['numNbrs'],          # INT8U   B
                m['numGoodNbrs'],      # INT8U   B
                m['requestedBw'],      # INT32U  I
                m['totalNeededBw'],    # INT32U  I
                m['assignedBw'],       # INT32U  I
                m['packetsReceived'],  # INT32U  I
                m['packetsLost'],      # INT32U  I
                m['avgLatency'],       # INT32U  I
            )]
            return_val += [chr(len(m['paths']))] # num_paths
            for p in m['paths']:
                return_val += [''.join([chr(b) for b in p['dest']])] # dest
                return_val += [struct.pack(
                    '>BBBbb',
                    p['direction'],    # INT8U   B
                    p['numLinks'],     # INT8U   B
                    p['quality'],      # INT8U   B
                    p['rssiSrcDest'],  # INT8    b
                    p['rssiDestSrc'],  # INT8    b
                )]
        return_val  = ''.join(return_val)
        return_val  = [ord(c) for c in return_val]

        return return_val

    def pack_obj_value(self, type_id, *args):
        '''Create a formated object value
        Args:
            type_id (int): the SOL type ID (see registry.md)
            kwargs (dict): a dictionary of values
        :returns: An list of bytes
        Example:
            create_value(SolDefines.SOL_TYPE_DUST_NOTIF_SOMETHING,
                    srcPort = 61625,
                    dstPort = 61625,
                    payload = [0, 0, 5, 0, 255])
            Will return:
                [240, 185, 240, 185, 0, 0, 5, 0, 255]
        '''
        ret_val = []

        # get SOL type name
        type_name = d.solTypeToString(d,type_id)

        # call corresponding DUST methods
        if type_name.startswith('SOL_TYPE_DUST') and getattr(d,type_name)==type_id:
            if hasattr(self,"create_value_%s" % type_name):
                ret_val = getattr(self,"create_value_%s" % type_name)(*args)
            else:
                # get SOL structure
                sol_item = d.solStructure(d,type_id)

                # change each args to a list if not already a list
                count = 0
                for a in args:
                    count += 1
                    if not isinstance(a, list):
                        size = struct.calcsize(sol_item['structure'][count])
                        item = self._num_to_list(a, size)
                    else:
                        item = a
                    # add list to return value
                    ret_val += item

        else:
            raise NotImplementedError

        return ret_val

    def unpack_obj_value(self, type_id,*payload):
        ''' Parsed the given sensor object value
            Returns parsed value as Dictionary object
        '''
        obj = {}
        type_name = SolDefines.solTypeToString(SolDefines,type_id)

        if type_name.startswith('SOL_TYPE_DUST') and getattr(SolDefines,type_name)==type_id:
            obj = self._parse_specific_DUST(type_id,payload)
        else:
            raise NotImplementedError

            # get SOL structure by type
            sol_item = SolDefines.solStructure(SolDefines,type_id)

            # verify enough bytes
            numBytes = struct.calcsize(sol_item['structure'])

            if len(payload)<numBytes:
                raise ValueError("not enough bytes for %s", type_id)

        return obj

    #======================== private =========================================

    def _backUpUntilStartFrame(self,file_name,curOffset):
        with open(file_name,'rb') as f:
            f.seek(curOffset,os.SEEK_SET)
            while True:
                byte = f.read(1)
                if byte==self.hdlc.HDLC_FLAG:
                    return f.tell()-1
                f.seek(-2,os.SEEK_CUR)

    @staticmethod
    def _num_to_list(num, length):
        output = []
        for l in range(length):
            output = [(num>>8*l)&0xff]+output
        return output

    @staticmethod
    def _list_to_num(l):
        output = 0
        for i in range(len(l)):
            output += l[i]<<(8*(len(l)-i-1))
        return output

    def _parse_specific_DUST(self,type_id,payload):
        '''
        Args:
            type_id (int): The SOL type ID
            payload (array of byte): The data to parse
        Description: Prepare the data and call corresponding DUST parser.
        Returns: a dict element with the parsed data
        Example:
            _parse_specific_DUST(
                    SOL_TYPE_DUST_NOTIF_DATA_RAW,
                    (240, 185, 240, 185, 0, 0, 5, 0, 255, 1, 5, 0, 0, 0, 0, 61, ...)
                )
            output =    {'packet_timestamp': (262572558848, 246301952),
                         'received_timestamp': 1454335765.694352,
                         'raw_data': ...}
        '''
        obj = {}

        # get SOL type
        type_name = SolDefines.solTypeToString(SolDefines,type_id)

        if type_id == SolDefines.SOL_TYPE_DUST_OAP:
            # TODO An OAP parser in the Smartmesh SDK should be used instead

            # convert into byte array (srcPort + destPort = 4 bytes)
            data = array.array('B',payload)

            # first two bytes are transport header
            trans = OAPMessage.extract_oap_header(data[0:2])

            # third byte is the command (GET, PUT, POST, DELETE, NOTIF)
            cmd_type = data[2]

            if trans['response']:
                oap_resp = OAPMessage.parse_oap_response(data, 2)
            elif cmd_type == OAPMessage.CmdType.NOTIF:
                # parse the OAP message into a OAPNotif class
                oap_notif = OAPNotif.parse_oap_notif(data,3)

                # store the parsed message attributes
                obj = oap_notif.__dict__

                # clear value for pymongo (does not accept arrays of bytes)
                obj['raw_data'] = obj['raw_data'].tolist()
                obj['channel'] = obj['channel'].tolist()[0]
                obj['received_timestamp'] = (obj['received_timestamp'] -
                        datetime.datetime(1970, 1, 1)
                    ).total_seconds()

        # Health Reports
        elif type_id == SolDefines.SOL_TYPE_DUST_NOTIF_HR_DEVICE:
            hr = [self.hrParser.HR_ID_DEVICE,len(payload)]+list(payload)
            obj = self.hrParser.parseHr(hr)
        elif type_id == SolDefines.SOL_TYPE_DUST_NOTIF_HR_NEIGHBORS:
            hr = [self.hrParser.HR_ID_NEIGHBORS,len(payload)]+list(payload)
            obj = self.hrParser.parseHr(hr)
        elif type_id == SolDefines.SOL_TYPE_DUST_NOTIF_HR_DISCOVERED:
            hr = [self.hrParser.HR_ID_DISCOVERED,len(payload)]+list(payload)
            obj = self.hrParser.parseHr(hr)

        # Dust Notifs
        elif (  type_name.startswith('SOL_TYPE_DUST_NOTIF_EVENT') and
                getattr(SolDefines,type_name)==type_id ):

            # get SOL structure
            sol_item = SolDefines.solStructure(SolDefines,type_id)

            # unpack payload to dict
            spayload = ''.join(chr( val ) for val in payload)
            values = struct.unpack(sol_item['structure'],spayload)
            obj = dict(zip(sol_item['fields'], values))

        elif (type_id in [
                    SolDefines.SOL_TYPE_DUST_SNAPSHOT,
                    SolDefines.SOL_TYPE_DUST_NOTIF_DATA_RAW
                ]
        ):
            # Return raw object (TODO: parse)
            obj = payload

        else:
            raise ValueError("Sol type "+str(type_id)+" does not exist.")

        return obj


#============================ main ============================================

if __name__=="__main__":
    os.system("py.test -vv -x tests/")
    raw_input("Press Enter to close.")
