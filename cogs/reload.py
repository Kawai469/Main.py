from discord.ext import commands

class ReloadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        await self.bot.reload_extension(f"cogs.{cog}")
        await ctx.send(f"Đã reload {cog}")

async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCog(bot))