# DiscordBotV2
## A modular Discord bot for tracking and analyzing FIRST Robotics Competition (FRC) team performance using Statbotics and The Blue Alliance (TBA) APIs.

## Features
- TBA, Statbotics, & Google Sheets integration
- JSON data caching & easy cache management
- Easy to use slash commands

## Setup
There are a few options with the setup. I set this up on an Oracle Cloud VM, but it runs just as well on a local machine, Raspberry Pi, or similar.
With this in mind, here is the setup instructions using an Oracle Cloud VM
1. Download the contents of this repository
2. Create a Google service account: https://cloud.google.com/iam/docs/service-accounts-create
3. Download the service account key and save it to the project folder as credentials.json
4. Create a discord application: https://discordpy.readthedocs.io/en/stable/discord.html
5. Create and Oracle Cloud account
6. Once you have your Oracle Cloud account, you will need to create a new instance by following these instructions: https://docs.oracle.com/en/learn/first-oci-linux-instance/index.html
7. Install PuTTy and WinSCP
   * https://winscp.net/eng/index.php
   * https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
8. Convert your Oracle VM key into a .ppk using PuTTyGen
9. Log into your VM with PuTTy using your converted .ppk and VM ip address

![PuTTyIp](/screenshots/PuTTyIp.png)
![PuTTyAuth](/screenshots/PuTTyAuth.png)
10. login as opc and install Python by running: ```sudo apt install python3 python3-pip```
11. verify the installation by running: ```python3 --version pip3 --version```
12. install the required dependencies by running: ```pip install statbotics python-dotenv gspread discord-py audioop-lts```
13. connect over WinSCP with the VM IP, Auth key, and username

![WinSCPIp](/screenshots/WinSCPIp.png)
![WinSCPAuth](/screenshots/WinSCPAuth.png)
14. open the Python-3.x.x folder and create a new folder, rename it discordbot, and transfer the project files into it
15. Back on PuTTy, run: ```sudo nano /etc/systemd/system/discord-bot.service```
16. copy and paste this into nano:
```
[Unit]
Description=Discord Bot
After=network.target

[Service]
User=opc
WorkingDirectory=/home/opc/Python-3.13.0/discordbot
ExecStart=/usr/bin/python3 /home/opc/Python-3.13.0/discordbot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```
17. press Ctrl + O to save, enter and Ctrl + X to exit nano
18. then run: ```sudo systemctl start discord-bot.service``` and ```sudo systemctl status discord-bot.service```