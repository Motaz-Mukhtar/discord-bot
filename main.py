import discord
import os
import requests
import asyncio
from dotenv import load_dotenv

load_dotenv()


FRIEND_ID = int(os.getenv("FRIEND_ID"))

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


TOKEN= os.getenv("TOKEN")

aternos_username= os.getenv("aternos_username")
aternos_server= os.getenv("aternos_server")



client = discord.Client(intents=discord.Intents.all())

async def getting_channel(id):
    channel = client.get_channel(CHANNEL_ID)
    print(channel)
    return channel


async def check_server_status():
    notified_online = False
    notified_offline = False

    while True:
        try:
            response = requests.get(f"https://api.mcsrvstat.us/2/{aternos_server}")
            data = response.json()
            #print(data)
            #print(data['motd']['clean'])
            channel = await client.fetch_channel(CHANNEL_ID)

            if data["online"]:
                print("✅ Server is online!")
                if not notified_online:
                    await channel.send(f"@everyone The Minecraft server `{aternos_server}` **{data['version']}**.")
                    notified_online = True
                    notified_offline = False
            else:
                print("❌ Server is offline.")
                if not notified_offline:
                    await channel.send(f"@everyone The Minecraft server `{aternos_server}` **{data['version']}**.")
                    notified_offline = True
                    notified_online = False

        except Exception as e:
            print("Error checking server status:", e)

        await asyncio.sleep(60)  # Check every 60 seconds


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await check_server_status()

client.run(TOKEN)
