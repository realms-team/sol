#!/usr/bin/python

# =========================== adjust path =====================================

import sys
import os

here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(here, '..', '..', 'smartmeshsdk', 'libs'))

# =========================== imports =========================================

# from default Python
import json
import struct
import base64
import threading
import time
import copy
import logging
import ast

# third-party packages
import flatdict

# project-specific
from SmartMeshSDK.utils                 import FormatUtils
from SmartMeshSDK.protocols.Hr          import HrParser
from SmartMeshSDK.protocols.oap         import OAPMessage

import SolDefines
from SolVersion import VERSION
import OpenHdlc

# =========================== logging =========================================

log = logging.getLogger(__name__)

# =========================== helpers =========================================

# =========================== classes =========================================

class SolDuplicateOapNotificationException(Exception):
    pass

class Sol(object):
    """
    Sensor Object Library
    """

    def __init__(self):
        self.fileLock   = threading.RLock()
        self.hdlc       = OpenHdlc.OpenHdlc()
        self.hrParser   = HrParser.HrParser()

    # ======================= public ==========================================

    # ==== admin

    @property
    def version(self):
        return VERSION

    # ==== "chain" of communication from the Dust manager to the server

    def dust_to_json(self, dust_notif, mac_manager=None, timestamp=None):
        """
        Convert a single Dust serial API notification into a list of JSON SOL Object.

        :param dict dust_notif: The Dust serial API notification as
            a json object created by the JsonServer application
        :param list mac_manager: A list of byte containing the MAC address of the manager
        :param int timestamp: the Unix epoch of the message creation in seconds (UTC)
        :return: A list of SOL Object in JSON format
        :rtype: list
        """

        notif_list  = self._split_dust_notif(dust_notif)
        sol_jsonl   = []

        for d_n in notif_list:
            # get sol_mac
            if d_n['name'] in [
                    'notifData',
                    'notifIpData',
                ]:
                sol_mac = d_n['fields']['macAddress']
            elif d_n['name'] in [
                    'hr', 'oap',
                ]:
                sol_mac = d_n['mac']
            else:
                sol_mac = mac_manager

            # get sol_type and sol_value
            try:
                (sol_type, sol_ts, sol_value) = self._dust_notif_to_sol_json(d_n)
            except SolDuplicateOapNotificationException:
                continue

            # get sol_ts
            if   sol_ts:
                pass # _dust_notif_to_sol_json() returned the ts (sol object with EPOCH ts)
            elif timestamp is None:
                sol_ts = int(time.time())  # timestamp in seconds
            else:
                sol_ts = timestamp

            # create JSON Object
            sol_json = {
                "mac":          sol_mac,
                "timestamp":    sol_ts,
                "type":         sol_type,
                "value":        sol_value,
            }
            sol_jsonl.append(sol_json)

        return sol_jsonl

    def json_to_bin(self, sol_json):
        """
        Convert a JSON SOL Object into a single binary SOL Object.

        :param dict sol_json: a JSON SOL Object
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
        if isinstance(sol_json['mac'], basestring):
            sol_bin += FormatUtils.format_mac_string_to_bytes(sol_json['mac'])
        else:
            sol_bin += sol_json['mac']

        # timestamp
        sol_bin        += _num_to_list(sol_json['timestamp'], 4)

        # type
        sol_bin        += _num_to_list(sol_json['type'], 1)

        # value
        if   sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS:
            sol_bin    += self._get_sol_binary_value_dust_hr_neighbors(
                sol_json['value']
            )
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HRDISCOVERED:
            sol_bin    += self._get_sol_binary_value_dust_hr_discovered(
                sol_json['value']
            )
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HREXTENDED:
            sol_bin    += self._get_sol_binary_value_dust_hr_extended(
                sol_json['value']
            )
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_SNAPSHOT:
            sol_bin    += self._get_sol_binary_value_snapshot(
                sol_json['value']
            )
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_SNAPSHOT_2:
            sol_bin    += [ord(c) for c in str(sol_json['value'])]
        else:
            sol_bin    += self._fields_to_binary_with_structure(
                sol_json['type'],
                sol_json['value']
            )

        return sol_bin

    def bin_to_http(self, sol_binl):
        """
        Convert a list of binary SOL objects (compound or not)
        into a JSON string to be sent as HTTP payload to the server.

        :param list sol_binl: a list of binary SOL Objects
        :return: A JSON string to be sent to the server over HTTP.
        :rtype: string
        """

        try:
            return_val = {
                "v":    SolDefines.SOL_HDR_V,
                "o":    [base64.b64encode(s) for s in ("".join(chr(b) for b in sol_bin) for sol_bin in sol_binl)]
            }
        except:
            print sol_binl
            raise

        return_val = json.dumps(return_val)

        return return_val

    def http_to_bin(self, sol_http):
        """
        Convert the JSON string contained in an HTTP request
        into a list of binary SOL objects (compound or not).

        :param string sol_http: JSON string contained in an HTTP request
        :return: list of binary SOL objects (compound or not)
        :rtype: list
        """

        sol_http = json.loads(sol_http)

        assert sol_http['v'] == SolDefines.SOL_HDR_V
        sol_binl = [[ord(b) for b in base64.b64decode(o)] for o in sol_http['o']]

        return sol_binl

    def bin_to_json(self, sol_bin, mac=None):
        """
        Convert a binary SOL object into a JSON SOL Object.

        :param list sol_bin: binary SOL object
        :param list mac: A list of byte containing the MAC address of the that created the object
        :return: JSON SOL Objects
        :rtpe: list
        """

        sol_json = {}

        # header

        h     = sol_bin[0]
        h_V   = (h >> SolDefines.SOL_HDR_V_OFFSET) & 0x03
        assert h_V == SolDefines.SOL_HDR_V
        h_H   = (h >> SolDefines.SOL_HDR_T_OFFSET) & 0x01
        assert h_H == SolDefines.SOL_HDR_T_SINGLE
        h_M   = (h >> SolDefines.SOL_HDR_M_OFFSET) & 0x01
        h_S   = (h >> SolDefines.SOL_HDR_S_OFFSET) & 0x01
        h_Y   = (h >> SolDefines.SOL_HDR_Y_OFFSET) & 0x01
        h_L   = (h >> SolDefines.SOL_HDR_L_OFFSET) & 0x03

        sol_bin = sol_bin[1:]

        # mac

        if h_M == SolDefines.SOL_HDR_M_NOMAC:
            assert mac is not None
            sol_json['mac']  = FormatUtils.formatBuffer(mac)
        else:
            assert len(sol_bin) >= 8
            sol_json['mac']  = FormatUtils.formatBuffer(sol_bin[:8])
            sol_bin          = sol_bin[8:]

        # timestamp

        assert h_S == SolDefines.SOL_HDR_S_EPOCH
        assert len(sol_bin) >= 4
        sol_json['timestamp'] = _list_to_num(sol_bin[:4])
        sol_bin = sol_bin[4:]

        # type

        assert h_Y == SolDefines.SOL_HDR_Y_1B
        sol_json['type'] = sol_bin[0]
        sol_bin = sol_bin[1:]

        # length

        if h_L == SolDefines.SOL_HDR_L_WK:
            sol_item              = SolDefines.solStructure(sol_json['type'])
            obj_size              = struct.calcsize(sol_item['structure'])
        elif h_L == SolDefines.SOL_HDR_L_1B:
            sol_json['length']    = sol_bin[0]
            obj_size              = sol_bin[0]
            sol_bin               = sol_bin[1:]
        elif h_L == SolDefines.SOL_HDR_L_2B:
            sol_json['length']    = sol_bin[:2]
            obj_size              = sol_bin[:2]
            sol_bin               = sol_bin[2:]
        elif h_L == SolDefines.SOL_HDR_L_ELIDED:
            obj_size              = len(sol_bin)

        # value
        assert len(sol_bin) == obj_size
        if   sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS:
            sol_json['value'] = self.hrParser.parseHr(
                [self.hrParser.HR_ID_NEIGHBORS, len(sol_bin)]+sol_bin,
            )['Neighbors']
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HRDISCOVERED:
            sol_json['value'] = self.hrParser.parseHr(
                [self.hrParser.HR_ID_DISCOVERED, len(sol_bin)]+sol_bin,
            )['Discovered']
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HREXTENDED:
            sol_json['value'] = self.hrParser.parseHr(
                [self.hrParser.HR_ID_EXTENDED, len(sol_bin)]+sol_bin,
            )['Extended']
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_SNAPSHOT:
            sol_json['value'] = self._binary_to_fields_snapshot(sol_bin)
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_SNAPSHOT_2:
            value_str = "".join([chr(b) for b in sol_bin])
            value_eval = ast.literal_eval(value_str)
            sol_json['value'] = json.loads(json.dumps(value_eval))
        else:
            sol_json['value'] = self._binary_to_fields_with_structure(
                sol_json['type'],
                sol_bin,
            )

        return sol_json

    def json_to_influxdb(self, sol_json, tags):
        """
        Convert a JSON SOL object into a InfluxDB point

        :param list sol_json: JSON SOL object
        :param dict tags: A dictionary of tags
        :return: InfluxDB point
        :rtpe: list
        """
        # tags
        obj_tags = copy.deepcopy(tags)

        # fields
        if   sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS:
            fields = {}
            for n in sol_json["value"]['neighbors']:
                fields["neighbors:" + str(n['neighborId'])] = n
            fields['numItems'] = sol_json["value"]['numItems']
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HRDISCOVERED:
            fields = sol_json["value"]
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_NOTIF_HREXTENDED:
            fields = {}
            for item, value in enumerate(sol_json["value"]['RSSI']):
                fields[str(item + 11)] = value # 11 is the first channel number
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_SNAPSHOT:
            fields = {"mote": []}
            for mote in sol_json["value"]:
                mote["macAddress"] = FormatUtils.formatBuffer(mote["macAddress"])
                for path in mote["paths"]:
                    path["macAddress"] = FormatUtils.formatBuffer(path["macAddress"])
                fields["mote"].append(mote)
        elif sol_json['type'] == SolDefines.SOL_TYPE_DUST_EVENTNETWORKRESET:
            fields = {'value': 'dummy'}
        else:
            fields = sol_json["value"]
            for (k, v) in fields.items():
                if type(v) == list:  # mac
                    if k in ['macAddress', 'source', 'dest']:
                        fields[k] = FormatUtils.formatBuffer(v)
                    elif k in ['sol_version', 'sdk_version', 'solmanager_version']:
                        fields[k] = ".".join(str(i) for i in v)

        f = flatdict.FlatDict(fields)
        fields = {}
        for (k, v) in f.items():
            fields[k] = v

        # add additionnal field or tag if apply_function exists
        try:
            obj_struct = SolDefines.solStructure(sol_json['type'])
            if 'apply' in obj_struct:
                for ap in obj_struct['apply']:
                    arg_list = [fields[arg] for arg in ap["args"]]
                    if "field" in ap:
                        fields[ap["field"]] = ap["function"](*arg_list)
                    if "tag" in ap:
                        obj_tags[ap["tag"]] = ap["function"](*arg_list)
        except ValueError:
            pass

        # get SOL type
        measurement = SolDefines.solTypeToTypeName(SolDefines, sol_json['type'])

        # convert SOL timestamp to UTC
        utc_time = sol_json["timestamp"]*1000000000

        sol_influxdb = {
                "time"          : utc_time,
                "tags"          : obj_tags,
                "measurement"   : measurement,
                "fields"        : fields,
                }

        return sol_influxdb

    def influxdb_to_json(self, sol_influxdb):
        """
        Converts an Influxdb query reply into a list of dicts.

        :param dict sol_influxdb: the result of a database query (sush as SELECT * FROM)
        :return: a list of JSON SOL objects
        :rtype: list

        """

        # verify influxdb data
        if not ("series" in sol_influxdb):
            raise ValueError("Influxdb data not recognized")

        # init
        json_list = []

        # remove unused headers
        for serie in sol_influxdb["series"]:
            for val in serie['values']:
                # convert to dict
                d_influxdb = dict(zip(serie['columns'], val))

                # unflat dict
                obj_value = flatdict.FlatDict(d_influxdb).as_dict()

                # parse specific HR_NEIGHBORS
                hr_nghb_name    = SolDefines.solTypeToTypeName(
                                    SolDefines,
                                    SolDefines.SOL_TYPE_DUST_NOTIF_HRNEIGHBORS)
                if serie['name'] == hr_nghb_name:
                    for i in range(0, len(obj_value["neighbors"])+1):
                        ngbr_id = str(i)

                        # new HR_NGBR parsing
                        if ngbr_id in obj_value["neighbors"]:
                            if obj_value["neighbors"][ngbr_id]["neighborFlag"] is None:
                                del obj_value["neighbors"][ngbr_id]

                        # old HR_NGBR parsing
                        if ngbr_id in obj_value:
                            if obj_value[ngbr_id]["neighborFlag"] is not None:
                                obj_value["neighbors"][ngbr_id] = obj_value[ngbr_id]
                            del obj_value[ngbr_id]

                # time is not passed in the "value" field
                del obj_value["time"]

                # create final dict
                jdic = {
                        'type'      : serie['name'],
                        'mac'       : serie['tags']['mac'],
                        'value'     : obj_value,
                        'timestamp' : d_influxdb['time'],
                        }
                json_list.append(jdic)
        return json_list

    # ==== file manipulation

    def dumpToFile(self, sol_jsonl, file_name):

        with self.fileLock:
            with open(file_name, 'ab') as f:
                for sol_json in sol_jsonl:
                    sol_bin = self.json_to_bin(sol_json)
                    sol_bin = self.hdlc.hdlcify(sol_bin)
                    sol_bin = ''.join([chr(b) for b in sol_bin])
                    f.write(sol_bin)

    def loadFromFile(self, file_name, start_timestamp=None, end_timestamp=None):

        if start_timestamp is not None or end_timestamp is not None:
            assert start_timestamp is not None and end_timestamp is not None

        if start_timestamp is None:
            # retrieve all data

            with self.fileLock:
                (bins, _) = self.hdlc.dehdlcify(file_name)

            sol_jsonl = []
            for b in bins:
                sol_jsonl += [self.bin_to_json(b)]

        else:

            with self.fileLock:

                #=== find start_offset

                while True:

                    start_offset = None

                    def one_object(offset):
                        (sol, offs) = self.hdlc.dehdlcify(file_name, fileOffset=offset, maxNum=1)
                        sol = sol[0]
                        sol = self.bin_to_json(sol)
                        return sol, offs

                    def oneTimestamp(offset):
                        (osol, offs) = one_object(offset)
                        return osol['timestamp'], offs

                    #=== get boundaries

                    left_offset_start = 0
                    try:
                        (left_timestamp, left_offset_stop) = oneTimestamp(left_offset_start)
                    except IndexError:
                        # complete file is corrupted
                        return []
                    with open(file_name, 'rb') as f:
                        f.seek(0, os.SEEK_END)
                        right_offset_start = f.tell()
                    while True:
                        right_offset_start = self._fileBackUpUntilStartFrame(file_name, right_offset_start)
                        try:
                            (right_timestamp, right_offset_stop) = oneTimestamp(right_offset_start)
                        except IndexError:
                            right_offset_start -= 1
                        else:
                            break

                    if left_timestamp > start_timestamp:
                        start_offset = left_timestamp
                        break
                    if right_timestamp < start_timestamp:
                        start_offset = right_timestamp
                        break

                    #=== binary search

                    while left_offset_stop < right_offset_start-1:

                        cur_offset_start = int((right_offset_start-left_offset_start)/2+left_offset_start)
                        (cur_timestamp, cur_offset_stop) = oneTimestamp(cur_offset_start)

                        if cur_timestamp == start_timestamp:
                            start_offset = cur_offset_start
                            break
                        elif cur_timestamp > start_timestamp:
                            right_offset_start = cur_offset_start
                        elif cur_timestamp < start_timestamp:
                            left_offset_start  = cur_offset_start
                            left_offset_stop   = cur_offset_stop

                    if start_offset is None:
                        start_offset = left_offset_start

                    break

                #=== read objects

                sol_jsonl = []

                curOffset = start_offset
                while True:
                    try:
                        (o, curOffset) = one_object(curOffset)
                    except IndexError:
                        # we have passed the end of the file
                        break
                    if o['timestamp'] > end_timestamp:
                        break
                    sol_jsonl += [o]

        return sol_jsonl

    # ======================= private =========================================

    def _split_dust_notif(self, dust_notif):
        """
        Split a single Dust serial API notification into a list of Dust notifications
        :param dict dust_notif: The Dust serial API notification as
                                created by the SmartMesh SDK
        :return: A list of Dust notifications
        :rtype: list
        """
        notif_list = []

        if (dust_notif['name'] == 'notifData') and (dust_notif['fields']['dstPort'] == SolDefines.SOL_PORT):
            # OAP: split if multi-MTTLV structure

            # parse header
            sol_header  = dust_notif['fields']['data'][0]
            header_V    = sol_header >> SolDefines.SOL_HDR_V_OFFSET & 0x03
            header_T    = sol_header >> SolDefines.SOL_HDR_T_OFFSET & 0x01
            header_S    = sol_header >> SolDefines.SOL_HDR_S_OFFSET & 0x01
            header_Y    = sol_header >> SolDefines.SOL_HDR_Y_OFFSET & 0x01
            header_L    = sol_header >> SolDefines.SOL_HDR_L_OFFSET & 0x03

            if header_T == 0:
                # single SOL object

                notif_list = [dust_notif]
            else:
                # multiple SOL objects

                # reset header Type bit
                sol_header = dust_notif['fields']['data'][0] & 0xdf

                # get structure size
                solheader_size  = SolDefines.SOL_HEADER_SIZE
                ts_size         = SolDefines.SOL_TIMESTAMP_SIZE
                objnum_size     = SolDefines.SOL_OBJNUMBER_SIZE

                # get time
                ts_sec  = 0
                ts_usec = 0
                ts_offset = 0
                if header_S == 0: # timestamp from smip header
                    ts_sec  = dust_notif['fields']['data'][0:ts_size]
                    ts_usec = 0
                    ts_offset = ts_size
                else: # timestamp from dust notif
                    ts_sec  = dust_notif['fields']['utcSecs']
                    ts_user = dust_notif['fields']['utcUsecs']

                # get number of objects
                obj_number  = dust_notif['fields']['data'][ts_offset+objnum_size]

                curr_ptr    = solheader_size + ts_offset + objnum_size
                for i in range(0,obj_number):
                    obj_type    = dust_notif['fields']['data'][curr_ptr]
                    sol_item    = SolDefines.solStructure(obj_type)
                    obj_size    = struct.calcsize(sol_item['structure'])
                    notif_list += [
                        {
                            'manager': dust_notif['manager'],
                            'name':    dust_notif['name'],
                            'fields': {
                                'macAddress': dust_notif['fields']['macAddress'],
                                'utcSecs': dust_notif['fields']['utcSecs'],
                                'utcUsecs': dust_notif['fields']['utcUsecs'],
                                'srcPort': dust_notif['fields']['srcPort'],
                                'dstPort': dust_notif['fields']['dstPort'],
                                # data = solheader + timestamp + object
                                'data': [sol_header]+
                                    dust_notif['fields']['data'][solheader_size:solheader_size+ts_offset] +
                                    dust_notif['fields']['data'][curr_ptr:curr_ptr+obj_size+1]
                            },
                        },
                    ]
                    curr_ptr   += obj_size+1

        elif dust_notif['name'] == 'hr':
            hr_type_list = ['Device', 'Discovered', 'Neighbors', 'Extended']
            notif_keys =  dust_notif['hr'].keys()
            for hrName in notif_keys:
                assert hrName in hr_type_list
            for hrName in notif_keys:
                dust_notif_copy = copy.deepcopy(dust_notif)
                for hr_type in [t for t in notif_keys if t != hrName]:
                    del dust_notif_copy['hr'][hr_type]
                notif_list += [dust_notif_copy]
        else:
            notif_list += [dust_notif]

        return notif_list

    # ==== dust notif to sol json

    def _dust_notif_to_sol_json(self, dust_notif):

        sol_ts = None

        if   dust_notif['name'] == 'notifData':
            (sol_type, sol_ts, sol_value) = self._dust_notifData_to_sol_json(dust_notif)
        elif dust_notif['name'] == 'hr':
            (sol_type, sol_value) = self._dust_hr_to_sol_json(dust_notif)
        elif dust_notif['name'] == 'oap':
            (sol_type, sol_value) = self._dust_oap_to_sol_json(dust_notif)
        elif dust_notif['name'] == 'snapshot':
            sol_type = SolDefines.SOL_TYPE_DUST_SNAPSHOT_2
            sol_value = dust_notif
        else:
            (sol_type, sol_value) = self._dust_other_notif_to_sol_json(dust_notif)

        return (sol_type, sol_ts, sol_value)

    # notifData

    def _dust_notifData_to_sol_json(self, dust_notif):

        sol_type   = None
        sol_ts     = None
        sol_value  = None

        if   dust_notif['fields']['dstPort'] == OAPMessage.OAP_PORT:
            # notifData contains OAP message

            # this notification will already appear as an oap notification
            raise SolDuplicateOapNotificationException()
        elif dust_notif['fields']['dstPort'] == SolDefines.SOL_PORT:
            # notifData contains SOL message

            (sol_type, sol_ts, sol_value) = self._dust_notifData_with_sol_to_sol_json(dust_notif)
        else:
            # notifData contains does NOT contain neither OAP nor SOL

            sol_type    = SolDefines.SOL_TYPE_DUST_NOTIFDATA
            sol_value   = copy.deepcopy(dust_notif['fields'])
            del(sol_value['macAddress'])
            del(sol_value['utcSecs'])
            del(sol_value['utcUsecs'])

        return (sol_type, sol_ts, sol_value)

    def _dust_notifData_with_sol_to_sol_json(self, dust_notif):
        """
        Turn a notifData dust notification which contains SOL objects
           (SOL_header + timestamp + SOL_object)
        into a dictionnary

        :return: (sol_type, sol_ts, sol_value)
        :rtype: tuple(int, int, int)
        """
        sol_ts          = None
        # check for timestamp flag in SOL_HEADER
        header_offset   = SolDefines.SOL_HEADER_OFFSET
        ts_offset       = SolDefines.SOL_TIMESTAMP_OFFSET
        header_S        = dust_notif['fields']['data'][0] >> SolDefines.SOL_HDR_S_OFFSET & SolDefines.SOL_HDR_S_SIZE
        if header_S == SolDefines.SOL_HDR_S_EPOCH:
            ts = list(dust_notif['fields']['data'][ts_offset:ts_offset+SolDefines.SOL_TIMESTAMP_SIZE])
            ts.reverse()
            #sol_ts      = Sol._list_to_num(ts)
            type_index  = SolDefines.SOL_HEADER_SIZE + SolDefines.SOL_TIMESTAMP_SIZE
        else:
            type_index  = SolDefines.SOL_HEADER_SIZE

        sol_type    = dust_notif['fields']['data'][type_index]
        sol_value   = self._binary_to_fields_with_structure(
            dust_notif['fields']['data'][type_index],
            dust_notif['fields']['data'][type_index+1:],
        )
        return (sol_type, sol_ts, sol_value)

    # hr

    def _dust_hr_to_sol_json(self, dust_notif):
        sol_type   = None
        sol_value  = None
        hr_type_list = ['Device', 'Discovered', 'Neighbors', 'Extended']
        for hr_type in hr_type_list:
            if hr_type in dust_notif['hr']:
                assert dust_notif['hr'].keys() == [hr_type]
                sol_type = getattr(SolDefines, "SOL_TYPE_DUST_NOTIF_HR{0}".format(hr_type.upper()))
                sol_value = dust_notif['hr'][hr_type]
        return (sol_type, sol_value)

    # oap

    def _dust_oap_to_sol_json(self, dust_notif):
        if dust_notif['fields']['channel_str'] == 'temperature':
            sol_type  = SolDefines.SOL_TYPE_DUST_OAP_TEMPSAMPLE
            sol_value = {
                'temperature': dust_notif['fields']['samples'][0],
            }
        elif dust_notif['fields']['channel_str'].startswith('analog'):
            sol_type  = SolDefines.SOL_TYPE_DUST_OAP_ANALOG
            sol_value = {
                'input':   dust_notif['fields']['input'],
                'voltage': dust_notif['fields']['samples'][0],
            }
        elif dust_notif['fields']['channel_str'].startswith('digital_in'):
            sol_type  = SolDefines.SOL_TYPE_DUST_OAP_DIGITAL_IN
            if "input" in  dust_notif['fields'] and "samples" in dust_notif['fields']:
                sol_value = {
                    'input':   dust_notif['fields']['input'],
                    'state':   dust_notif['fields']['samples'][0],
                }
            elif "channel_str" in dust_notif['fields'] and "new_val" in dust_notif['fields']:
                sol_value = {
                    'input' : dust_notif['fields']['channel'][1],
                    'state' : dust_notif['fields']['new_val'],
                }
            else:
                log.debug("Unknow format for sol type {0}. dust_notif={1}".format(sol_type, dust_notif))
        else:
            raise NotImplementedError()
        return (sol_type, sol_value)

    # other

    def _dust_other_notif_to_sol_json(self, dust_notif):
        sol_typeName    = self._dust_notifName_to_sol_typeName(dust_notif['name'])
        sol_type        = getattr(SolDefines, sol_typeName)
        sol_value       = self._fields_to_json_with_structure(
            sol_type,
            dust_notif,
        )

        return sol_type, sol_value

    def _dust_notifName_to_sol_typeName(self, notifName):
        return 'SOL_TYPE_DUST_{0}'.format(notifName.upper())

    def _fields_to_json_with_structure(self, sol_type, dust_notif):

        sol_struct          = SolDefines.solStructure(sol_type)

        returnVal       = {}
        for name in sol_struct['fields']:
            returnVal[name] = dust_notif['fields'][name]
            if name in ['source','dest','macAddress']:
                returnVal[name] = FormatUtils.format_mac_string_to_bytes(returnVal[name])
        if 'extrafields' in sol_struct:
            returnVal[sol_struct['extrafields']] = dust_notif['fields'][sol_struct['extrafields']]

        for (k, v) in returnVal.items():
            if type(v) == tuple:
                returnVal[k] = [b for b in v]

        return returnVal

    # ==== json_to_bin

    def _fields_to_binary_with_structure(self, sol_type, fields):

        sol_struct      = SolDefines.solStructure(sol_type)

        pack_format     = sol_struct['structure']
        pack_values     = [fields[name] for name in sol_struct['fields'] if name in fields]

        # convert [0x01,0x02,0x03] into 0x010203 to be packable
        for i in range(len(pack_values)):
            if type(pack_values[i]) == list:
                pack_values[i] = _list_to_num(pack_values[i])

        # unpacking field by field
        returnVal = []
        for id, val in enumerate(pack_values):
            returnVal += [ord(b) for b in struct.pack(pack_format[0] + pack_format[id+1], val)]
        #returnVal       = [ord(b) for b in struct.pack(pack_format, *pack_values)]
        if 'extrafields' in sol_struct:
            returnVal  += fields[sol_struct['extrafields']]

        return returnVal

    # ==== bin_to_json

    def _binary_to_fields_with_structure(self, sol_type, binary):

        sol_struct      = SolDefines.solStructure(sol_type)

        pack_format     = sol_struct['structure']
        pack_length     = struct.calcsize(pack_format)

        # unpacking field by field
        t = []
        ptr = 0
        for frmt in pack_format[1:]:
            size = struct.calcsize(pack_format[0] + frmt)
            if len(binary[ptr:ptr+size]) > 0:
                t.append(struct.unpack(pack_format[0] + frmt,
                                       "".join(chr(b) for b in binary[ptr:ptr+size]))[0])
            ptr += size

        returnVal = {}
        for (k, v) in zip(sol_struct['fields'], t):
            returnVal[k] = v

        if 'extrafields' in sol_struct:
            returnVal[sol_struct['extrafields']] = binary[pack_length:]

        for (k, v) in returnVal.items():
            if k in ['macAddress', 'source', 'dest']:
                returnVal[k] = _num_to_list(v, 8)
            elif k in ['sol_version', 'sdk_version', 'solmanager_version']:
                returnVal[k] = _num_to_list(v, 4)

        return returnVal

    def _binary_to_fields_snapshot(self, binary):
        return_val      = []

        # set SNAPSHOT structure
        mote_structure  = ">QHBBBBBIIIIII"
        mote_fields     = [
                    'macAddress', 'moteId', 'isAP', 'state', 'isRouting', 'numNbrs',
                    'numGoodNbrs', 'requestedBw', 'totalNeededBw', 'assignedBw',
                    'packetsReceived', 'packetsLost', 'avgLatency'
                ]
        mote_size       = struct.calcsize(mote_structure)
        path_structure  = ">QBBBbb"
        path_fields     = [
                    'macAddress', 'direction', 'numLinks', 'quality',
                    'rssiSrcDest', 'rssiDestSrc'
                ]
        path_size       = struct.calcsize(path_structure)

        # get number of motes in snapshot
        num_motes       = struct.unpack('>B', chr(binary[0]))[0]
        binary          = binary[1:]

        # parse SNAPSHOT
        for i in range(0, num_motes):
            # create mote dict
            mote = {}
            m = struct.unpack(mote_structure, ''.join(chr(b) for b in binary[:mote_size]))
            binary          = binary[mote_size:]
            for (k, v) in zip(mote_fields, m):
                mote[k] = v

            # format mac address
            mote["macAddress"] = _num_to_list(mote["macAddress"], 8)

            # get number of paths in mote
            num_paths       = struct.unpack('>B', chr(binary[0]))[0]
            binary          = binary[1:]

            # create path dict
            path_list       = []
            for j in range(0, num_paths):
                path = {}
                p = struct.unpack('>QBBBbb', ''.join(chr(b) for b in binary[:path_size]))
                binary = binary[path_size:]
                for (k, v) in zip(path_fields, p):
                    path[k] = v

                # format mac address
                path["macAddress"] = _num_to_list(path["macAddress"], 8)

                path_list.append(path)

            mote["paths"] = path_list

            return_val.append(mote)

        return return_val

    def _get_sol_binary_value_dust_hr_neighbors(self, hr):
        return_val  = []
        return_val += [chr(hr['numItems'])]
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
        return_val = ''.join(return_val)
        return_val = [ord(c) for c in return_val]

        return return_val

    def _get_sol_binary_value_dust_hr_discovered(self, hr):
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

    def _get_sol_binary_value_dust_hr_extended(self, hr):
        HR_ID_EXTENDED_RSSI_STRUCT = ">" + "".join([i[1] for i in self.hrParser.HR_DESC_EXTENDED_RSSI_DATA])
        HR_ID_EXTENDED_RSSI_SIZE = struct.calcsize(HR_ID_EXTENDED_RSSI_STRUCT) * 15 # 15 channels
        return_val = []
        if "RSSI" in hr.keys():
            return_val += [struct.pack("<BB",
                                       self.hrParser.HR_ID_EXTENDED_RSSI, # extType
                                       HR_ID_EXTENDED_RSSI_SIZE)] # extLength
            for n in hr['RSSI']:
                return_val += [struct.pack(
                    HR_ID_EXTENDED_RSSI_STRUCT,
                    n['idleRssi'],          # INT8    b
                    n['txUnicastAttempts'], # INT16U  H
                    n['txUnicastFailures'], # INT16U  H
                )]
            return_val  = ''.join(return_val)
            return_val  = [ord(c) for c in return_val]
        else:
            raise NotImplementedError

        return return_val

    def _get_sol_binary_value_snapshot(self, snapshot):
        return_val  = ""

        # adding number of items
        return_val  += struct.pack('>B', len(snapshot))

        # converting json to bytes
        for mote in snapshot:
            if isinstance(mote['macAddress'], (str, unicode)):
                mote['macAddress'] = [int(c, 16) for c in mote['macAddress'].split("-")]
            m = struct.pack(
                '>QHBBBBBIIIIII',
                _list_to_num(mote['macAddress']),      # INT64U  Q
                mote['moteId'],                             # INT16U  H
                mote['isAP'],                               # BOOL    B
                mote['state'],                              # INT8U   B
                mote['isRouting'],                          # BOOL    B
                mote['numNbrs'],                            # INT8U   B
                mote['numGoodNbrs'],                        # INT8U   B
                mote['requestedBw'],                        # INT32U  I
                mote['totalNeededBw'],                      # INT32U  I
                mote['assignedBw'],                         # INT32U  I
                mote['packetsReceived'],                    # INT32U  I
                mote['packetsLost'],                        # INT32U  I
                mote['avgLatency'],                         # INT32U  I
            )
            return_val  += m

            # adding paths list size
            return_val  += struct.pack('B', len(mote['paths']))

            p = ""
            for path in mote['paths']:
                if isinstance(path['macAddress'], (str, unicode)):
                    path['macAddress'] = [int(c, 16) for c in path['macAddress'].split("-")]
                p += struct.pack(
                    '>QBBBbb',
                    _list_to_num(path['macAddress']),  # INT64U  Q
                    path['direction'],                      # INT8U   B
                    path['numLinks'],                       # INT8U   B
                    path['quality'],                        # INT8U   B
                    path['rssiSrcDest'],                    # INT8    b
                    path['rssiDestSrc'],                    # INT8    b
                )
            return_val += p
        return_val  = ''.join(return_val)
        return_val  = [ord(c) for c in return_val]
        return return_val

    # ==== file manipulation

    def _fileBackUpUntilStartFrame(self, file_name, curOffset):
        with open(file_name, 'rb') as f:
            f.seek(curOffset, os.SEEK_SET)
            while True:
                byte = f.read(1)
                if byte == self.hdlc.HDLC_FLAG:
                    return f.tell()-1
                f.seek(-2, os.SEEK_CUR)

# ==== miscellaneous helpers

def _num_to_list(num, length):
    output = []
    for l in range(length):
        output = [int((num >> 8*l) & 0xff)]+output
    return output

def _list_to_num(l):
    output = 0
    for i in range(len(l)):
        output += l[i] << (8*(len(l)-i-1))
    return output

# =========================== main ============================================

if __name__ == "__main__":
    os.system("py.test -vv -x tests/")
    raw_input("Press Enter to close.")
