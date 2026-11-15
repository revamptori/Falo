import falo
from falo.network import NetworkServer, NetworkClient

game = falo.Game(title="Net Demo", width=800, height=600, mode="2d")
server = NetworkServer(port=7777)
server.start()
client = NetworkClient("127.0.0.1:7777")
client.connect()

@game.update
def update(dt):
    client.send(b"hello")

game.run(headless=True, max_frames=2)
