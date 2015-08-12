
class Sol(object):
    '''
    Sensor Object Library.
    '''
    
    #======================== public ==========================================
    
    def dict_to_bin(self,o_dict):
        '''
        \brief Convert list of dictionaries into a binary string.        
        '''
        raise NotImplementedError()
    
    def bin_to_dict(self,o_bin,mac=None):
        '''
        \brief Convert a binary string onto a list of dictionaries, each
            representing a sensor object.
        '''
        raise NotImplementedError()
    
    def dict_to_json(self,o_dict,mode="verbose"):
        '''
        \brief Convert list of dictionaries into a JSON string.
        '''
        raise NotImplementedError()

    def json_to_dict(self,o_json):
        '''
        \brief Convert list of dictionaries into a JSON string.
        '''
        raise NotImplementedError()
    
    #======================== private =========================================
    
if __name__=="__main__":
    import os
    os.system("py.test tests/")
    raw_input("Press Enter to close.")
