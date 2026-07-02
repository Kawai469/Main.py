import discord
import random
import time
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import keep_alive
from cryptography.fernet import Fernet
import base64
import hashlib
import requests 
import io
from datetime import datetime, timezone
import re
import asyncio
import aiohttp

from PIL import Image, ImageDraw, ImageFont

load_dotenv()

# ===== ENCRYPTION SYSTEM =====
class SecretManager:
    """Manages encryption/decryption of sensitive data"""
    
    def __init__(self, master_password: str):
        """Initialize with master password"""
        # Derive a key from master password
        key = base64.urlsafe_b64encode(hashlib.sha256(master_password.encode()).digest())
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt sensitive data"""
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            raise ValueError(f"Decryption failed - wrong password or corrupted data: {e}")

# Get master password from environment or user input
MASTER_PASSWORD = os.getenv('MASTER_PASSWORD')
if not MASTER_PASSWORD:
    print("⚠️  MASTER_PASSWORD not set in environment variables!")
    print("Set MASTER_PASSWORD env var to decrypt secrets")
    MASTER_PASSWORD = ""

if MASTER_PASSWORD:
    secret_manager = SecretManager(MASTER_PASSWORD)
else:
    secret_manager = None

cooldowns = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix=["k!","K!"], intents=intents, case_insensitive=True)
client.load_extension("cogs.fun")

class TraLoiModal(discord.ui.Modal, title="Trả lời câu hỏi"):
    cau_tra_loi = discord.ui.TextInput(
        label="Câu trả lời của bạn",
        placeholder="Nhập nội dung...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        log_channel = interaction.guild.get_channel(LOGTRL_ID)

        embed = discord.Embed(
            title="📩 Có câu trả lời mới",
            description=self.cau_tra_loi.value,
            color=discord.Color.green()
        )
        embed.add_field(
            name="👤 Người trả lời",
            value=interaction.user.mention,
            inline=False
        )
        if log_channel:
            await log_channel.send(embed=embed)
        await interaction.response.send_message("Đã gửi câu trả lời", ephemeral=True)
        await interaction.response.send_message(embed=embed)

class TraLoiView(discord.ui.View):
    @discord.ui.button(
        label="Trả Lời",
        style=discord.ButtonStyle.primary
    )
    async def traloi(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(
            TraLoiModal()
        )

# ===== ID ZONE =====

GUILD_ID = discord.Object(id=1459553409521684510)
ALLOWED_ID = 1307657523926663189
CHANNEL_ID = 1459553410381512776
LOGTRL_ID = 1508014060510380052
KAWAI_ID = 1307657523926663189
KAWAI2_ID = 1499602905567596665
RULES_MESSAGE_ID = 1495053362553557077
CARLBOT_ID = 235148962103951360

# ===== LỆNH KHỞI ĐỘNG BOT =====

@client.event
async def on_ready():
    print(f'Đã đăng nhập vào {client.user}!')
    try:
        synced = await client.tree.sync(guild=GUILD_ID)
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


@client.event
async def on_error(event, *args, **kwargs):
    import traceback
    print(f'Error in {event}: {traceback.format_exc()}')

# ===== LỆNH CHẠY BOT =====

@client.event
async def on_message(message):

    global RULES_MESSAGE_ID

    if message.author == client.user:
        return

    if message.content.lower() == "k!serverinfo":
        guild = message.guild
        name = guild.name
        owner = guild.owner or await client.fetch_user(guild.owner_id)
        member_count = guild.member_count
        bots = sum(1 for m in guild.members if m.bot)
        users = member_count - bots
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        roles = len(guild.roles)

        embed = discord.Embed(title="📊 Thông tin Server", color=discord.Color.blue())
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
        await message.channel.send(embed=embed)
    
    elif message.content.startswith("!chat2 "):
        if message.author.id != ALLOWED_ID:
            await message.channel.send("Bạn không có quyền sử dụng lệnh này")
            return
        content = message.content[7:]
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(content)
            await message.channel.send("✅ Đã gửi!")
        else:
            await message.channel.send("❌ Không tìm thấy channel!")

    elif message.content.lower().startswith("!ktratnhan"):
        if message.author.id != ALLOWED_ID:
            await message.channel.send("Bạn không có quyền kiểm tra tin nhắn")
            return
        if len(message.mentions) == 0:
            await message.channel.send(
                "Hãy mention người cần kiểm tra."
            )
            return

        member = message.mentions[0]

        start_date = datetime(
            2026, 5, 4,
            tzinfo=timezone.utc
        )

        end_date = datetime(
            2026, 5, 31, 23, 59, 59,
            tzinfo=timezone.utc
        )

        count = 0
        links = []

        await message.channel.send(
            "🔍 Đang quét lịch sử tin nhắn..."
        )

        for channel in message.guild.text_channels:

            try:

                async for msg in channel.history(
                    limit=None,
                    after=start_date,
                    before=end_date
                ):

                    if msg.author.id == member.id:

                        count += 1

                        links.append(
                            f"• {msg.jump_url}"
                        )

            except discord.Forbidden:
                continue

        embed = discord.Embed(
            title="📊 Thống kê tin nhắn",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="👤 Thành viên",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="💬 Số tin nhắn",
            value=str(count),
            inline=False
        )

        # Discord giới hạn 1024 ký tự mỗi field
        if links:
            embed.add_field(
                name="🔗 Link tin nhắn",
                value="\n".join(links[:20]),
                inline=False
            )

        await message.channel.send(
            embed=embed
        )

    elif message.content.startswith("!createchannel"):
        args = message.content.split(" ", 1)
        if len(args) < 2:
            await message.channel.send("nhập tên channel")
            return
        name = args[1]
        channel = await message.guild.create_text_channel(name)
        await message.channel.send(f"đã tạo channel: {channel.mention}")

    elif message.content.startswith("!deletechannel"):
        if len(message.channel.mentions) == 0:
            await message.channel.send("hãy ping channel để xóa")
            return
        channel = message.channel_mentions[0]
        await channel.delete()

    elif message.content.startswith("!editchannel"):
        args = message.content.split(" ")
        if len(message.channel_mentions) ==0:
            await message.channel.send("hãy ping channel")
            return
        if len(args) < 3:
            await message.channel.send("nhập tên mới")
            return
        channel = message.channel_mentions[0]
        new_name = args[-1]
        await channel.edit(name=new_name)
        await message.channel.send(f"đã đổi tên thành {new_name}")

    elif message.content.startswith("!addrole"):
        if len(message.mentions) == 0:
            await message.channel.send("mention user")
            return
        member = message.mentions[0]
        role = discord.utils.get(
            message.guild.roles,
            name="Member"
        )
        if role is None:
            await message.channel.send("Không tìm thấy role")
            return
        await member.add_roles(role)
        await message.channel.send(
            f"đã add role {role.mention} cho {member.mention}"
        )

    elif message.content.startswith("!addrole"):
        if len(message.mentions) == 0:
            await message.channel.send("mention user")
            return
        member = message.mentions[0]
        role = discord.utils.get(
            message.guild.roles,
            name="Member"
        )
        if role is None:
            await message.channel.send("Không tìm thấy role")
            return
            await member.remove_roles(role)
            await message.channel.send(f"Đã xoá role {role.mention} khỏi {member.mention}")

    elif message.content.lower() == "!webhook":
        if message.author.id != ALLOWED_ID:
            await message.channel.send("❌ Bạn không có quyền.")
            return

        url = os.getenv("WEBHOOK_URL")

        if not url:
            await message.channel.send("❌ Chưa thiết lập WEBHOOK_URL.")
            return

        data = {
            "content": "https://discord.gg/HxPCChgAKw"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 204:
                    await message.channel.send("✅ Đã gửi webhook!")
                else:
                    await message.channel.send(f"❌ Lỗi webhook ({response.status})")

    elif message.content.startswith("!dm"):
        if message.author.id != ALLOWED_ID:
            await message.channel.send("❌ Bạn không có quyền sử dụng lệnh này!")
            return

        if not message.mentions:
            await message.channel.send("❌ Vui lòng mention người cần gửi.")
            return

        args = message.content.split(" ", 2)

        if len(args) < 3:
            await message.channel.send("❌ Vui lòng nhập nội dung.")
            return

        member = message.mentions[0]
        content = args[2]

        try:
            await member.send(content)
            await message.channel.send(f"✅ Đã gửi DM cho **{member}**!")
        except Exception:
            await message.channel.send("❌ Không thể gửi DM cho người này.")

    elif message.content.startswith("!chat "):
        if message.author.id != ALLOWED_ID:
            await message.channel.send("Bạn không có quyền sử dụng lệnh này!")
            return
        content = message.content[6:]
        await message.delete()
        await message.channel.send(content)

    # ===== EMBED ZONE =====

    elif message.content.lower() == "k!menu":
        embed = discord.Embed()
        embed.title = "Menu Tiệm Trà"
        embed.description = """**## 🌸✨ MENU TRÀ "NỮ HOÀNG" ✨🌸

"Một chút ngọt ngào cho ngày bình yên..."

### ╭─────────────♡─────────────╮

🍵 TRÀ NHẸ NHÀNG ❀
🌸 Trà hoa anh đào – 24k
🍃 Trà lài sữa nhẹ – 22k
🍯 Trà mật ong chanh – 25k
ꕀꕀꕀꕀꕀꕀꕀꕁꕀꕀꕀꕀꕀꕀꕀ
🧋 TRÀ SỮA NGỌT NGÀO ❀
🐰 Trà sữa trân châu – 25k
🍓 Trà sữa dâu – 28k
🍵 Matcha latte – 32k
🍫 Socola sữa – 32k
🍮 Caramel milk tea – 35k
ꕀꕀꕀꕀꕀꕀꕀꕁꕀꕀꕀꕀꕀꕀꕀ
🍹 TRÀ TRÁI CÂY MÁT LẠNH
🍊 Trà cam sả – 28k
🍉 Trà dưa hấu – 25k
🍇 Trà nho – 27k
🍋 Trà chanh leo – 27k
ꕀꕀꕀꕀꕀꕀꕀꕁꕀꕀꕀꕀꕀꕀꕀ
🍨 ĐỒ ĂN NGOÀI
🍪 Cookies & Cream – 40k (loại lớn)
🍪 Cookies & Cream – 28k (loại nhỏ)
⚡ Sting – 10k
🍮 Pudding trứng – 8k

### ╰─────────────♡─────────────╯

💖 ƯU ĐÃI NHỎ XINH
🌟 Mua 2 ly giảm 10%
💌 Khách quen được giảm giá bí mật**"""
        embed.color = discord.Color(0xFCB2C5)
        embed.set_footer(text="""🌙 GÓC NHẮN NHỦ:
"Dù hôm nay có mệt mỏi, hãy để một ly trà làm dịu tâm hồn bạn nhé...""")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494344734121005076/5c535af93368c98666e3c8ee70cd8ee5.gif")
        await message.channel.send(embed=embed)

    elif message.content == "!luatletan":
        embed = discord.Embed(
            title="Luật Lễ Tân",
            description="""# I. Lễ Tân đối với Khách

## 1. Thái độ lịch sự
- Luôn chào hỏi và nói chuyện lịch sự với thành viên mới.
- Không dùng lời toxic, xúc phạm hoặc gây tranh cãi.
## 2. Chào đón thành viên mới
- Khi có Khách mới vào Quán, Lễ Tân nên:
- Chào mừng 
- Hướng dẫn đọc kênh luật 
## 3. Hướng dẫn đúng thông tin
- Chỉ hướng dẫn những thông tin chính xác của Server.
## 4. Hoạt động tương đối thường xuyên
- Khi online nên hỗ trợ Khách mới nếu họ cần.""",
            color=discord.Color(0xFCB2C5)
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494182901976141956/dcd78396326fab10cd9c7b5a3f1e75cf.jpg?ex=69e1adc4&is=69e05c44&hm=fe953a09415d90b08d07ffa527bec2db675721463ec1f4838a38b7cf6a946396&")
        embed2 = discord.Embed(
            description="""# II. Lễ Tân dối với Ticket (Quầy Lễ Tân)

## 1. Phản hồi
- Càng nhanh càng tốt
## 2. Thái độ
- Luôn lịch sự, tôn trọng, không toxic.
- Không tranh cãi với member.
- Không dùng từ ngữ thô tục, gây khó chịu.
## 3. Xử lí vấn đề
- Đọc kĩ vấn đề của Khách
- Nếu chưa, hãy hỏi thắc mắc
## 4. Bảo Mật
- Không chia sẻ nội dung ticket ra ngoài.
Không leak thông tin cá nhân của Khách
## 5. Trường hợp khác
**Không tự xử lý nếu:**
- Liên quan đến ban/unban
- Khiếu nại
- Vấn đề nghiêm trọng
**- Tag hoặc chuyển cho Mod/Admin.**
## 6. Đóng ticket
**Chỉ đóng khi:**
- Khách xác nhận đã giải quyết xong
- Hoặc không phản hồi sau 24–48h
## 7 Những điều KHÔNG được làm
- Không trả lời kiểu “idk”, “tự tìm đi”
- Không lạm dụng quyền hạn
## 8. Ghi nhận lỗi
**Nếu member báo lỗi server/bot:**
- Ghi lại chi tiết
- Báo cho Quản lý/Chủ Quán""",
            color=discord.Color(0xFCB2C5)
        )
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494186163488165919/eb667e1bf9915395a7847f5f5f1230ad.jpg?ex=69e1b0ce&is=69e05f4e&hm=7b1ca98122d541da3d33c02d8835de11d80844c0a2beda5c768c9dd7818f7048&")
        embed3 = discord.Embed(
            description="""## III. Lễ Tân đối với Lễ Tân
### 1. Lương 
- Chào Khách Mới = 10k
**Lưu ý: Chào đầu tiên được thưởng**
### 2. Hình Phạt
Lần 1: Nhắc nhở
Lần 2: Trừ lương
Lần 3: Hủy lương
Lần 4: Đuổi việc
**Lưu ý: những việc khác nhưng nặng thì không cần nhắc và sẽ trừ lương/ hủy lương/ đuổi việc**
### 3. Làm tốt
- Những bạn nào chăm ngoan, làm việc tốt sẽ lên @ Thực Tập Sinh
**### 4. Lưu Ý
- Mỗi lần Mem mới vô thì cần 1 Lễ Tân chào được rồi, không cần 2-3 Lễ Tân ping có câu hướng dẫn đọc luật phiền Khách**""",
            color=discord.Color(0xFCB2C5)
        )
        embed3.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1498604585185447946/5102ea84ec5e84d61fb24477a758a3fb.jpg?ex=69f1c3c7&is=69f07247&hm=a60f0216db9461d78f0b9a13df6dd3d5e62150a5f60353e2cdb3e73478040693&")
        await message.channel.send(embeds=[embed, embed2, embed3])

    elif message.content == "!cauhoi":
        embed = discord.Embed(
            title="Câu hỏi 1",
            description="Yuzi Béo Không?",
            color=discord.Color.red()
        )
        await message.channel.send(
            embed=embed,
            view=TraLoiView()
        )

    elif message.content == "!emoji":
        embed = discord.Embed(title="Emoji Test", description="Testing custom emojis", color=discord.Color.purple())
        embed.set_footer(text="<:Zero_Love:1490270183707644025>")
        sent_message = await message.channel.send(embed=embed)
        RULES_MESSAGE_ID = sent_message.id
        await message.channel.send(embed=embed)

    elif message.content == "!editrules":
        if RULES_MESSAGE_ID is None:
            await message.channel.send("Không thấy Rules Embed")
            return
        if message.author.id != ALLOWED_ID:
            await message.channel.send("Bạn không có quyền")
            return

        old_message = await message.channel.fetch_message(RULES_MESSAGE_ID)
            
        new_embed = discord.Embed(
            title="『📃』ʟᴜậᴛˋˋᴛʀà",
            description="""1. Tôn Trọng Những Người Trong Tiệm
2. Cấm Chửi Bới, Xúc Phạm, công kích cá nhân dưới mọi hình thức
3. Cấm Gửi Nội Dung 18+, Phản Cảm, Bạo Lực, Nhạy Cảm, Nsfw Và Gore
4. Cấm Quảng Cáo, Gửi Link Server Khác Khi Chưa Được Phép (Trừ Partners)
5. Cấm Spam Dưới Mọi Hình Thức
6. Cấm Leak Thông Tin Cá Nhân Người Khác
7. Chat Đúng Chủ Đề của Từng Kênh
8. Xài Bot Đúng Nơi Quy Định""",
            color=discord.Color(0xFCB2C5)
        )
        new_embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494182901976141956/dcd78396326fab10cd9c7b5a3f1e75cf.jpg?ex=69e1adc4&is=69e05c44&hm=fe953a09415d90b08d07ffa527bec2db675721463ec1f4838a38b7cf6a946396&")
        new_embed2 = discord.Embed(
            description="""# Hình Phạt
Vi phạm lần 1: Warn
Vi phạm lần 2: Warn
Vi phạm lần 3: Warn
Vi phạm lần 4: Mute 1 Ngày
Vi phạm lần 5: Mute 3 Ngày
Vi phạm lần 6: Mute 7 Ngày
Vi phạm lần 7: Mute 14 Ngày
Vi phạm lần 8: Ban 1 Ngày
Vi phạm lần 9: Ban 3 Ngày
Vi phạm lần 10: Ban 7 Ngày
Vi phạm lần 11: Ban 14 Ngày
Vi phạm lần 12: Ban Vĩnh Viễn

# Trường Hợp Xử Lí Đặc Biệt

Đăng vid, hình ảnh mang tính chất Chính Trị, Gây Hại, Low Nsfw, Low Gore: Mute 14 Ngày
Đăng vid, hình ảnh mang tính chất Nsfw, Gore: ban vĩnh viễn
Leak thông tin cá nhân: Ban Vĩnh Viễn
Sử dụng acc Clone để tránh Mute, Ban,...: Ban Vĩnh Viễn (  cả chính và Clone)
Acc bị Hack, Scam: Ban Vĩnh Tiễn
**__Lưu Ý__**: 1. Những trường hợp nặng dù không được nêu rõ trong luật vẫn xử lí nghêm khắc
2. Luật có thể thay đổi bất cứ lúc nào
3. Nếu gặp các Manager Server vi phạm luật thì cứ báo cáo ở https://discord.com/channels/1459553409521684510/1463538921832059001 để được xử lí nhé!""",
            color=discord.Color(0xFCB2C5)
        )
        new_embed2.set_footer(text="Chúc Bạn Có Thời Gian Vui Vẻ Nha! <3")
        new_embed2.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494186163488165919/eb667e1bf9915395a7847f5f5f1230ad.jpg?ex=69e1b0ce&is=69e05f4e&hm=7b1ca98122d541da3d33c02d8835de11d80844c0a2beda5c768c9dd7818f7048&")
        await old_message.edit(embed=new_embed)
        await message.channel.send(content="Các bạn đọc luật để tránh bị Warn, Mute hoặc Ban nha<:Zero_Love:1490270183707644025>", embeds=[new_embed, new_embed2])

    elif message.content == "!rulespartner":
        embed = discord.Embed(title="Điều kiện Partner", description="""- Server có hoạt động thường xuyên (không dead)
- Server phải 100 Member trở lên
- Phải sử dụng Link Vĩnh Viễn
- Server không có NSFW, Scam,... Những thứ vi phạm tiêu chuẩn cộng đồng
- Trường hợp người đại diện out Server hoặc xóa bài thì Server tụi mình sẽ xóa theo

**__Lưu Ý:__** Server trở về chỉ ping <@&1503409786085965974> để tránh gây phiền và ảnh hưởng Member""", color=discord.Color(0xFCB2C5))
        embed.set_footer(text="Sửa đổi lần cuối 19/06/2026")
        await message.delete()
        await message.channel.send(embed=embed)

    elif message.content == "!roleinfo":
        embed = discord.Embed(
            title="Các Thông Tin Về Role Server",
            description="""# Role Quản Lí

<@&1459553975396466880> : Chủ Server
<@&1459754108486553751> : Trưởng Quản lý, điều hành Sivi
<@&1459554666458386718> : Quản lý Kênh, Sivi 
<@&1479882660041199757> : Quản lý bot
<@&1459754552285724738> : Có kinh nghiệm, làm việc lâu và quản lí, hướng dẫn các <@&1459756165146738952> và <@&1459555244186013749>
<@&1459555244186013749> : Quản lý Member
<@&1459756165146738952> : Những bạn thực tập để lên <@&1459555244186013749> 
<@&1459753366019248209> : Đón Tiếp, Hướng Dẫn Và Hỗ Trợ Member
<@&1459558389230207006> : Bot Hỗ Trỡ Server

# Role Đặc Biệt
<@&1484803226095190147> 

<@&1459762480178925601> : Bạn Của Chủ Quán và nhận các quyền thưởng lợi như:
- Gửi ảnh/vid, sử dụng Emoji/Sticker/SoundBoard ngoài Server, nhúng Link liên kết

<@&1501002947214180372>

> Đối với Booster Server sẽ nhận được các thưởng lợi sau đây:
- Nhận được Custom Role free trong `1 tháng`
- Mở khoá các quyền như: gửi ảnh/vid, sử dụng Emoji/Sticker/SoundBoard ngoài Server, nhúng Link liên kết

<@&1494212948338413658> <@&1493930685306507325> <@&1483309965354729592> 

Nhân Viên Phục Vụ trong Trà Quán

<@&1485186735028703435> 

Là 2 bên Server quảng cáo và hợp tác với nhau, được post và quảng cáo ở <#1485199404599214090> và <#1484408516721508563> 

# Custom Role

- Có thể sở hữu Role Custom từ các Giveaway, sự kiện,... hoặc mua với 100.000 Owo/ tháng
- **__Lưu ý:__** Nếu ai sở hữu Custom Role mà out hoặc Ban Vĩnh Viễn Server thì nó sẽ bị **xóa**

# Role Level
<@&1481975631678799903> 

https://discord.com/channels/1459553409521684510/1459770418410950770

# Role Khác 
<@&1495034749545222304> Ko thể nhận EXP
<@&1494283924820459520> bị cấm chat trong khoảng tgian**""",
            color=discord.Color(0xFCB2C5)
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1498604585185447946/5102ea84ec5e84d61fb24477a758a3fb.jpg?ex=69f1c3c7&is=69f07247&hm=a60f0216db9461d78f0b9a13df6dd3d5e62150a5f60353e2cdb3e73478040693&")
        await message.channel.send(embed=embed)

    elif message.content == "!infolevel":
        embed = discord.Embed(
            description="""# Thông Tin về Role Levels

### - Level: 5 <@&1459747725917556857>  : Đổi tên trong server, Được quyền gửi ảnh, video, link nhúng và gửi emoji, sticker ngoài Server
### - Level: 10 <@&1459748084769624158>: Được quyền gửi Link nhúng
### - Level: 15 <@&1459748426215325854> 
### - Level: 20 <@&1459748664170525854> 
### - Level: 25 <@&1459749092065280040>  : Được Custom Role 1 Tuần 
### - Level: 30 <@&1459749260454264944> 
### - Level: 35 <@&1459749256557760632>
### - Level: 40 <@&1459749248299171950> 
### - Level: 45 <@&1459749242909364323>: Được Custom Role 1 Tháng
### - Level: 50 <@&1459749240279531571> 
### - Level: 55 <@&1459749236190220369> 
### - Level: 60 <@&1459749231630749871>   
### - Level: 65 <@&1459749222948802673> : Custom Role Vĩnh Viễn 
### - Level: 70 <@&1459750280022200392>  
### - Level: 75 <@&1459750347055566993>""",
            color=discord.Color.red()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1498598473249849394/6fe6ef210ba77ad0e2459eb68a2dcb2d.jpg?ex=69f1be16&is=69f06c96&hm=33a5e193a21cd1d03d7528766b30703e7af0ed8a5654d4c52784a9a50f142d94&")
        await message.channel.send(embed=embed)

    elif message.content == "!ticketrules":
        embed = discord.Embed(
            title="HƯỚNG DẪN SỬ DỤNG TICKET HỢP LÝ",
            description="""## 1. Ticket dùng để làm gì?
### Ticket được mở để xử lý các trường hợp sau:
Hỗ trợ kỹ thuật / lỗi bot / lỗi server

> - Không nhận được role
> - Bot không phản hồi
> - Lỗi bot, event,...

### GÓP Ý – ĐỀ XUẤT
- Ý tưởng event mới.
- Gợi ý cải thiện server.
- Đề xuất thêm/bớt kênh, tính năng
### Report người vi phạm

- Spam, toxic, scam, xúc phạm
- Quấy rối người khác
- Gửi ảnh, link không phù hợp
(YÊU CẦU: có bằng chứng ảnh hoặc video)

### Gửi khiếu nại / phản hồi

- Bị mute/ban/kick oan
- Muốn giải thích về một tình huống

### Xin hỗ trợ riêng tư

- Không muốn nói ở chat công khai
- Vấn đề nhạy cảm cần Lễ Tân xử lý

## 2. Ticket KHÔNG được dùng để làm gì?

- Không mở ticket cho các lý do sau:
> - Hỏi chuyện linh tinh (như chat, hỏi thăm, meme)
> - Gây sự, troll, đùa giỡn Lễ Tân
> - Spam mở nhiều ticket liên tục
> - Cãi nhau với người khác và lôi Lễ Tân vào nếu không cần thiết
> - Xin role không liên quan
> - Nếu bạn cố tình lạm dụng → Warn / mute / ban

## 3. Cách mở ticket đúng cách

1. Nhấn vào nút “🎫 Open Ticket”
2. Nêu rõ lí do tạo ticket (Report / Support / Appeal).
3. Ghi rõ nội dung ngay khi mở:
Vấn đề gì?
Xảy ra khi nào?
Bạn có bằng chứng không?
4. Đính kèm hình ảnh hoặc video

> Càng rõ ràng → Lễ Tân xử lý càng nhanh.

## 4. Cách làm việc trong ticket

- Luôn giữ thái độ bình tĩnh, lịch sự.
- Không kéo người không liên quan vào ticket (trừ khi Lễ Tân yêu cầu).
- Không spam tin nhắn.

## 5. Đóng ticket

### Ticket sẽ được đóng khi:

- Vấn đề được giải quyết
- Bạn xác nhận đã xong""",
            color=discord.Color(0xFCB2C5)
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1498547991970320464/341d0e8691a316891bf88a69f2abf90f.jpg?ex=69f18f12&is=69f03d92&hm=8aeeb40e4157c584a3248f5eef3e2b17cde4dfe8eb9e12cfac076d2aa3630cbc&")
        await message.channel.send(embed=embed)

    elif client.user.mentioned_in(message):
        await message.reply(
            "https://cdn.discordapp.com/attachments/1498885197192495208/1507593582641549363/image0.gif?ex=6a12776f&is=6a1125ef&hm=4f84997e94316f36d47fa2d8b89a833813fc9effb7396c8bd197eea27676b15d&"
        )

    await client.process_commands(message)

# ===== SLASH COMMAND ZONE =====

@client.tree.command(name="roleinfo", description="Xem thông tin role", guild=GUILD_ID)
async def roleinfo(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.defer()

    mentionable = "Có" if role.mentionable else "Không"
    hoist = "Có" if role.hoist else "Không"

    created = role.created_at
    now = datetime.now(timezone.utc)

    days = (now - created).days

    permissions = [
        perm.replace("_", " ").title()
        for perm, value in role.permissions
        if value
    ]

    permissions_text = (
        "\n".join(f"• {p}" for p in permissions)
        if permissions
        else "Không có quyền nào"
    )

    embed = discord.Embed(
        title=f"📜 Thông Tin Role: {role.name}",
        color=role.color
    )

    embed.add_field(
        name="🆔 ID",
        value=role.id,
        inline=True
    )

    embed.add_field(
        name="👥 Thành viên",
        value=len(role.members),
        inline=True
    )

    embed.add_field(
        name="📢 Cho phép mention",
        value=mentionable,
        inline=True
    )

    embed.add_field(
        name="📌 Hiển thị riêng",
        value=hoist,
        inline=True
    )

    embed.add_field(
        name="🎨 Màu",
        value=str(role.color),
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
        name="🔐 Quyền",
        value=permissions_text[:1024],
        inline=False
    )

    if role.display_icon:
        embed.set_thumbnail(url=role.display_icon.url)

    await interaction.followup.send(embed=embed)

@client.tree.command(name="rules", description="Xem Luật Server", guild=GUILD_ID)
async def rules(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="『📃』ʟᴜậᴛˋˋᴛʀà",
        description="""1. Tôn Trọng Những Người Trong Tiệm
2. Cấm Chửi Bới, Xúc Phạm, công kích cá nhân dưới mọi hình thức
3. Cấm Gửi Nội Dung 18+, Phản Cảm, Bạo Lực, Nhạy Cảm, Nsfw Và Gore
4. Cấm Quảng Cáo, Gửi Link Server Khác Khi Chưa Được Phép (Trừ Partners)
5. Cấm Spam Dưới Mọi Hình Thức
6. Cấm Leak Thông Tin Cá Nhân Người Khác
7. Chat Đúng Chủ Đề của Từng Kênh
8. Xài Bot Đúng Nơi Quy Định""",
            color=discord.Color(0xFCB2C5)
        )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494182901976141956/dcd78396326fab10cd9c7b5a3f1e75cf.jpg?ex=69e1adc4&is=69e05c44&hm=fe953a09415d90b08d07ffa527bec2db675721463ec1f4838a38b7cf6a946396&")
    embed2 = discord.Embed(
        description="""# Hình Phạt
Vi phạm lần 1: Warn
Vi phạm lần 2: Warn
Vi phạm lần 3: Warn
Vi phạm lần 4: Mute 1 Ngày
Vi phạm lần 5: Mute 3 Ngày
Vi phạm lần 6: Mute 7 Ngày
Vi phạm lần 7: Mute 14 Ngày
Vi phạm lần 8: Ban 1 Ngày
Vi phạm lần 9: Ban 3 Ngày
Vi phạm lần 10: Ban 7 Ngày
Vi phạm lần 11: Ban 14 Ngày
Vi phạm lần 12: Ban Vĩnh Viễn

# Trường Hợp Xử Lí Đặc Biệt

Đăng vid, hình ảnh mang tính chất Chính Trị, Gây Hại, Low Nsfw, Low Gore: Mute 14 Ngày
Đăng vid, hình ảnh mang tính chất Nsfw, Gore: ban vĩnh viễn
Leak thông tin cá nhân: Ban Vĩnh Viễn
Sử dụng acc Clone để tránh Mute, Ban,...: Ban Vĩnh Viễn (  cả chính và Clone)
Acc bị Hack, Scam: Ban Vĩnh Tiễn
**__Lưu Ý__**: 1. Những trường hợp nặng dù không được nêu rõ trong luật vẫn xử lí nghêm khắc
2. Luật có thể thay đổi bất cứ lúc nào
3. Nếu gặp các Manager Server vi phạm luật thì cứ báo cáo ở https://discord.com/channels/1459553409521684510/1463538921832059001 để được xử lí nhé!""",
            color=discord.Color(0xFCB2C5)
        )
    embed2.set_footer(text="Chúc Bạn Có Thời Gian Vui Vẻ Nha! <3")
    embed2.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494186163488165919/eb667e1bf9915395a7847f5f5f1230ad.jpg?ex=69e1b0ce&is=69e05f4e&hm=7b1ca98122d541da3d33c02d8835de11d80844c0a2beda5c768c9dd7818f7048&")
    await interaction.followup.send(
        content="Các bạn đọc luật để tránh bị Warn, Mute hoặc Ban nha<:Zero_Love:1490270183707644025>",
        embeds=[embed, embed2]
    )

@client.tree.command(name="menu", description="Xem Menu Trà Quán", guild=GUILD_ID)
async def menu(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed()
    embed.title = "Menu Tiệm Trà"
    embed.description = """🌸✨ MENU TRÀ "NỮ HOÀNG" ✨🌸

"Một chút ngọt ngào cho ngày bình yên..."

╭─────────────♡─────────────╮

🍵 TRÀ NHẸ NHÀNG ❀
🌸 Trà hoa anh đào – 24k
🍃 Trà lài sữa nhẹ – 22k
🍯 Trà mật ong chanh – 25k
ꕀꕀꕀꕀꕀꕀꕀꕁꕀꕀꕀꕀꕀꕀꕀ
🧋 TRÀ SỮA NGỌT NGÀO ❀
🐰 Trà sữa trân châu – 25k
🍓 Trà sữa dâu – 28k
🍵 Matcha latte – 32k
🍫 Socola sữa – 32k
🍮 Caramel milk tea – 35k
ꕀꕀꕀꕀꕀꕀꕀꕁꕀꕀꕀꕀꕀꕀꕀ
🍹 TRÀ TRÁI CÂY MÁT LẠNH
🍊 Trà cam sả – 28k
🍉 Trà dưa hấu – 25k
🍇 Trà nho – 27k
🍋 Trà chanh leo – 27k
ꕀꕀꕀꕀꕀꕀꕀꕁꕀꕀꕀꕀꕀꕀꕀ
🍨 ĐỒ ĂN NGOÀI
🍪 Cookies & Cream – 40k (loại lớn)
🍪 Cookies & Cream – 28k (loại nhỏ)
⚡ Sting – 10k
🍮 Pudding trứng – 8k

╰─────────────♡─────────────╯

💖 ƯU ĐÃI NHỎ XINH
🌟 Mua 2 ly giảm 10%
💌 Khách quen được giảm giá bí mật

🌙 GÓC NHẮN NHỦ:
"Dù hôm nay có mệt mỏi, hãy để một ly trà làm dịu tâm hồn bạn nhé..."""
    embed.color = discord.Color(0xFCB2C5)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494344734121005076/5c535af93368c98666e3c8ee70cd8ee5.gif")
    await interaction.followup.send(embed=embed)

@client.tree.command(name="avatar", description="Xem Avatar", guild=GUILD_ID)
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    await interaction.response.defer()
    if member is None:
        member = interaction.user

    embed = discord.Embed(title=f"Avatar của {member.display_name}", color=discord.Color.green())
    embed.set_image(url=member.display_avatar.url)
    await interaction.followup.send(embed=embed)

@client.tree.command(name="ship", description="Ship 2 người", guild=GUILD_ID)
async def ship(
    interaction: discord.Interaction,
    user1: discord.Member,
    user2: discord.Member
):
    await interaction.response.defer()

    percent = random.randint(0, 100)

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

    # dán avatar
    bg.paste(avatar1, (30, 25), avatar1)
    bg.paste(avatar2, (470, 25), avatar2)

    draw = ImageDraw.Draw(bg)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # trái tim
    heart = Image.open("heart.png.png").resize((80, 80)).convert("RGBA")
    bg.paste(heart, (310, 45), heart)

    # phần trăm
    draw.text((290, 140), f"{percent}%", fill="white", font=font)

    # lưu ảnh
    output = io.BytesIO()
    bg.save(output, format="PNG")
    output.seek(0)

    file = discord.File(output, filename="ship.png")

    embed = discord.Embed(
        title="💖 Ship Result",
        description=f"{user1.mention} ❤️ {user2.mention}\nĐộ hợp nhau: **{percent}%**",
        color=discord.Color(0xFCB2C5)
    )

    embed.set_image(url="attachment://ship.png")

    await interaction.followup.send(embed=embed, file=file)

@client.tree.command(name="gay", description="Kiểm tra độ gay", guild=GUILD_ID)
async def gay(interaction: discord.Interaction, member: discord.Member = None):
    await interaction.response.defer()

    user_id = interaction.user.id
    current_time = time.time()

    # Cooldown
    if user_id in cooldowns:
        remaining = cooldowns[user_id] - current_time

        if remaining > 0:
            await interaction.followup.send(
                f"⏳ Bạn cần chờ {int(remaining)} giây!"
            )
            return

    cooldowns[user_id] = current_time + 10

    # Nếu không chọn member
    if member is None:
        member = interaction.user

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

    await interaction.followup.send(embed=embed)
    
@client.tree.command(name="serverinfo", description="Xem thông tin server", guild=GUILD_ID)
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
    embed = discord.Embed(title="📊 Thông tin Server", color=discord.Color.blue())
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

async def main():
    async with client:
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                await client.load_extension(f"cogs.{file[:-3]}")

        await client.start(TOKEN)

# ===== TOKEN LOADING =====
def get_discord_token():
    """Load Discord token (encrypted or plain)"""
    # First, try to get encrypted token
    encrypted_token = os.getenv('DISCORD_TOKEN_ENCRYPTED')
    if encrypted_token and secret_manager:
        try:
            return secret_manager.decrypt(encrypted_token)
        except Exception as e:
            print(f"Failed to decrypt token: {e}")
            print("Falling back to plain DISCORD_TOKEN...")
    
    # Fall back to plain token from env
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("DISCORD_TOKEN or DISCORD_TOKEN_ENCRYPTED environment variable is not set")
    return token

TOKEN = get_discord_token()

keep_alive.keep_alive()
asyncio.run(main())