import unittest

from server import MyWebServer
from urllib import request

BASEURL = "http://127.0.0.1:8080"


class MyTestCase(unittest.TestCase):
    def setUp(self, baseurl=BASEURL):
        """do nothing"""
        self.baseurl = baseurl

    def test_decode_hex(self):
        self.assertEqual(MyWebServer.decode_hex("20"), " ")
        self.assertEqual(MyWebServer.decode_hex("E58686"), "円")

    def test_decode_percent_encoded_str(self):
        self.assertEqual(MyWebServer.decode_percent_encoded_str("test%20here"), "test here")
        self.assertEqual(MyWebServer.decode_percent_encoded_str("test%E5%86%86"), "test円")

    # Custom
    def test_get_percent_encoded(self):
        url = self.baseurl + "/percent%20encoding.html"
        req = request.urlopen(url, None, 3)
        self.assertTrue(req.getcode() == 200, "200 OK Not FOUND!")

        url = self.baseurl + "/percent%20encoding%E5%86%86.html"
        req = request.urlopen(url, None, 3)
        self.assertTrue(req.getcode() == 200, "200 OK Not FOUND!")

    def test_get_directory(self):
        url = self.baseurl + "/space%20space"
        req = request.urlopen(url, None, 3)
        self.assertTrue(req.getcode() == 200, "200 OK Not FOUND!")


if __name__ == '__main__':
    unittest.main()
