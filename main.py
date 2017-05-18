import discord

client = discord.Client()

@client.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author == client.user:
        return

    # If the bot sees "!hello"
    if message.content.startswith("!hello"):

        # Print "Prepare to be terminated, <user>"
        msg = "Prepare to be terminated, {0.author.mention}".format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print("%s (ID: %s) logged in" % (client.user.name, client.user.id))
    print("----------------------------------------")

client.run("XXXXX")
