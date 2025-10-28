import socket
import random
import threading
import time
from enum import Enum
from sys import maxsize as maxint
from message import Message, MessageType
from sensors import Sensor, SensorType, ThermoNode, WindSense, RainDetect, AirQualityBox

DEFAULT_PORT = 50601
SOCK_TIMEOUT = 5.0

class FunOptions(Enum):
    EXIT = 0
    CONFIGURE = 1
    LISTEN = 2
    NO_DATA_CONFIRM = 3
    SH_ALL_MSGS = 10
    HIDE_AUTO_MSGS = 11

class Server():
    def __init__(self) -> None:
        self.ip: str
        self.port: int
        self.sock: socket.socket
        self.connectedSensors: list[Sensor] = []
        self.noConfirmSensorsI: list[list[int]] = [] #[[index, repeats], ...]
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

                case FunOptions.NO_DATA_CONFIRM.value:
                    self.SetNoDataConfirm()

                case FunOptions.SH_ALL_MSGS.value:
                    self.ShowMsgHistory()

                case FunOptions.HIDE_AUTO_MSGS.value:
                    self.hideAutoMsg = not self.hideAutoMsg
                    if self.hideAutoMsg:
                        print("Auto messages are now hidden")
                    else:
                        print("Auto messages will be displayed again")

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
        self.sock.settimeout(SOCK_TIMEOUT)

    def Listen(self) -> None:
        print("Started listening")
        while not self.stopBgThread.is_set():
            rcvmsg = self.ReceiveMessage()

            if rcvmsg is not None: 
                tokenOk = False
                for sensor in self.connectedSensors:
                    if rcvmsg.token == sensor.token:
                        tokenOk = True
                if rcvmsg.token == -1:
                    tokenOk = True
                if not tokenOk:
                    print("Error: Message has unknown token!")
                    continue
                
                if not (self.CheckCrc(rcvmsg)):
                    if rcvmsg.msgType == MessageType.DATA.value:
                        print(f"INFO: {rcvmsg.sensorType} CORRUTPED DATA at {rcvmsg.timestamp}. REQUESTING DATA")
                        self.SendMessage(Message(rcvmsg.sensorType, MessageType.DATA_BAD, rcvmsg.token))
                    else:
                        print("Error: Message has wrong crc!")
                    continue

                match rcvmsg.msgType:
                    case MessageType.REG.value:
                        if rcvmsg.sensorType == SensorType.THERMONODE.value:
                            self.connectedSensors.append(ThermoNode(random.randint(0, maxint)))
                            self.SendMessage(Message(rcvmsg.sensorType, MessageType.REGT, self.connectedSensors[-1].token))

                        elif rcvmsg.sensorType == SensorType.WINDSENSE.value:
                            self.connectedSensors.append(WindSense(random.randint(0, maxint)))
                            self.SendMessage(Message(rcvmsg.sensorType, MessageType.REGT, self.connectedSensors[-1].token))

                        elif rcvmsg.sensorType == SensorType.RAINDETECT.value:
                            self.connectedSensors.append(RainDetect(random.randint(0, maxint)))
                            self.SendMessage(Message(rcvmsg.sensorType, MessageType.REGT, self.connectedSensors[-1].token))

                        elif rcvmsg.sensorType == SensorType.AIRQUALITYBOX.value:
                            self.connectedSensors.append(AirQualityBox(random.randint(0, maxint)))
                            self.SendMessage(Message(rcvmsg.sensorType, MessageType.REGT, self.connectedSensors[-1].token))

                        else:
                            print("Error: Unknown sensor!")
                            continue
                        print(f"INFO: {rcvmsg.sensorType} REGISTERED at {rcvmsg.timestamp}")

                    case MessageType.DATA.value:
                        if rcvmsg.isLowBattery:
                            print(f"{rcvmsg.timestamp} - WARNING: LOW BATTERY {rcvmsg.sensorType}")
                        else:
                            print(f"{rcvmsg.timestamp} - {rcvmsg.sensorType}")
                        for param in rcvmsg.data:
                            print(f"{param}: {rcvmsg.data[param]}", end="; ")
                        print("")

                        if len(self.noConfirmSensorsI) == 0: # noConfirmSensorsI is empty
                            self.SendMessage(Message(rcvmsg.sensorType, MessageType.DATA_CONFIRM, rcvmsg.token))

                        for nocons in self.noConfirmSensorsI.copy():
                            if rcvmsg.token == self.connectedSensors[nocons[0]]: # find noConfirmSensor -> dont confirm
                                nocons[1] -= 1
                                if nocons[1] == 0:
                                    self.noConfirmSensorsI.remove(nocons)
                            else:
                                self.SendMessage(Message(rcvmsg.sensorType, MessageType.DATA_CONFIRM, rcvmsg.token))
                    
                    case MessageType.AUTO_DATA.value:
                        if not self.hideAutoMsg:
                            if rcvmsg.isLowBattery:
                                print(f"{rcvmsg.timestamp} - WARNING: LOW BATTERY {rcvmsg.sensorType}")
                            else:
                                print(f"{rcvmsg.timestamp} - {rcvmsg.sensorType}")
                            for param in rcvmsg.data:
                                print(f"{param}: {rcvmsg.data[param]}", end="; ")
                            print("")
                        
                        if len(self.noConfirmSensorsI) == 0: # noConfirmSensorsI is empty -> send confirm
                            # print("sending confirmation")
                            self.SendMessage(Message(rcvmsg.sensorType, MessageType.DATA_CONFIRM, rcvmsg.token))

                        for nocons in self.noConfirmSensorsI.copy():
                            if rcvmsg.token == self.connectedSensors[nocons[0]].token: # find noConfirmSensor -> dont confirm
                                nocons[1] -= 1
                                # print(f"not confirming for next {nocons[1]} times")
                                if nocons[1] == 0:
                                    self.noConfirmSensorsI.remove(nocons)
                                    # print(f"removed nocon: {self.noConfirmSensorsI}")
                            else:
                                self.SendMessage(Message(rcvmsg.sensorType, MessageType.DATA_CONFIRM, rcvmsg.token))
                
                    case _:
                        print("Error: Unknown message type!") 

    def SetNoDataConfirm(self) -> None:
        i = 0
        print("Connected Sensors:")
        for sensor in self.connectedSensors:
            print(f"{i} - {SensorType(sensor.type)}")
            i += 1
        
        if i == 0:
            print("Error: No connected sensors!")
            return

        try:
            selectedSensor = int(input("Select sensor: "))
        except:
            print("Error: Unknown sensor!")
            return
        
        self.noConfirmSensorsI.append([selectedSensor, 3])

    def ReceiveMessage(self) -> Message | None:
        """Returns None after socket timeout"""
        try:
            data, self.client = self.sock.recvfrom(2048) #buffer size bytes
        except socket.timeout:
            return None
        
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
            self.stopBgThread.set()
            while self.bgThread.is_alive():
                time.sleep(0.5)
                print("Waiting for bgThread to stop")
            self.sock.close() # correctly closing socket
        except AttributeError:
            pass
        print("Exited server")

if __name__ == '__main__':
    Server()
    