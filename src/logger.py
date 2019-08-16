from datetime import datetime


class Logger:
    def __init__(self):
        self.reaction_set = set()  # Set of (discord.Reaction, Union[Member, User], datetime) tuples

    def add(self, reaction, user):
        added_time = datetime.now()  # datetime.datetime
        self.reaction_set.add((reaction, user, added_time))

    def remove(self, reaction, user):
        removed_time = datetime.now()

        for r in self.reaction_set.copy():
            # Remove old ones
            if (removed_time - r[2]).seconds > 5:
                self.reaction_set.discard(r)
                print('removed ', r)

            # Check for stealth reactions
            elif user.id == r[1].id and reaction.message == r[0].message and reaction.emoji == r[0].emoji:
                emoji = reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.name
                self.reaction_set.discard(r)
                return f'{user} stealth reacted `{emoji}` to `{reaction.message.author}: {reaction.message.content}`'

        return None

    def get(self):
        return str(self.reaction_set)
