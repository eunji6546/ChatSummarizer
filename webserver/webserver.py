from http.server import BaseHTTPRequestHandler, HTTPServer
 
# HTTPRequestHandler class
class httpRequestHandler(BaseHTTPRequestHandler):
 
    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # GET
    def do_GET(self):
        self.set_headers()
 
        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    # POST
    def do_POST(self):
        self.set_headers()

 
def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, httpRequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()