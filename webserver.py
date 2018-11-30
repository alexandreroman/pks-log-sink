#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import os
import logging

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info("Received request: %s", self.headers["User-Agent"])
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        hostname = socket.gethostname()
        self.wfile.write(bytes("Hello world!\nMy hostname is %s\n" % hostname, "UTF-8"))

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    FORMAT = '%(asctime)-15s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    port = os.getenv("PORT", 8080)
    logging.info("Listening on port: %d", port)
    httpd = HTTPServer(("", port), GetHandler)
    httpd.serve_forever()
