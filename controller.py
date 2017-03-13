#!/usr/bin/env python
#  Arup IoT Desk Controller
#  Ben Hussey <ben.hussey@arup.com> - March 2017

import sched
import time
from tinkerforge.ip_connection import IPConnection
from config import *


class Controller:
    ipcon = None
    current_module = None
    previous_module = None
    screen = None

    modules = {}
    ticklist = []

    scheduler = sched.scheduler(time.time, time.sleep)

    def __init__(self, ipcon):
        self.ipcon = ipcon

        for module in MODULES:
            self.add_module(module)

        if self.modules["MenuModule"]:
            for module in MENU_MODULES:
                self.add_module(module)
                self.modules["MenuModule"].add_menu_item(
                    self.modules[module[0]])

        self.ipcon.register_callback(
            IPConnection.CALLBACK_ENUMERATE, self.assign_bricklets)
        self.ipcon.enumerate()

    def add_module(self, module):
        self.modules[module[0]] = getattr(__import__(
            module[1], fromlist=[module[0]]), module[0])(self)
        if self.modules[module[0]].always_tick:
            self.ticklist.append(module[0])
        print "initialised " + module[0]

    def tick(self):
        if self.current_module:
            self.current_module.tick()
        for module in self.ticklist:
            self.modules[module].tick()
        self.scheduler.enter(1, 1, desk.tick, (),)

    def get_current_module(self):
        return self.current_module

    def change_module(self, module):
        if self.current_module:
            self.previous_module = self.current_module
        if module in self.modules:
            print "changing to " + module
            self.current_module = self.modules[module]
        self.current_module.draw()

    def prev_module(self):
        if self.previous_module:
            self.change_module(self.previous_module.id)
        else:
            self.change_module("MenuModule")

    def navigate(self, direction):
        if direction not in ["forward", "back", "up", "down", "enter"]:
            return
        if self.current_module:
            self.current_module.navigate(direction)
        else:
            self.change_module("MenuModule")

    def assign_bricklets(self, uid, connected_uid, position, hardware_version,
                         firmware_version, device_identifier,
                         enumeration_type):
        if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
            return
        for state in self.modules:
            self.modules[state].try_bricklet(uid, device_identifier, position)


if __name__ == "__main__":
    ipcon = IPConnection()
    ipcon.connect(HOST, PORT)
    desk = Controller(ipcon)
    desk.tick()
    desk.scheduler.run()
    ipcon.disconnect()
