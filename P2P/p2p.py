import socket
import threading

class P2PClient:
    def __init__(self, port):
        self.port = port
        self.peers = []            # 存储其他客户端的信息
        self.connect_thread = threading.Thread(target=self.connect_to_peer)
        self.listen_thread = threading.Thread(target=self.listen_to_peer)

    def start(self):
        self.connect_thread.start()
        self.listen_thread.start()

    def stop(self):
        for conn in self.peers:
            conn.close()

    def listen_to_peer(self):
        """监听其他客户端连接请求的线程"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', self.port))
        s.listen(2)           # 设置最大连接数为2，即两个客户端
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            self.peers.append(conn)
            t = threading.Thread(target=self.recv_thread, args=(conn,))
            t.start()

    def connect_to_peer(self):
        """连接到其他客户端的线程"""
        while True:
            host = input("Enter peer's IP address: ")
            if not host:    # 输入为空时退出
                return
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, self.port))
            self.peers.append(s)
            t = threading.Thread(target=self.recv_thread, args=(s,))
            t.start()
            t = threading.Thread(target=self.input_thread, args=(s,))
            t.start()

    def recv_thread(self, sock):
        """接收消息的线程"""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print("From peer:", data.decode())

    def input_thread(self, sock):
        """发送消息的线程"""
        while True:
            data = input("To peer: ")
            sock.sendall(data.encode())
