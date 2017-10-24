import requests


class WebsiteApis:

    wow_key = ""
    hearthstone_key = ""

    # Worgen: 22, APanda: 25, HPanda: 26
    wow_races = ["Human", "Orc", "Dwarf", "Night Elf", "Undead", "Tauren",
                 "Gnome", "Troll", "Goblin", "Blood Elf", "Draenei"]

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

            # Level
            character_level = int(data['level'])

            # Race (some values had to be hardcoded)
            race_num = int(data['race'])
            character_race = ""
            if race_num <= 12:
                character_race = self.wow_races[race_num - 1]
            else:
                if race_num == 22:
                    character_race = "Worgen"
                elif race_num == 25:
                    character_race = "A. Panda"
                elif race_num == 26:
                    character_race = "H. Panda"

            # Class
            class_num = int(data['class'])
            character_class = self.wow_classes[class_num - 1]

            # Average item level
            character_ilevel = data['items']['averageItemLevel']

            # Remove the "-" from a server name for displaying
            server = server.replace("-", " ")

            # Output
            output += "%s-%s\n" % (character, server)
            output += "%d %s %s\n" % (character_level, character_race, character_class)
            output += "Average item level: %d" % character_ilevel

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
                if "img" in d and "collectible" in d:
                    output = d["img"]
                    break

        else:

            # Card not found error
            if data["error"] == 404:
                output = "Card not found."

            else:
                output = "Error code 2"

        return output
