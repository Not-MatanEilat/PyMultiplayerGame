from socket import AF_INET,SOCK_STREAM,socket
import struct
import json
from threading import Thread

class Communicator:

    IP = '127.0.0.1'
    PORT = 6984

    CONNECT_TO_GAME_CODE = 1
    MOVE_CODE = 2

    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)

        self.on_packet_received = None

    def connect_to_server(self):
        self.sock.connect((self.IP, self.PORT))
        print("Successfully connected to server")

        # setup thread for listening for packets
        listen_thread = Thread(target=self.listen_for_packets_from_server)
        listen_thread.start()

    def listen_for_packets_from_server(self):
        while True:
            try:
                message = self.receive_message()
                if self.on_packet_received is not None:
                    response_code, msg_length, message = self.parse_message(message)
                    response_json = json.loads(message)

                    self.on_packet_received(response_code, response_json)
            except ConnectionResetError:
                print("Connection to server lost")
                break

    def parse_message(self, message):
        code = struct.unpack('!B', message[0:1])[0]
        msg_length = struct.unpack('!I', message[1:5])[0]
        message = message[5:].decode()

        return code, msg_length, message


    def build_request(self, code, message):
        msg_length = len(message)
        return struct.pack('!B', code) + struct.pack('!I', msg_length) + message.encode()

    def send_request_bytes(self, buffer):

        self.sock.sendall(buffer)

    def send_dict_request(self, code, dictionary=None):

        if dictionary is None:
            dictionary = {}

        built_request = self.build_request(code, str(dictionary))

        self.send_request_bytes(built_request)

    def receive_message(self):
        return self.sock.recv(1024)

    # requests
    def connect_to_game(self):
        self.send_dict_request(self.CONNECT_TO_GAME_CODE, {"name": "player1"})




