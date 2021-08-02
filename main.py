import discord
import json
from discord.ext import commands, tasks
import os
from itertools import cycle
from keep_alive import keep_alive

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())

game = cycle(['The Golden Lyre', 'Pranks On Other Gods', 'With His Perfect Hair'])

@client.event
async def on_ready():
    change_status.start()
    print('Apollo has descended!')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
     prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
   with open('prefixes.json', 'r') as f:
     prefixes = json.load(f)

   prefixes.pop(str(guild.id))

   with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
     prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)
  
    await ctx.send(f'Prefix changed to: {prefix}')

@client.command()
async def dm(ctx, member : discord.Member, *, message=None):
  await member.send(message)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@tasks.loop(minutes=1)
async def change_status():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(next(game)))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
client.run(os.getenv('TOKEN'))
