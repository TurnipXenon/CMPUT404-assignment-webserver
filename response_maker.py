"""
TODO(Turnip): document
"""
import os.path
import socketserver
import datetime
import sys


class ResponseMaker:
    # Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
    # todo(Turnip): follow standard better
    _HTTP_TEMPLATE = """HTTP/1.1 {status_code}\r
Date: {date}\r
{location}{content_meta}"""
    _CONTENT_TEMPLATE = """Content-Length: {content_length}\r
Content-Type: {content_type}

{content}"""
    _CONTENT_TYPE_MAP = {
        "css": "text/css",
        "html": "text/html",
    }


    class StatusCode:
        # todo(Turnip): follow the standards
        OK = "200 OK"
        MOVED_PERMANENTLY = "301 Moved Permanently"
        NOT_FOUND = "404 Not Found"
        METHOD_NOT_ALLOWED = "405 Method Not Allowed"

    def __init__(self):
        self.status_code = ResponseMaker.StatusCode.OK
        self.content_length = 0
        self.content_type = "text/css"
        self.content = ""
        self.content_meta = ""
        self.location = None

    def set_status_code(self, status_code):
        self.status_code = status_code
        return self

    def set_content(self, content: str, raw_addr: str):
        extension = os.path.splitext(raw_addr)[1].lstrip(".")
        if extension in ResponseMaker._CONTENT_TYPE_MAP:
            self.content_type = ResponseMaker._CONTENT_TYPE_MAP[extension]
        else:
            self.content_type = extension
            print(f"Unknown extension type: {extension}; Content: \n{content}")

        self.content_length = sys.getsizeof(content.encode('utf-8'))
        self.content = content
        self.content_meta = ResponseMaker._CONTENT_TEMPLATE.format(
            content_length=self.content_length,
            content_type=self.content_type,
            content=self.content
        )
        return self

    def set_location(self, location: str, server_address: (str, int)):
        stripped_location = location.lstrip("www/").rstrip("index.html/").rstrip("index.html")
        self.location = f"http://{server_address[0]}:{server_address[1]}/{stripped_location}/"
        return self

    def generate(self) -> str:
        data = "" if self.content is None else self.content
        data_len = 0 if len(data) == 0 else sys.getsizeof(data.encode('utf-8'))
        return ResponseMaker._HTTP_TEMPLATE.format(
            status_code=self.status_code,
            date=datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"),  # todo(Turnip): get timezone
            location="" if self.location is None else f"Location: {self.location}\r\n",
            content_meta=self.content_meta
        )

    def send_all(self, handler: socketserver.BaseRequestHandler):
        # print(self.generate())
        handler.request.sendall(bytearray(self.generate(), "utf-8"))
