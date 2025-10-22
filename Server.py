import socket
from enum import Enum

DEFAULT_PORT = 50601

class FunOptions(Enum):
    EXIT = 0
    CONFIGURE = 1
    AUTO_CONFIG = 11
    LISTEN = 2

class Server():
    ip: str
    port: int
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
                case FunOptions.AUTO_CONFIG.value:
                    self.Configure(True)
                case FunOptions.LISTEN.value:
                    self.Listen()
                case _:
                    print("Error: Unknown function!")
    
        

    def Configure(self, autoconfig = False) -> None:
        if autoconfig:
            self.ip = socket.gethostbyname(socket.gethostname())
            self.port = DEFAULT_PORT
        else:
            self.ip = input("Enter server ip: ")
            self.port = int(input("Enter server port: "))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket creation
        self.sock.bind((self.ip, self.port)) #needs to be tuple (string,int)

    def Listen(self):
        data = self.Receive()
        print(f"Recieved: {data}")

    def Receive(self) -> str:
        data = None
        while data == None:
            data, self.client = self.sock.recvfrom(1024) #buffer size is 1024 bytes
        return str(data, encoding="utf-8")

    def PrintFunOptions(self) -> None:
        print("Available functions:\n"
            f"{FunOptions.EXIT.value} - {FunOptions.EXIT.name}\n"
            f"{FunOptions.CONFIGURE.value} - {FunOptions.CONFIGURE.name} ({FunOptions.AUTO_CONFIG.value} - auto)\n"
            f"{FunOptions.LISTEN.value} - {FunOptions.LISTEN.name}\n"
        )
    
    def Exit(self) -> None:
        self.sock.close() # correctly closing socket
        print("Exited server")

if __name__ == '__main__':
    Server()
    