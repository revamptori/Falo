class NetworkServer:
    def __init__(self, port=7777):
        self.port = port
        self.clients = 0
    def start(self): print(f"[NetworkServer] start port {self.port}")
    def broadcast(self, msg): print(f"[NetworkServer] broadcast {msg}")

class NetworkClient:
    def __init__(self, addr="127.0.0.1:7777"):
        self.addr = addr
    def connect(self): print(f"[NetworkClient] connect {self.addr}")
    def send(self, msg): print(f"[NetworkClient] send {msg}")
