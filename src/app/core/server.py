import socket
from . import config
import threading
import select


class Server:
    server = None

    def __init__(self, address, queue_length=None):
        self.address = address
        self.family = socket.AF_INET
        self.type = socket.SOCK_STREAM
        self.queue_length = queue_length if queue_length else 5
        self.__serve = True
        self.clients_sockets = []
        self.server = socket.socket(family=self.family, type=self.type)

    @staticmethod
    def get_server_instance():
        if Server.server:
            return Server.server

        Server.server = Server(config.SERVER_ADDRESS)
        Server.server.listen()

        return Server.server, config.SERVER_ADDRESS

    @staticmethod
    def is_server_running():
        if Server.server:
            return True
        return False

    def listen(self):
        self.server.bind(self.address)
        self.server.listen(self.queue_length)

        print("Server is started and listening at :", self.address)

        server_thread = threading.Thread(target=self.serve).start()
        manager_thread = threading.Thread(target=self.__manage).start()

        return

    def __manage(self):
        while True:
            if self.clients_sockets:
                readable_client_sockets,__, __ = \
                    select.select(self.clients_sockets, self.clients_sockets, self.clients_sockets)

                for _client_socket in readable_client_sockets:
                    message = _client_socket.recv(1024)
                    for __client_socket in self.clients_sockets:
                        if _client_socket != __client_socket:
                            __client_socket.send(message)
                        else:
                            continue


    def serve(self):
        while self.__serve:
            client_socket, client_address = self.server.accept()
            self.clients_sockets.append(client_socket)

            for _client_socket in self.clients_sockets:
                _client_socket.send(f"New member: ({client_address}) added to the group".encode())


if __name__ == "__main__":
    Server(config.SERVER_ADDRESS, queue_length=config.QUEUE_LENGTH).listen()
