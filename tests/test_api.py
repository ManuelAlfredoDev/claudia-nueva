import json, threading, unittest
from http.client import HTTPConnection
from app import Handler
from http.server import ThreadingHTTPServer

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.server=ThreadingHTTPServer(("127.0.0.1",0),Handler); self.thread=threading.Thread(target=self.server.serve_forever); self.thread.start()
    def tearDown(self): self.server.shutdown(); self.thread.join(); self.server.server_close()
    def test_health_chat_and_simulated_voice(self):
        c=HTTPConnection("127.0.0.1",self.server.server_port); c.request("GET","/health"); self.assertEqual(c.getresponse().status,200)
        for path in ("/chat","/voice"):
            c.request("POST",path,json.dumps({"text":"hello"}),{"Content-Type":"application/json"}); self.assertEqual(c.getresponse().status,200)
        c.close()

if __name__ == "__main__": unittest.main()
