import discord
from discord.ext import commands

import random

KAWAI_ID = 1307657523926663189

class KawaiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="tx")
    async def tx(self, ctx: commands.Context):
        if ctx.author.id != KAWAI_ID:
            await ctx.send("Bạn không có quyền sử lệnh", delete_after=5)
            return
        percent=random.randint(0,100)
        if percent < 50:
            result="head"
        else:
            result="tail"
    
        await ctx.send(f"Kết quả: {result}")

async def setup(bot: commands.Bot):
    await bot.add_cog(KawaiCog(bot))