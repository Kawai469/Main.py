import discord
from discord.ext import commands

import time
from datetime import datetime, timezone

intents = discord.Intents.default()
intents.members = True

class ModeratorCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

@commands.command(name="roleinfo")
async def roleinfo(self, ctx:commands.Context):
    if not ctx.message.role_mentions:
        await ctx.send("Bạn cần ping 1 role")
        return
    role = ctx.message.role_mentions[0]
    mentionable = "Có" if role.mentionable else "Không"
    member_count = len(role.members)
    created = role.created_at
    now = datetime.now(timezone.utc)
    days = (now - created).days
    permissions = [perm.replace("_", " ").title()
        for perm, value in role.permissions
        if value]
    permissions_text = ("\n".join(f"• {p}" for p in permissions)
        if permissions else
        "Không có quyền nào")
    hoist = "Có" if role.hoist else "Không"
    role_icon = role.display_icon.url if role.display_icon else "Không có"
    role_type = "Ổn Định"
    color_info = str(role.color)
    embed = discord.Embed(title=f"Thông Tin Role: {role.name}",
        color=role.color if role.color.value else discord.Color.blurple())
    embed.add_field(
        name="📛 Tên Role",
        value=role.name,
        inline=False
    )

    embed.add_field(
        name="🆔 ID",
        value=role.id,
        inline=True
    )

    embed.add_field(
        name="👥 Thành viên",
        value=member_count,
        inline=True
    )

    embed.add_field(
        name="🎨 Kiểu màu",
        value=role_type,
        inline=True
    )

    embed.add_field(
        name="🌈 Mã màu",
        value=color_info,
        inline=True
    )

    embed.add_field(
        name="📌 Hiển thị riêng",
        value=hoist,
        inline=True
    )

    embed.add_field(
        name="📢 Cho phép mention",
        value=mentionable,
        inline=True
    )

    embed.add_field(
        name="🕒 Ngày tạo",
        value=f"<t:{int(created.timestamp())}:F>",
       inline=False
    )

    embed.add_field(
        name="⏳ Đã tồn tại",
        value=f"{days} ngày",
        inline=False
    )

    embed.add_field(
        name="🎭 Icon Role",
        value=role_icon,
        inline=False
    )

    embed.add_field(
        name="🔐 Quyền",
        value=permissions_text[:1024],
        inline=False
    )
    if role.display_icon:
        embed.set_thumbnail(url=role.display_icon.url)
    await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ModeratorCog(bot))