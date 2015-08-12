
class sol(object):
    
    #======================== public ==========================================
    
    def bin_to_dict(o_bin):
        '''
        \brief Convert a binary string onto a list of dictionaries, each
            representing a sensor object.
        '''
        raise NotImplementedError()

    def dict_to_bin(o_dict):
        '''
        \brief Convert list of dictionaries into a binary string.        
        '''
        raise NotImplementedError()

    def dict_to_json(o_dict,mode="verbose"):
        '''
        \brief Convert list of dictionaries into a JSON string.
        '''
        raise NotImplementedError()

    def json_to_dict(o_json):
        '''
        \brief Convert list of dictionaries into a JSON string.
        '''
        raise NotImplementedError()
    
    #======================== private =========================================
    
