# Configure the server
import socket
import subprocess

host = '0.0.0.0'
port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(10)

print("Control server listening on {}:{}".format(host, port))

while True:
    client, address = server.accept()
    print("Accepted connection from {}:{}".format(address[0], address[1]))

    command = client.recv(1024).decode('utf-8')
    print("Received command: {}".format(command))

    # Execute the command on the EC2 instance
    result = subprocess.getoutput(command)
    client.send(result.encode('utf-8'))

    client.close()

