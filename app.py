"""Sanitized local demo of an operational-assistant prototype."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path


def answer(text):
    prompt = text.lower()
    responses = [
        ("system" in prompt, "The DEMO system is operating normally. 18 units are active, 3 tasks are pending, and 2 simulated incidents are recorded.", False, False),
        ("near" in prompt and "p-014" in prompt, "There are 3 DEMO units within the configured radius of P-014. U-021 is the closest.", True, False),
        ("closest" in prompt, "U-021 is the closest at 0.4 km. It is currently en route.", True, False),
        ("north" in prompt and "report to" not in prompt, "North District is a fictional demo area. U-021 and U-017 are shown there for this portfolio scenario.", True, False),
        ("pending" in prompt, "There are 3 fictional pending tasks in this demo: T-1042, T-1045, and T-1048.", False, False),
        ("location" in prompt, "Displaying the demo location for U-021.", True, False),
        ("send a message" in prompt, "What message would you like to send?", False, False),
        ("report to north service point 3" in prompt, "Message prepared for U-021.", False, True),
    ]
    for match, reply, show_map, prepared in responses:
        if match:
            return {"text": reply, "show_map": show_map, "message_ready": prepared}
    return {"text": "This local portfolio demo can show fictional system status, units, tasks, a demo location, or a safe message-preparation flow.", "show_map": False, "message_ready": False}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): return
    def reply(self, status, payload):
        body = json.dumps(payload).encode(); self.send_response(status)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path in {"/", "/index.html"}:
            content = (Path(__file__).parent / "public" / "index.html").read_bytes()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(content))); self.end_headers(); self.wfile.write(content); return
        if self.path == "/health": return self.reply(200, {"status":"alive", "mode":"demo-local", "external_systems":False})
        self.reply(404, {"error":"not found"})
    def do_POST(self):
        if self.path not in {"/chat", "/voice"}: return self.reply(404, {"error":"not found"})
        try:
            size = int(self.headers.get("Content-Length", "0")); data = json.loads(self.rfile.read(size) or b"{}")
            text = str(data.get("text", "")).strip() if isinstance(data, dict) else ""
            if not text: raise ValueError("text is required")
            result = answer(text); result.update({"source":"DEMO DATA", "channel":"voice-simulated" if self.path == "/voice" else "text"}); self.reply(200, result)
        except (ValueError, json.JSONDecodeError) as error: self.reply(400, {"error":str(error)})


if __name__ == "__main__": ThreadingHTTPServer(("127.0.0.1",8765),Handler).serve_forever()
