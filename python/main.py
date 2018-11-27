import asyncio
import discord
import json
import weekday_timers

from hearthstone_apis import HearthstoneApis
from weekday import Weekday
from wow_apis import WowApis


# Create the bot client
client = discord.Client()

# Parse keys.json
with open("../strings/keys.json") as keys_json_file:
    keys = json.load(keys_json_file)

# Parse long_strings.json
with open("../strings/long_strings.json") as strings_json_file:
    long_strings = json.load(strings_json_file)

# Create the API objects
wow = WowApis(keys['wow']['client_id'], keys['wow']['client_secret'])
hs = HearthstoneApis(keys['hearthstone']['key'])


@client.event
async def on_ready():
    """
    When the bot signs in
    """

    print(f"{client.user.name} (ID: {client.user.id}) logged in")
    print("----------------------------------------")

    # Post a message when the bot comes online
    msg = "*T-800 ONLINE. YOUR CLOTHES, GIVE THEM TO ME. NOW.*"
    await client.send_message(client.get_channel(keys["discord"]["test_channel_id"]), msg)

    # Set the bot's "Playing" status
    await client.change_presence(game=discord.Game(name="Type /help"))

    # Start the Wednesday "timer"
    await post_wednesday()


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

        # If someone says "Kel'Thuzad"
        if "kel'thuzad" in message.content.lower():
            await client.send_message(message.channel, long_strings["kel'thuzad"])

        # If someone calls /help, /purge, /remindme, /color, /ilevel, /ilvl, /mplus, /wow, /affixes, /card, or /hs
        if message.content.startswith("/help"):
            await client.send_message(message.channel, "\n".join(long_strings["help"]))

        elif message.content.startswith("/purge"):
            await purge(message)

        elif message.content.startswith("/remindme"):
            await remind_me(message)

        elif message.content.startswith("/color"):
            await color(message)

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
    wait_time = weekday_timers.time_until(Weekday.WEDNESDAY)
    await asyncio.sleep(wait_time)

    await client.send_message(client.get_channel("373164195283337218"),
                              "http://i1.kym-cdn.com/photos/images/newsfeed/001/091/264/665.jpg")

    await post_wednesday()


async def purge(message):
    """
    Splits a message into ["/purge", <num_messages>]
    Remove up to <num_messages> most recent messages
    """

    command = message.content.split(" ")
    error_msg = ""

    # If the author is an administrator
    if message.channel.permissions_for(message.author).administrator:

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
                    plural = "S" if num_removed > 1 else ""
                    results_message = f"*{num_removed} MESSAGE{plural} REMOVED.*"

                    await client.send_message(message.channel, results_message)

                except:
                    await client.send_message(message.channel, "Invalid <num_messages>; some may be too old")

            else:
                error_msg = "Invalid <num_messages>; must be [1, 100]"

        else:
            error_msg = "Invalid number of arguments"

    else:
        error_msg = "Error: /purge requires administrator privileges"

    # Post an error message, if necessary
    if error_msg is not "":
        await client.send_message(message.channel, f"Error: {error_msg}")


async def remind_me(message):
    """
    Splits a message into ["/remindme", <duration and segment>, <message>]
    After <duration>, mention the author and post <message>
    Note: <message> could be multiple strings, so join() is used
    """

    command = message.content.split(" ")
    error_msg = ""

    # If valid number of args
    if len(command) >= 3:

        # Formatted author
        author = "{0.author.mention}".format(message)

        # Attempt to parse <duration> (-1 if NaN)
        duration = parse_int(command[1][:-1])
        plural = "S" if duration > 1 else ""

        # Confirmation message with %s placeholder for "HOUR" or "MINUTE"
        confirmation = f"*I WILL REMIND YOU OF THAT IN {duration} %s{plural}, {author}.*"

        # Reminder message
        reminder = f"*{author}: \"{' '.join(command[2:])}\"*"

        # Hours
        if command[1][-1:] == 'h':

            # Check [1, 24]
            if 1 <= duration <= 24:
                await post_reminder(message.channel, confirmation % "HOUR", reminder, duration * 3600)

            else:
                error_msg = "Invalid <duration>; must be [1, 24] for hours"

        # Minutes
        elif command[1][-1:] == 'm':

            # Check [1, 60]
            if 1 <= duration <= 60:
                await post_reminder(message.channel, confirmation % "MINUTE", reminder, duration * 60)

            else:
                error_msg = "Invalid <duration>; must be [1, 60] for minutes"

        else:
            error_msg = "Invalid time specifier; must be 'h' or 'm'"

    else:
        error_msg = "Invalid number of arguments"

    # Post an error message, if necessary
    if error_msg is not "":
        await client.send_message(message.channel, f"Error: {error_msg}")


async def post_reminder(channel, confirmation, reminder, duration):
    """
    Helper function for remind_me
    Posts a confirmation immediately, and the actual reminder later
    """

    await client.send_message(channel, confirmation)
    await asyncio.sleep(duration)
    await client.send_message(channel, reminder)


async def color(message):
    """
    Splits a message into ["/color", <color>]
    Assigns the user a role, which gives them the specified color
    """

    command = message.content.split(" ")
    error_msg = ""

    # Colors to choose from
    valid_colors = ["blue", "green", "orange", "purple", "red", "teal", "white", "yellow"]

    # Role IDs for the colors
    color_ids = ["459132667498332163", "459132517845434378", "459132844497960971", "459132711039401984",
                 "459132750230716437", "459131976885075999", "459892614129254400", "459132789640396810"]

    # If valid number of args
    if len(command) == 2:

        # If the second arg is a valid color
        if command[1] in valid_colors:

            # The user's non-color roles
            user_roles = [role for role in message.author.roles if role.id not in color_ids]

            # Add the chosen color's role to the list
            user_roles.append(discord.utils.get(message.author.server.roles, name=command[1]))

            # Set the new roles. Note: replace_roles has to be used when removing/adding, and the * unpacks the list
            await client.replace_roles(message.author, *user_roles)

        else:
            error_msg = "Error: Invalid color"

    else:
        error_msg = "Error: Invalid number of arguments"

    # Post an error message, if necessary
    if error_msg is not "":
        await client.send_message(message.channel, f"Error: {error_msg}")


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


client.run(keys["discord"]["token"])
