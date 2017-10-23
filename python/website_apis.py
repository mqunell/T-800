import requests


wow_key = ""
hearthstone_key = ""

wow_classes = ["Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Death Knight",
               "Shaman", "Mage", "Warlock", "Monk", "Druid", "Demon Hunter"]


# World of Warcraft average item level
def wow_item_level(character, server):

    # Format the input
    character = character.title()
    server = server.title()

    # Web address
    fields = "items&"  # Change for different fields
    url = "https://us.api.battle.net/wow/character/%s/%s?fields=%slocale=en_US&apikey=%s" \
          % (server, character, fields, wow_key)

    # Retrieve the data
    data = requests.get(url).json()

    # Check its validity - "status" key is only in invalid data
    if "status" not in data:
        # Parse the class and average item level
        class_num = int(data['class']) - 1
        average_item_level = data['items']['averageItemLevel']

        # Output
        print("%s-%s" % (character, server))
        print("Class: %s" % wow_classes[class_num])
        print("Average item level: %d" % average_item_level)

    else:
        print("Invalid character name and/or server")


# Hearthstone card
def hearthstone_card(card):

    # Web address
    url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/%s" % card

    # Create a request, attach the key
    request = requests.Session()
    request.headers.update({"X-Mashape-Key": hearthstone_key})

    # Get, parse, and print the information
    data = request.get(url).json()

    # Check its validity - "error" key is only in invalid data
    if "error" not in data:

        # Post the first image link
        for d in data:
            if "img" in d:
                print(d["img"])
                break

    else:

        # Card not found error
        if data["error"] == 404:
            print("Card not found.")

        else:
            print("Error code 2")