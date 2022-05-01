import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('178.250.158.150', 1337))

while True:
    server_data = server.recv(65536)
    if server_data:
        print(server_data.decode('utf-8'))
