"""
⚠️ DEVELOPMENT TOOL ONLY - NOT FOR PRODUCTION
Simple HTTP upload server for local development.
Requires hardcoded AUTH_TOKEN for basic security.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import os

UPLOAD_DIR = 'assets'
AUTH_TOKEN = os.environ.get("UPLOAD_AUTH_TOKEN", "dev-token-change-me")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class UploadHandler(BaseHTTPRequestHandler):
    def _check_auth(self):
        auth = self.headers.get("Authorization", "")
        return auth == f"Bearer {AUTH_TOKEN}"

    def do_POST(self):
        if not self._check_auth():
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            file_path = os.path.join(UPLOAD_DIR, 'final_video.mp4')
            with open(file_path, 'wb') as f:
                f.write(post_data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Upload successful')
            print(f"Video saved to {file_path}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=UploadHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting upload server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
