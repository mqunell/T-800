from datetime import datetime


class Logger:
    def __init__(self):
        """
        Initialize two sets for tracking reactions and voice channel connections

        self.reaction_set: Set of (discord.Reaction, Union[Member, User], datetime) tuples
        self.voice_set: Set of (discord.Member, discord.VoiceState, datetime) tuples
        """

        self.reaction_set = set()
        self.voice_set = set()


    def add_reaction(self, user, reaction):
        """
        Stores an added reaction and timestamp in self.reaction_set

        :param user: The Union[Member, User] that added the discord.Reaction
        :param reaction: The discord.Reaction, which contains the emoji and message
        """

        self.reaction_set.add((reaction, user, datetime.now()))


    def remove_reaction(self, user, reaction):
        """
        Checks if a user removed a reaction within 5 seconds of adding it

        :param user: The Union[Member, User] that removed the discord.Reaction
        :param reaction: The discord.Reaction, which contains the emoji and message
        :return: A log message if a stealth reaction was found; None if not
        """

        for r in self.reaction_set.copy():

            # Remove old ones
            if (datetime.now() - r[2]).seconds > 5:
                self.reaction_set.discard(r)

            # Check for stealth reactions
            elif user == r[1] and reaction.message == r[0].message and reaction.emoji == r[0].emoji:
                emoji = reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.name
                self.reaction_set.discard(r)
                return f'{user} stealth reacted `{emoji}` to `{reaction.message.author}: {reaction.message.content}`'

        return None


    def connect_voice(self, member, connected_channel):
        """
        Stores a voice channel connection and timestamp in self.voice_set

        :param member: The discord.Member that connected to a discord.VoiceChannel
        :param connected_channel: The discord.VoiceChannel that was connected to
        """

        self.voice_set.add((member, connected_channel, datetime.now()))


    def disconnect_voice(self, member, disconnected_channel):
        """
        Checks if a user disconnected from a channel within 5 seconds of connecting to it

        :param member: The discord.Member that disconnected from a discord.VoiceChannel
        :param disconnected_channel: The discord.VoiceChannel that was disconnected from
        :return: A log message if a stealth join was found; None if not
        """

        for v in self.voice_set.copy():

            # Remove old ones
            if (datetime.now() - v[2]).seconds > 5:
                self.voice_set.discard(v)

            # Check for stealth connections
            elif member == v[0] and disconnected_channel == v[1]:
                self.voice_set.discard(v)
                return f'{member} stealth connected to `{disconnected_channel}`'

        return None
