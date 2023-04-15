import socket
import ssl

class HTTPSServer:
    def __init__(self, address, port, certfile, keyfile):
        self.address = address
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile, keyfile)

    def start(self):
        # 创建TCP套接字并监听端口
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind((self.address, self.port))
        self.server_sock.listen(1)

        # 循环处理客户端请求
        while True:
            client_sock, client_addr = self.server_sock.accept()
            ssl_sock = self.context.wrap_socket(client_sock, server_side=True)

            request = ssl_sock.recv(4096)
            # 处理HTTPS请求（这里假设它是纯文本）
            print(request.decode())

            # 发送响应
            response = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
            ssl_sock.sendall(response)

            ssl_sock.close()
            client_sock.close()

    def stop(self):
        self.server_sock.close()

if __name__ == '__main__':
    server = HTTPSServer('0.0.0.0', 443, 'server.crt', 'server.key')
    server.start()
    # 在这里进行其他操作（比如监听键盘输入等）
    server.stop()

