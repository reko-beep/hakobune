from discord.ext.commands import Bot
from discord import Intents, Embed
from embed_builder import EmbedView
import requests
import json
client = Bot(command_prefix='!', intents=Intents.all())

@client.command()
async def eb(ctx):

    embed_list = [{
    "footer": {
        "text": "Character Name Here"
    },
    "thumbnail": {
        "url": "https://i.imgur.com/47mFsx4.png"
    },
    "fields": [
        {
            "inline": "true",
            "name": "Best Weapon(s):",
            "value": "weapons name here"
        },
        {
            "inline": "true",
            "name": "Replacement Weapon:",
            "value": "weapons name here"
        },
        {
            "inline": "false",
            "name": "Best Artifact Set:",
            "value": "artifacts name here"
        },
        {
            "inline": "false",
            "name": "Second Best Artifact Set:",
            "value": "artifacts name here"
        },
        {
            "inline": "false",
            "name": "Third Best Artifact Set:",
            "value": "artifacts name here"
        },
        {
            "inline": "true",
            "name": "Main Stats Priority",
            "value": "artifact piece (goblet, sand) : stat"
        },
        {
            "inline": "true",
            "name": "Substats Priority",
            "value": "stats here"
        },
        {
            "inline": "false",
            "name": "Talent Priority",
            "value": "**1)** Talent Type : Talent Name\n**2)** Talent Type : Talent Name\n**3)** Talent Type : Talent Name\n"
        },
        {
            "inline": "false",
            "name": "Notes:",
            "value": "Normal Attack talent does not have to be raised at all for this build. "
        }
    ],
    "color": 10147839,
    "type": "rich",
    "title": "Character name | Build Type here"
}]
    embed = Embed.from_dict(embed_list[0])
    msg = await ctx.send('embed builder')  
    embed_builder = EmbedView(ctx, msg, embed_list, 0)
    await msg.edit(embed=embed, view=embed_builder)


client.run('token here')