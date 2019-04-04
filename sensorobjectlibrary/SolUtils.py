import time
import logging
import traceback
import threading
import configparser

# =========================== logging =========================================

log = logging.getLogger(__name__)

# =========================== helpers =========================================


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
    print(output)
    return output


# =========================== singletons ======================================


class AppConfig(object):
    """
    Singleton which contains the configuration of the application.

    Configuration is read once from file CONFIGFILE
    """
    _instance = None
    _init     = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppConfig, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, config_file = ""):
        if self._init:
            return
        self._init = True

        # local variables
        self.dataLock   = threading.RLock()
        self.config     = {}
        self.config_file = config_file

        config = configparser.ConfigParser()
        config.read(self.config_file)

        with self.dataLock:
            for (k, v) in config.items('config'):
                try:
                    self.config[k] = float(v)
                except ValueError:
                    try:
                        self.config[k] = int(v)
                    except ValueError:
                        self.config[k] = v

    def get(self, name):
        with self.dataLock:
            return self.config[name]


class AppStats(object):
    """
    Singleton which contains the stats of the application.

    Stats are read once from file STATSFILE.
    """
    _instance = None
    _init     = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppStats, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, stats_list = "", stats_file = ""):
        if self._init:
            return
        self._init      = True

        self.dataLock   = threading.RLock()
        self.stats      = {}
        self.stats_list = stats_list
        self.stats_file = stats_file

        try:
            with open(self.stats_file, 'r') as f:
                for line in f:
                    k        = line.split('=')[0].strip()
                    v        = line.split('=')[1].strip()
                    try:
                        v    = int(v)
                    except ValueError:
                        pass
                    self.stats[k] = v
                log.info("Stats recovered from file.")
        except (EnvironmentError, EOFError) as e:
            log.info("Could not read stats file: %s", e)
            self._backup()

    # ======================= public ==========================================

    def increment(self, statName):
        self._validateStatName(statName)
        with self.dataLock:
            if statName not in self.stats:
                self.stats[statName] = 0
            self.stats[statName] += 1
        self._backup()

    def update(self, k, v):
        self._validateStatName(k)
        with self.dataLock:
            self.stats[k] = v
        self._backup()

    def set(self, stats_file):
        self.stats_file = stats_file

    def get(self):
        with self.dataLock:
            stats = self.stats.copy()
        return stats

    # ======================= private =========================================

    def _validateStatName(self, statName):
        if statName.startswith("NUMRX_") is False:
            if statName not in self.stats_list:
                print(statName)
            assert statName in self.stats_list

    def _backup(self):
        with self.dataLock:
            output = ['{0} = {1}'.format(k, v) for (k, v) in self.stats.items()]
            output = '\n'.join(output)
            with open(self.stats_file, 'w') as f:
                f.write(output)
