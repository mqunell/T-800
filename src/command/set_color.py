import discord


async def set_color(client, message):
    """
    Splits a message into ["/color", <color>]
    Assigns the user a role, which gives them the specified color

    Params: Discord client, posted message
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