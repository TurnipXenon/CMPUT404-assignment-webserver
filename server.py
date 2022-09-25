#  coding: utf-8 
import socketserver
from os import path
from response_maker import ResponseMaker

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
import response_maker


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % data)
        # todo(TurnipXenon): validate
        data_str = data.decode("utf-8").split("\r\n")
        # todo(TurnipXenon): validate
        top_str = data_str[0].split(" ")
        print(f"Got a request of: {top_str}\n")
        if top_str[0] != "GET":
            response = ResponseMaker() \
                .set_status_code(ResponseMaker.StatusCode.METHOD_NOT_ALLOWED) \
                .send_all(self)
            return

        # todo(TurnipXenon): protect!!!
        raw_addr = top_str[1]
        if raw_addr == "/":
            raw_addr = "/index.html"
        data = None
        if path.exists(f"www/{raw_addr}"):
            with open(f"www/{raw_addr}", "r") as file:
                data = file.read()
        else:
            # TODO(TURNIPXENON): fix response!!!
            response = ResponseMaker() \
                .set_status_code(ResponseMaker.StatusCode.NOT_FOUND) \
                .send_all(self)
            return

        # todo(TurnipXenon): clean up and remove the hardcodes
        response = ResponseMaker() \
            .set_data(data) \
            .send_all(self)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
