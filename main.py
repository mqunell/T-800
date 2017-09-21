import sys
import discord
import asyncio


client = discord.Client()


@client.event
async def on_ready():
    """
    When the bot signs in
    """

    print("%s (ID: %s) logged in" % (client.user.name, client.user.id))
    print("----------------------------------------")

    # "bot-testing" chat channel id
    channel_id = "352531997262086144"

    # Post a message when the bot comes online
    msg = "*T-800 ONLINE. YOUR CLOTHES, GIVE THEM TO ME. NOW.*"
    await client.send_message(client.get_channel(channel_id), msg)

    # Set the bot's "Playing" status
    await client.change_presence(game=discord.Game(name="Type !help"))


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
            author = "*{0.author.mention}".format(message)
            msg = "%s said \"%s\"*\n" % (author, message.content)
            msg += "*FAKE NEWS DETECTED. TERMINATING FAKE NEWS.*"
            await client.send_message(message.channel, msg)

        # If someone calls "!help"
        if message.content.startswith("!help"):
            await help(message)

        # If someone calls "!purge"
        if message.content.startswith("!purge"):
            await purge(message)

        # If someone calls "!remindme"
        if message.content.startswith("!remindme"):
            await remind_me(message)


async def help(message):
    """
    Writes what the bot can do
    """

    msg = "*I AM A HIGHLY CAPABLE MACHINE. THESE ARE MY FUNCTIONS:*\n\n"
    msg += "Reminders: `!remindme <minutes (1-60)> <message>`\n"
    msg += "    Example: `!remindme 30 Make something for dinner`"

    await client.send_message(message.channel, msg)


async def purge(message):
    """
    Splits a message into ["!purge", <num_messages>]
    Remove up to <num_messages> most recent messages
    """

    command = message.content.split(" ")

    # If valid number of args
    if len(command) == 2:

        # Attempt to parse <num_messages>
        num_messages = parse_int(command[1])

        # If valid <num_messages>
        if num_messages > 0:

            # Remove (<num_messages> + 1) messages, which accounts for the command
            removed_messages = await client.purge_from(message.channel, limit=(num_messages + 1))

            # Post a results message
            num_removed = len(removed_messages) - 1
            results_message = "*%d MESSAGE%s REMOVED.*" % (num_removed, "S" if num_removed > 1 else "")
            await client.send_message(message.channel, results_message)


async def remind_me(message):
    """
    Splits a message into ["!remindme", <minutes>, <message>]
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
            confirmation = author + (": I WILL REMIND YOU OF THAT IN %d MINUTES.*" % minutes)
            reminder = author + (": \"%s\"*" % " ".join(command[2:]))

            # Post the confirmation immediately, and the reminder later
            await client.send_message(message.channel, confirmation)
            await asyncio.sleep(minutes * 60)
            await client.send_message(message.channel, reminder)

        else:
            error_msg = "Invalid <minutes>; must be [1, 60]"

    else:
        error_msg = "Invalid number of commands"

    if error_msg is not "":
        await client.send_message(message.channel, "Error: %s" % error_msg)


def parse_int(str_input):
    """
    Helper function for remind_me(message)
    Attempts to parse an int from a string
    """

    minutes = -1

    try:
        minutes = int(str_input)
    except:
        None

    return minutes


token = sys.argv[1]
client.run(token)
