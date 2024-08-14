from Engine import Engine
from MenuScreen import MenuScreen

from socket import AF_INET,SOCK_STREAM,socket
import struct

def main():
    game = Engine()
    game.run(MenuScreen)


if "__main__" == __name__:
    main()

