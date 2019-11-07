import asyncio
import discord
import json
import sys

# Windows and AWS Ubuntu paths
sys.path.append('C:\\Users\\mqune\\OneDrive\\Documents\\Code\\PycharmProjects\\T-800')
#sys.path.append('/home/ubuntu/T-800')

# Module imports
from src.command.set_color import set_color
from src.command.purge import purge
from src.command.remind_me import remind_me
from src.weekday.weekday_timers import time_until

# Class imports
from src.api.hearthstone import HearthstoneApis
from src.api.wow import WowApis
from src.logger import Logger
from src.weekday.weekday import Weekday


class T800(discord.Client):
    def __init__(self):
        super().__init__()

        # Parse the JSON files
        with open('../strings/keys.json') as keys_json_file:
            self.keys = json.load(keys_json_file)

        with open('../strings/long_strings.json') as strings_json_file:
            self.long_strings = json.load(strings_json_file)

        # Create the API objects
        self.hs = HearthstoneApis(self.keys['hearthstone']['key'])
        self.wow = WowApis(self.keys['wow']['client_id'], self.keys['wow']['client_secret'])
        self.logger = Logger()


    async def on_ready(self):
        """
        When the bot signs in
        """
        print(f'{self.user.name} (ID: {self.user.id}) logged in')
        print('----------------------------------------')

        # Post a message when the bot comes online
        test_channel = self.get_channel(self.keys['discord']['test_channel_id'])
        await test_channel.send('*T-800 ONLINE. YOUR CLOTHES, GIVE THEM TO ME. NOW.*')

        # Set the bot's "Playing" status
        await self.change_presence(activity=discord.Game('Type /help'))

        # Start the Wednesday "timer"
        #await post_wednesday()


    async def on_message(self, message):
        """
        When a message is posted
        """

        # Prevent the bot from responding to itself
        if message.author != self.user:

            # If someone tags the bot
            if self.user in message.mentions:
                msg = '*TALK TO THE HAND, {0.author.mention}.*'.format(message)
                await message.channel.send(msg)

            # If someone says "fake news"
            if 'fake news' in message.content.lower():
                await message.add_reaction(self.get_emoji(self.keys['discord']['fake_news_emoji_id']))

            # If someone says "Kel'Thuzad"
            if 'kel\'thuzad' in message.content.lower():
                await message.channel.send(self.long_strings['kel\'thuzad'])

            # Check for commands
            if message.content.startswith('/help'):
                await message.channel.send('\n'.join(self.long_strings['help']))

            elif message.content.startswith('/purge'):
                await purge(message)

            elif message.content.startswith('/remindme'):
                await remind_me(message)

            elif message.content.startswith('/color'):
                await set_color(message, self.keys['discord']['color_roles'])

            elif message.content.startswith('/ilevel') or message.content.startswith('/ilvl'):
                await self.parse_wow(message, self.wow.item_level)

            elif message.content.startswith('/mplus'):
                await self.parse_wow(message, self.wow.mythic_plus)

            elif message.content.startswith('/wow'):
                await self.parse_wow(message, self.wow.all)

            elif message.content.startswith('/affixes'):
                await message.channel.send(self.wow.affixes())

            elif message.content.startswith('/card') or message.content.startswith('/hs'):
                await self.hearthstone_card(message)


    async def on_message_delete(self, message):
        log_channel = self.get_channel(self.keys['discord']['log_channel_id'])
        await log_channel.send(f'Someone deleted `{message.author}: {message.content}`')


    async def on_message_edit(self, before, after):
        log_channel = self.get_channel(self.keys['discord']['log_channel_id'])
        if before.content != after.content:
            await log_channel.send(f'{before.author} edited `{before.content}` to `{after.content}`')


    async def on_reaction_add(self, reaction, user):
        self.logger.add_reaction(user, reaction)


    async def on_reaction_remove(self, reaction, user):
        result = self.logger.remove_reaction(user, reaction)

        if result:
            log_channel = self.get_channel(self.keys['discord']['log_channel_id'])
            await log_channel.send(result)


    async def on_voice_state_update(self, member, before, after):
        log_channel = self.get_channel(self.keys['discord']['log_channel_id'])

        # Only check if the channel was changed (ignores VoiceState changes like muting/unmuting)
        if before.channel != after.channel:

            # When someone disconnects from a channel
            if before.channel is not None:
                result = self.logger.disconnect_voice(member, before.channel)
                if result:
                    await log_channel.send(result)

            # When someone connects to a channel
            if after.channel is not None:
                self.logger.connect_voice(member, after.channel)


    async def post_wednesday(self):
        """
        Sleeps until Wednesday, posts a link, then repeats
        """

        wait_time = time_until(Weekday.WEDNESDAY)
        await asyncio.sleep(wait_time)

        link = self.keys['discord']['wednesday_img']
        await self.get_channel(self.keys['discord']['wednesday_channel_id']).send(link)

        await self.post_wednesday()


    async def parse_wow(self, message, function):
        """
        Splits a message into ["/ilevel", <character>, <server>]
        Calls the passed-in WowApis function and posts the results
        """

        command = message.content.split(' ')

        # If valid number of args
        if len(command) == 3:

            # Make the API call, which handles invalid input
            await message.channel.send(function(command[1], command[2]))

        else:
            await message.channel.send('Error: Invalid number of arguments')


    async def hearthstone_card(self, message):
        """
        Splits a message into ["/card", <card>]
        Calls HearthstoneApis.card() for the API call and results
        """

        command = message.content.split(" ")

        # If valid number of args
        if len(command) >= 2:

            # Make the API call, which handles invalid input
            await message.channel.send(self.hs.card(' '.join(command[1:])))

        else:
            await message.channel.send('Error: Invalid number of arguments')


    def run(self):
        super().run(self.keys['discord']['token'])