import requests


class WowApis:

    # Dictionaries for parsing in item_level()
    wow_races = {1: 'Human', 2: 'Orc', 3: 'Dwarf', 4: 'Night Elf', 5: 'Undead', 6: 'Tauren', 7: 'Gnome', 8: 'Troll',
                 9: 'Goblin', 10: 'Blood Elf', 11: 'Draenei', 22: 'Worgen', 25: 'A. Panda', 26: 'H. Panda',
                 27: 'Nightborne', 28: 'Highmountain Tauren', 29: 'Void Elf', 30: 'Lightforged Draenei',
                 34: 'Dark Iron Dwarf', 36: 'Mag\'har Orc'}

    wow_classes = {1: 'Warrior', 2: 'Paladin', 3: 'Hunter', 4: 'Rogue', 5: 'Priest', 6: 'Death Knight', 7: 'Shaman',
                   8: 'Mage', 9: 'Warlock', 10: 'Monk', 11: 'Druid', 12: 'Demon Hunter'}

    # Final output for item_level()
    item_level_invalid = 'Invalid character name and/or server'

    # Final output for mythic_plus()
    mythic_plus_not_found = 'Could not find character'


    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = self.client_secret = client_secret


    def item_level(self, character, server):
        """
        Accesses the Battle.net API to get a character's level, race, class, and average item level
        """

        # Get the OAuth token
        auth = requests.get(f'https://us.battle.net/oauth/token?grant_type=client_credentials&'
                            f'client_id={self.client_id}&client_secret={self.client_secret}')
        auth_token = auth.json()['access_token']

        # Web address
        fields = 'items&'  # Change for different fields
        url = f'https://us.api.blizzard.com/wow/character/{server}/{character}' \
              f'?fields={fields}locale=en_US&access_token={auth_token}'

        # Make the request
        r = requests.get(url)

        output = ''

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
            server = server.replace('-', ' ')

            # Output
            output += f'{character.title()}-{server.title()}\n'
            output += f'{character_level} {character_race} {character_class}\n'
            output += f'Average item level: {character_ilevel}'

        else:
            output += self.item_level_invalid

        return output


    def mythic_plus(self, character, server):
        """
        Accesses the Raider.IO API to get a character's overall Mythic Plus score, highest completed Mythic Plus dungeon
        in the last week, and a link to their Raider.IO profile
        """

        # Web address
        url = f'https://raider.io/api/v1/characters/profile?region=us&realm={server}&name={character}'
        url += '&fields=mythic_plus_scores%2Cmythic_plus_weekly_highest_level_runs'

        # Make the request
        r = requests.get(url)

        output = ''

        # If the request is successful
        if r.status_code == 200:

            # Retrieve the data
            data = r.json()

            # Profile URL
            profile_url = data['profile_url']

            # Overall M+ score
            overall_score = data['mythic_plus_scores']['all']

            # Attempt to find the highest completed in the last week
            highest = '-'
            if len(data['mythic_plus_weekly_highest_level_runs']) > 0:
                highest = f'{data["mythic_plus_weekly_highest_level_runs"][0]["dungeon"]} ' \
                          f'{data["mythic_plus_weekly_highest_level_runs"][0]["mythic_level"]}'

            output += f'{character.title()}-{server.title()}\n'
            output += f'Overall Mythic Plus score: {overall_score}\n'
            output += f'Highest Mythic Plus this week: {highest}\n'
            output += f'Raider.IO profile: <{profile_url}>\n'

        else:
            output = self.mythic_plus_not_found

        return output


    def all(self, character, server):
        """
        Gathers and formats information from item_level and mythic_plus
        """

        # Get the item_level() info
        output = self.item_level(character, server)

        # If valid item_level() info was received, attempt to get mythic_plus() info
        if output != self.item_level_invalid:
            output += '\n\n'

            mplus = self.mythic_plus(character, server)

            # If valid mythic_plus() info was received, parse it to remove "<name>-<server>"
            if mplus != self.mythic_plus_not_found:
                output += mplus[mplus.index('\n')+1:]

            else:
                output += 'No Mythic Plus data'

        return output


    def affixes(self):
        """
        Accesses the Raider.IO API to get the current affixes and their details
        """

        # Web address
        url = 'https://raider.io/api/v1/mythic-plus/affixes?region=us'

        # Make the request
        r = requests.get(url)

        output = ''

        # If the request is successful
        if r.status_code == 200:

            # Retrieve the data
            data = r.json()

            for affix in data['affix_details']:
                output += f'**{affix["name"]}**\n'
                output += f'{affix["description"]}\n\n'

        else:
            output = 'API error'

        return output
