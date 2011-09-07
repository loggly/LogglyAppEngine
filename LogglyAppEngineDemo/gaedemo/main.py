#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import logging
import loggly

#Global
ep="https://logs.loggly.com/inputs/8f4e64db-f994-43c5-b147-2327b23680d2"
HOOVER = loggly.LogglyLogger(endpoint=ep,
        level=logging.INFO)

class MainHandler(webapp.RequestHandler):
    def get(self):
        logging.info("TEST:Logging From GAE in GET method")
        self.response.out.write("""
        <html>
          <body>
            <form action="/" method="post">
            <p>Enter A Message To Send To Loggly.com: <input type="text" name="message" /></p>
              <div><input type="submit" value="message"></div>
            </form>
          </body>
        </html>
        """)
    
    def post(self):
        message = self.request.get("message")
        logging.info("POST: %s" % message)
        self.response.out.write("Sent POST: %s" % message)

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
