import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

TOKEN = "YOUR_TOKEN"
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    channel_id = 1171876038284951612
    if message.channel.id == channel_id:
        thumbs_up_emoji = "✅"
        await message.add_reaction(thumbs_up_emoji)

@bot.command(name='clear')
async def clear(ctx):
    channel = ctx.channel
    await channel.purge(limit=100, check=lambda msg: msg != ctx.message)

bot.run(TOKEN)
