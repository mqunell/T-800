import discord
import asyncio
from wow_apis import WowApis
from hearthstone_apis import HearthstoneApis


# Create the bot client
client = discord.Client()

# Create the API objects
wow = WowApis()
hs = HearthstoneApis()


@client.event
async def on_ready():
    """
    When the bot signs in
    """

    print("%s (ID: %s) logged in" % (client.user.name, client.user.id))
    print("----------------------------------------")

    # Get the "bot_testing" chat channel id
    id_file = open("../secret/channel_id", "r")
    channel_id = id_file.read().strip()
    id_file.close()

    # Post a message when the bot comes online
    msg = "*T-800 ONLINE. YOUR CLOTHES, GIVE THEM TO ME. NOW.*"
    await client.send_message(client.get_channel(channel_id), msg)

    # Set the bot's "Playing" status
    await client.change_presence(game=discord.Game(name="Type /help"))


@client.event
async def on_message(message):
    """
    When messages are posted
    """

    # Prevent the bot from responding to itself
    if message.author != client.user:

        # If someone tags the bot
        if client.user in message.mentions:
            msg = "*TALK TO THE HAND, {0.author.mention}.*".format(message)
            await client.send_message(message.channel, msg)

        # If someone says "fake news"
        if "fake news" in message.content.lower():
            fake_news_emoji = discord.Emoji(name="fakenews", id="377290554909917186", server=message.server)
            await client.add_reaction(message, fake_news_emoji)

        # If someone calls "/help"
        if message.content.startswith("/help"):
            await help(message)

        # If someone calls "/purge"
        if message.content.startswith("/purge"):
            await purge(message)

        # If someone calls "/remindme"
        if message.content.startswith("/remindme"):
            await remind_me(message)

        # If someone calls "/ilevel" or "/ilvl"
        if message.content.startswith("/ilevel") or message.content.startswith("/ilvl"):
            await wow_item_level(message)

        # If someone calls "/mplus"
        if message.content.startswith("/mplus"):
            await wow_mythic_plus(message)

        # If someone calls "/card" or "/hs"
        if message.content.startswith("/card") or message.content.startswith("/hs"):
            await hearthstone_card(message)


async def help(message):
    """
    Writes what the bot can do
    """

    msg = "*I AM A HIGHLY CAPABLE MACHINE. THESE ARE MY FUNCTIONS:*\n\n"

    msg += "Reminders\n```"
    msg += "Command: /remindme <minutes (1-60)> <message>\n"
    msg += "Example: /remindme 30 Make something for dinner\n"
    msg += "```\n"

    msg += "WoW item levels\n```"
    msg += "Command: /ilevel <character name> <server>\n"
    msg += "Shorter: /ilvl ...\n"
    msg += "Example: /ilevel Matchi Shadowsong\n"
    msg += "```\n"

    msg += "WoW Mythic Plus\n```"
    msg += "Command: /mplus <character name> <server>\n"
    msg += "Example: /mplus Matchi Shadowsong\n"
    msg += "```\n"

    msg += "Hearthstone cards\n```"
    msg += "Command: /hearthstone <card name>\n"
    msg += "Shorter: /card ...\n"
    msg += "Example: /hearthstone Illidan\n"
    msg += "```"

    await client.send_message(message.channel, msg)


async def purge(message):
    """
    Splits a message into ["/purge", <num_messages>]
    Remove up to <num_messages> most recent messages
    """

    # If the author is an administrator
    if message.channel.permissions_for(message.author).administrator:

        command = message.content.split(" ")
        error_msg = ""

        # If valid number of args
        if len(command) == 2:

            # Attempt to parse <num_messages>
            num_messages = parse_int(command[1])

            # If valid <num_messages>
            if num_messages > 0:

                # Attempt to remove <num_messages> messages
                try:
                    # Remove (<num_messages> + 1) messages, which accounts for the command
                    removed_messages = await client.purge_from(message.channel, limit=(num_messages + 1))

                    # Post a results message
                    num_removed = len(removed_messages) - 1
                    results_message = "*%d MESSAGE%s REMOVED.*" % (num_removed, "S" if num_removed > 1 else "")
                    await client.send_message(message.channel, results_message)

                except:
                    await client.send_message(message.channel, "Invalid <num_messages>; some may be too old")

            else:
                error_msg = "Invalid <num_messages>; must be [1, 100]"

        else:
            error_msg = "Invalid number of arguments"

        # Post an error message, if necessary
        if error_msg is not "":
            await client.send_message(message.channel, "Error: %s" % error_msg)


async def remind_me(message):
    """
    Splits a message into ["/remindme", <minutes>, <message>]
    After <minutes>, mention the author and post <message>
    Note: <message> could be multiple strings, so join() is used
    """

    command = message.content.split(" ")
    error_msg = ""

    # If valid number of args
    if len(command) >= 3:

        # Attempt to parse <minutes>
        minutes = parse_int(command[1])

        # If valid number of <minutes>
        if 1 <= minutes <= 60:
            # Create the messages (*'s for Discord italics)
            author = "*{0.author.mention}".format(message)
            confirmation = author + (": I WILL REMIND YOU OF THAT IN %d MINUTE%s.*" % (minutes,
                                                                                       "S" if minutes > 1 else ""))
            reminder = author + (": \"%s\"*" % " ".join(command[2:]))

            # Post the confirmation immediately, and the reminder later
            await client.send_message(message.channel, confirmation)
            await asyncio.sleep(minutes * 60)
            await client.send_message(message.channel, reminder)

        else:
            error_msg = "Invalid <minutes>; must be [1, 60]"

    else:
        error_msg = "Invalid number of arguments"

    # Post an error message, if necessary
    if error_msg is not "":
        await client.send_message(message.channel, "Error: %s" % error_msg)


async def wow_item_level(message):
    """
    Splits a message into ["/ilevel", <character>, <server>]
    Calls WowApis.item_level() for the API call and results
    """

    command = message.content.split(" ")

    # If valid number of args
    if len(command) == 3:

        # Make the API call, which handles invalid input
        await client.send_message(message.channel, wow.item_level(command[1], command[2]))

    else:
        await client.send_message(message.channel, "Error: Invalid number of arguments")


async def wow_mythic_plus(message):
    """
    Splits a message into ["/mplus", <character>, <server>]
    Calls WowApis.mythic_plus() for the API call and results
    """

    command = message.content.split(" ")

    # If valid number of args
    if len(command) == 3:

        # Make the API call, which handles invalid input
        await client.send_message(message.channel, wow.mythic_plus(command[1], command[2]))

    else:
        await client.send_message(message.channel, "Error: Invalid number of arguments")


async def hearthstone_card(message):
    """
    Splits a message into ["/card", <card>]
    Calls HearthstoneApis.card() for the API call and results
    """

    command = message.content.split(" ")
    output = ""

    # If valid number of args
    if len(command) >= 2:

        # Make the API call, which handles invalid input
        await client.send_message(message.channel, hs.card(" ".join(command[1:])))

    else:
        await client.send_message(message.channel, "Error: Invalid number of arguments")


def parse_int(str_input):
    """
    Helper function that attempts to parse an int from a string
    """

    minutes = -1

    try:
        minutes = int(str_input)
    except:
        None

    return minutes


# Get the token and run the bot
token_file = open("../secret/discord_token", "r")
discord_token = token_file.read().strip()
token_file.close()

client.run(discord_token)
