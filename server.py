#!/usr/bin/env python3
"""
Simple HTTP Server for Frontend Development
Serves static files from ./public similar to Firebase Hosting.
"""

import http.server
import socketserver
import os

# Configuration
PORT = 3500
DIRECTORY = "./public"

class FirebaseLikeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Strip query/hash and normalize root requests to index.html
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == "/":
            self.path = "/index.html"
        else:
            self.path = path

        # If a directory is requested, serve its index.html
        file_path = self.translate_path(self.path)
        if os.path.isdir(file_path):
            self.path = self.path.rstrip("/") + "/index.html"

        # If file exists, serve it; otherwise fall back to index.html (SPA style)
        if os.path.exists(self.translate_path(self.path)):
            return super().do_GET()

        self.path = "/index.html"
        return super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), FirebaseLikeHTTPRequestHandler) as httpd:
        print(f"🚀 Server running at http://localhost:{PORT}/")
        print(f"📁 Serving files from: {os.path.abspath(DIRECTORY)}")
        print("\nAvailable pages:")
        print(f"  - http://localhost:{PORT}/")
        print(f"  - http://localhost:{PORT}/login.html")
        print(f"  - http://localhost:{PORT}/master-dashboard.html")
        print(f"  - http://localhost:{PORT}/campaign-detail.html")
        print(f"  - http://localhost:{PORT}/login-debug.html")
        print(f"  - http://localhost:{PORT}/test-api.html")
        print("\n⏹️  Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
