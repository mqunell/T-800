import requests


class WowApis:

    api_key = ""

    wow_races = {1: "Human", 2: "Orc", 3: "Dwarf", 4: "Night Elf", 5: "Undead", 6: "Tauren", 7: "Gnome", 8: "Troll",
                 9: "Goblin", 10: "Blood Elf", 11: "Draenei", 22: "Worgen", 25: "A. Panda", 26: "H. Panda"}

    wow_classes = {1: "Warrior", 2: "Paladin", 3: "Hunter", 4: "Rogue", 5: "Priest", 6: "Death Knight",
                   7: "Shaman", 8: "Mage", 9: "Warlock", 10: "Monk", 11: "Druid", 12: "Demon Hunter"}


    def __init__(self):

        # Parse the API key
        key_file = open("../secret/wow_key", "r")
        self.api_key = key_file.read().strip()
        key_file.close()


    # World of Warcraft average item level
    def item_level(self, character, server):

        # Web address
        fields = "items&"  # Change for different fields
        url = "https://us.api.battle.net/wow/character/%s/%s?fields=%slocale=en_US&apikey=%s" \
              % (server, character, fields, self.api_key)

        # Make the request
        r = requests.get(url)

        output = ""

        # If the request is successful
        if r.status_code == 200:

            # Retrieve the data
            data = r.json()

            # Level
            character_level = int(data['level'])

            # Race
            race_num = int(data['race'])
            character_race = self.wow_races[race_num]

            # Class
            class_num = int(data['class'])
            character_class = self.wow_classes[class_num]

            # Average item level
            character_ilevel = data['items']['averageItemLevel']

            # Remove the "-" from a server name for displaying
            server = server.replace("-", " ")

            # Output
            output += "%s-%s\n" % (character.title(), server.title())
            output += "%d %s %s\n" % (character_level, character_race, character_class)
            output += "Average item level: %d" % character_ilevel

        else:
            output += "Invalid character name and/or server"

        return output


    # Mythic Plus info
    def mythic_plus(self, character, server):

        # Web address
        url = "https://raider.io/api/v1/characters/profile?region=us&realm=%s&name=%s" % (server, character)
        url += "&fields=mythic_plus_scores%2Cmythic_plus_weekly_highest_level_runs"

        # Make the request
        r = requests.get(url)

        output = ""

        # If the request is successful
        if r.status_code == 200:

            # Retrieve the data
            data = r.json()

            # Name
            name = data["name"]

            # Profile URL
            profile_url = data["profile_url"]

            # Overall M+ score
            overall_score = data["mythic_plus_scores"]["all"]

            # Attempt to find the highest completed in the last week
            highest = "-"
            if len(data["mythic_plus_weekly_highest_level_runs"]) > 0:
                highest = "%s %d" % (data["mythic_plus_weekly_highest_level_runs"][0]["dungeon"],
                                     data["mythic_plus_weekly_highest_level_runs"][0]["mythic_level"])

            output += "%s-%s\n" % (character.title(), server.title())
            output += "Overall Mythic Plus score: %s\n" % overall_score
            output += "Highest Mythic Plus this week: %s\n" % highest
            output += "Raider.IO profile: <%s>\n" % profile_url

        else:
            output = "Could not find character"

        return output