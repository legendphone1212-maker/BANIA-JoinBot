import http.server
import socketserver

PORT = 10000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Fake server running on port", PORT)
    httpd.serve_forever()
