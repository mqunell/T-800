# T-800 Discord Bot

![Image of example usage](https://i.imgur.com/OE5WyKn.png)


<br/>

## Automatic Functionality

* Announcing its arrival and demanding clothes
* Telling users to talk to the hand
* Reacting to fake news with a custom emoji
* Posting weekly Wednesday meme


<br/>

## On-Demand Functionality via Explicit Commands

General:

|Command|Details|
|---|---|
|`/color <color>`|Sets the user's name color|
|`/help`|Displays a list of commands in the server chat|
|`/purge <num_messages>`|Attempts to remove the <num_messages> most recent messages from the server (admin only)
|`/remindme <duration><m/h> <message>`|Tags users with their message after the designated amount of time (1-60m, or 1-24h)|

<br/>
World of Warcraft:

|Command|Details|
|---|---|
|`/affixes`|Displays the current Mythic Plus affixes|
|`/ilevel <character name> <server>` (also works as `/ilvl`)|Displays the character's basic information and average item level|
|`/mplus <character name> <server>`|Displays the character's Mythic Plus score and highest completed dungeon in the current weekly reset|
|`/wow <character name> <server>`|Combines `/ilevel` and `/mplus`|

<br/>
Hearthstone:

|Command|Details|
|---|---|
|`/card <card name>` (also works as `/hs`)|Displays an image of the card|


<br/>

## Adding the Bot to a Server

Since I have limited hosting time, adding the bot to other servers is currently not supported.
The following web address would be used to add the bot to servers, where ID is replaced with the bot's actual ID.

https://discordapp.com/oauth2/authorize?client_id=ID&scope=bot