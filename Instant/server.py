import socket
import threading

class Server:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'服务器已经启动，等待客户端连接...')

    def handle_client(self, client_socket):
        while True:
            # 接收客户端发送的消息
            data = client_socket.recv(1024)
            if not data:
                break
            # 将消息原样返回给客户端
            client_socket.send(data)
        # 断开连接
        client_socket.close()

    def run_forever(self):
        while True:
            # 接受客户端连接请求
            client_socket, client_address = self.server_socket.accept()
            print(f'客户端 {client_address} 已连接')

            # 在新线程中处理客户端请求
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
