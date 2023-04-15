from p2p import P2PClient

if __name__ == '__main__':
    client = P2PClient(8000)
    client.start()