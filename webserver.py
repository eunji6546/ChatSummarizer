from http.server import BaseHTTPRequestHandler, HTTPServer
import ChatSummarize
 
# HTTPRequestHandler class
class httpRequestHandler(BaseHTTPRequestHandler):
 
    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # GET
    def do_GET(self):
        print("GET request!!!")
        self.set_headers()
 
        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    # POST
    def do_POST(self):
        self.set_headers()
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        chatSummarizer = ChatSummarize.ChatSummarizer(post_data.decode('utf-8'))
        chatSummarizer.preprocess()
        summary = chatSummarizer.summarize(4)
        response = "callback(" + summary + ")"
        self.wfile.write(response.encode('utf-8'))
        return

 
def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8080)
  httpd = HTTPServer(server_address, httpRequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()