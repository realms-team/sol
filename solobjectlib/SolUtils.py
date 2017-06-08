import time
import logging
import traceback

#============================ logging =========================================

log = logging.getLogger(__name__)


def currentUtcTime():
    """ Returns the time in UTC string format"""
    return time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime())


def logCrash(err, appstats, threadName=None):
    output         = []
    output        += ["============================================================="]
    output        += [currentUtcTime()]
    output        += [""]
    output        += ["CRASH"]
    if threadName:
        output    += ["Thread {0}!".format(threadName)]
    output        += [""]
    output         += ["=== exception type ==="]
    output += [str(type(err))]
    output += [""]
    output += ["=== traceback ==="]
    output += [traceback.format_exc()]
    output  = '\n'.join(output)

    # update stats
    appstats.increment('ADM_NUM_CRASHES')
    log.critical(output)
    print output
    return output