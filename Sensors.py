import random
from abc import ABC, abstractmethod
from enum import Enum

class SensorType(Enum):
    THERMONODE = 0
    WINDSENSE = 1
    RAINDETECT = 2
    AIRQUALITYBOX = 3

class Sensor(ABC):
    def __init__(self, devType, token) -> None:
        super().__init__()
        self.type: SensorType = devType
        self.token: int = token # -1 == invalid token/not registered to server
        self.isActive: bool = True
        self.battery: int = 100

    @abstractmethod
    def UpdateData(self) -> None:
        pass

class ThermoNode(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.THERMONODE, token)
        self.temperature: float = random.uniform(-50.0, 60.0)
        self.humidity: float = random.uniform(0.0, 100.0)
        self.dewPoint: float = random.uniform(-50.0, 60.0)
        self.pressure: float = random.uniform(800.0, 1100.0)

    def UpdateData(self) -> None:
        self.temperature = random.uniform(-50.0, 60.0)
        self.humidity = random.uniform(0.0, 100.0)
        self.dewPoint = random.uniform(-50.0, 60.0)
        self.pressure = random.uniform(800.0, 1100.0)
        self.battery = max(0, self.battery-1)

class WindSense(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.WINDSENSE, token)
        self.windSpeed: float = random.uniform(0.0, 50.0)
        self.windGust: float = random.uniform(0.0, 70.0)
        self.windDir: int = random.randint(0, 359)
        self.turbulence: float = random.random()

    def UpdateData(self) -> None:
        self.windSpeed = random.uniform(0.0, 50.0)
        self.windGust = random.uniform(0.0, 70.0)
        self.windDir = random.randint(0, 359)
        self.turbulence = random.random()
        self.battery = max(0, self.battery-1)

class RainDetect(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.RAINDETECT, token)
        self.rainfall: float = random.uniform(0.0, 500.0)
        self.soilMoisture: float = random.uniform(0.0, 100.0)
        self.floodRisk: int = random.randint(0, 3)
        self.rainDuration: int = random.randint(0, 60)

    def UpdateData(self) -> None:
        self.rainfall = random.uniform(0.0, 500.0)
        self.soilMoisture = random.uniform(0.0, 100.0)
        self.floodRisk = random.randint(0, 3)
        self.rainDuration = random.randint(0, 60)
        self.battery = max(0, self.battery-1)

class AirQualityBox(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.AIRQUALITYBOX, token)
        self.co2: float = random.randint(300, 5000)
        self.ozone: float = random.uniform(0.0, 500.0)
        self.airQualityIndex: int = random.randint(0, 500)

    def UpdateData(self) -> None:
        self.co2 = random.randint(300, 5000)
        self.ozone = random.uniform(0.0, 500.0)
        self.airQualityIndex = random.randint(0, 500)
        self.battery = max(0, self.battery-1)


if __name__ == '__main__':
    sensor = ThermoNode()
    print(sensor.temperature, sensor.humidity, sensor.dewPoint, sensor.pressure)