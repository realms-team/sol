#!/usr/bin/python

# =========================== adjust path =====================================

import sys
import os

here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(here, 'smartmeshsdk', 'libs'))
sys.path.insert(0, os.path.join(here, 'smartmeshsdk', 'external_libs'))

# =========================== imports =========================================

# from default Python
import json
import struct
import base64
import threading
import time
import array
import datetime

# third-party packages
import flatdict

# project-specific
from SmartMeshSDK.utils                 import FormatUtils
from SmartMeshSDK.ApiDefinition         import IpMgrDefinition
from SmartMeshSDK.IpMgrConnectorSerial  import IpMgrConnectorSerial
from SmartMeshSDK.protocols.Hr          import HrParser
from SmartMeshSDK.protocols.oap         import OAPDispatcher, \
                                               OAPMessage,    \
                                               OAPNotif

import SolDefines
import SolVersion as ver
import OpenHdlc

#============================ defines =========================================

#============================ helpers =========================================

#============================ classes =========================================

class Sol(object):
    '''
    Sensor Object Library
    '''

    def __init__(self):
        self.fileLock   = threading.RLock()
        self.hdlc       = OpenHdlc.OpenHdlc()
        self.hrParser   = HrParser.HrParser()
        self.api        = IpMgrDefinition.IpMgrDefinition()
        self.connSerial = IpMgrConnectorSerial.IpMgrConnectorSerial()
        self.oapLock    = threading.RLock()
        self.oap        = OAPDispatcher.OAPDispatcher()
        self.oap.register_notif_handler(self._handle_oap_notif)

    #======================== public ==========================================

    #===== admin

    @property
    def version(self):
        return ver.VERSION

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
        if type(dust_notif) in [
                self.connSerial.Tuple_notifData,
                self.connSerial.Tuple_notifIpData,
                self.connSerial.Tuple_notifHealthReport,
            ]:
            sol_mac = getattr(dust_notif,'macAddress')
        else:
            sol_mac = macManager
        
        # get sol_ts
        if timestamp==None:
            sol_ts = int(time.time()) # timestamp in seconds
        else:
            sol_ts = timestamp
        
        # get sol_type and sol_value
        (sol_type,sol_value) = self._get_sol_json_value(dust_notif)
        
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
        Convert a JSON SOL Object into a single binary SOL Object.

        :param list sol_json: a JSON SOL Object
        :return: A single binary SOL Object
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
        h    |= SolDefines.SOL_HDR_L_ELIDED << SolDefines.SOL_HDR_L_OFFSET
        sol_bin        += [h]

        # mac
        sol_bin        += sol_json['mac']

        # timestamp
        sol_bin        += self._num_to_list(sol_json['timestamp'],4)

        # type
        sol_bin        += self._num_to_list(sol_json['type'],1)

        # value
        if   sol_json['type']==SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS:
            sol_bin    += self._get_sol_binary_value_dust_hr_neighbors(
                sol_json['value']
            )
        elif sol_json['type']==SolDefines.SOL_TYPE_DUST_NOTIF_HRDISCOVERED:
            sol_bin    += self._get_sol_binary_value_dust_hr_discovered(
                sol_json['value']
            )
        else:
            sol_bin    += self._fields_to_binary_with_structure(
                sol_json['type'],
                sol_json['value']
            )
        
        sol_json['value']

        return sol_bin
    
    def bin_to_http(self, sol_binl):
        """
        Convert a list of binary SOL objects (compound or not)
        into a JSON string to be sent as HTTP payload to the server.
        
        :param list sol_binl: a list of binary SOL Objects
        :return: A JSON string to be sent to the server over HTTP.
        :rtype: string
        """
        
        returnVal = {
            "v":    SolDefines.SOL_HDR_V,
            "o":    [base64.b64encode(s) for s in ("".join(chr(b) for b in sol_bin) for sol_bin in sol_binl)]
        }
        
        returnVal = json.dumps(returnVal)
        
        return returnVal
    
    def http_to_bin(self, sol_http):
        """
        Convert the JSON string contained in an HTTP request
        into a list of binary SOL objects (compound or not).
        
        :param string sol_http: JSON string contained in an HTTP request
        :return: list of binary SOL objects (compound or not)
        :rtype: list
        """

        sol_http = json.loads(sol_http)
        
        assert sol_http['v']==SolDefines.SOL_HDR_V
        sol_binl = [[ord(b) for b in base64.b64decode(o)] for o in sol_http['o']]
        
        return sol_binl
    
    def bin_to_json(self, sol_bin, mac=None):
        """
        Convert a binary SOL object into a JSON SOL Object.

        :param list sol_bin: binary SOL object
        :return: JSON SOL Objects
        :rtpe: list
        """
        
        sol_json = {}

        # header

        h     = sol_bin[0]
        h_V   = (h>>SolDefines.SOL_HDR_V_OFFSET)&0x03
        assert h_V==SolDefines.SOL_HDR_V
        h_H   = (h>>SolDefines.SOL_HDR_T_OFFSET)&0x01
        assert h_H==SolDefines.SOL_HDR_T_SINGLE
        h_M   = (h>>SolDefines.SOL_HDR_M_OFFSET)&0x01
        h_S   = (h>>SolDefines.SOL_HDR_S_OFFSET)&0x01
        h_Y   = (h>>SolDefines.SOL_HDR_Y_OFFSET)&0x01
        h_L   = (h>>SolDefines.SOL_HDR_L_OFFSET)&0x03

        sol_bin = sol_bin[1:]
        
        # mac

        if h_M==SolDefines.SOL_HDR_M_NOMAC:
            assert mac is not None
            sol_json['mac']  = mac
        else:
            assert len(sol_bin)>=8
            sol_json['mac']  = sol_bin[:8]
            sol_bin          = sol_bin[8:]
        
        # timestamp
        
        assert h_S==SolDefines.SOL_HDR_S_EPOCH
        assert len(sol_bin)>=4
        sol_json['timestamp'] = self._list_to_num(sol_bin[:4])
        sol_bin = sol_bin[4:]
        
        # type

        assert h_Y==SolDefines.SOL_HDR_Y_1B
        assert len(sol_bin)>=1
        sol_json['type'] = sol_bin[0]
        sol_bin = sol_bin[1:]
        
        # length

        if h_L==SolDefines.SOL_HDR_L_WK:
            sol_item              = SolDefines.solStructure(sol_json['type'])
            obj_size              = struct.calcsize(sol_item['structure'])
        elif h_L==SolDefines.SOL_HDR_L_1B:
            sol_json['length']    = sol_bin[0]
            obj_size              = sol_bin[0]
            sol_bin               = sol_bin[1:]
        elif h_L==SolDefines.SOL_HDR_L_2B:
            sol_json['length']    = sol_bin[:2]
            obj_size              = sol_bin[:2]
            sol_bin               = sol_bin[2:]
        elif h_L==SolDefines.SOL_HDR_L_ELIDED:
            obj_size              = len(sol_bin)

        # value
        assert len(sol_bin)==obj_size
        if   sol_json['type']==SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS:
            sol_json['value'] = self.hrParser.parseHr(
                [self.hrParser.HR_ID_NEIGHBORS,len(sol_bin)]+sol_bin,
            )['Neighbors']['neighbors']
        elif sol_json['type']==SolDefines.SOL_TYPE_DUST_NOTIF_HRDISCOVERED:
            sol_json['value'] = self.hrParser.parseHr(
                [self.hrParser.HR_ID_DISCOVERED,len(sol_bin)]+sol_bin,
            )['Discovered']
        else:
            sol_json['value'] = self._binary_to_fields_with_structure(
                sol_json['type'],
                sol_bin,
            )
        
        return sol_json
    
    def json_to_influxdb(self,sol_json):
        """
        Convert a JSON SOL object into a InfluxDB point
        
        :param list sol_json: JSON SOL object
        :return: InfluxDB point
        :rtpe: list
        """
        
        # fields
        if   sol_json['type']==SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS:
            fields = {}
            for n in sol_json["value"]:
                fields[str(n['neighborId'])] = n
        elif sol_json['type']==SolDefines.SOL_TYPE_DUST_NOTIF_HRDISCOVERED:
            fields = sol_json["value"]
        else:
            fields = sol_json["value"]
            for (k,v) in fields.items():
                if type(v)==list:
                    fields[k] = FormatUtils.formatBuffer(v)
        f = flatdict.FlatDict(fields)
        fields = {}
        for (k,v) in f.items():
            fields[k] = v
        
        sol_influxdb = {
            "timestamp"  : sol_json["timestamp"],
            "tag"        : {
                'mac'    : FormatUtils.formatBuffer(sol_json["mac"]),
            },
            "measurement": SolDefines.solTypeToTypeName(SolDefines,sol_json['type']),
            "fields"     : fields,
        }
        
        return sol_influxdb

    #===== file manipulation

    def dumpToFile(self, sol_jsonl, file_name):

        with self.fileLock:
            with open(file_name,'ab') as f:
                for sol_json in sol_jsonl:
                    sol_bin = self.json_to_bin(sol_json)
                    sol_bin = self.hdlc.hdlcify(sol_bin)
                    sol_bin = ''.join([chr(b) for b in sol_bin])
                    f.write(sol_bin)

    def loadFromFile(self,file_name,startTimestamp=None,endTimestamp=None):

        if startTimestamp is not None or endTimestamp is not None:
            assert startTimestamp is not None and endTimestamp is not None

        if startTimestamp is None:
            # retrieve all data

            with self.fileLock:
                (bins,_) = self.hdlc.dehdlcify(file_name)

            sol_jsonl = []
            for b in bins:
                sol_jsonl += [self.bin_to_json(b)]

        else:

            with self.fileLock:

                #=== find startOffset

                while True:

                    startOffset = None

                    def oneObject(offset):
                        (sol,offs) = self.hdlc.dehdlcify(file_name,fileOffset=offset,maxNum=1)
                        sol = sol[0]
                        sol = self.bin_to_json(sol)
                        return (sol, offs)

                    def oneTimestamp(offset):
                        (osol,offs) = oneObject(offset)
                        return (osol['timestamp'], offs)

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
                        right_offset_start = self._fileBackUpUntilStartFrame(file_name,right_offset_start)
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

                sol_jsonl = []

                curOffset = startOffset
                while True:
                    try:
                        (o,curOffset) = oneObject(curOffset)
                    except IndexError:
                        # we have passed the end of the file
                        break
                    if o['timestamp']>endTimestamp:
                        break
                    sol_jsonl += [o]

        return sol_jsonl
    
    #======================== private =========================================
    
    #===== create value (generic code)
    
    def _get_sol_json_value(self,dust_notif):
        
        sol_type   = None
        sol_value  = None
        
        if   type(dust_notif)==self.connSerial.Tuple_notifData:
            (sol_type,sol_value) = self._get_sol_json_value_dust_notifData(dust_notif)
        elif type(dust_notif)==self.connSerial.Tuple_notifHealthReport:
            (sol_type,sol_value) = self._get_sol_json_value_dust_hr(dust_notif)
        else:
            (sol_type,sol_value) = self._get_sol_json_value_generic(dust_notif)
        
        if (sol_type==None or sol_value==None):
            raise NotImplementedError()
        
        return (sol_type,sol_value)
    
    def _get_sol_json_value_generic(self,dust_notif):
        sol_typeName    = self._dust_notifName_to_sol_typeName(str(type(dust_notif)))
        sol_type        = getattr(SolDefines,sol_typeName)
        sol_value       = self._fields_to_json_with_structure(
            sol_type,
            dust_notif._asdict(),
        )
        
        return (sol_type,sol_value)
    
    def _dust_notifName_to_sol_typeName(self,notifName):
        n = notifName.split('.')[-1][:-2]
        assert n.startswith('Tuple_')
        n = n[len('Tuple_'):]
        n = n.upper()
        n = 'SOL_TYPE_DUST_{0}'.format(n)
        return n
        
    def _fields_to_json_with_structure(self,sol_type,fields):
        
        sol_struct          = SolDefines.solStructure(sol_type)
        
        returnVal       = {}
        for name in sol_struct['fields']:
            returnVal[name] = fields[name]
        if 'extrafields' in sol_struct:
            returnVal[sol_struct['extrafields']] = fields[sol_struct['extrafields']]
        
        for (k,v) in returnVal.items():
            if type(v)==tuple:
                returnVal[k] = [b for b in v]
        
        return returnVal
    
    def _fields_to_binary_with_structure(self,sol_type,fields):
        
        sol_struct      = SolDefines.solStructure(sol_type)
        
        
        pack_format     = sol_struct['structure']
        pack_values     = [fields[name] for name in sol_struct['fields']]
        
        # convert [0x01,0x02,0x03] into 0x010203 to be packable
        for i in range(len(pack_values)):
            if type(pack_values[i])==list:
                pack_values[i] = self._list_to_num(pack_values[i])
        
        returnVal       = [ord(b) for b in struct.pack(pack_format,*pack_values)]
        if 'extrafields' in sol_struct:
            returnVal  += fields[sol_struct['extrafields']]
        
        return returnVal
    
    def _binary_to_fields_with_structure(self,sol_type,binary):
        
        sol_struct      = SolDefines.solStructure(sol_type)
        
        pack_format     = sol_struct['structure']
        pack_length     = struct.calcsize(pack_format)
        
        t = struct.unpack(pack_format,''.join(chr(b) for b in binary[:pack_length]))
        
        returnVal = {}
        for (k,v) in zip(sol_struct['fields'],t):
            returnVal[k]= v
        
        if 'extrafields' in sol_struct:
            returnVal[sol_struct['extrafields']] = binary[pack_length:]
        
        for (k,v) in returnVal.items():
            if k in ['macAddress','source','dest']:
                returnVal[k] = self._num_to_list(v,8)
        
        return returnVal
    
    #===== create value (specific)
    
    def _get_sol_json_value_dust_notifData(self,dust_notif):
        
        sol_type   = None
        sol_value  = None
        
        if getattr(dust_notif,'dstPort')==OAPMessage.OAP_PORT:
            (sol_type,sol_value) = self._get_sol_json_value_OAP(dust_notif)
        
        if sol_type==None and sol_value==None:
            sol_type    = SolDefines.SOL_TYPE_DUST_NOTIFDATA
            sol_value   = self._fields_to_json_with_structure(
                SolDefines.SOL_TYPE_DUST_NOTIFDATA,
                dust_notif._asdict(),
            )
        
        return (sol_type,sol_value)
    
    def _get_sol_json_value_OAP(self,dust_notif):
        sol_type   = None
        sol_value  = None
        with self.oapLock:
            self.oap_mac   = None
            self.oap_notif = None
            self.oap.dispatch_pkt(
                self.connSerial.NOTIFDATA,
                dust_notif
            )
            if self.oap_mac!=None and self.oap_notif!=None:
                if type(self.oap_notif)==OAPNotif.OAPTempSample:
                    sol_type  = SolDefines.SOL_TYPE_DUST_OAP_TEMPSAMPLE
                    sol_value = self._fields_to_json_with_structure(
                        SolDefines.SOL_TYPE_DUST_OAP_TEMPSAMPLE,
                        {
                            'temperature': self.oap_notif.samples[0],
                        },
                    )
        
        return (sol_type,sol_value)
    
    def _handle_oap_notif(self,mac,notif):
        self.oap_mac    = mac
        self.oap_notif  = notif
    
    def _get_sol_json_value_dust_hr(self,dust_notif):
        hr = self.hrParser.parseHr(dust_notif.payload)
        sol_type   = None
        sol_value  = None
        if 'Device' in hr:
            assert 'Neighbors'  not in hr
            assert 'Discovered' not in hr
            sol_type    = SolDefines.SOL_TYPE_DUST_NOTIF_HRDEVICE
            sol_value   = self._fields_to_json_with_structure(
                SolDefines.SOL_TYPE_DUST_NOTIF_HRDEVICE,
                hr['Device'],
            )
        if 'Neighbors' in hr:
            assert 'Device'  not in hr
            assert 'Discovered' not in hr
            sol_type    = SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS
            sol_value   = hr['Neighbors']['neighbors']
        if 'Discovered' in hr:
            assert 'Device'  not in hr
            assert 'Neighbors' not in hr
            sol_type    = SolDefines.SOL_TYPE_DUST_NOTIF_HRDISCOVERED
            sol_value   = hr['Discovered']
        return (sol_type,sol_value)
    
    def _get_sol_binary_value_dust_hr_neighbors(self,hr):
        return_val  = []
        return_val += [chr(len(hr))] # num_neighbors
        for n in hr:
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

    def _get_sol_binary_value_dust_hr_discovered(self,hr):
        return_val  = []
        return_val += [chr(hr['numJoinParents'])]
        return_val += [chr(hr['numItems'])]
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
    
    #===== file manipulation

    def _fileBackUpUntilStartFrame(self,file_name,curOffset):
        with open(file_name,'rb') as f:
            f.seek(curOffset,os.SEEK_SET)
            while True:
                byte = f.read(1)
                if byte==self.hdlc.HDLC_FLAG:
                    return f.tell()-1
                f.seek(-2,os.SEEK_CUR)
    
    #===== miscellaneous
    
    @staticmethod
    def _num_to_list(num, length):
        output = []
        for l in range(length):
            output = [int((num>>8*l)&0xff)]+output
        return output

    @staticmethod
    def _list_to_num(l):
        output = 0
        for i in range(len(l)):
            output += l[i]<<(8*(len(l)-i-1))
        return output

''' TO BE REMOVED
    def _parse_specific_DUST(self,type_id,payload):
        obj = {}

        # get SOL type
        type_name = SolDefines.solTypeToTypeName(SolDefines,type_id)

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
        elif type_id == SolDefines.SOL_TYPE_DUST_NOTIF_HRDEVICE:
            hr = [self.hrParser.HR_ID_DEVICE,len(payload)]+list(payload)
            obj = self.hrParser.parseHr(hr)
        elif type_id == SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS:
            hr = [self.hrParser.HR_ID_NEIGHBORS,len(payload)]+list(payload)
            obj = self.hrParser.parseHr(hr)
        elif type_id == SolDefines.SOL_TYPE_DUST_NOTIF_HRDISCOVERED:
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
                    SolDefines.SOL_TYPE_DUST_NOTIFDATA
                ]
        ):
            # Return raw object (TODO: parse)
            obj = payload

        else:
            raise ValueError("Sol type "+str(type_id)+" does not exist.")

        return obj
'''

#============================ main ============================================

if __name__=="__main__":
    os.system("py.test -vv -x tests/")
    raw_input("Press Enter to close.")
