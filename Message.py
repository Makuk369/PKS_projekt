import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from Sensors import SensorType

class MessageType(Enum):
    REG = 0
    REGT = 1

def JsonSerializer(obj):
    if isinstance(obj, Enum):
        return obj.value               # Store enum as its value
    raise TypeError(f"Type {type(obj)} not serializable")

def GetTimestamp():
    return datetime.now().timestamp()

@dataclass
class Message():
    sensorType: SensorType
    msgType: MessageType
    token: int = field(default=-1)
    battery: int = field(default=100)
    timestamp: float = field(default_factory=GetTimestamp) # UNIX timestamp
    data: list = field(default_factory=list) #additional data

    def ToJsonStr(self) -> str:
        return json.dumps(asdict(self), default=JsonSerializer)
    
    @classmethod
    def InitFromJsonStr(cls, jsonStr: str):
        return cls(**json.loads(jsonStr)) #dict -> Message
    

if __name__ == '__main__':
    msg = Message(SensorType.THERMONODE, MessageType.REG)
    print("msg: ", msg)
    # msg.data = ["daco", 123, 3.14]
    rcv = msg.ToJsonStr()
    print("rcv: ", rcv)

    msg2 = Message.InitFromJsonStr(rcv)
    print("msg2: ", msg2)

    # msg2 = Message(SensorType.THERMONODE, MessageType.REGT, 123)
    # rcv = msg2.ToJsonStr()
    # print(rcv)
