from Engine import Engine
from MenuScreen import MenuScreen

from socket import AF_INET,SOCK_STREAM,socket
import struct

def main():

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('127.0.0.1', 6984))
    while True:
        code = 1
        msg = "my_msg"
        msg_length = len(msg)
        message = struct.pack('!B', code) + struct.pack('!I', msg_length) + msg.encode()
        print(message)
        sock.sendall(message)
        message = sock.recv(1024)
        print(message.decode())
    # game = Engine()
    # game.run(MenuScreen)


if "__main__" == __name__:
    main()

