import discord
from discord.ext import commands
from siegeapi import Auth
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

async def get_player_stats(name):
    auth = Auth("", "")
    player = None
    try:
        player = await auth.get_player(name=name)
        if player is None:
            return {"exists": False}
        
        await player.load_playtime()
        await player.load_ranked_v2()
        await player.load_progress()
        total_time_played_hours = player.total_time_played / 3600
        kd_ratio = player.ranked_profile.kills / player.ranked_profile.deaths if player.ranked_profile.deaths > 0 else player.ranked_profile.kills
        win_lose_ratio = player.ranked_profile.wins / player.ranked_profile.losses if player.ranked_profile.wins > 0 else player.ranked_profile.losses
        data = {
            "exists": True,
            "Profile Pic URL": player.profile_pic_url_500,
            "Allgemein": f"KD: `{kd_ratio:.2f}` | Win%: `{win_lose_ratio:.2f}`",
            "Spielzeit": f"`{total_time_played_hours:.2f}` Stunden ",
            "XP Info": f"Level: `{player.level}`, XP: `{player.xp:,}` Total XP: `{player.total_xp:,}`, Naechstes Level: `{player.xp_to_level_up:,}`",
            "Ranked Info": f"RP: `{player.ranked_profile.rank_points}`, Rang: `{player.ranked_profile.rank}`, Max RP: `{player.ranked_profile.max_rank_points}`, Max Rang: `{player.ranked_profile.max_rank}`",
        }
    except Exception as e:
        print(f"Error fetching player data: {e}")
        data = {"exists": False}
    finally:
        await auth.close()
    
    return data

@bot.event
async def on_ready():
    print(f'{bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.bot or message.author == bot.user:
        return
    
    if isinstance(message.channel, discord.DMChannel):
        requester = f"{message.author.name}#{message.author.discriminator} (ID: {message.author.id})"
        name = message.content
        print(f"Received request for player '{name}' from {requester}")
        
        data = await get_player_stats(name)
        
        if not data["exists"]:
            await message.channel.send(f"Konnte den Spieler `{name}` nicht finden.")
            return
        
        embed = discord.Embed(title=f"{name}", color=0x8E7CC3)
        embed.set_thumbnail(url=data["Profile Pic URL"])
        embed.add_field(name="Allgemein:", value=data["Allgemein"], inline=False)
        embed.add_field(name="Spielzeit:", value=data["Spielzeit"], inline=False)
        embed.add_field(name="XP Info:", value=data["XP Info"], inline=False)
        embed.add_field(name="Ranked Info:", value=data["Ranked Info"], inline=False)
        embed.set_footer(text="Data provided by SiegeAPI | Bot made by 187.fynn")
        
        await message.channel.send(embed=embed)

bot.run('')
