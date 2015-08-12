import json
import base64
import threading

import SolDefines as d
import SolVersion as ver
import OpenHdlc

class Sol(object):
    '''
    Sensor Object Library.
    '''
    
    def __init__(self):
        self.fileLock = threading.RLock()
        self.hdlc     = OpenHdlc.OpenHdlc()
    
    #======================== public ==========================================
    
    #===== admin
    
    @property
    def version(self):
        return ver.SOL_VERSION
    
    #===== conversions
    
    def dict_to_bin(self,o_dict):
        bin   = []
        
        # header
        h     = 0
        h    |=             d.SOL_HDR_V<<d.SOL_HDR_V_OFFSET
        h    |=       d.SOL_HDR_H_START<<d.SOL_HDR_H_OFFSET
        h    |= d.SOL_HDR_START_M_8BMAC<<d.SOL_HDR_START_M_OFFSET
        h    |= d.SOL_HDR_START_S_EPOCH<<d.SOL_HDR_START_S_OFFSET
        h    |=    d.SOL_HDR_START_Y_1B<<d.SOL_HDR_START_Y_OFFSET
        h    |=    d.SOL_HDR_START_L_WK<<d.SOL_HDR_START_L_OFFSET
        bin  += [h]
        
        # mac
        bin  += o_dict['mac']
        
        # timestamp 
        bin  += self._num_to_list(o_dict['timestamp'],4)
        
        # type 
        bin  += self._num_to_list(o_dict['type'],1)
        
        # value 
        bin  += o_dict['value']
        
        return bin
    
    def bin_to_dict(self,o_bin,mac=None):
        returnVal = {}
        
        # header
        
        assert len(o_bin)>=1
        
        h     = o_bin[0]
        h_V   = (h>>d.SOL_HDR_V_OFFSET)&0x03
        assert h_V==d.SOL_HDR_V
        h_H   = (h>>d.SOL_HDR_H_OFFSET)&0x01
        assert h_H==d.SOL_HDR_H_START
        h_M   = (h>>d.SOL_HDR_START_M_OFFSET)&0x01
        h_S   = (h>>d.SOL_HDR_START_S_OFFSET)&0x01
        assert h_S==d.SOL_HDR_START_S_EPOCH
        h_Y   = (h>>d.SOL_HDR_START_Y_OFFSET)&0x01
        assert h_Y==d.SOL_HDR_START_Y_1B
        h_L   = (h>>d.SOL_HDR_START_L_OFFSET)&0x03
        assert h_L==d.SOL_HDR_START_L_WK
        
        o_bin = o_bin[1:]
        
        # mac
        
        if h_M==d.SOL_HDR_START_M_NOMAC:
            assert mac!=None
            returnVal['mac'] = mac
        else:
            assert len(o_bin)>=8
            returnVal['mac'] = o_bin[:8]
            o_bin = o_bin[8:]
        
        # timestamp
        
        assert len(o_bin)>=4
        returnVal['timestamp'] = self._list_to_num(o_bin[:4])
        o_bin = o_bin[4:]
        
        # type
        
        assert len(o_bin)>=1
        returnVal['type'] = o_bin[0]
        o_bin = o_bin[1:]
        
        # value
        assert len(o_bin)>=0
        returnVal['value'] = o_bin
        
        return returnVal
    
    def dict_to_json(self,o_dict,mode="verbose"):
        output = {
            'v': d.SOL_HDR_V,
            'o': self._o_to_json(o_dict,mode)
        }
        
        return json.dumps(output)
    
    def json_to_dict(self,o_json,mode="verbose"):
        returnVal = json.loads(o_json)['o']
        
        if   mode=="minimal":
            bin = base64.b64decode(returnVal)
            bin = [ord(b) for b in bin]
            returnVal = self.bin_to_dict(bin)
        elif mode=="verbose":
            returnVal['mac'] = [int(b,16) for b in returnVal['mac'].split('-')]
            returnVal['value'] = [ord(b) for b in base64.b64decode(returnVal['value'])]
        else:
            raise SystemError()
        
        return returnVal
    
    #===== file manipulation
    
    def dumpToFile(self,dicts,fileName):
        
        with self.fileLock:
            with open(fileName,'ab') as f:
                for d in dicts:
                    bin = self.dict_to_bin(d)
                    bin = self.hdlc.hdlcify(bin)
                    bin = ''.join([chr(b) for b in bin])
                    f.write(bin)
    
    def loadFromFile(self,fileName):
        
        with self.fileLock:
            bins = self.hdlc.dehdlcify(fileName)
        
        print bins
        
        dicts = [self.bin_to_dict(b) for b in bins]
        
        return dicts
    
    #======================== private =========================================
    
    def _num_to_list(self,num,length):
        output = []
        for l in range(length):
            output = [(num>>8*l)&0xff]+output 
        return output
    
    def _list_to_num(self,l):
        print l
        output = 0
        for i in range(len(l)):
            output += l[i]<<(8*(len(l)-i-1))
            print l[i]
            print hex(output)
        return output
    
    def _o_to_json(self,o_dict,mode):
        if   mode=="minimal":
            return base64.b64encode(''.join(chr(b) for b in self.dict_to_bin(o_dict)))
        elif mode=="verbose":
            return {
                "mac":       '-'.join(['%02x'%b for b in o_dict['mac']]),
                "timestamp": o_dict['timestamp'],
                "type":      o_dict['type'],
                "value":     base64.b64encode(''.join(chr(b) for b in o_dict["value"])),
            }
        else:
            raise SystemError()


#============================ main ============================================

if __name__=="__main__":
    import os
    os.system("py.test -x tests/")
    raw_input("Press Enter to close.")
