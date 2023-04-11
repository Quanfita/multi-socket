import socket
import threading
from log import logger
import time


class TCPServer:
    def __init__(self, host, port, num) -> None:
        self._socket = socket.socket()
        # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((host, port))
        self._socket.listen(num)

    def start(self):
        self._stop = False
        self._listen_thread = threading.Thread(target=self.listen)
        self._listen_thread.start()

    def stop(self):
        self._stop = True

    def listen(self):
        client, address = self._socket.accept()
        logger.info(f'TCPServer is connected with {address}.')
        while not self._stop:
            try:
                data = client.recv(1024).decode('utf-8')
                if data:
                    logger.info(f'TCPServer: Received data from {address}: {data}.')
                    client.sendall('world'.encode('utf-8'))
            except ConnectionResetError:
                logger.warning(f'TCPServer: The connection with {address} has been disconnected.')
                client, address = self._socket.accept()
                logger.info(f'TCPServer is connected with {address}.')

    def close(self):
        self.stop()
        self._listen_thread.join()
        self._socket.close()


class TCPClient:
    def __init__(self, host, port) -> None:
        self._socket = socket.socket()
        self._address = (host, port)
        self.status = self.connect()
        self._check_thread = threading.Thread(target=self.check)
        self._check_thread.start()

    def check(self):
        while True:
            if not self.status:
                self.status = self.connect()
            time.sleep(1)

    def connect(self):
        try:
            self._socket.connect(self._address)
            logger.info(f'TCPClient is connected with {self._address}.')
            return True
        except Exception:
            return False

    def send(self, msg):
        self._socket.sendall(msg.encode('utf-8'))
        logger.info(f'TCPClient: Sent data to {self._address}: {msg}.')
        response = self._socket.recv(1024).decode('utf-8')
        if response:
            logger.info(f'TCPClient: Received data from {self._address}: {response}.')

    def close(self):
        self._socket.close()
