from s_socket import TCPServer, TCPClient
import time


class Client:
    def __init__(self, host, port, self_host, self_port) -> None:
        self._tcp_server = TCPServer(self_host, self_port, 1)
        self._tcp_server.start()

        self._tcp_client = TCPClient(host, port)

    def send(self, msg):
        self._tcp_client.send(msg)

    def run(self):
        for _ in range(10):
            self.send('server hello')
            time.sleep(1)

    def close(self):
        self._tcp_client.close()
        self._tcp_server.stop()
        self._tcp_server.close()
        # self._tcp_server_thread.join()


if __name__ == '__main__':
    client = Client('127.0.0.1', 65512, '127.0.0.1', 55512)
