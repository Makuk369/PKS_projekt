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
        self.deviceType: SensorType = devType
        self.token: int = token # -1 == invalid token/not registered to server
        self.isActive: bool = True

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
        self.temperature: float = random.uniform(-50.0, 60.0)
        self.humidity: float = random.uniform(0.0, 100.0)
        self.dewPoint: float = random.uniform(-50.0, 60.0)
        self.pressure: float = random.uniform(800.0, 1100.0)

class WindSense(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.WINDSENSE, token)
        self.windSpeed: float = random.uniform(0.0, 50.0)
        self.windGust: float = random.uniform(0.0, 70.0)
        self.windDir: int = random.randint(0, 359)
        self.turbulence: float = random.random()

    def UpdateData(self) -> None:
        self.windSpeed: float = random.uniform(0.0, 50.0)
        self.windGust: float = random.uniform(0.0, 70.0)
        self.windDir: int = random.randint(0, 359)
        self.turbulence: float = random.random()

class RainDetect(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.RAINDETECT, token)
        self.rainfall: float = random.uniform(0.0, 500.0)
        self.soilMoisture: float = random.uniform(0.0, 100.0)
        self.floodRisk: int = random.randint(0, 3)
        self.rainDuration: int = random.randint(0, 60)

    def UpdateData(self) -> None:
        self.rainfall: float = random.uniform(0.0, 500.0)
        self.soilMoisture: float = random.uniform(0.0, 100.0)
        self.floodRisk: int = random.randint(0, 3)
        self.rainDuration: int = random.randint(0, 60)

class AirQualityBox(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.AIRQUALITYBOX, token)
        self.co2: float = random.randint(300, 5000)
        self.ozone: float = random.uniform(0.0, 500.0)
        self.airQualityIndex: int = random.randint(0, 500)

    def UpdateData(self) -> None:
        self.co2: float = random.randint(300, 5000)
        self.ozone: float = random.uniform(0.0, 500.0)
        self.airQualityIndex: int = random.randint(0, 500)


if __name__ == '__main__':
    sensor = ThermoNode()
    print(sensor.temperature, sensor.humidity, sensor.dewPoint, sensor.pressure)