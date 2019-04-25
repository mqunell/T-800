from src.helper.parse_int import parse_int


async def purge(message):
    """
    Splits a message into ["/purge", <num_messages>]
    Remove up to <num_messages> most recent messages

    Params: Posted message
    """

    command = message.content.split(' ')
    error_msg = ''

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
                    # Remove (<num_messages> + 1) messages to account for the command
                    removed_messages = await message.channel.purge(limit=(num_messages + 1))

                    # Post a results message
                    num_removed = len(removed_messages) - 1
                    plural = 'S' if num_removed > 1 else ''
                    results = f'*{num_removed} MESSAGE{plural} REMOVED.*'

                    await message.channel.send(results)

                except:
                    error_msg = 'Invalid <num_messages>; some may be too old'

            else:
                error_msg = 'Invalid <num_messages>; must be [1, 100]'

        else:
            error_msg = 'Invalid number of arguments'

    else:
        error_msg = 'Error: /purge requires administrator privileges'

    # Post an error message, if necessary
    if error_msg is not '':
        await message.channel.send(f'Error: {error_msg}')
