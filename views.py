from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader
from pathlib import Path


class BasicAPI(BaseHTTPRequestHandler):
    def _send_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            if self.path == '/':
                self.path = '/index.html'
                index_file = open(self.path[1:]).read()
                self._send_response(200)
                self.wfile.write(bytes(index_file, 'utf-8'))
            else:
                self._send_response(404)
        except Exception:
            self._send_response(500)

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_params = parse_qs(post_data)

            if self.path == '/calculate':
                number = post_params.get('name', [''])
                number_str = ''.join(number)

                num_sqrd = int(number_str)**2
                num_cubed = int(number_str)**3

                if is_prime(int(number_str)):
                    prime = 1
                else:
                    prime = 0

                self._send_response(200)

                template = env.get_template('display_data.html')
                rendered_template = template.render(number=number_str, num_sqrd=num_sqrd, num_cubed=num_cubed, prime=prime)
                self.wfile.write(rendered_template.encode('utf-8'))
            else:
                self._send_response(404)

        except Exception:
            self._send_response(500)


def is_prime(num):
    if num == 0 or num == 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


if __name__ == "__main__":
    cwd = Path.cwd()
    env = Environment(loader=FileSystemLoader(str(cwd)+"/templates"))
    server = HTTPServer(('localhost', 8000), BasicAPI)
    print('Server Up')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print('Server Down')
