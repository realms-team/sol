import os
from solobjectlib import openhdlc as hdlc
from solobjectlib import Sol as sol

JSON = {
    'timestamp': 1521645792,
    'mac': '00-17-0d-00-00-58-5b-02',
    'type': 33,
    'value': {
        'manager': '00-17-0d-00-00-58-5b-02',
        'valid': True,
        'snapshot': {
            'getNetworkInfo': {
                'numLostPackets': 0,
                'advertisementState': 0,
                'ipv6Address': 'fe80:0000:0000:0000:0017:0d00:0058:5b02',
                'asnSize': 7250,
                'numMotes': 0,
                'numArrivedPackets': 0,
                'netLatency': 0,
                'netState': 0,
                'netPathStability': 0,
                'downFrameState': 1,
                'maxNumbHops': 0,
                'RC': 0,
                'netReliability': 0
            },
            'timestamp_stop': 'Wed, 21 Mar 2018 15:23:12 UTC',
            'getMoteConfig': {
                '00-17-0d-00-00-58-5b-02': {
                    'macAddress': '00-17-0d-00-00-58-5b-02',
                    'reserved': 1,
                    'state': 4,
                    'isRouting': True,
                    'RC': 0,
                    'moteId': 1,
                    'isAP': True}
            },
            'epoch_stop': 1521645792.786726,
            'getSystemInfo': {
                'macAddress': '00-17-0d-00-00-58-5b-02',
                'swBuild': 9,
                'swPatch': 1, 'hwModel': 16, 'swMajor': 1, 'swMinor': 4,
                'RC': 0, 'hwRev': 1
            },
            'getMoteLinks': {
                '00-17-0d-00-00-58-5b-02': {
                    'links': []
                }
            },
            'getMoteInfo': {
                '00-17-0d-00-00-58-5b-02': {
                    'macAddress': '00-17-0d-00-00-58-5b-02',
                    'assignedBw': 0,
                    'stateTime': 1355,
                    'numGoodNbrs': 0, 'numJoins': 1, 'state': 4,
                    'packetsReceived': 6, 'hopDepth': 0,
                    'totalNeededBw': 55890, 'requestedBw': 55890, 'avgLatency': 0,
                    'RC': 0, 'numNbrs': 0, 'packetsLost': 0
                }
            },
            'getPathInfo': {
                '00-17-0d-00-00-58-5b-02': {

                }
            },
            'timestamp_start': 'Wed, 21 Mar 2018 15:23:12 UTC',
            'getNetworkConfig': {
                'networkId': 1229, 'apTxPower': 8, 'ccaMode': 0, 'locMode': 0,
                'numParents': 2, 'channelList': 32767, 'baseBandwidth': 9000,
                'maxMotes': 101, 'bbSize': 1, 'bbMode': 0, 'oneChannel': 255,
                'isRadioTest': 0, 'downFrameMultVal': 1, 'RC': 0,
                'bwMult': 300, 'frameProfile': 1, 'autoStartNetwork': True
            }
        },
        'name': 'snapshot'}}

JSON2 = {
    'timestamp': 1521645792,
    'mac': '00-17-0d-00-00-58-5b-02',
    'type': 40,
    'value': {
        'SolManager': [2, 0, 1, 0],
        'Sol': [1, 4, 0, 0],
        'SmartMesh SDK': [1, 1, 2, 4]}
}

def test_hdlc():
    file_name = "test_hdlc.backup"

    h = hdlc.hdlcify(sol.json_to_bin(JSON))
    s = "".join(chr(c) for c in h)
    with open(file_name, 'ab') as f:
        f.write(s)
    (d,o) = hdlc.dehdlcify(file_name)
    assert d[0] == sol.json_to_bin(JSON)
    assert sol.bin_to_json(d[0]) == JSON
    os.remove(file_name)
