import asyncio
import discord
import json


# Module imports
from src.command.set_color import set_color
from src.command.purge import purge
from src.command.remind_me import remind_me
from src.weekday.weekday_timers import time_until

# Class imports
from src.api.hearthstone import HearthstoneApis
from src.api.wow import WowApis
from src.weekday.weekday import Weekday


# Create the bot client
client = discord.Client()

# Parse the JSON files
with open('../strings/keys.json') as keys_json_file:
    keys = json.load(keys_json_file)

with open('../strings/long_strings.json') as strings_json_file:
    long_strings = json.load(strings_json_file)

# Create the API objects
#hs = HearthstoneApis(keys['hearthstone']['key'])
#wow = WowApis(keys['wow']['client_id'], keys['wow']['client_secret'])


@client.event
async def on_ready():
    """
    When the bot signs in
    """

    print(f'{client.user.name} (ID: {client.user.id}) logged in')
    print('----------------------------------------')

    # Post a message when the bot comes online
    test_channel = client.get_channel(keys['discord']['test_channel_id'])
    await test_channel.send('*T-800 ONLINE. YOUR CLOTHES, GIVE THEM TO ME. NOW.*')

    # Set the bot's "Playing" status
    await client.change_presence(activity=discord.Game('Type /help'))

    # Start the Wednesday "timer"
    #await post_wednesday()


@client.event
async def on_message(message):
    """
    When messages are posted
    """

    # Prevent the bot from responding to itself
    if message.author != client.user:

        # If someone tags the bot
        if client.user in message.mentions:
            msg = '*TALK TO THE HAND, {0.author.mention}.*'.format(message)
            await message.channel.send(msg)

        # If someone says "fake news"
        if 'fake news' in message.content.lower():
            await message.add_reaction(client.get_emoji(keys['discord']['fake_news_emoji_id']))

        # If someone says "Kel'Thuzad"
        if 'kel\'thuzad' in message.content.lower():
            await message.channel.send(long_strings['kel\'thuzad'])

        # Check for commands
        if message.content.startswith('/help'):
            await message.channel.send('\n'.join(long_strings['help']))

        elif message.content.startswith('/purge'):
            await purge(message)

        elif message.content.startswith("/remindme"):
            await remind_me(message)

        '''
        elif message.content.startswith("/color"):
            await set_color(client, message)

        elif message.content.startswith("/ilevel") or message.content.startswith("/ilvl"):
            await parse_wow(message, wow.item_level)

        elif message.content.startswith("/mplus"):
            await parse_wow(message, wow.mythic_plus)

        elif message.content.startswith("/wow"):
            await parse_wow(message, wow.all)

        elif message.content.startswith("/affixes"):
            msg = wow.affixes()
            await client.send_message(message.channel, msg)

        elif message.content.startswith("/card") or message.content.startswith("/hs"):
            await hearthstone_card(message)


async def post_wednesday():
    """
    Sleeps until Wednesday, posts a link, then repeats
    """

    wait_time = time_until(Weekday.WEDNESDAY)
    await asyncio.sleep(wait_time)

    await client.send_message(client.get_channel(keys["discord"]["general_channel_id"]),
                              "http://i1.kym-cdn.com/photos/images/newsfeed/001/091/264/665.jpg")

    await post_wednesday()


async def parse_wow(message, function):
    """
    Splits a message into ["/ilevel", <character>, <server>]
    Calls the passed-in WowApis function and posts the results
    """

    command = message.content.split(" ")

    # If valid number of args
    if len(command) == 3:

        # Make the API call, which handles invalid input
        await client.send_message(message.channel, function(command[1], command[2]))

    else:
        await client.send_message(message.channel, "Error: Invalid number of arguments")


async def hearthstone_card(message):
    """
    Splits a message into ["/card", <card>]
    Calls HearthstoneApis.card() for the API call and results
    """

    command = message.content.split(" ")

    # If valid number of args
    if len(command) >= 2:

        # Make the API call, which handles invalid input
        await client.send_message(message.channel, hs.card(" ".join(command[1:])))

    else:
        await client.send_message(message.channel, "Error: Invalid number of arguments")'''


client.run(keys['discord']['token'])
