import asyncio

from python.parse_int import parse_int


async def remind_me(client, message):
    """
    Splits a message into ["/remindme", <duration and segment>, <message>]
    After <duration>, mention the author and post <message>
    Note: <message> could be multiple strings, so join() is used

    Params: Discord client, posted message, parse_int function
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
                await post_reminder(client, message.channel, confirmation % "HOUR", reminder, duration * 3600)

            else:
                error_msg = "Invalid <duration>; must be [1, 24] for hours"

        # Minutes
        elif command[1][-1:] == 'm':

            # Check [1, 60]
            if 1 <= duration <= 60:
                await post_reminder(client, message.channel, confirmation % "MINUTE", reminder, duration * 60)

            else:
                error_msg = "Invalid <duration>; must be [1, 60] for minutes"

        else:
            error_msg = "Invalid time specifier; must be 'h' or 'm'"

    else:
        error_msg = "Invalid number of arguments"

    # Post an error message, if necessary
    if error_msg is not "":
        await client.send_message(message.channel, f"Error: {error_msg}")


async def post_reminder(client, channel, confirmation, reminder, duration):
    """
    Helper function for remind_me
    Posts a confirmation immediately, and the actual reminder later
    """

    await client.send_message(channel, confirmation)
    await asyncio.sleep(duration)
    await client.send_message(channel, reminder)