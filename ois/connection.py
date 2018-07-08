import serial
import re
from time import sleep

from .connection_state import ConnectionState
from .data_request import DataRequest
from .data_request_type import DataRequestType

requestPattern = re.compile(".*=.*")
requests = {
    "1": DataRequest("IS_MOVING", DataRequestType.BOOLEAN),
    "2": DataRequest("MAIN_ENGINE_BURNING", DataRequestType.BOOLEAN),
    "3": DataRequest("PWR_REACTOR_ON", DataRequestType.BOOLEAN),
    "4": DataRequest("PWR_REACTOR_OFF", DataRequestType.BOOLEAN),
    "5": DataRequest("EMCON_MODE", DataRequestType.BOOLEAN),
    "6": DataRequest("STATUS_WARNING", DataRequestType.BOOLEAN),
    "7": DataRequest("STATUS_DANGER", DataRequestType.BOOLEAN),
    "8": DataRequest("STATUS_NOMINAL", DataRequestType.BOOLEAN),
    "9": DataRequest("IN_ASTEROID_FIELD", DataRequestType.BOOLEAN),
    "10": DataRequest("IN_NEBULA", DataRequestType.BOOLEAN),
    "11": DataRequest("IS_DOCKED", DataRequestType.BOOLEAN),
    "12": DataRequest("IFF_ACTIVE", DataRequestType.BOOLEAN),
    "13": DataRequest("DIRECTION", DataRequestType.NUMERIC),
    "14": DataRequest("CURRENT_SPEED", DataRequestType.NUMERIC),
    "15": DataRequest("POWER_LEVEL", DataRequestType.NUMERIC),
    "16": DataRequest("POWER_DRAIN", DataRequestType.NUMERIC),
    "17": DataRequest("UNREAD_EMAILS", DataRequestType.NUMERIC),
    "18": DataRequest("PENDING_EMAILS", DataRequestType.NUMERIC)
}

class Connection():

    def __init__(self):
        # start out disconnected
        self.state = ConnectionState.DISCONNECTED
        self.port = '/dev/ttyS4'

    def connect(self):
        self.ser = serial.Serial(self.port, 9600, timeout=1)
        self.state = ConnectionState.PORT_CONNECTED
        # Reset input buffer
        self.ser.reset_input_buffer()
        print("Port connection established to port {}. {} bytes in input buffer.".format(self.port, self.ser.in_waiting))

    def handshake(self):
        # Handshake with the OIS Game
        self.ser.reset_input_buffer()
        print("Attempting to handshake by sending 451 and waiting for 452...")
        self.ser.write(b"451\n")
        enc_line = self.ser.readline()
        line = enc_line.decode("utf-8")
        print("Received {}".format(line))

        if line == "452\n":
            print("Handshake of 452 received. Proceeding to register commands...")
            self.state = ConnectionState.CONNECTED_TO_OIS

    def sync(self):
        # Register some requests and commands
        for key, request in requests.items():
            s = request.requestType.value + "=" + request.fieldName + "," + key + "\n"
            request.key = key
            print("Sending {}".format(s))
            self.ser.write(s.encode())
            sleep(0.25)

        # Go active
        print("Sending {} to go active".format("ACT"))
        self.ser.write(b"ACT\n")
        self.state = ConnectionState.ACTIVE

    def checkStatus(self):
        print("{} bytes waiting in input buffer. Reading lines...".format(self.ser.in_waiting))
        lines = self.ser.readlines()
        print("Read {} lines".format(len(lines)))
        
        for line in lines:
            decoded_line = line.decode("utf-8")
            print("Parsing " + decoded_line)
            # Most lines are in the form x=y, where x is the key, y is the value

            if requestPattern.match(decoded_line) == None:
                print("Line doesn't match pattern. Skipping...")
                continue

            data = decoded_line.split("=")

            key = data[0]
            value = data[1]

            if key in requests:
                requests[key].value = value

        print("Status update finished.")

    def getData(self):
        return requests
