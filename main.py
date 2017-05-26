import discord

client = discord.Client()

@client.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author != client.user:

        # If someone tags the bot
        if client.user in message.mentions:
            msg = "*TALK TO THE HAND, {0.author.mention}.*".format(message)
            await client.send_message(message.channel, msg)


        # If someone says "fake news"
        if "fake news" in message.content.lower():
            msg = "*FAKE NEWS DETECTED. TERMINATING FAKE NEWS.*"
            await client.send_message(message.channel, msg)


        # If someone calls "!purge"
        if message.content.startswith("!purge"):
            await client.purge_from(message.channel)


        # If someone calls "!remindme"
        if message.content.startswith("!remindme"):

            # Split the message into "!remindme", <minutes>, <message>
            # Note: <message> could be multiple strings
            command = message.content.split(" ")

            error_msg = ""

            # If valid number of args
            if len(command) >= 3:

                # Attempt to parse <minutes>
                minutes = parse_minutes(command[1])

                # If valid number of <minutes>
                if 1 <= minutes <= 60:

                    # TESTING: Post the data to be timed
                    msg  = "Author: <{0.author.mention}>, ".format(message)
                    msg += "Minutes: <%d>" % minutes
                    msg += "Message: <%s>" % " ".join(command[2:])

                    await client.send_message(message.channel, msg)

                else:
                    error_msg = "Invalid <minutes>; must be [1, 60]"

            else:
                error_msg = "Invalid number of commmands"

            if error_msg is not "":
                await client.send_message(message.channel, "Error: %s" % error_msg)


@client.event
async def on_ready():
    print("%s (ID: %s) logged in" % (client.user.name, client.user.id))
    print("----------------------------------------")

    # "general" chat channel id
    general_id = "311344943111340033"

    # Post a message when the bot comes online
    msg = "*T-800 ONLINE. YOUR CLOTHES, GIVE THEM TO ME. NOW.*"
    await client.send_message(client.get_channel(general_id), msg)

    # Set the bot's "Playing" status
    await client.change_presence(game=discord.Game(name="Human Simulator"))


# Attempts to parse an int from a string
def parse_minutes(str_input):
    minutes = -1

    try:
        minutes = int(str_input)
    except:
        None
    
    return minutes


client.run("")
