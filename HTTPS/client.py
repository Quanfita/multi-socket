import socket
import ssl

class HTTPSClient:
    def __init__(self, hostname):
        self.hostname = hostname
        self.context = ssl.create_default_context()
        self.sock = None
    
    def connect(self):
        # 创建TCP套接字并连接到目标服务器的443端口
        self.sock = socket.create_connection((self.hostname, 443))
        
        # 使用套接字创建TLS/SSL会话
        self.wrapped_socket = self.context.wrap_socket(self.sock, server_hostname=self.hostname)
        
    def request(self):
        # 发送HTTPS请求并读取响应
        self.wrapped_socket.sendall(b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % self.hostname.encode())
        response = self.wrapped_socket.recv(4096)

        # 打印响应内容（这里假设它是纯文本）
        print(response.decode())

    def close(self):
        # 关闭连接
        if self.wrapped_socket is not None:
            self.wrapped_socket.close()
        if self.sock is not None:
            self.sock.close()
