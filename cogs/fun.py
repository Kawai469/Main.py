import discord
from discord.ext import commands

import random
import io
import requests
from PIL import Image, ImageDraw, ImageFont
import time

cooldowns={}

SHIP_CHANNEL_ID = 1503259441074798723
GAY_CHANNEL_ID = 1505579229985771651

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="avatar")
    async def avatar(self, ctx:commands.Context):
        if ctx.message.mentions:
            member=ctx.mentions[0]
        else:
            member=ctx.author
        embed = discord.Embed(
            title=f"Avatar của {member.name}",
            color=0x00ffcc
        )
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="ship")
    async def ship(self, ctx:commands.Context):
        if ctx.channel.id != SHIP_CHANNEL_ID:
            await ctx.send("Bạn chỉ thực hiện lệnh ở https://discord.com/channels/1459553409521684510/1503259441074798723", delete_after= 5)
            return
        if len(ctx.message.mentions) !=2:
            await ctx.send("Cần ping 2 người", delete_afer=5)
            return
        if user1==user2:
            await ctx.send("Bạn không thể ship chính mình", delete_after=5)
            return
        user1=ctx.message.mentions[0]
        user2=ctx.message.mentions[1]

        percent=random.randit(0.100)
        avatar1 = requests.get(user1.display_avatar.url).content
        avatar2 = requests.get(user2.display_avatar.url).content

        avatar1 = Image.open(io.BytesIO(avatar1)).resize((200, 200)).convert("RGBA")
        avatar2 = Image.open(io.BytesIO(avatar2)).resize((200, 200)).convert("RGBA")

        mask = Image.new("L", (200, 200), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 200, 200), fill=255)

        avatar1.putalpha(mask)
        avatar2.putalpha(mask)

        bg = Image.open("romantic-night-sky-5120x2880-25549.jpg").resize((700, 250))

        #dán avt
        bg.paste(avatar1, (30,25), avatar1)
        bg.paste(avatar2, (470, 25), avatar2)

        # vẽ chữ
        draw = ImageDraw.Draw(bg)
        # font
        try:
            font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 40)
        except IOError:
            font = ImageFont.load_default()

        # trái tim
        heart = Image.open("heart.png.png").resize((80, 80))
        bg.paste(heart, (310, 45), heart)

        # phần trăm
        draw.text((290, 140), f"{percent}%", fill="white", font=font)

        # lưu ảnh
        output = io.BytesIO()
        bg.save(output, format="PNG")
        output.seek(0)

        file = discord.File(output, filename="ship.png")

        embed=discord.Embed(title="💖 Ship Result", description=f"{user1.mention} ❤️ {user2.mention}\nĐộ hợp nhau: **{percent}%**", color=discord.Color(0xFCB2C5))
        embed.set_image(url="attachment://ship.png")

        await ctx.send(embed=embed, file=file)

    @commands.command(name="gay")
    async def gay(self, ctx, member: discord.Member = None):

        # Chỉ dùng trong kênh cố định
        if ctx.channel.id != GAY_CHANNEL_ID:
            await ctx.send(
                "Bạn chỉ thực hiện lệnh ở https://discord.com/channels/1459553409521684510/1505579229985771651",
                delete_after=5
            )
            return

        # Cooldown
        user_id = ctx.author.id
        current_time = time.time()

        if user_id in cooldowns:
            remaining = cooldowns[user_id] - current_time

            if remaining > 0:
                timestamp = int(cooldowns[user_id])

                await ctx.send(
                    f"⏳ Bạn cần chờ <t:{timestamp}:R>!",
                    delete_after=10
                )
                return

        cooldowns[user_id] = current_time + 10

        # Nếu không ping ai thì dùng chính mình
        if member is None:
            member = ctx.author

        # Random %
        percent = random.randint(0, 100)

        if percent < 20:
            result = "🗿 Quá thẳng luôn"

        elif percent < 40:
            result = "🙂 Có dấu hiệu nhẹ"

        elif percent < 60:
            result = "🤨 Đáng nghi lắm rồi"

        elif percent < 80:
            result = "😳 Gay khá rõ"

        else:
            result = "🏳️‍🌈 Siêu gay"

        embed = discord.Embed(
            title="🏳️‍🌈 Gay Detector",
            description=(
                f"{member.mention} gay **{percent}%**\n\n"
                f"{result}"
            ),
            color=discord.Color.random()
        )

        await ctx.send(embed=embed)

        
async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))