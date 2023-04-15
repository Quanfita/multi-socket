import socket

class HTTPClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def request(self, url):
        # 解析URL，获取主机名和路径信息
        url_parts = url.split('/')
        host = url_parts[2]
        path = '/' + '/'.join(url_parts[3:])

        # 创建TCP连接
        self.client_socket.connect((host, 80))

        # 发送HTTP请求
        request_msg = f'GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n'
        self.client_socket.sendall(request_msg.encode())

        # 接收响应消息
        response_msg = ''
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            response_msg += data.decode()

        # 解析响应消息，提取响应头和响应体
        response_parts = response_msg.split('\r\n\r\n')
        response_headers = response_parts[0]
        response_body = response_parts[1]

        # 打印响应头和响应体
        print(response_headers)
        print(response_body)

        # 断开连接
        self.client_socket.close()

if __name__ == '__main__':
    client = HTTPClient()
    client.request('http://www.baidu.com/')
