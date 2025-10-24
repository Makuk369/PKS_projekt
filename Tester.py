import socket
from enum import Enum
from Sensors import Sensor, SensorType, ThermoNode, WindSense, RainDetect, AirQualityBox

# SERVER_IP = "192.168.0.118"
# SERVER_PORT = 50601 (client port != server port)

class FunOptions(Enum):
    EXIT = 0
    CONFIGURE = 1
    REGISTER_SENSORS = 2
    AUTO_DATA_MSG = 3

class Tester():
    def __init__(self) -> None:
        self.serverIp: str
        self.serverPort: int
        self.sock: socket.socket
        self.connectedSensors: list[Sensor] = []
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
                    self.AutoDataMsg()
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
                self.SendMessage("REG")
                if self.ReceiveMessage() == "123":
                    self.connectedSensors.append(ThermoNode(123))
            case _:
                print("Error: Unknown sensor!")

        return True

    def AutoDataMsg(self) -> None:
        self.SendMessage("test")

    def ReceiveMessage(self) -> str:
        data = None
        while data == None:
            data = self.sock.recv(1024) #buffer size is 1024 bytes
        return str(data, encoding="utf-8")

    def SendMessage(self, message: str):
        self.sock.sendto(message.encode("utf8"), (self.serverIp, self.serverPort))

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
    