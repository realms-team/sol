import pytest
import json
import os

from SmartMeshSDK.IpMgrConnectorSerial  import IpMgrConnectorSerial

#============================ defines ===============================


#============================ fixtures ==============================

FILES = [
    {
        "file_name"     : "sites/test1.csv",
        "file_content"  : (
                        "mac,latitude,longitude\n"
                        "00-00-00-00-00-00-00-00,-11.1111,-22.2222\n"
                        "00-11-22-33-44-55-66-77,-33.3333,-44.4444\n"
                    ),
    },
    {
        "file_name"     : "sites/test2.csv",
        "file_content"  : (
                        "mac,latitude,longitude\n"
                        "11-11-11-11-11-11-11-11,-11.1111,-22.2222\n"
                        "11-22-33-44-55-66-77-88,-55.5555,-44.4444\n"
                    ),
    }
]
LOCATION_TESTS = [
    {
        "mac"           : "00-11-22-33-44-55-66-77",
        "location"      : ("test1", "-33.3333", "-44.4444"),
    },
    {
        "mac"           : "11-22-33-44-55-66-77-88",
        "location"      : ("test2", "-55.5555", "-44.4444"),
    },
    {
        "mac"           : "XX-XX-XX-XX-XX-XX-XX-XX",
        "location"      : ("unknown", "0", "0"),
    },
]

@pytest.fixture()
def write_test_file(request):
    for param in FILES:
        test_file = open(param['file_name'], 'w')
        test_file.write(param['file_content'])
        test_file.close()

    def remove_file():
        for param in FILES:
            os.remove(param['file_name'])

    request.addfinalizer(remove_file)

@pytest.fixture(params=LOCATION_TESTS)
def pass_params(request):
    return request.param

#============================ helpers ===============================


#============================ tests =================================

def test_get_location(write_test_file, pass_params):
    import Sol
    sol = Sol.Sol()

    assert sol.get_location(pass_params['mac'])==pass_params['location']

