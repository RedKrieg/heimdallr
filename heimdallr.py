#!python3

import asyncio
import datetime
import discord
import json
import subprocess
import sys

# Discord client
client = discord.Client()

def check_admin(message):
    """Checks if the message is from an administrator"""
    perms = message.channel.permissions_for(message.author)
    is_admin = perms.administrator
    try:
        for role in message.author.roles:
            if "Asgardians" in role.name:
                is_admin = True
                break
    except AttributeError:
        # Bypass for redkrieg to work in private messages
        #if str(message.author.id) == "135195179219943424":
        #    is_admin = True
        pass
    return is_admin

@client.event
async def on_message(message):
    """Handles incoming messages"""
    if message.author == client.user:
        return
    if not check_admin(message):
        return
    if message.content.startswith('!bifrost'):
        default_msg = "State your business!  '!bifrost open' to open the Bifröst, '!bifrost close' to close it."
        args = message.content.split()
        if len(args) < 2:
            await message.channel.send(
                default_msg
            )
        else:
            command = args[1]
            if command == "open":
                await message.channel.send(
                    "Hold fast while I summon the Bifröst..."
                )
                try:
                    subprocess.run(["/home/vhserver/vhserver", "start"], check=True, capture_output=True)
                    await message.channel.send(
                        "The Bifröst is now open!  Good hunting."
                    )
                except subprocess.CalledProcessError as exc:
                    await message.channel.send(
                        "A terrible fate has befallen the Bifröst, I cannot open it!  Please contact <@135195179219943424>, for only he holds the keys to Asgard and the machinations which drive the Bifröst.\n\n```\n===STDOUT===\n{}\n\n===STDERROR===\n{}\n```".format(exc.stdout, exc.stderr)
                    )
            elif command == "close":
                await message.channel.send(
                    "The Bifröst closes!!!"
                )
                try:
                    subprocess.run(["/home/vhserver/vhserver", "stop"], check=True, capture_output=True)
                    await message.channel.send(
                        "The Bifröst is closed, rest well warrior."
                    )
                except subprocess.CalledProcessError as exc:
                    if exc.returncode == 2:
                        await message.channel.send("Wait, the Bifröst is already closed...")
                    else:
                        await message.channel.send(
                            "Hmm, not all is well.  I'm certain <@135195179219943424> can divine what happened from this:\n\n```\n===RC===\n{}\n===STDOUT===\n{}\n\n===STDERROR===\n{}\n```".format(exc.returncode, exc.stdout, exc.stderr)
                        )
            elif command == "status":
                result = subprocess.run(["/home/vhserver/vhserver", "monitor"], capture_output=True)
                if result.returncode == 0:
                    await message.channel.send(
                        "The Bifröst is open!!!"
                    )
                elif result.returncode == 2:
                    await message.channel.send(
                        "The Bifröst is closed, shall I open it?"
                    )
                else:
                    await message.channel.send(
                        "Something strange is afoot, the Bifröst is in an unknown state.  Perhaps <@135195179219943424> can make sense of this:\n\n```\n===RC===\n{}\n===STDOUT===\n{}\n\n===STDERROR===\n{}\n```".format(result.returncode, result.stdout, result.stderr)
                    )
            else:
                await message.channel.send(
                    default_msg
                )

@client.event
async def on_ready():
    """Print out some status info on connect"""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    sys.stdout.flush()

# Configuration
with open('token.json') as f:
    token = json.load(f)['token']
    
# Run it
client.run(token)
