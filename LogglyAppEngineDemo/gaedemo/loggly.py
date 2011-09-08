"""Asynchronous Logging To Loggly From App Engine

Example Usage::

#GLOBAL
EPOINT = "https://logs.loggly.com/inputs/8f4e64db-f994-43c5-b147-2327b23680d2"
HOOVER = loggly.LogglyLogger(endpoint=epoint,
        level=logging.INFO)

logging.info("This will go to loggly via https RPC call")

"""
import logging, os
from logging import handlers
from google.appengine.api import urlfetch 

class LogglyHTTPSHandler(handlers.MemoryHandler):
    """Custom Handler That Performs Async Calls"""
    
    def __init__(self, capacity, flush_level, target, endpoint):
        handlers.MemoryHandler.__init__(self, capacity, flush_level, target)
        self.appname = os.getcwd().split('/')[-2]
        self.version = os.getcwd().split('/')[-1]
        self.endpoint = endpoint

    def flush(self):
        """Overides flush method with rpc based flush.
        
        Returns :
            (list) An empty list which represents an empty buffer
        """
        
        rpc = urlfetch.create_rpc()
        stuff = "source=%s-%s" % (self.appname, self.version)
        for record in self.buffer:
            stuff += self.format(record)
            urlfetch.make_fetch_call(rpc,
                                    url=self.endpoint,
                                    payload=stuff,
                                    method=urlfetch.POST)
        self.buffer = []
        return self.buffer

class LogglyLogger():
    """Configures The Loggly Logger Handler"""
    
    def __init__(self, endpoint, level):
        self.endpoint = endpoint
        self.level = level
        self.log_handler = self.configure_logger()
        
    def configure_logger(self):
        """Configures HTTPS Logger Handler.
        
        Returns:
            (object) log_handler object
            
        """
        
        log_handler = LogglyHTTPSHandler(100, self.level,
                                         None,
                                         self.endpoint)
        format_str = '''%(asctime)s level=%(levelname)s, msg="%(message)s",
                    module=%(module)s, file="%(filename)s", lineno=%(lineno)d'''
        logging.Formatter(format_str)
        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(self.level)
        return log_handler
        
    def flush(self):
        """Perform RPC based flush via customized MemoryHandler
        
        Returns:
            (list) An empty list which represents an empty buffer
            
        """
        
        return self.log_handler.flush()
        
