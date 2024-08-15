from socket import AF_INET,SOCK_STREAM,socket
import struct
import json
from threading import Thread

class ResponseCodes:
    CONNECTED_TO_SERVER = 1
    GAME_CONNECTED = 2
    MOVE = 3

class RequestCodes:
    CONNECT_TO_GAME = 2
    MOVE = 3

class Communicator:

    IP = '127.0.0.1'
    PORT = 6984

    def __init__(self, engine):
        self.sock = socket(AF_INET, SOCK_STREAM)

        self.engine = engine

    def connect_to_server(self):
        # setup thread for connecting to server and then listening to packets
        thread = Thread(target=self.connect_socket_to_server)
        thread.start()

    def connect_socket_to_server(self):
        try:
            self.sock.connect((self.IP, self.PORT))
            print("Successfully connected to server")

            self.listen_for_packets_from_server()
        except ConnectionRefusedError as e:
            # if on communicator function is set, pass it to the function, otherwise raise the exception as normal
            if self.engine.current_screen.on_communicator_error is not None:
                self.engine.current_screen.on_communicator_error(e)
            else:
                raise e
    def listen_for_packets_from_server(self):
        while True:
            try:
                message = self.receive_message()
                if self.engine.current_screen.on_packet_received is not None:
                    response_code, msg_length, message = self.parse_message(message)
                    print("Received message with code: " + str(response_code) + " and message: " + message)
                    response_json = json.loads(message)

                    self.engine.current_screen.on_packet_received(response_code, response_json)
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
        self.send_dict_request(RequestCodes.CONNECT_TO_GAME, {"name": "player1"})

    def update_player_position(self, x, y):
        self.send_dict_request(RequestCodes.MOVE, {"position": {"x": x, "y": y}})




