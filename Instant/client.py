import socket

class Client:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        # 连接服务器
        self.client_socket.connect((self.host, self.port))

    def send(self, message):
        # 发送消息
        self.client_socket.sendall(message.encode())

    def receive(self):
        # 接收服务器返回的消息
        data = self.client_socket.recv(1024)
        return data.decode()

    def close(self):
        # 关闭连接
        self.client_socket.close()
