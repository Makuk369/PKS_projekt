import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from Sensors import SensorType

class MessageType(Enum):
    REG = 0

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
    token: int = field(default=-1)
    battery: int = field(default=100)
    timestamp: datetime = field(default=datetime.now())
    data: list = field(default_factory=list) #additional data

    def ToJson(self) -> None:
        with open("msg.json", "w") as f:
            json.dump(asdict(self), f, default=JsonSerializer, indent=4)

    def FromJson(self) -> dict:
        with open("msg.json", "r") as f:
            data = json.load(f)
            return data
    

if __name__ == '__main__':
    msg = Message(SensorType.THERMONODE, MessageType.REG)
    # msg.data = ["daco", 123, 3.14]
    msg.ToJson()
    rcv = msg.FromJson()
    print(rcv)