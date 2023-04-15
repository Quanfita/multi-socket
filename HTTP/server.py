import socket

class HTTPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def run_forever(self):
        while True:
            print('等待客户端连接...')
            client_socket, client_address = self.server_socket.accept()
            print('客户端已连接', client_address)

            request_msg = ''
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                request_msg += data.decode()
                if '\r\n\r\n' in request_msg:
                    break

            request_lines = request_msg.split('\r\n')
            request_line = request_lines[0]
            request_parts = request_line.split(' ')
            request_method = request_parts[0]
            request_path = request_parts[1]
            request_headers = {}
            for request_header in request_lines[1:]:
                if ':' in request_header:
                    key, value = request_header.split(':', 1)
                    request_headers[key] = value.strip()

            response_body, response_headers, response_status = self.handle_request(request_path)

            response_msg = response_status + '\r\n'
            for key, value in response_headers.items():
                response_msg += f'{key}: {value}\r\n'
            response_msg += '\r\n' + response_body
            client_socket.sendall(response_msg.encode())

            client_socket.close()

    def handle_request(self, path):
        if path == '/':
            response_body = '<h1>Hello, World!</h1>'
            response_headers = {
                'Content-Type': 'text/html',
                'Content-Length': str(len(response_body))
            }
            response_status = 'HTTP/1.1 200 OK'
        else:
            response_body = '<h1>404 Not Found</h1>'
            response_headers = {
                'Content-Type': 'text/html',
                'Content-Length': str(len(response_body))
            }
            response_status = 'HTTP/1.1 404 Not Found'

        return response_body, response_headers, response_status


if __name__ == '__main__':
    server = HTTPServer()
    server.run_forever()
