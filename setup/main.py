#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim:set et sts=4 sw=4:
#
# ibus-array - The Array 30 Engine for IBus
#
# Copyright (c) 2009 Yu-Chun Wang <mainlander1122@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 
import sys
import os
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import IBus
import gettext
import config

class Setup:
    def __init__(self, bus):
        self.__bus = bus 
        self.__config = self.__bus.get_config()
        self.__config.connect("value-changed", self.on_value_changed, None)
        self.__create_ui()

    def __create_ui(self):
        self.__window = Gtk.Dialog('ibus-array setup', None, 
                                    Gtk.DialogFlags.MODAL, 
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
                                     Gtk.STOCK_OK, Gtk.ResponseType.OK)
                                  )
        icon_file = os.path.join(config.datadir, "ibus-array", "icons", "ibus-array.png")
        self.__window.set_icon_from_file(icon_file)
        self.__special_notify_button = Gtk.CheckButton("Special Code Notification")
        self.__window.vbox.pack_start(self.__special_notify_button, True, True, 10)
        self.__special_only_button = Gtk.CheckButton("Speical Code Only Mode")
        self.__window.vbox.pack_start(self.__special_only_button, True, True ,10)

        current_special_mode = self.__read("SpecialOnly", "0")
        current_special_notify = self.__read("SpecialNotify", "0")

        if current_special_notify == "1":
            self.__special_notify_button.set_active(True)
        if current_special_mode == "1":
            self.__special_only_button.set_active(True)

        self.__window.show_all()

    def run(self):
        res = self.__window.run()
        if res == Gtk.ResponseType.OK:
            self.apply()
        self.__window.destroy()

    def apply(self):
        select_special_notify = self.__special_notify_button.get_active()
        select_special_mode = self.__special_only_button.get_active()

        if select_special_notify:
            self.__write("SpecialNotify", GLib.Variant.new_string("1"))
        else:
            self.__write("SpecialNotify", GLib.Variant.new_string("0"))
        if select_special_mode:
            self.__write("SpecialOnly", GLib.Variant.new_string("1"))
        else:
            self.__write("SpecialOnly", GLib.Variant.new_string("0"))

    def on_value_changed(self, config, section, name, value, data):
        if section == 'engine/Array':
            if name == 'SpecialNotify':
                if value == '1':
                    self.__special_notify_button.set_active(True)
                else:
                    self.__special_notify_button.set_active(False)
            elif name == 'SpecialOnly':
                if value == '1':
                    self.__special_notify_button.set_active(True)
                else:
                    self.__special_notify_button.set_active(False)

    def __read(self, name, v):
	value = self.__config.get_value("engine/Array", name)
	if value is None:
		return v
        return value

    def __write(self, name, v):
        return self.__config.set_value("engine/Array", name, v)

if __name__ == '__main__':
    bus = IBus.Bus()
    if bus.is_connected():
        Setup(bus).run()
