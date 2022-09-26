"""
TODO(Turnip): document
"""
import socketserver
import datetime
import sys


class ResponseMaker:
    # Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
    # todo(Turnip): follow standard better
    HTTP_TEMPLATE = """HTTP/1.1 {status_code}\r
Date: {date}\r
Content-Length: {content_length}\r
{location}Content-Type: {content_type}{data_padding}{data}
"""

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
        self.data = ""
        self.location = None

    def set_status_code(self, status_code):
        self.status_code = status_code
        return self

    def set_data(self, data: str):
        self.data = data
        return self

    def set_content_type(self, content_type):
        # todo(Turnip): make less hardcoded
        self.content_type = content_type
        return self

    def set_location(self, location: str):
        stripped_location = location.lstrip("www/").rstrip("index.html/").rstrip("index.html")
        self.location = f"/{stripped_location}/"
        return self

    def generate(self) -> str:
        data = "" if self.data is None else self.data
        data_len = 0 if len(data) == 0 else sys.getsizeof(data.encode('utf-8'))
        return ResponseMaker.HTTP_TEMPLATE.format(
            status_code=self.status_code,
            date=datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"),  # todo(Turnip): get timezone
            content_length=data_len,
            location="" if self.location is None else f"Location: {self.location}\r\n",
            content_type=self.content_type,
            data_padding=("\r\n\r\n" if data_len > 0 else ""),
            data=data
        )

    def send_all(self, handler: socketserver.BaseRequestHandler):
        #  todo(Turnip): remove debug here
        print(self.generate())
        handler.request.sendall(bytearray(self.generate(), "utf-8"))
