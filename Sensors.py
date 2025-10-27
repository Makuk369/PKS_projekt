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
        # self.isLowBattery: bool = False

    @abstractmethod
    def UpdateData(self) -> None:
        pass

    @abstractmethod
    def GetData(self) -> dict[str, float | int]:
        pass


class ThermoNode(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.THERMONODE, token)
        self.temperature: float = round(random.uniform(-50.0, 60.0), 1)
        self.humidity: float = round(random.uniform(0.0, 100.0), 1)
        self.dewPoint: float = round(random.uniform(-50.0, 60.0), 1)
        self.pressure: float = round(random.uniform(800.0, 1100.0), 2)

    def UpdateData(self) -> None:
        self.temperature = round(random.uniform(-50.0, 60.0), 1)
        self.humidity = round(random.uniform(0.0, 100.0), 1)
        self.dewPoint = round(random.uniform(-50.0, 60.0), 1)
        self.pressure = round(random.uniform(800.0, 1100.0), 2)

    def GetData(self) -> dict[str, float | int]:
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "dewPoint": self.dewPoint,
            "pressure": self.pressure
        }

class WindSense(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.WINDSENSE, token)
        self.windSpeed: float = round(random.uniform(0.0, 50.0), 1)
        self.windGust: float = round(random.uniform(0.0, 70.0), 1)
        self.windDir: int = random.randint(0, 359)
        self.turbulence: float = round(random.random(), 1)

    def UpdateData(self) -> None:
        self.windSpeed = round(random.uniform(0.0, 50.0), 1)
        self.windGust = round(random.uniform(0.0, 70.0), 1)
        self.windDir = random.randint(0, 359)
        self.turbulence = round(random.random(), 1)

    def GetData(self) -> dict[str, float | int]:
        return {
            "windSpeed": self.windSpeed,
            "windGust": self.windGust,
            "windDir": self.windDir,
            "turbulence": self.turbulence
        }

class RainDetect(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.RAINDETECT, token)
        self.rainfall: float = round(random.uniform(0.0, 500.0), 1)
        self.soilMoisture: float = round(random.uniform(0.0, 100.0), 1)
        self.floodRisk: int = random.randint(0, 3)
        self.rainDuration: int = random.randint(0, 60)

    def UpdateData(self) -> None:
        self.rainfall = round(random.uniform(0.0, 500.0), 1)
        self.soilMoisture = round(random.uniform(0.0, 100.0), 1)
        self.floodRisk = random.randint(0, 3)
        self.rainDuration = random.randint(0, 60)

    def GetData(self) -> dict[str, float | int]:
        return {
            "rainfall": self.rainfall,
            "soilMoisture": self.soilMoisture,
            "floodRisk": self.floodRisk,
            "rainDuration": self.rainDuration
        }

class AirQualityBox(Sensor):
    def __init__(self, token = -1) -> None:
        super().__init__(SensorType.AIRQUALITYBOX, token)
        self.co2: int = random.randint(300, 5000)
        self.ozone: float = round(random.uniform(0.0, 500.0), 1)
        self.airQualityIndex: int = random.randint(0, 500)

    def UpdateData(self) -> None:
        self.co2 = random.randint(300, 5000)
        self.ozone = round(random.uniform(0.0, 500.0), 1)
        self.airQualityIndex = random.randint(0, 500)

    def GetData(self) -> dict[str, float | int]:
        return {
            "co2": self.co2,
            "ozone": self.ozone,
            "airQualityIndex": self.airQualityIndex
        }


if __name__ == '__main__':
    sensor = ThermoNode()
    print(sensor.temperature, sensor.humidity, sensor.dewPoint, sensor.pressure)