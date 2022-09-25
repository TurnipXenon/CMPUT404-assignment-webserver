"""
TODO(Turnip): document
"""
import datetime
import sys


class ResponseMaker:
    # Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
    # todo(Turnip): follow standard better
    HTTP_TEMPLATE = """HTTP/1.1 {status_code}
Date: {date}
Server: Apache
Content-Length: {content_length}
Content-Type: {content_type}{data_padding}{data}
"""

    class StatusCode:
        # todo(Turnip): follow the standards
        OK = "200 OK"
        NOT_FOUND = "404 NOT_FOUND"

    def __init__(self):
        self.status_code = ResponseMaker.StatusCode.OK
        self.content_length = 0
        self.content_type = "text/css"
        self.data = ""

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

    def generate(self) -> str:
        data_len = sys.getsizeof(self.data.encode('utf-8'))
        return ResponseMaker.HTTP_TEMPLATE.format(
            status_code=self.status_code,
            date=datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"), # todo(Turnip): get timezone
            content_length=data_len,
            content_type=self.content_type,
            data_padding=("\n\n" if data_len > 0 else ""),
            data=self.data
        )
