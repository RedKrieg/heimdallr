Heimdallr - Valheim server discord bot
----

This bot is based on discord.py and uses a token you can get using the [Discord.py bot creation guide](https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro).  The second half of the page has instructions for inviting your new bot to your server.  The commands it issues are for [Linux Game Server Manager](https://linuxgsm.com/) but should be easy to adapt to other server managers.

Setup
====

Clone the heimdallr repo:

```
git clone [repo_url]
cd heimdallr
```

Configure the venv and install requirements:

```
sudo apt -y install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `token.json.example` to `token.json` and change to your bot's token:

```
cp token.json.example token.json
nano -w token.json #put your bot's token here
```

Try running your bot from the command line to ensure it works:

```
(venv) $ python heimdallr.py 
Logged in as
[your bot name]
[your unique bot id]
------
```

If the bot connected and shows online in discord, exit with Ctrl+C and configure it as a service so it starts on boot:

```
nano -w heimdallr.service #make changes here for your environment
sudo cp heimdallr.service /etc/systemd/system/heimdallr.service
sudo chown root:root /etc/systemd/system/heimdallr.service
sudo systemctl daemon-reload
sudo systemctl enable heimdallr.service
sudo systemctl start heimdallr.service
```

Usage
====

- `!bifrost open` - start the server
- `!bifrost close` - stop the server
- `!bifrost status` - check status of the server
