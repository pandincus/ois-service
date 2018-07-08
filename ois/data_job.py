from .connection import Connection
from .connection_state import ConnectionState

def run(connection):
    if connection.state == ConnectionState.DISCONNECTED:
        print("Connection is {}. Trying to establish...".format(connection.state))

        connection.connect()
        return

    if connection.state == ConnectionState.PORT_CONNECTED:
        print("Connection is {}. Trying to handshake...".format(connection.state))

        connection.handshake()
        return

    if connection.state == ConnectionState.CONNECTED_TO_OIS:
        print("Connection is {}. Trying to sync...".format(connection.state))

        connection.sync()
        return

    if connection.state == ConnectionState.ACTIVE:
        print("Connection is {}. Performing status update...".format(connection.state))

        connection.checkStatus()

        return

    print("WARN: Unknown connetion state {}".format(connection.state))
