from http.server import BaseHTTPRequestHandler, HTTPServer
import os

PORT_NUMBER = 8080

class WifakeHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		rootdir = './web' #file location
		try:
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				print("User is opening", rootdir + self.path)
				f = open(rootdir + self.path)# open requested file
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read().encode())
				f.close()
			return

		except IOError:
			self.send_error(404, 'File not found')

try:
	# Currently to access the dummy page, user must go to
	# 127.0.01:8080/fbIndex.html
	server = HTTPServer(('', PORT_NUMBER), WifakeHandler)
	print('Wifake running on port' , PORT_NUMBER)
	server.serve_forever()

except KeyboardInterrupt:
	print('Wifake shutting down')
	server.socket.close()
