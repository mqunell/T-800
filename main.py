import discord

client = discord.Client()

@client.event
async def on_message(message):  
    # Per the discord.py docs this is to not have the bot respond to itself
    if message.author == client.user:
        return
    #If the bot sees the command !hello we will respond with our msg string
    if message.content.startswith('!hello'):
        msg = 'Prepare to be terminated, {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():  
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('') 
