import requests


class WebsiteApis:

    wow_key = ""
    hearthstone_key = ""

    wow_classes = ["Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Death Knight",
                   "Shaman", "Mage", "Warlock", "Monk", "Druid", "Demon Hunter"]


    def __init__(self):
        key_file = open("../other/api_keys", "r")
        lines = key_file.read().split("\n")
        key_file.close()

        keys = {}

        for line in lines:
            keys[line[0:line.index(',')]] = line[line.index(',') + 1:]

        self.wow_key = keys["wow"]
        self.hearthstone_key = keys["hearthstone"]


    # World of Warcraft average item level
    def wow_item_level(self, character, server):

        # Format the input
        character = character.title()
        server = server.title()

        # Web address
        fields = "items&"  # Change for different fields
        url = "https://us.api.battle.net/wow/character/%s/%s?fields=%slocale=en_US&apikey=%s" \
              % (server, character, fields, self.wow_key)

        # Retrieve the data
        data = requests.get(url).json()

        output = ""

        # Check its validity - "status" key is only in invalid data
        if "status" not in data:
            # Parse the class and average item level
            class_num = int(data['class']) - 1
            average_item_level = data['items']['averageItemLevel']

            # Remove the "-" from a server name for displaying
            server = server.replace("-", " ")

            # Output
            output += "%s-%s\n" % (character, server)
            output += "Class: %s\n" % self.wow_classes[class_num]
            output += "Average item level: %d" % average_item_level

        else:
            output += "Invalid character name and/or server"

        return output


    # Hearthstone card
    def hearthstone_card(self, card):

        # Web address
        url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/%s" % card

        # Create a request, attach the key
        request = requests.Session()
        request.headers.update({"X-Mashape-Key": self.hearthstone_key})

        # Get, parse, and print the information
        data = request.get(url).json()

        output = ""

        # Check its validity - "error" key is only in invalid data
        if "error" not in data:

            # Post the first image link
            for d in data:
                if "img" in d:
                    output = d["img"]
                    break

        else:

            # Card not found error
            if data["error"] == 404:
                output = "Card not found."

            else:
                output = "Error code 2"

        return output
