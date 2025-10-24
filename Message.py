import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from Sensors import SensorType

class MessageType(Enum):
    REGISTRATION = 0
    DEREGISTRATION = 1

def JsonSerializer(obj):
    if isinstance(obj, Enum):
        return obj.value               # Store enum as its value
    if isinstance(obj, datetime):
        return obj.isoformat()        # Store datetime as ISO string
    raise TypeError(f"Type {type(obj)} not serializable")

@dataclass
class Message():
    sensorType: SensorType
    msgType: MessageType
    timestamp: datetime = field(default=datetime.now())
    battery: int = field(default=100)
    token: int = field(default=-1)

    def ToJson(self) -> None:
        with open("msg.json", "w") as f:
            json.dump(asdict(self), f, default=JsonSerializer, indent=4)

    # @abstractmethod
    def FromJson(self) -> dict:
        with open("msg.json", "r") as f:
            data = json.load(f)
            return data

# @dataclass
# class RegistrationMsg(Message):
#     def __post_init__(self) -> None:
#         self.msgType = MessageType.REGISTRATION

    # def ToJson(self) -> None:
    #     with open("msg.json", "w") as f:
    #         json.dump(asdict(self), f, default=JsonSerializer, indent=4)

    # def FromJson(self) -> None:
    #     pass
    

if __name__ == '__main__':
    msg = Message(SensorType.THERMONODE, MessageType.REGISTRATION)
    msg.ToJson()
    rcv = msg.FromJson()
    print(rcv)