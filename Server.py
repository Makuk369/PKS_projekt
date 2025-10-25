import socket
import random
from enum import Enum
from Message import Message, MessageType
from sys import maxsize as maxint

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
        self.tokens: list[int] = []
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
            print(f"Autoconfigured - IP: {self.ip}, Port: {self.port}")
        else:
            self.ip = input("Enter server ip: ")
            self.port = int(input("Enter server port: "))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket creation
        self.sock.bind((self.ip, self.port)) #needs to be tuple (string,int)

    def Listen(self):
        rcvmsg = self.ReceiveMessage()
        print(f"Recieved: {rcvmsg}")
        match rcvmsg.msgType:
            case MessageType.REG.value:
                self.tokens.append(random.randint(0, maxint))
                self.SendMessage(Message(rcvmsg.sensorType, MessageType.REGT, self.tokens[-1], rcvmsg.battery))

    def ReceiveMessage(self) -> Message:
        data = None
        while data == None:
            data, self.client = self.sock.recvfrom(2048) #buffer size bytes
        return Message.InitFromJsonStr(str(data, encoding="utf-8"))
    
    def SendMessage(self, message: Message):
        self.sock.sendto(message.ToJsonStr().encode("utf8"), self.client)

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
    