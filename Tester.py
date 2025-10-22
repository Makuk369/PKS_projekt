import socket
from enum import Enum

# SERVER_IP = "147.175.162.126"
# SERVER_PORT = 50601 (client port != server port)

class FunOptions(Enum):
    EXIT = 0
    CONFIGURE = 1
    AUTO_DATA_MSG = 2

class Tester():
    serverIp: str
    serverPort: int
    sock: socket.socket

    def __init__(self) -> None:
        self.Run()
        pass

    def Run(self):
        while(True):
            self.PrintFunOptions()
            fun = int(input("Select function: "))
            match fun:
                case FunOptions.EXIT.value:
                    self.Exit()
                    break
                case FunOptions.CONFIGURE.value:
                    self.Configure()
                case FunOptions.AUTO_DATA_MSG.value:
                    self.AutoDataMsg()
                case _:
                    print("Error: Unknown function!")

    def Configure(self) -> None:
        self.serverIp = input("Enter server ip: ")
        self.serverPort = int(input("Enter server port: "))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket creation
        # self.sock.bind((self.serverIp, self.serverPort)) #needs to be tuple (string,int)

    def AutoDataMsg(self) -> None:
        self.SendMessage("test")

    def SendMessage(self, message):
        self.sock.sendto(bytes(message, encoding="utf8"), (self.serverIp, self.serverPort))

    def PrintFunOptions(self) -> None:
        print("Available functions:\n"
            f"{FunOptions.EXIT.value} - {FunOptions.EXIT.name}\n"
            f"{FunOptions.CONFIGURE.value} - {FunOptions.CONFIGURE.name}\n"
            f"{FunOptions.AUTO_DATA_MSG.value} - {FunOptions.AUTO_DATA_MSG.name}\n"
        )

    def Exit(self) -> None:
        self.sock.close() # correctly closing socket
        print("Exited tester")

if __name__ == '__main__':
    Tester()
    