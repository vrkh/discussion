import socket
import threading
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('178.250.158.150', 7070))
server.listen()


def client_socket_listener(client, address):
    global clients
    clients.append(client)
    while True:
        try:
            client_request = client.recv(4096).decode()
            if client_request:
                print(client_request)
        except Exception:
            clients.remove(client)
            raise Exception('Socket thread stoped')


global clients
clients = []
while True:
    client_socket, client_address = server.accept()
    answer = f'connected to server from {client_address[0]}:{client_address[1]}'.encode()
    client_socket.send(answer)
    threading.Thread(target=client_socket_listener, args=(client_socket, client_address,)).start()
    print('starting')
