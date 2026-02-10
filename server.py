#!/usr/bin/env python3
"""
Simple HTTP Server for Frontend Development
Serves static files on localhost:3500
"""

import http.server
import socketserver
import os

# Configuration
PORT = 3500
DIRECTORY = "./public"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Server running at http://localhost:{PORT}/")
        print(f"📁 Serving files from: {os.path.abspath(DIRECTORY)}")
        print("\nAvailable pages:")
        print(f"  - http://localhost:{PORT}/login.html")
        print(f"  - http://localhost:{PORT}/dashboard.html")
        print("\n⏹️  Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
