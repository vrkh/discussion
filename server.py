from typing import Any
import threading
import socket
import random
import glob
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('178.250.158.150', 7070))
server.listen()


def client_socket_listener(client: object, address: Any) -> None:
    global clients
    clients.append(client)
    while True:
        try:
            client_request = client.recv(4096).decode('utf-8')
            if client_request:
                print(client_request)

            if client_request.startswith('trytoreg'):
                registration_data = client_request.split(' ')
                user_login = registration_data[1]
                user_password = registration_data[2]

                # If user are not registrated
                if not os.path.exists(f'{user_login}.txt'):

                    with open(f'{user_login}.txt', 'w') as file:
                        file.write(user_password)
                    client.send(f'auth {user_login} {user_password}'.encode())

                else:
                    client.send(f'useralreadyexist'.encode())

            if client_request.startswith('trytoauth'):
                login_data = client_request.split(' ')
                user_login = login_data[1]
                user_password = login_data[2]

                # If user not exist
                if not os.path.exists(f'{user_login}.txt'):
                    client.send(f'usernotexist'.encode())

                else:
                    with open(f'{user_login}.txt', 'r') as file:
                        if user_password.strip() == file.read().strip():
                            client.send(f'authsuccess {user_login} {user_password}'.encode())
                        else:
                            client.send('wrongpassword'.encode())

            if client_request.startswith('userslist'):
                users_list = glob.glob('*.txt')
                print(users_list)
                client.send(f'userslist {users_list}'.encode())

            if client_request.startswith('message'):
                for user in clients:
                    user.send(client_request.encode())

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
