import socket
from . import config
import threading
import time


def get_client_and_connect(address):
    Client(address).start_communication()


class Client:
    def __init__(self, address):
        self.address = address
        self.terminate = False
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    @staticmethod
    def get_client_instance():
        return Client(config.SERVER_ADDRESS)

    def connect(self):
        print(f"connecting to {self.address}...")
        self.client_socket.connect(self.address)
        return

    def terminate_connection(self):
        self.send_message(config.STOP_SIGN)
        self.client_socket.close()
        print(":Connection Terminated.")
        return

    def send_message(self, message):
        return self.client_socket.send(message.encode('utf-8'))

    def receive_message(self):
        return self.client_socket.recv(1024).decode()

    def start_communication(self):
        self.connect()
        print(f"Connected to the server.!!\nEnter '{config.STOP_SIGN}' to quit communication.")

        sender = threading.Thread(target=self.sender)
        receiver = threading.Thread(target=self.receiver)

        sender.start()
        receiver.start()
        return

    def sender(self):
        message = ''
        while message != config.STOP_SIGN:
            while not message:
                message = input("You:")
            self.send_message(message)
            message = input("You:")
        return

    def receiver(self):
        message = ""
        while not self.terminate or message is not config.STOP_SIGN:
            message = self.receive_message()
            print("Server Response:", message)
            print("------------------------------------------------------")
        return


if __name__ == "__main__":
    get_client_and_connect(config.SERVER_ADDRESS)
