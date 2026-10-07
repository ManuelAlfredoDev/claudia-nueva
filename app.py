"""Sanitized local demo of an operational-assistant prototype."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

DEMO_REPLY = "Demo response: I can describe the safe local prototype, but I do not connect to external systems."

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        return
    def reply(self, status, payload):
        body=json.dumps(payload).encode()
        self.send_response(status); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path in {"/", "/index.html"}:
            content=(Path(__file__).parent / "public" / "index.html").read_bytes()
            self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(content))); self.end_headers(); self.wfile.write(content); return
        if self.path == "/health": return self.reply(200,{"status":"alive","mode":"demo-local","external_systems":False})
        self.reply(404,{"error":"not found"})
    def do_POST(self):
        if self.path not in {"/chat","/voice"}: return self.reply(404,{"error":"not found"})
        try:
            size=int(self.headers.get("Content-Length","0")); payload=json.loads(self.rfile.read(size) or b"{}")
            if not isinstance(payload,dict) or not str(payload.get("text","")).strip(): raise ValueError("text is required")
            self.reply(200,{"text":DEMO_REPLY,"source":"MOCK","channel":"voice-simulated" if self.path=="/voice" else "text"})
        except (ValueError,json.JSONDecodeError) as error: self.reply(400,{"error":str(error)})

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1",8765),Handler).serve_forever()
