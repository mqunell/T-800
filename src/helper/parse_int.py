def parse_int(str_input):
    """
    Helper function that attempts to parse an int from a string
    """

    minutes = -1

    try:
        minutes = int(str_input)
    except:
        pass

    return minutes