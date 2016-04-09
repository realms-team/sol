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

from SmartMeshSDK.ApiDefinition         import IpMgrDefinition
from SmartMeshSDK.IpMgrConnectorMux     import IpMgrConnectorMux
from SmartMeshSDK.protocols.Hr          import HrParser
from SmartMeshSDK.protocols.oap         import OAPMessage, \
                                               OAPNotif

class Sol(object):
    '''
    Sensor Object Library
    '''

    def __init__(self):
        self.fileLock = threading.RLock()
        self.hdlc     = OpenHdlc.OpenHdlc()
        self.hrParser = HrParser.HrParser()
        self.api      = IpMgrDefinition.IpMgrDefinition()
        self.mux      = IpMgrConnectorMux.IpMgrConnectorMux()

    #======================== public ==========================================

    #===== admin

    @property
    def version(self):
        return ver.SOL_VERSION

    #===== "chain" of communication from the Dust manager to the server
    
    def dust_to_json(self, dust_notif, macManager=None, timestamp=None):
        """
        Convert a single Dust serial API notification into a single JSON SOL Object.
        
        :param dict dust_notif: The Dust serial API notification as
            created by the SmartMesh SDK
        :return: A SOL Object in JSON format
        :rtype: dict
        """
        
        # get sol_mac
        if 'macAddress' in dust_notif._asdict():
            sol_mac = getattr(dust_notif,'macAddress')
        else:
            sol_mac = macManager
        
        # get sol_ts
        if timestamp==None:
            sol_ts = time.time()
        else:
            sol_ts = timestamp
        
        # get sol_type and sol_value
        (sol_type,sol_value) = self._get_sol_value(dust_notif)
        
        # create JSON Object
        sol_json = {
            "mac":          sol_mac,
            "timestamp":    sol_ts,
            "type":         sol_type,
            "value":        sol_value,
        }

        return sol_json
    
    def json_to_bin(self, sol_json):
        """
        Convert a list of JSON SOL Objects into a single compound  binary SOL Object.

        :param list sol_json: a list of JSON SOL Objects
        :return: A single compound binary SOL Object
        :rtype: list
        """

        sol_bin = []

        # header
        h     = 0
        h    |= SolDefines.SOL_HDR_V        << SolDefines.SOL_HDR_V_OFFSET
        h    |= SolDefines.SOL_HDR_T_SINGLE << SolDefines.SOL_HDR_T_OFFSET
        h    |= SolDefines.SOL_HDR_M_8BMAC  << SolDefines.SOL_HDR_M_OFFSET
        h    |= SolDefines.SOL_HDR_S_EPOCH  << SolDefines.SOL_HDR_S_OFFSET
        h    |= SolDefines.SOL_HDR_Y_1B     << SolDefines.SOL_HDR_Y_OFFSET

        assert type(sol_json) == list
        if 'length' in sol_json[0]:
            #TODO implement other length field
            h    |= SolDefines.SOL_HDR_L_1B<<SolDefines.SOL_HDR_L_OFFSET
        else:
            h    |= SolDefines.SOL_HDR_L_WK<<SolDefines.SOL_HDR_L_OFFSET

        sol_bin  += [h]

        for obj in sol_json:
            # mac
            sol_bin         += obj['mac']

            # timestamp
            sol_bin         += self._num_to_list(obj['timestamp'],4)

            # type
            sol_bin         += self._num_to_list(obj['type'],1)

            # length
            if 'length' in obj:
                sol_bin     += self._num_to_list(obj['length'],1)

            # value
            sol_bin         += obj['value']

        return sol_bin
    
    def bin_to_http(self, sol_bin):
        """
        Convert a list of binary SOL objects (compound or not) into a JSON string
        to be sent as HTTP payload to the server.
        
        :param list sol_bin: a list of binary SOL Objects
        :return: A JSON string to be sent to the server over HTTP.
        :rtype: string
        """
        
        base64_bin_list = []
        for bin_obj in sol_bin:
            base64_bin_list.append(base64.b64encode("".join(chr(b) for b in bin_obj)))

        content = {
            "v":    SolDefines.SOL_HDR_V,
            "o":    base64_bin_list,
        }

        return json.dumps(content)
    
    def http_to_bin(self, sol_http):
        """
        :param dict sol_http:
        :rtype: list
        """

        sol_bin = []
        json_content = json.loads(sol_http)

        for bin_obj in json_content['o']:
            dec_obj = base64.b64decode(bin_obj)
            for json_obj in self.bin_to_json([ord(b) for b in dec_obj]):
                sol_bin.append(json_obj)

        return sol_bin
    
    def bin_to_json(self, sol_bin, mac=None):
        """
        Converts a binary compound into a list of SOL Objects

        :param list sol_bin: A SOL binary compound
        :return: A list of SOL Objects
        :rtpe: list
        """

        obj_list = []

        # header

        assert len(sol_bin)>=1

        h     = sol_bin[0]
        h_V   = (h>>SolDefines.SOL_HDR_V_OFFSET)&0x03
        assert h_V==SolDefines.SOL_HDR_V
        h_H   = (h>>SolDefines.SOL_HDR_T_OFFSET)&0x01
        assert h_H==SolDefines.SOL_HDR_T_SINGLE
        h_M   = (h>>SolDefines.SOL_HDR_M_OFFSET)&0x01
        h_S   = (h>>SolDefines.SOL_HDR_S_OFFSET)&0x01
        assert h_S==SolDefines.SOL_HDR_S_EPOCH
        h_Y   = (h>>SolDefines.SOL_HDR_Y_OFFSET)&0x01
        assert h_Y==SolDefines.SOL_HDR_Y_1B
        h_L   = (h>>SolDefines.SOL_HDR_L_OFFSET)&0x03

        sol_bin = sol_bin[1:]

        while len(sol_bin) >= 4:
            obj = {}

            # mac

            if h_M==SolDefines.SOL_HDR_M_NOMAC:
                assert mac is not None
                obj['mac'] = mac
            else:
                assert len(sol_bin)>=8
                obj['mac'] = sol_bin[:8]
                sol_bin = sol_bin[8:]

            # timestamp

            assert len(sol_bin)>=4
            obj['timestamp'] = self._list_to_num(sol_bin[:4])
            sol_bin = sol_bin[4:]

            # type

            assert len(sol_bin)>=1
            obj['type'] = sol_bin[0]
            sol_bin = sol_bin[1:]

            # length

            if h_L==SolDefines.SOL_HDR_L_WK:
                sol_item = SolDefines.solStructure(SolDefines,obj['type'])
                obj_size = struct.calcsize(sol_item['structure'])
            elif h_L==SolDefines.SOL_HDR_L_1B:
                obj['length'] = sol_bin[0]
                obj_size = sol_bin[0]
                sol_bin = sol_bin[1:]
            elif h_L==SolDefines.SOL_HDR_L_2B:
                obj['length'] = sol_bin[:2]
                obj_size = sol_bin[:2]
                sol_bin = sol_bin[2:]
            else:
                obj_size = 0    # elided length

            # value
            assert len(sol_bin)>=obj_size
            obj['value'] = sol_bin[:obj_size]
            sol_bin = sol_bin[obj_size:]

            # store object to returned list
            obj_list.append(obj)

        return obj_list
    
    def json_to_influx(self,sol_json):
        """
        Transform list of Sol Objects to list of InfluxDB points
        Args: sol_json (list) list of dictionaries
        Returns: idicts (list) list of converted dictionaries
        Example:
            sol_json = {
                "timestamp" : 1455202067
                "mac" : [ 0, 23, 13, 0, 0, 56, 0, 99 ]
                "type" 14
                "value" : [ 240, 185, 240, 185, 0, 0 ]
            }
        """
        
        idicts = []

        for obj in sol_json:
            iobj = {}

            # get SOL type name
            type_name = SolDefines.solTypeToString(SolDefines,obj['type'])

            # (temporary) only keep DUST types
            if type_name.startswith('SOL_TYPE_DUST') and getattr(SolDefines,type_name)==obj['type']:

                iobj = {
                    # convert timestamp to UTC
                    "time" : datetime.datetime.utcfromtimestamp(obj['timestamp']),

                    # change type name
                    "measurement" : SolDefines.solTypeToString(SolDefines,obj['type']),

                    # tags
                    "tags" : {
                        "mac" : '-'.join(["{0:02x}".format(i) for i in obj['mac']])
                    },

                    # populate fields
                    "fields" : flatdict.FlatDict(obj['value'])
                }

                # append element to list
                idicts.append(iobj)

        return idicts
    
    #===== file manipulation

    def dumpToFile(self, dicts, file_name):

        with self.fileLock:
            with open(file_name,'ab') as f:
                for o_dict in dicts:
                    o_bin = self.json_to_bin([o_dict])
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

            dicts = []
            for b in bins:
                dicts.extend(self.bin_to_json(b))

        else:

            with self.fileLock:

                #=== find startOffset

                while True:

                    startOffset = None

                    def oneObject(offset):
                        (o,idx) = self.hdlc.dehdlcify(file_name,fileOffset=offset,maxNum=1)
                        o = o[0]
                        o = self.bin_to_json(o)[0]
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
    
    def _get_sol_value(self,dust_notif):
        
        notifName = [k for (k,v) in self.mux.notifTupleTable.items() if v==type(dust_notif)][0]
        
        print dust_notif
        print notifName
    
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
        Example ::

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
        Example ::

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
        return_val += [chr(hr['numItems'])] # num_neighbors
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
        Example ::

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
        Example ::

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

        if type_id == SolDefines.SOL_TYPE_DUST_OAP_TEMPSAMPLE:
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

            # quick fix macAddrr parsing
            if "macAddress" in obj:
                mac_str = struct.pack('>Q', obj['macAddress'])
                obj['macAddress'] = [ord(b) for b in mac_str]
            if "dest" in obj:
                mac_str = struct.pack('>Q', obj['dest'])
                obj['dest'] = [ord(b) for b in mac_str]
            if "source" in obj:
                mac_str = struct.pack('>Q', obj['source'])
                obj['source'] = [ord(b) for b in mac_str]
            if "asn" in obj:
                obj['asn'] = [ord(i) for i in obj['asn']]

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
