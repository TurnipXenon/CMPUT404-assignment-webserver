#  coding: utf-8
import os.path
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
        # todo(TurnipXenon): validate
        data_str = data.decode("utf-8").split("\r\n")

        response = ResponseMaker()
        # todo(TurnipXenon): validate
        top_str = data_str[0].split(" ")
        if top_str[0] != "GET":
            response.set_status_code(ResponseMaker.StatusCode.METHOD_NOT_ALLOWED) \
                .send_all(self)
            return

        # todo(TurnipXenon): protect!!!
        raw_addr = top_str[1]
        # todo(Turnip): handle relative vs absolute
        print(f"Look: {raw_addr}")
        if len(raw_addr) != 0 and raw_addr[-1] == "/":
            raw_addr = f"{raw_addr}/index.html"

        data = None
        raw_path = f"www/{raw_addr}"
        if path.exists(raw_path):
            if os.path.isdir(raw_path):
                response.set_location(raw_path)
                response.set_status_code(ResponseMaker.StatusCode.MOVED_PERMANENTLY)
            elif os.path.isfile(raw_path):
                with open(raw_path, "r") as file:
                    data = file.read()
        else:
            # TODO(TURNIPXENON): fix response!!!
            response.set_status_code(ResponseMaker.StatusCode.NOT_FOUND) \
                .send_all(self)
            return

        # todo(TurnipXenon): clean up and remove the hardcodes
        # todo(TurnipXenon): don't hardcode the content type
        response.set_data(data) \
            .send_all(self)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
