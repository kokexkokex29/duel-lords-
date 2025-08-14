import discord
from discord.ext import commands, tasks
import os
import logging
import asyncio
from datetime import datetime, timedelta
from database import DatabaseManager
from translations import get_translation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
db = DatabaseManager()

# BombSquad server info
BOMBSQUAD_IP = "18.228.228.44"
BOMBSQUAD_PORT = "3827"

# Admin user IDs (you can modify this list)
ADMIN_USERS = []  # Add Discord user IDs here

def is_admin(interaction):
    """Check if user is an admin"""
    return interaction.user.id in ADMIN_USERS or interaction.user.guild_permissions.administrator

@bot.event
async def on_ready():
    logger.info(f'✅ {bot.user} has connected to Discord!')
    logger.info(f'🤖 Bot ID: {bot.user.id}')
    try:
        synced = await bot.tree.sync()
        logger.info(f"⚡ Synced {len(synced)} slash commands")
        
        if not reminder_check.is_running():
            reminder_check.start()
            logger.info("⏰ Reminder task started")
            
        logger.info("🎉 Bot is fully ready!")
    except Exception as e:
        logger.error(f"❌ Error in on_ready: {e}")

@bot.tree.command(name="ip", description="Display BombSquad server IP and port")
async def ip_command(interaction: discord.Interaction):
    """Display server IP and port"""
    embed = discord.Embed(
        title="🎮 BombSquad Server Information",
        description="Connect to our official tournament server!",
        color=0x00ff00
    )
    embed.add_field(name="🌐 IP Address", value=f"`{BOMBSQUAD_IP}`", inline=True)
    embed.add_field(name="🔌 Port", value=f"`{BOMBSQUAD_PORT}`", inline=True)
    embed.add_field(name="📋 Full Address", value=f"`{BOMBSQUAD_IP}:{BOMBSQUAD_PORT}`", inline=False)
    embed.set_footer(text="Duel Lords Tournament • Copy and paste into BombSquad")
    embed.timestamp = datetime.utcnow()
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="register", description="Register a new player (Admin only)")
async def register_player(interaction: discord.Interaction, player: discord.Member, player_name: str):
    """Register a new player"""
    if not is_admin(interaction):
        embed = discord.Embed(
            title="❌ Access Denied",
            description="Only administrators can register players.",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    try:
        success = db.add_player(player.id, player_name, player.display_name)
        if success:
            embed = discord.Embed(
                title="✅ Player Registered Successfully",
                description=f"Player **{player_name}** has been registered for the tournament!",
                color=0x00ff00
            )
            embed.add_field(name="Discord User", value=player.mention, inline=True)
            embed.add_field(name="Player Name", value=player_name, inline=True)
            embed.set_thumbnail(url=player.avatar.url if player.avatar else None)
            embed.set_footer(text="Duel Lords Tournament")
            embed.timestamp = datetime.utcnow()
        else:
            embed = discord.Embed(
                title="⚠️ Registration Failed",
                description="Player is already registered or an error occurred.",
                color=0xffa500
            )
    except Exception as e:
        logger.error(f"Error registering player: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="An error occurred while registering the player.",
            color=0xff0000
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="remove_player", description="Remove a player from tournament (Admin only)")
async def remove_player(interaction: discord.Interaction, player: discord.Member):
    """Remove a player from the tournament"""
    if not is_admin(interaction):
        embed = discord.Embed(
            title="❌ Access Denied",
            description="Only administrators can remove players.",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    try:
        success = db.remove_player(player.id)
        if success:
            embed = discord.Embed(
                title="✅ Player Removed",
                description=f"Player {player.mention} has been removed from the tournament.",
                color=0x00ff00
            )
        else:
            embed = discord.Embed(
                title="⚠️ Player Not Found",
                description="Player was not found in the tournament.",
                color=0xffa500
            )
    except Exception as e:
        logger.error(f"Error removing player: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="An error occurred while removing the player.",
            color=0xff0000
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="stats", description="View player statistics")
async def player_stats(interaction: discord.Interaction, player: discord.Member = None):
    """Display player statistics"""
    target_player = player if player is not None else interaction.user
    
    try:
        stats = db.get_player_stats(target_player.id)
        if not stats:
            embed = discord.Embed(
                title="❌ Player Not Found",
                description=f"{target_player.mention} is not registered in the tournament.",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Calculate additional stats
        total_matches = stats['wins'] + stats['losses'] + stats['draws']
        win_rate = (stats['wins'] / total_matches * 100) if total_matches > 0 else 0
        kd_ratio = (stats['kills'] / stats['deaths']) if stats['deaths'] > 0 else stats['kills']
        
        embed = discord.Embed(
            title=f"📊 Tournament Statistics",
            description=f"Statistics for **{stats['player_name']}**",
            color=0x0099ff
        )
        
        # Basic stats
        embed.add_field(name="🏆 Wins", value=f"`{stats['wins']}`", inline=True)
        embed.add_field(name="💔 Losses", value=f"`{stats['losses']}`", inline=True)
        embed.add_field(name="🤝 Draws", value=f"`{stats['draws']}`", inline=True)
        
        # Combat stats
        embed.add_field(name="⚔️ Kills", value=f"`{stats['kills']}`", inline=True)
        embed.add_field(name="💀 Deaths", value=f"`{stats['deaths']}`", inline=True)
        embed.add_field(name="📈 K/D Ratio", value=f"`{kd_ratio:.2f}`", inline=True)
        
        # Advanced stats
        embed.add_field(name="🎯 Total Matches", value=f"`{total_matches}`", inline=True)
        embed.add_field(name="📊 Win Rate", value=f"`{win_rate:.1f}%`", inline=True)
        embed.add_field(name="🏅 Points", value=f"`{stats['points']}`", inline=True)
        
        embed.set_thumbnail(url=target_player.avatar.url if target_player.avatar else None)
        embed.set_footer(text="Duel Lords Tournament • /leaderboard for rankings")
        embed.timestamp = datetime.utcnow()
        
    except Exception as e:
        logger.error(f"Error getting player stats: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="An error occurred while retrieving statistics.",
            color=0xff0000
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="update_stats", description="Update player match results (Admin only)")
async def update_stats(interaction: discord.Interaction, player1: discord.Member, player2: discord.Member, 
                      result: str, player1_kills: int = 0, player1_deaths: int = 0, 
                      player2_kills: int = 0, player2_deaths: int = 0):
    """Update player statistics after a match"""
    if not is_admin(interaction):
        embed = discord.Embed(
            title="❌ Access Denied",
            description="Only administrators can update statistics.",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    valid_results = ["player1_win", "player2_win", "draw"]
    if result not in valid_results:
        embed = discord.Embed(
            title="❌ Invalid Result",
            description="Result must be: `player1_win`, `player2_win`, or `draw`",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    try:
        success = db.update_match_result(player1.id, player2.id, result, 
                                       player1_kills, player1_deaths, 
                                       player2_kills, player2_deaths)
        
        if success:
            # Determine winner for embed
            if result == "player1_win":
                winner = player1.mention
                loser = player2.mention
            elif result == "player2_win":
                winner = player2.mention
                loser = player1.mention
            else:
                winner = "Draw"
                loser = ""
            
            embed = discord.Embed(
                title="✅ Match Result Updated",
                description="Statistics have been successfully updated!",
                color=0x00ff00
            )
            
            if result != "draw":
                embed.add_field(name="🏆 Winner", value=winner, inline=True)
                embed.add_field(name="💔 Defeated", value=loser, inline=True)
            else:
                embed.add_field(name="🤝 Result", value="Draw", inline=True)
            
            embed.add_field(name="⚔️ Combat Stats", 
                          value=f"{player1.mention}: {player1_kills}K/{player1_deaths}D\n{player2.mention}: {player2_kills}K/{player2_deaths}D", 
                          inline=False)
            
            embed.set_footer(text="Duel Lords Tournament")
            embed.timestamp = datetime.utcnow()
        else:
            embed = discord.Embed(
                title="❌ Update Failed",
                description="One or both players are not registered.",
                color=0xff0000
            )
    except Exception as e:
        logger.error(f"Error updating stats: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="An error occurred while updating statistics.",
            color=0xff0000
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="leaderboard", description="View tournament leaderboard")
async def leaderboard(interaction: discord.Interaction):
    """Display tournament leaderboard"""
    try:
        players = db.get_leaderboard()
        
        if not players:
            embed = discord.Embed(
                title="📊 Tournament Leaderboard",
                description="No players registered yet!",
                color=0xffa500
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title="🏆 Tournament Leaderboard",
            description="Top performers in the Duel Lords tournament",
            color=0xffd700
        )
        
        # Top 10 players
        leaderboard_text = ""
        for i, player in enumerate(players[:10], 1):
            total_matches = player['wins'] + player['losses'] + player['draws']
            win_rate = (player['wins'] / total_matches * 100) if total_matches > 0 else 0
            kd_ratio = (player['kills'] / player['deaths']) if player['deaths'] > 0 else player['kills']
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"`{i}.`"
            
            leaderboard_text += f"{medal} **{player['player_name']}**\n"
            leaderboard_text += f"   Points: `{player['points']}` | W/L/D: `{player['wins']}/{player['losses']}/{player['draws']}`\n"
            leaderboard_text += f"   K/D: `{kd_ratio:.2f}` | Win Rate: `{win_rate:.1f}%`\n\n"
        
        embed.description = leaderboard_text
        embed.set_footer(text="Duel Lords Tournament • Visit our website for full rankings")
        embed.timestamp = datetime.utcnow()
        
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="An error occurred while retrieving the leaderboard.",
            color=0xff0000
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="players", description="List all registered players")
async def list_players(interaction: discord.Interaction):
    """List all registered players"""
    try:
        players = db.get_all_players()
        
        if not players:
            embed = discord.Embed(
                title="👥 Registered Players",
                description="No players registered yet!",
                color=0xffa500
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title="👥 Registered Players",
            description=f"Total registered players: **{len(players)}**",
            color=0x0099ff
        )
        
        player_list = ""
        for i, player in enumerate(players, 1):
            total_matches = player['wins'] + player['losses'] + player['draws']
            player_list += f"`{i}.` **{player['player_name']}** - {total_matches} matches\n"
        
        embed.add_field(name="🎮 Players", value=player_list, inline=False)
        embed.set_footer(text="Duel Lords Tournament")
        embed.timestamp = datetime.utcnow()
        
    except Exception as e:
        logger.error(f"Error listing players: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="An error occurred while retrieving players.",
            color=0xff0000
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="duel", description="Schedule a duel between two players")
async def schedule_duel(interaction: discord.Interaction, player1: discord.Member, player2: discord.Member, 
                       day: int, hour: int, minute: int):
    """Schedule a duel with reminder"""
    try:
        # Validate time
        if not (1 <= day <= 31) or not (0 <= hour <= 23) or not (0 <= minute <= 59):
            embed = discord.Embed(
                title="❌ Invalid Time",
                description="Please provide valid day (1-31), hour (0-23), and minute (0-59).",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Create datetime for the match (assuming current month/year)
        now = datetime.utcnow()
        match_time = datetime(now.year, now.month, day, hour, minute)
        
        # If the date has passed this month, schedule for next month
        if match_time < now:
            if now.month == 12:
                match_time = match_time.replace(year=now.year + 1, month=1)
            else:
                match_time = match_time.replace(month=now.month + 1)
        
        # Save the duel to database
        duel_id = db.schedule_duel(player1.id, player2.id, match_time)
        
        if not duel_id:
            embed = discord.Embed(
                title="❌ Scheduling Failed",
                description="Could not schedule the duel. Please ensure both players are registered.",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Create timestamp for Discord
        timestamp = int(match_time.timestamp())
        
        # Create rich embed
        embed = discord.Embed(
            title="⚔️ Duel Scheduled",
            description="A new tournament match has been scheduled!",
            color=0xff6b35
        )
        
        embed.add_field(name="🥊 Fighters", 
                       value=f"**{player1.mention}** ⚔️ **{player2.mention}**", 
                       inline=False)
        
        embed.add_field(name="🕐 Match Time", 
                       value=f"<t:{timestamp}:F>\n<t:{timestamp}:R>", 
                       inline=True)
        
        embed.add_field(name="🌐 Server", 
                       value=f"`{BOMBSQUAD_IP}:{BOMBSQUAD_PORT}`", 
                       inline=True)
        
        embed.add_field(name="📱 Reminders", 
                       value="Both players will receive a DM reminder 5 minutes before the match", 
                       inline=False)
        
        embed.set_footer(text="Duel Lords Tournament • Good luck to both fighters!")
        embed.timestamp = datetime.utcnow()
        
        # Send DMs to both players
        try:
            dm_embed = discord.Embed(
                title="⚔️ Duel Scheduled",
                description="You have been scheduled for a tournament match!",
                color=0xff6b35
            )
            dm_embed.add_field(name="🥊 Opponent", 
                             value=player2.mention if player1.id != interaction.user.id else player1.mention, 
                             inline=True)
            dm_embed.add_field(name="🕐 Time", 
                             value=f"<t:{timestamp}:F>", 
                             inline=True)
            dm_embed.add_field(name="🌐 Server", 
                             value=f"`{BOMBSQUAD_IP}:{BOMBSQUAD_PORT}`", 
                             inline=False)
            dm_embed.set_footer(text="You'll receive a reminder 5 minutes before the match")
            
            await player1.send(embed=dm_embed)
            await player2.send(embed=dm_embed)
        except discord.Forbidden:
            logger.warning("Could not send DM to one or both players")
        
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        logger.error(f"Error scheduling duel: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="An error occurred while scheduling the duel.",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tasks.loop(minutes=1)
async def reminder_check():
    """Check for upcoming duels and send reminders"""
    try:
        upcoming_duels = db.get_upcoming_duels()
        
        for duel in upcoming_duels:
            try:
                player1 = bot.get_user(duel['player1_id'])
                player2 = bot.get_user(duel['player2_id'])
                
                if player1 and player2:
                    embed = discord.Embed(
                        title="⏰ Match Reminder",
                        description="Your tournament match is starting in 5 minutes!",
                        color=0xff9500
                    )
                    embed.add_field(name="🥊 Opponent", value="Your scheduled opponent", inline=True)
                    embed.add_field(name="🌐 Server", value=f"`{BOMBSQUAD_IP}:{BOMBSQUAD_PORT}`", inline=True)
                    embed.add_field(name="📋 Instructions", 
                                  value="Please join the server and prepare for your match!", 
                                  inline=False)
                    embed.set_footer(text="Duel Lords Tournament • Good luck!")
                    
                    await player1.send(embed=embed)
                    await player2.send(embed=embed)
                
                # Mark reminder as sent
                db.mark_reminder_sent(duel['id'])
                
            except Exception as e:
                logger.error(f"Error sending reminder for duel {duel['id']}: {e}")
                
    except Exception as e:
        logger.error(f"Error in reminder check: {e}")

@reminder_check.before_loop
async def before_reminder_check():
    await bot.wait_until_ready()

def run_bot():
    """Run the Discord bot"""
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable not set!")
        return
    
    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
