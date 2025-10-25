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
    SH_MSG_HISTORY = 10

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
            fun = int(input("Select function: "))
            match fun:
                case FunOptions.EXIT.value:
                    self.Exit()
                    break

                case FunOptions.CONFIGURE.value:
                    self.Configure()

                case FunOptions.REGISTER_SENSORS.value:
                    if not self.RegisterSensors():
                        print("Error: Could not connect sensor!")

                case FunOptions.AUTO_DATA_MSG.value:
                    choice = input("Turn auto message [on/off]?: ").strip().lower()
                    if choice == "on":
                        if not self.bgThread.is_alive():
                            self.stopBgThread.clear()
                            self.bgThread.start()
                        else:
                            print("Auto message is already on")
                    elif choice == "off":
                        self.stopBgThread.set()
                    else:
                        print("Error: Unknown choice!")

                case FunOptions.SH_MSG_HISTORY.value:
                    self.ShowMsgHistory()

                case _:
                    print("Error: Unknown function!")

    def Configure(self) -> None:
        self.serverIp = input("Enter server ip: ")
        self.serverPort = int(input("Enter server port: "))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket creation

    def RegisterSensors(self) -> bool:
        print("Available sensors:")
        for sensr in SensorType:
            print(f"{sensr.value} - {sensr.name}")
        print("4 - ALL")
        selectedSensor = int(input("Select sensor to register: "))

        match selectedSensor:
            case SensorType.THERMONODE.value:
                self.SendMessage(Message(SensorType.THERMONODE, MessageType.REG))
                rcvmsg = self.ReceiveMessage()
                self.connectedSensors.append(ThermoNode(rcvmsg.token))
            case _:
                print("Error: Unknown sensor!")

        return True

    def AutoDataMsg(self) -> None:
        print("Started Automessage")
        while not self.stopBgThread.is_set():
            for sensor in self.connectedSensors:
                sensor.UpdateData()
                self.SendMessage(Message(sensor.type, MessageType.AUTO_DATA, sensor.token, sensor.battery), True)
            time.sleep(10)

    def ReceiveMessage(self) -> Message:
        data = None
        while data == None:
            data = self.sock.recv(2048) #buffer size
        rcvmsg = Message.InitFromJsonStr(str(data, encoding="utf-8"))
        self.recievedMsgs.append(rcvmsg)
        return rcvmsg

    def SendMessage(self, message: Message, inBg = False):
        if not inBg:
            self.sock.sendto(message.ToJsonStr().encode("utf8"), (self.serverIp, self.serverPort))
        else:
            self.sock.sendto(message.ToJsonStr().encode("utf8"), (self.serverIp, self.serverPort+1))

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
        print("Exited tester")

if __name__ == '__main__':
    Tester()
    