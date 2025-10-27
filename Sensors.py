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

    @abstractmethod
    def SetData(self) -> None:
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
    
    def SetData(self) -> None:
        while True:
            try:
                self.temperature = float(input("Temperature [-50.0, 60.0]: "))
                self.temperature = round(self.temperature, 1)
                if self.temperature <= -50.0 or self.temperature >= 60.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.humidity = float(input("Humidity [0.0, 100.0]: "))
                self.humidity = round(self.humidity, 1)
                if self.humidity <= 0.0 or self.humidity >= 100.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.dewPoint = float(input("DewPoint [-50.0, 60.0]: "))
                self.dewPoint = round(self.dewPoint, 1)
                if self.dewPoint <= -50.0 or self.dewPoint >= 60.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.pressure = float(input("Pressure [800.0, 1100.0]: "))
                self.pressure = round(self.pressure, 2)
                if self.pressure <= 800.0 or self.pressure >= 1100.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue

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
    
    def SetData(self) -> None:
        while True:
            try:
                self.windSpeed = float(input("WindSpeed [0.0, 50.0]: "))
                self.windSpeed = round(self.windSpeed, 1)
                if self.windSpeed <= 0.0 or self.windSpeed >= 50.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.windGust = float(input("WindGust [0.0, 70.0]: "))
                self.windGust = round(self.windGust, 1)
                if self.windGust <= 0.0 or self.windGust >= 70.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.windDir = int(input("WindDir [0, 359]: "))
                if self.windDir <= 0 or self.windDir >= 359:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.turbulence = float(input("Turbulence [0.0, 1.0]: "))
                self.turbulence = round(self.turbulence, 1)
                if self.turbulence <= 0.0 or self.turbulence >= 1.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue

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
    
    def SetData(self) -> None:
        while True:
            try:
                self.rainfall = float(input("Rainfall [0.0, 500.0]: "))
                self.rainfall = round(self.rainfall, 1)
                if self.rainfall <= 0.0 or self.rainfall >= 500.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.soilMoisture = float(input("SoilMoisture [0.0, 100.0]: "))
                self.soilMoisture = round(self.soilMoisture, 1)
                if self.soilMoisture <= 0.0 or self.soilMoisture >= 100.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.floodRisk = int(input("FloodRisk [0, 3]: "))
                if self.floodRisk <= 0 or self.floodRisk >= 3:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.rainDuration = int(input("RainDuration [0, 60]: "))
                if self.rainDuration <= 0 or self.rainDuration >= 60:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue

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
    
    def SetData(self) -> None:
        while True:
            try:
                self.co2 = int(input("CO2 [300, 5000]: "))
                if self.co2 <= 300 or self.co2 >= 5000:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.ozone = float(input("Ozone [0.0, 500.0]: "))
                self.ozone = round(self.ozone, 1)
                if self.ozone <= 0.0 or self.ozone >= 500.0:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue
        while True:
            try:
                self.airQualityIndex = int(input("AirQualityIndex [0, 500]: "))
                if self.airQualityIndex <= 0 or self.airQualityIndex >= 500:
                    print("Error: Value out of bounds!")
                    continue
                break
            except:
                print("Error: Unknown value!")
                continue

if __name__ == '__main__':
    sensor = ThermoNode()
    sensor.SetData()
    print(sensor.temperature, sensor.humidity, sensor.dewPoint, sensor.pressure)