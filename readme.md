# IoT Desk Controller
Code to provide local controls for the Arup IoT desk. Utilises the tinkerforge hardware stack.

## Hardware
Intended to run on a tinkerforge redbrick but can run anywhere so long as you can connect to the tinkerforge stack over a network.

Will auto-detect bricklets compatible with the code and provide sensor readings / control of relays on a 128x64 OLED - joystick or multitouch can be used to navigate the menu.

## Installation
Requires python-cryptography (use apt-get over pip)
Install pip dependancies
Testing:
Start with ./python controller.py

Installation on Redbrick / Debian Jessie:
```
sudo cp deskcontrol /etc/init.d/deskcontrol
sudo update-rc.d deskcontrol defaults
sudo service deskcontrol start
```

## ToDo
* Add menu items to disable/change motion detection timer (currently 10 mins)
* Implement lighting control functionality (protocol tbc)

## Credits
Ben Hussey <ben.hussey@arup.com>
