from enum import Enum

class ConnectionState(Enum):
    DISCONNECTED = 1,
    PORT_CONNECTED = 2,
    CONNECTED_TO_OIS = 3,
    ACTIVE = 4
