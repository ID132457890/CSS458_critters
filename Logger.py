class Logger(object):
    def __init__(self, model, log_type="Console", options = {}):
        self.model = model
        self._logger = exec("__Logger" + log_type)(self.options)

    def log(self, loglevel, message):
        self._logger(loglevel, message)

class __LoggerConsole(object):
    def __init__(self, options = {}):
        self.threshold = options['threshold'] if 'threshold' in options else 0

    def log(self, loglevel, message):
        if self.threshold <= loglevel:
            print ("(%d): %s" % (loglevel, message))