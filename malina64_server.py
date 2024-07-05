from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.hash import pbkdf2_sha256
import config

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, response_code, response):
        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        if self.path == "/get_users_role":
            self.handle_get_users_role()
        else:
            self._send_response(404, {"message": "Not found"})

    def do_POST(self):
        if self.path == "/login":
            self.handle_login()
        else:
            self._send_response(404, {"message": "Not found"})

    def handle_get_users_role(self):
        try:
            conn = psycopg2.connect(
                dbname=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                host=config.DB_HOST,
                port=config.DB_PORT
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM users_role")
            rows = cur.fetchall()
            self._send_response(200, {"data": rows})
            cur.close()
            conn.close()
        except Exception as e:
            self._send_response(500, {"error": str(e)})

    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        username = data.get('username')
        password = data.get('password')

        try:
            conn = psycopg2.connect(
                dbname=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                host=config.DB_HOST,
                port=config.DB_PORT
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if user is None:
                self._send_response(401, {"message": "Invalid username or password"})
                return

            if not pbkdf2_sha256.verify(password, user[2]):
                self._send_response(401, {"message": "Invalid username or password"})
                return

            cur.execute("SELECT role FROM users_role WHERE username = %s", (username,))
            role_row = cur.fetchone()
            role = 'None' if role_row is None else role_row[0]

            self._send_response(200, {"message": "Login successful", "role": role})
            cur.close()
            conn.close()
        except Exception as e:
            self._send_response(500, {"error": str(e)})

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()