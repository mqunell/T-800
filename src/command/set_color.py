import discord


async def set_color(client, message):
    """
    Splits a message into ["/color", <color>]
    Assigns the user a role, which gives them the specified color

    Params: Discord client, posted message
    """

    command = message.content.split(' ')
    error_msg = ''

    # Colors to choose from and their role IDs
    color_roles = {'blue': 459132667498332163,
                   'green': 459132517845434378,
                   'orange': 459132844497960971,
                   'purple': 459132711039401984,
                   'red': 459132750230716437,
                   'teal': 459131976885075999,
                   'white': 459892614129254400,
                   'yellow': 459132789640396810}

    # If valid number of args
    if len(command) == 2:

        # If the second arg is a valid color
        if command[1] in color_roles.keys():

            # The user's non-color roles
            user_roles = [role for role in message.author.roles if role.id not in color_roles.values()]

            # Add the chosen color's role to the list
            user_roles.append(discord.utils.get(message.author.guild.roles, name=command[1]))

            # Replace all existing roles with the new list
            await message.author.edit(roles=user_roles)

        else:
            error_msg = 'Invalid color'

    else:
        error_msg = 'Invalid number of arguments'

    # Post an error message, if necessary
    if error_msg is not '':
        await message.channel.send(f'Error: {error_msg}')
