from s_socket import TCPServer, TCPClient
import time
from log import logger


class Server:
    def __init__(self, host, port, listen_num) -> None:
        self._tcp_server = TCPServer(host, port, listen_num)
        self._tcp_server.start()
        self._tcp_client_list = []
        logger.info('Server: Initial successful.')

    def connect(self, host, port):
        self._tcp_client_list.append(TCPClient(host, port))
        logger.info(f'Server: Connected {host}:{port}.')

    def broadcast(self, msg):
        for s in self._tcp_client_list:
            print(s.status)
            if not s.status:
                s.connect()
            s.send(msg)

    def run(self):
        for _ in range(10):
            self.broadcast('client hello')
            time.sleep(1)

    def close(self):
        for s in self._tcp_client_list:
            s.close()
        self._tcp_server.stop()
        self._tcp_server.close()
        # self._tcp_server_thread.join()


if __name__ == '__main__':
    client = Server('127.0.0.1', 65512, 5)
    client.connect('127.0.0.1', 55512)
    client.run()
