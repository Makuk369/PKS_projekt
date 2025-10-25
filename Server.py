import socket
import random
import threading
from enum import Enum
from Message import Message, MessageType
from sys import maxsize as maxint

DEFAULT_PORT = 50601

class FunOptions(Enum):
    EXIT = 0
    CONFIGURE = 1
    LISTEN = 2
    SH_MSG_HISTORY = 10

class Server():
    def __init__(self) -> None:
        self.ip: str
        self.port: int
        self.sock: socket.socket
        self.bgsock: socket.socket
        self.tokens: list[int] = []
        self.recievedMsgs: list[Message] = [] #something like a history of messages

        self.bgThread = threading.Thread(target=self.AutoListen, daemon=True)
        self.stopBgThread = threading.Event()

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
                    if input("Use autoconfig [y/n]?: ").strip().lower() == "y":
                        self.Configure(True)
                    else:
                        self.Configure()

                case FunOptions.LISTEN.value:
                    choice = input("Turn auto listen (messages will not show in terminal) [on/off/skip]?: ").strip().lower()
                    if choice == "on":
                        if not self.bgThread.is_alive():
                            self.stopBgThread.clear()
                            self.bgThread.start()
                        else:
                            print("Auto listen is already on")
                    elif choice == "off":
                        self.stopBgThread.set()
                    elif choice == "skip":
                        self.Listen()
                    else:
                        print("Error: Unknown choice!")

                case FunOptions.SH_MSG_HISTORY.value:
                    self.ShowMsgHistory()

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

        self.bgsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bgsock.bind((self.ip, self.port+1))

    def Listen(self):
        rcvmsg = self.ReceiveMessage()
        if (rcvmsg.token in self.tokens) or (rcvmsg.token == -1):
            match rcvmsg.msgType:
                case MessageType.REG.value:
                    self.tokens.append(random.randint(0, maxint))
                    self.SendMessage(Message(rcvmsg.sensorType, MessageType.REGT, self.tokens[-1], rcvmsg.battery))

    def AutoListen(self):
        print("Started Autolisten")
        while not self.stopBgThread.is_set():
            self.ReceiveMessage(True)

    def ReceiveMessage(self, inBg = False) -> Message:
        data = None
        while data == None:
            if inBg:
                data, self.client = self.bgsock.recvfrom(2048)
            else:
                data, self.client = self.sock.recvfrom(2048) #buffer size bytes
        rcvmsg = Message.InitFromJsonStr(str(data, encoding="utf-8"))
        self.recievedMsgs.append(rcvmsg)
        return rcvmsg
    
    def SendMessage(self, message: Message):
        self.sock.sendto(message.ToJsonStr().encode("utf8"), self.client)

    def ShowMsgHistory(self):
        for msg in self.recievedMsgs:
            print(msg)

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
    