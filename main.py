#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3, GLib
import psutil
import time
import json
import os


CONFIG_DIR = os.path.expanduser("~/.config/netmonitor")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


DEFAULT_CONFIG = {
    "interval": 1
}


class SettingsWindow(Gtk.Window):

    def __init__(self, app):

        super().__init__(title="Network Monitor Settings")
        self.app = app

        self.set_default_size(300, 150)
        self.set_border_width(15)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        label = Gtk.Label(label="Update Interval (seconds)")
        box.pack_start(label, False, False, 0)

        self.spin = Gtk.SpinButton()
        self.spin.set_range(1, 10)
        self.spin.set_value(self.app.config["interval"])
        self.spin.set_increments(1, 1)

        box.pack_start(self.spin, False, False, 0)

        save_btn = Gtk.Button(label="Save")
        save_btn.connect("clicked", self.save_settings)

        box.pack_start(save_btn, False, False, 0)


    def save_settings(self, widget):

        self.app.config["interval"] = int(self.spin.get_value())
        self.app.save_config()
        self.app.restart_timer()

        self.destroy()


class NetworkMonitor:

    def __init__(self):

        self.load_config()

        self.indicator = AppIndicator3.Indicator.new(
            "net-monitor",
            "network-transmit-receive",
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
        )

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()

        settings_item = Gtk.MenuItem(label="Settings")
        settings_item.connect("activate", self.open_settings)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit)

        self.menu.append(settings_item)
        self.menu.append(quit_item)

        self.menu.show_all()

        self.indicator.set_menu(self.menu)

        self.old_data = psutil.net_io_counters()
        self.old_time = time.time()

        self.timer_id = GLib.timeout_add_seconds(
            self.config["interval"],
            self.update_speed
        )


    # ---------------- Config ----------------

    def load_config(self):

        os.makedirs(CONFIG_DIR, exist_ok=True)

        if not os.path.exists(CONFIG_FILE):
            self.config = DEFAULT_CONFIG.copy()
            self.save_config()
        else:
            with open(CONFIG_FILE, "r") as f:
                self.config = json.load(f)


    def save_config(self):

        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)


    # ---------------- UI ----------------

    def open_settings(self, source):

        win = SettingsWindow(self)
        win.show_all()


    def restart_timer(self):

        if self.timer_id:
            GLib.source_remove(self.timer_id)

        self.timer_id = GLib.timeout_add_seconds(
            self.config["interval"],
            self.update_speed
        )


    # ---------------- Network ----------------

    def format_speed(self, bytes):

        if bytes < 1024:
            return f"{bytes:.0f} B/s"
        elif bytes < 1024**2:
            return f"{bytes/1024:.1f} KB/s"
        else:
            return f"{bytes/1024**2:.1f} MB/s"


    def update_speed(self):

        new_data = psutil.net_io_counters()
        new_time = time.time()

        interval = new_time - self.old_time

        download = (new_data.bytes_recv - self.old_data.bytes_recv) / interval
        upload = (new_data.bytes_sent - self.old_data.bytes_sent) / interval

        down = self.format_speed(download)
        up = self.format_speed(upload)

        self.indicator.set_label(f"↓ {down} | ↑ {up}", "")

        self.old_data = new_data
        self.old_time = new_time

        return True


    # ---------------- System ----------------

    def quit(self, source):

        Gtk.main_quit()


if __name__ == "__main__":

    app = NetworkMonitor()
    Gtk.main()

