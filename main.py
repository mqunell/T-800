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

@client.event
async def on_ready():
    print("%s (ID: %s) logged in" % (client.user.name, client.user.id))
    print("----------------------------------------")

client.run("X")