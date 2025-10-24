from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from Sensors import DeviceType


@dataclass
class Message(ABC):
    device: DeviceType = field(init=False)
    timestamp: datetime
    battery: int = field(default=100)
    token: int = field(default=-1)



if __name__ == '__main__':
    pass