from datetime import datetime


class Logger:
    def __init__(self):
        self.reaction_set = set()  # Set of (discord.Reaction, Union[Member, User], datetime) tuples
        self.voice_set = set()  # Set of (discord.Member, discord.VoiceState, datetime) tuples


    def add_reaction(self, reaction, user):
        added_time = datetime.now()  # datetime.datetime
        self.reaction_set.add((reaction, user, added_time))


    def remove_reaction(self, reaction, user):
        removed_time = datetime.now()

        for r in self.reaction_set.copy():
            # Remove old ones
            if (removed_time - r[2]).seconds > 5:
                self.reaction_set.discard(r)

            # Check for stealth reactions
            elif user == r[1] and reaction.message == r[0].message and reaction.emoji == r[0].emoji:
                emoji = reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.name
                self.reaction_set.discard(r)
                return f'{user} stealth reacted `{emoji}` to `{reaction.message.author}: {reaction.message.content}`'

        return None


    def join_voice(self, member, joined_channel):
        joined_time = datetime.now()
        self.voice_set.add((member, joined_channel, joined_time))


    def leave_voice(self, member, left_channel):
        left_time = datetime.now()

        for v in self.voice_set.copy():
            # Remove old ones
            if (left_time - v[2]).seconds > 5:
                self.voice_set.discard(v)

            # Check for stealth joins
            elif member == v[0] and left_channel == v[1]:
                self.voice_set.discard(v)
                return f'{member} stealth joined `{left_channel}`'

        return None