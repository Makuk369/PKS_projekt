from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class DeviceType(Enum):
    THERMONODE = 0
    WINDSENSE = 1
    RAINDETECT = 2
    AIRQUALITYBOX = 3


@dataclass
class Message(ABC):
    device: DeviceType = field(init=False)
    timestamp: datetime
    battery: int = field(default=100)
    token: int = field(default=-1)



if __name__ == '__main__':
    pass