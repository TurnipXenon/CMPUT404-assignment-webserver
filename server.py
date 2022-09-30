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


class MyWebServer(socketserver.BaseRequestHandler):
    @classmethod
    def decode_hex(cls, hex_str: str):
        # from https://stackoverflow.com/questions/5649407/hexadecimal-string-to-byte-array-in-python
        hex_byte = bytearray.fromhex(hex_str) # bytes.fromhex(f"{hex_str}")
        return hex_byte.decode("utf-8")

    @classmethod
    def decode_percent_encoded_str(cls, encoded_str: str):
        # Parse code
        split_path = encoded_str.split("%")

        decoded = ""
        is_first = True
        full_code = ""
        getting_full_code = False
        for to_parse in split_path:
            if is_first:
                is_first = False
                decoded += to_parse
                continue

            if len(to_parse) == 2:
                getting_full_code = True
                full_code += to_parse
            elif getting_full_code:
                getting_full_code = False
                full_code += to_parse[:2]
                decoded += MyWebServer.decode_hex(full_code)
                decoded += to_parse[2:]
                full_code = ""
            else:
                code = to_parse[:2]
                decoded += MyWebServer.decode_hex(code)
                decoded += to_parse[2:]

        if getting_full_code:
            decoded += MyWebServer.decode_hex(full_code)

        return decoded

    def handle(self):
        data = self.request.recv(1024).strip()
        data_str = data.decode("utf-8").split("\r\n")

        response = ResponseMaker()
        top_str = data_str[0].split(" ")
        if top_str[0] != "GET":
            response.set_status_code(ResponseMaker.StatusCode.METHOD_NOT_ALLOWED) \
                .send_all(self)
            return

        raw_addr = top_str[1]
        encoded_addr = MyWebServer.decode_percent_encoded_str(raw_addr)
        if len(encoded_addr) != 0 and encoded_addr[-1] == "/":
            encoded_addr = f"{encoded_addr}/index.html"

        raw_path = f"www/{encoded_addr}"

        # validate not doing going out -.-
        abs_path = os.path.abspath(raw_path)
        curr_path = os.path.abspath("www/")
        if not abs_path.startswith(curr_path):
            response.set_status_code(ResponseMaker.StatusCode.NOT_FOUND)
        elif path.exists(raw_path):
            if os.path.isdir(raw_path):
                response.set_location(f"www/{raw_addr}", self.server.server_address)
                response.set_status_code(ResponseMaker.StatusCode.MOVED_PERMANENTLY)
            elif os.path.isfile(raw_path):
                # we might be serving a file we don't support but let's try anyway
                # if it fails, let just return a 404
                try:
                    with open(raw_path, "r") as file:
                        response.set_content(file.read(), raw_path)
                except:
                    print(f"Failed to decode non-text data at: {raw_path}")
                    response.set_status_code(ResponseMaker.StatusCode.NOT_FOUND)
        else:
            response.set_status_code(ResponseMaker.StatusCode.NOT_FOUND)

        response.send_all(self)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
