# 🌐 NetMonitor – Linux Network Speed Indicator

NetMonitor is a lightweight and simple network speed monitor for Linux desktops.  
It displays real-time download and upload speed directly in the system panel.

---

## ✨ Features

- Real-time upload & download speed
- Panel / tray integration
- Auto start on login
- Settings window
- Lightweight and fast
- Open source

---

## 🖥 Supported Systems

- Ubuntu 20.04+
- Ubuntu 22.04+
- Ubuntu 24.04+

---

## 📦 Installation (Using .deb)

1. Download `.deb` from:
   https://github.com/125Akash/netmonitor-linux/releases

2. Install:

```bash
1 sudo dpkg -i netmonitor_1.0.0.deb

▶ Run From Source
git clone https://github.com/125Akash/netmonitor-linux.git
cd netmonitor-linux
python3 main.py

⚙️ Settings

Right click tray → Settings
Change refresh time.

Config stored in:

~/.config/netmonitor/

🗑 Uninstall
sudo apt remove netmonitor
rm -rf ~/.config/netmonitor

🛠 Technologies

Python 3

GTK

AppIndicator

psutil

Cairo

🚀 Future Plans

Graph view

Dark mode

Interface selection

Data usage stats

👨‍💻 Author

Akash
GitHub: https://github.com/125Akash

Email: sabeakash125@gmail.com

⭐ Support

Star the repo if you like it ❤️
