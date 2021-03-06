import requests


class HearthstoneApis:

    def __init__(self, api_key):
        self.api_key = api_key


    # Hearthstone card
    def card(self, card):

        # Web address
        url = f'https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/{card}'

        # Create a request, attach the key
        request = requests.Session()
        request.headers.update({'X-Mashape-Key': self.api_key})

        # Get, parse, and print the information
        data = request.get(url).json()

        # Final output if data contains > 0 cards, but none of them have images to display
        plural = '' if len(data) > 1 else 's'
        output = f'{len(data)} card{plural} found, but no image{plural} to display'

        # Check its validity - "error" key is only in invalid data
        if 'error' not in data:

            # Post the first image link
            for d in data:
                if 'img' in d:
                    if 'collectible' in d:
                        output = d['img']
                        break

                    else:
                        output = f'Did not find a collectible card, but found this:\n{d["img"]}'

        else:

            # Card not found error
            if data['error'] == 404:
                output = 'Card not found.'

            else:
                output = 'Hearthstone API error. (non-404)'

        return output
