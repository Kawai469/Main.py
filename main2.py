import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1497555916235735262)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')

    try:
        synced = await client.tree.sync(guild=GUILD_ID)
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('ping'):
        await message.channel.send(f'pong')

    await client.process_commands(message)  # cần nếu dùng commands

@client.tree.command(name="serverinfo", description="Xem thông tin Server", guild=GUILD_ID)
async def serverinfo(interaction: discord.Interaction):
    await interaction.response.defer()

    guild = interaction.guild

    name = guild.name
    owner = guild.owner or await client.fetch_user(guild.owner_id)
    member_count = guild.member_count

    bots = sum(1 for m in guild.members if m.bot)
    users = sum(1 for m in guild.members if not m.bot)

    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    roles = len(guild.roles)

    embed = discord.Embed(
        title="📊 Thông tin Server",
        color=discord.Color.blue()
        )

    embed.add_field(name="Tên Server", value=name, inline=False)
    embed.add_field(name="Owner", value=owner, inline=False)
    embed.add_field(name="Tổng Member", value=member_count)
    embed.add_field(name="Người dùng", value=users)
    embed.add_field(name="Bot", value=bots)

    embed.add_field(name="Text Channels", value=text_channels)
    embed.add_field(name="Voice Channels", value=voice_channels)
    embed.add_field(name="Categories", value=categories)
    embed.add_field(name="Roles", value=roles)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
        
    await interaction.followup.send(embed=embed)

@client.tree.command(name="avatar", description="Xem avatar")
@app_commands.describe(user="Người muốn xem avatar")
async def avatar(
    interaction: discord.Interaction,
    user: discord.Member = None
):

    # Loading
    await interaction.response.defer()

    # Nếu không nhập user -> lấy chính người dùng
    if user is None:
        user = interaction.user

    embed = discord.Embed(
        title=f"Avatar của {user.name}",
        color=discord.Color.pink()
    )

    # Avatar
    embed.set_image(url=user.display_avatar.url)

    embed.set_footer(
        text=f"ID: {user.id}"
    )

    # Sau defer
    await interaction.edit_original_response(
        embeds=[embed]
    )


TOKEN = os.getenv('DISCORD_TOKEN2')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN2 environment variable is not set")

client.run(TOKEN)