import discord


async def set_color(message, color_roles):
    """
    Splits a message into ["/color", <color>]
    Assigns the user a role, which gives them the specified color

    Params: Posted message, dictionary of colors and their role IDs
    """

    command = message.content.split(' ')
    error_msg = ''

    # If valid number of args
    if len(command) == 2:

        # If the second arg is a valid color
        if command[1].lower() in color_roles.keys():

            # The user's non-color roles
            user_roles = [role for role in message.author.roles if role.id not in color_roles.values()]

            # Add the chosen color's role to the list
            user_roles.append(discord.utils.get(message.author.guild.roles, name=command[1].lower()))

            # Replace all existing roles with the new list
            await message.author.edit(roles=user_roles)

        else:
            error_msg = 'Invalid color'

    else:
        error_msg = 'Invalid number of arguments'

    # Post an error message, if necessary
    if error_msg is not '':
        await message.channel.send(f'Error: {error_msg}')
