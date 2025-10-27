import socket
import threading
import time
from enum import Enum
from Sensors import Sensor, SensorType, ThermoNode, WindSense, RainDetect, AirQualityBox
from Message import Message, MessageType

# SERVER_IP = "192.168.0.118"
# SERVER_PORT = 50601 (client port != server port), +1 for bg port

class FunOptions(Enum):
    EXIT = 0
    CONFIGURE = 1
    REGISTER_SENSORS = 2
    AUTO_DATA_MSG = 3
    CUSTOM_MSG = 4
    SH_ALL_MSGS = 10

class Tester():
    def __init__(self) -> None:
        self.serverIp: str
        self.serverPort: int
        self.sock: socket.socket
        self.connectedSensors: list[Sensor] = []
        self.recievedMsgs: list[Message] = [] #something like a history of messages

        self.bgThread = threading.Thread(target=self.AutoDataMsg, daemon=True)
        self.stopBgThread = threading.Event()

        self.Run()

    def Run(self):
        while(True):
            self.PrintFunOptions()
            
            try:
                fun = int(input("Select function: "))
            except:
                fun = -1

            match fun:
                case FunOptions.EXIT.value:
                    self.Exit()
                    break

                case FunOptions.CONFIGURE.value:
                    self.Configure()

                case FunOptions.REGISTER_SENSORS.value:
                    self.RegisterSensors()

                case FunOptions.AUTO_DATA_MSG.value:
                    choice = input("Turn auto message [on/off]?: ").strip().lower()
                    if choice == "on":
                        if not self.bgThread.is_alive():
                            self.stopBgThread.clear()
                            self.bgThread = threading.Thread(target=self.AutoDataMsg, daemon=True)
                            self.bgThread.start()
                        else:
                            print("Auto message is already on")
                    elif choice == "off":
                        self.stopBgThread.set()
                    else:
                        print("Error: Unknown choice!")

                case FunOptions.CUSTOM_MSG.value:
                    self.CustomMsg()

                case FunOptions.SH_ALL_MSGS.value:
                    self.ShowMsgHistory()

                case _:
                    print("Error: Unknown function!")

    def Configure(self) -> None:
        self.serverIp = input("Enter server ip: ")
        self.serverPort = int(input("Enter server port: "))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket creation

    def RegisterSensors(self) -> None:
        self.PrintSensorOptions()
        try:
            selectedSensor = int(input("Select sensor to register: "))
        except:
            selectedSensor = -1

        match selectedSensor:
            case SensorType.THERMONODE.value:
                self.SendMessage(Message(SensorType.THERMONODE, MessageType.REG))
                rcvmsg = self.ReceiveMessage()
                self.connectedSensors.append(ThermoNode(rcvmsg.token))

            case SensorType.WINDSENSE.value:
                self.SendMessage(Message(SensorType.WINDSENSE, MessageType.REG))
                rcvmsg = self.ReceiveMessage()
                self.connectedSensors.append(WindSense(rcvmsg.token))

            case SensorType.RAINDETECT.value:
                self.SendMessage(Message(SensorType.RAINDETECT, MessageType.REG))
                rcvmsg = self.ReceiveMessage()
                self.connectedSensors.append(RainDetect(rcvmsg.token))

            case SensorType.AIRQUALITYBOX.value:
                self.SendMessage(Message(SensorType.AIRQUALITYBOX, MessageType.REG))
                rcvmsg = self.ReceiveMessage()
                self.connectedSensors.append(AirQualityBox(rcvmsg.token))

            case _:
                print("Error: Unknown sensor!")

    def AutoDataMsg(self) -> None:
        print("Started Automessage")
        while not self.stopBgThread.is_set():
            for sensor in self.connectedSensors:
                sensor.UpdateData()
                self.SendMessage(Message(sensor.type, MessageType.DATA, sensor.token, data=sensor.GetData()))
            time.sleep(10)

    def CustomMsg(self) -> None:
        i = 0
        print("Connected Sensors:")
        for sensor in self.connectedSensors:
            print(f"{i} - {SensorType(sensor.type)}")
            i += 1

        selectedSensor = int(input("Select sensor: "))
        msg = Message(self.connectedSensors[selectedSensor].type, MessageType.DATA, self.connectedSensors[selectedSensor].token, data=self.connectedSensors[selectedSensor].GetData())

        lowBat = input("Low battery warning [y/n]?: ").strip().lower()
        if lowBat == "y":
            msg.isLowBattery = True
        
        self.SendMessage(msg)

    def ReceiveMessage(self) -> Message:
        data = None
        while data == None:
            data = self.sock.recv(2048) #buffer size
        rcvmsg = Message.InitFromJsonStr(str(data, encoding="utf-8"))
        self.recievedMsgs.append(rcvmsg)
        return rcvmsg

    def SendMessage(self, message: Message, doCrcError = False):
        if doCrcError:
            message.CalcCrc()
            message.crc += 1
        else:
            message.CalcCrc()

        self.sock.sendto(message.ToJsonStr().encode("utf8"), (self.serverIp, self.serverPort))

    def ShowMsgHistory(self):
        print("----- All Message History -----")
        for msg in self.recievedMsgs:
            print(msg)
        print("-------------------------------")

    def PrintFunOptions(self) -> None:
        print("Available functions:")
        for opts in FunOptions:
            print(f"{opts.value} - {opts.name}")

    def PrintSensorOptions(self):
        print("Available sensors:")
        for sensr in SensorType:
            print(f"{sensr.value} - {sensr.name}")

    def Exit(self) -> None:
        try:
            self.sock.close() # correctly closing socket
        except AttributeError:
            pass
        print("Exited tester")

if __name__ == '__main__':
    Tester()
    