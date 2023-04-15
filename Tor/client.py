import socket
import socks

class TorConnection:
    """使用tor代理连接的socket对象，支持http请求"""
    def __init__(self, tor_proxy_host='127.0.0.1', tor_proxy_port=9050):
        self.client_socket = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.set_proxy(
            proxy_type=socks.SOCKS5,
            addr=tor_proxy_host,
            port=tor_proxy_port
        )

    def __enter__(self):
        """进入context manager"""
        return self

    def __exit__(self, type, value, traceback):
        """退出context manager"""
        self.client_socket.close()

    def connect(self, host, port):
        """连接服务器"""
        ip = socket.gethostbyname(host)
        self.client_socket.connect((ip, port))

    def send_request(self, host):
        """发送HTTP请求"""
        request_msg = f'GET / HTTP/1.1\r\nHost: {host}\r\n\r\n'
        self.client_socket.sendall(request_msg.encode())

    def receive_response(self):
        """接收响应"""
        response_msg = ''
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            response_msg += data.decode()
        return response_msg

if __name__ == '__main__':
    # 创建一个TorConnection对象
    with TorConnection() as tor:
        # 连接到谷歌服务器
        tor.connect('www.google.com', 443)

        # 发送HTTP请求
        tor.send_request('www.google.com')

        # 接收响应消息
        response_msg = tor.receive_response()

        # 打印响应消息
        print(response_msg)
