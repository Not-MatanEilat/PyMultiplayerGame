from Engine import Engine
from MenuScreen import MenuScreen

from socket import AF_INET,SOCK_STREAM,socket
import struct

def main():
    engine = Engine()
    menu_screen = MenuScreen(engine)
    engine.run(menu_screen)


if "__main__" == __name__:
    main()

