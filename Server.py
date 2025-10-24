import socket
from enum import Enum

DEFAULT_PORT = 50601

class FunOptions(Enum):
    EXIT = 0
    CONFIGURE = 1
    LISTEN = 2

class Server():
    def __init__(self) -> None:
        self.ip: str
        self.port: int
        self.sock: socket.socket
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
                    if input("Use autoconfig [y/n]?: ") == "y":
                        self.Configure(True)
                    else:
                        self.Configure()
                case FunOptions.LISTEN.value:
                    self.Listen()
                case _:
                    print("Error: Unknown function!")
    
        

    def Configure(self, autoconfig = False) -> None:
        if autoconfig:
            self.ip = socket.gethostbyname(socket.gethostname())
            self.port = DEFAULT_PORT
            print(f"IP: {self.ip}, Port: {self.port}")
        else:
            self.ip = input("Enter server ip: ")
            self.port = int(input("Enter server port: "))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket creation
        self.sock.bind((self.ip, self.port)) #needs to be tuple (string,int)

    def Listen(self):
        data = self.ReceiveMessage()
        print(f"Recieved: {data}")
        if data == "REG":
            self.SendMessage("123")

    def ReceiveMessage(self) -> str:
        data = None
        while data == None:
            data, self.client = self.sock.recvfrom(1024) #buffer size is 1024 bytes
        return str(data, encoding="utf-8")
    
    def SendMessage(self, message: str):
        self.sock.sendto(message.encode("utf8"), self.client)

    def PrintFunOptions(self) -> None:
        print("Available functions:")
        for opts in FunOptions:
            print(f"{opts.value} - {opts.name}")
    
    def Exit(self) -> None:
        try:
            self.sock.close() # correctly closing socket
        except AttributeError:
            pass
        print("Exited server")

if __name__ == '__main__':
    Server()
    