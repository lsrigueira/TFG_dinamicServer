# client.py

import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = "172.16.0.145"           # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
s.send(b"Hello server!")

nomearquivo=s.recv(1024)

with open(nomearquivo, 'wb') as f:
    while True:
        data = s.recv(1024)
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
