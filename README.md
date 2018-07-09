# ois-service

A little service API for the space game "Objects In Space".

This is completely a toy project at the moment, and will likely remain so for some time :-)

# about

Objects In Space is a indie early-access "modempunk" space game that takes a submarine-like approach to space navigation and combat.
Take a look here: https://store.steampowered.com/app/824070/Objects_in_Space/

The developers have exposed a Serial Data Protocol for the game.
The main intention is to allow folsk to build Arduino-esque hardware controls/indicators for the game.
You can actually control quite a bit of your spacecraft just from these controllers.

I am not really into hardware, but I liked the idea of plugging into this protocol from software and taking a look at it.
I have some future plans as well :-)

This is a simple Python Flask app that, when started, runs a background thread that attempts to connect to a virtual COM port.
Once it receives the handshake from OIS, it registers a few commands and starts listening for updates.

If you browse to the HTTP server running on http://127.0.0.1:5000/, you'll be presented with a (currently) unstyled collection of data values.

# usage

You first need to set up a virtual com port pair on your computer.
I used [com0com](http://com0com.sourceforge.net/) for this and created a pair of COM3 and COM4.
The app (for now) is hard-coded to connect to COM4, but that's easy to change.

To start the app:

```
pipenv shell
export FLASK_APP=./ois/index.py
flask run -h 0.0.0.0
```

Once it starts, it'll begin listening for a 452 response on its paired COM port:

```
(ois-service-ZM92vDb9) --- ~/ois-service ‹master› » export FLASK_APP=./ois/index.py
(ois-service-ZM92vDb9) --- ~/ois-service ‹master› » flask run -h 0.0.0.0
 * Serving Flask app "./ois/index.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
Connection is ConnectionState.DISCONNECTED. Trying to establish...
Port connection established to port /dev/ttyS4. 0 bytes in input buffer.
Connection is ConnectionState.PORT_CONNECTED. Trying to handshake...
Attempting to handshake by sending 451 and waiting for 452...
```

At this point, go ahead and start Objects In Space, which should start listening on COM3 right away (assuming you've changed the config file to enable hardware).
Once you enter a ship, you should start seeing updates.

I'm using Bash on Ubuntu for Windows, so YMMV on like ... how it all works.
But please let me know and feel free to submit change requests.

# troubleshooting

## permission error connecting to port

You may need to open up perms to the port:

```
sudo chmod 666 /dev/ttyS4
```

Try that and see if it's able to connect.
