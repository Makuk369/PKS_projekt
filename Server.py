import socket
import random
import threading
from enum import Enum
from Message import Message, MessageType
from sys import maxsize as maxint

DEFAULT_PORT = 50601
# SOCK_TIMEOUT = 5.0

class FunOptions(Enum):
    EXIT = 0
    CONFIGURE = 1
    LISTEN = 2
    HIDE_AUTO_MSGS = 10
    SH_ALL_MSGS = 11

class Server():
    def __init__(self) -> None:
        self.ip: str
        self.port: int
        self.sock: socket.socket
        self.tokens: list[int] = []
        self.recievedMsgs: list[Message] = [] #something like a history of messages

        self.bgThread = threading.Thread(target=self.Listen, daemon=True)
        self.stopBgThread = threading.Event()
        self.hideAutoMsg = False

        self.Run()

    def Run(self):
        while(True):
            self.PrintFunOptions()

            fun = 0
            try:
                fun = int(input("Select function: "))
            except:
                print("Error: Wrong input")
                continue

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
                    if self.bgThread.is_alive():
                        print("Already listening")
                    else:
                        self.bgThread.start()
                    # self.Listen()

                case FunOptions.HIDE_AUTO_MSGS.value:
                    self.hideAutoMsg = not self.hideAutoMsg

                case FunOptions.SH_ALL_MSGS.value:
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
        # self.sock.settimeout(SOCK_TIMEOUT)

    def Listen(self) -> None:
        print("Started listening")
        while not self.stopBgThread.is_set():
            rcvmsg = self.ReceiveMessage()
            print("Recieved: ", rcvmsg)

            if not ((rcvmsg.token in self.tokens) or (rcvmsg.token == -1)):
                print("Error: Message has unknown token")
                return
            
            if not (self.CheckCrc(rcvmsg)):
                print("Error: Message has wrong crc")
                return

            match rcvmsg.msgType:
                case MessageType.REG.value:
                    self.tokens.append(random.randint(0, maxint))
                    self.SendMessage(Message(rcvmsg.sensorType, MessageType.REGT, self.tokens[-1]))
                    print(f"INFO: {rcvmsg.sensorType} REGISTERED at {rcvmsg.timestamp}")
                
                case MessageType.DATA.value:
                    if self.hideAutoMsg:
                        # continue
                        pass

                    print(f"{rcvmsg.timestamp} - {rcvmsg.sensorType}")
                    for param in rcvmsg.data:
                        print(f"{param}: {rcvmsg.data[param]}", end="; ")
                    print("")
            
                case _:
                    print("Error: Unknown message type!") 

    def ReceiveMessage(self) -> Message:
        data = None
        while data == None:
            data, self.client = self.sock.recvfrom(2048) #buffer size bytes
        rcvmsg = Message.InitFromJsonStr(str(data, encoding="utf-8"))
        self.recievedMsgs.append(rcvmsg)
        return rcvmsg
    
    def SendMessage(self, message: Message):
        message.CalcCrc()
        self.sock.sendto(message.ToJsonStr().encode("utf8"), self.client)

    def CheckCrc(self, message: Message) -> bool:
        return message.crc == abs(message.token - int(message.timestamp))

    def ShowMsgHistory(self):
        print("----- All Message History -----")
        for msg in self.recievedMsgs:
            print(msg)
        print("-------------------------------")

    def PrintFunOptions(self) -> None:
        print("Available functions:")
        for opts in FunOptions:
            print(f"{opts.value} - {opts.name}")
    
    def Exit(self) -> None:
        try:
            # self.stopBgThread.set()
            self.sock.close() # correctly closing socket
        except AttributeError:
            pass
        print("Exited server")

if __name__ == '__main__':
    Server()
    