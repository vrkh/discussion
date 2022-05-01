import socket
import threading
from time import sleep
import os

# NE TROGAT BLYAT'!!! TOL'KO TAK RABOTAET S NESKOL'KIMI SOCKETAMI ZA RAZ
# KOSTILI, NO RABOTAET


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('178.250.158.150', 1337))
server.listen(1024)


def client_socket_listener(client, address):
    while True:
        try:
            client_request = client.recv(2048).decode('utf-8')
            print(client_request)
            if client_request.startswith('auth'):
                pass
            sleep(0.01)
        except Exception:
            raise Exception('Socket thread stoped')


while True:
    client_socket, client_address = server.accept()
    answer = f'connected to server from {client_address[0]}:{client_address[1]}'.encode('utf-8')
    client_socket.send(answer)
    threading.Thread(target=client_socket_listener, args=(client_socket, client_address,)).start()
    print('starting')
    sleep(0.01)
