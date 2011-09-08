"""

TEST Coverage:

To Test This:

1.  You must set path to google_appengine SDK
2.  You must install nosetests, coverage
3.  Then run this command:

nosetests --with-coverage --cover-package=loggly test_loggly.py

"""

import unittest
import logging
import sys
try:
    import sys
    path = '/usr/local/google_appengine'
    sys.path.insert(0,path)
    from loggly import LogglyHTTPSHandler, LogglyLogger
except ImportError:
    "Cannot find Google App Engine SDK at: %s" % path
    sys.exit(1)

#import Google App Engine Test Code
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch_stub

# Create a stub map so we can build App Engine mock stubs.
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

# Register App Engine mock stubs.
apiproxy_stub_map.apiproxy.RegisterStub(
    'urlfetch', urlfetch_stub.URLFetchServiceStub())

class TestLogglyHTTPSHandler(unittest.TestCase):
    
    def setUp(self):
        self.endpoint = "http://logs.loggly.com/inputs/83e527d7-fad3-4d93-89da-0c2d8c0bcd6c"
        self.log_handler = LogglyHTTPSHandler(100, logging.INFO,
                                         None,
                                         self.endpoint)
        self.buffer = [1]
    
    def test_constructor(self):
        self.assertTrue(self.log_handler)
    
    def test_flush(self):
        """The buffer should be empty after flush is called"""
        
        my_buffer = self.log_handler.flush()
        self.assertFalse(my_buffer)
    
    def tearDown(self):
        del self.endpoint
        del self.log_handler
        del self.buffer
        
class TestLogglyLogger(unittest.TestCase):
    
    def setUp(self):
        self.endpoint = "http://logs.loggly.com/inputs/83e527d7-fad3-4d93-89da-0c2d8c0bcd6c"
        self.loggly = LogglyLogger(self.endpoint,level=logging.INFO)
        self.buffer = [1]

    def test_constructor_loggly(self):
        self.assertTrue(self.loggly)

    def test_configure_logger(self):
        
        handler = self.loggly.configure_logger()
        self.assertTrue(hasattr(handler, "flush"))

    def test_flush_loggly_loggly(self):
        """The buffer should be empty after flush is called"""
        
        my_buffer = self.loggly.flush()
        self.assertFalse(my_buffer)
    
    def tearDown(self):
        del self.endpoint
        del self.loggly
        del self.buffer

if __name__ == '__main__':
    unittest.main()