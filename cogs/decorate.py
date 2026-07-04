import discord
from discord.ext import commands

class DecorateCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="Menu")
    async def menu(self, ctx:commands.Context):
        embed=discord.Embed(
            title="Menu Trà Quán",
            description="""**## 🌸✨ MENU TRÀ "NỮ HOÀNG" ✨🌸

"Một chút ngọt ngào cho ngày bình yên..."

### ╭───────────── ☀️ ─────────────╮

🍊 TRÀ MÙA HÈ

🍹 Trà Cam Mật Ong Summer – 25k Cowoncy
🍋 Trà Chanh Leo Nhiệt Đới – 26k Cowoncy
🍉 Trà Dưa Hấu Mát Lạnh – 24k Cowoncy
🥭 Trà Xoài Hoàng Hôn – 25k Cowoncy
🍓 Trà Dâu Tuyết Mùa Hạ – 24k Cowoncy

🧋 TRÀ SỮA ĐẶC BIỆT

🌸 Sakura Milk Tea – 25k Cowoncy
🍪 Cookies & Cream Milk Tea – 35k Cowoncy
🍵 Matcha Cloud Tea – 30k Cowoncy
🍫 Choco Dream Milk Tea – 30k Cowoncy

❄️ ĐÁ XAY GIẢI NHIỆT

🍵 Matcha Ice Blend – 27k Cowoncy
🍓 Strawberry Snow Blend – 40k Cowoncy
🥭 Mango Paradise Blend – 35k Cowoncy

🍮 TOPPING

🍮 Pudding Trứng +8.000
🍓 Thạch Dâu +8.000

### ╰───────────── ☀️ ─────────────╯**""",
            color=discord.Color(0xFCB2C5)
        )
        embed.set_footer(text="""🌙 GÓC NHẮN NHỦ:
    "Dù hôm nay có mệt mỏi, hãy để một ly trà làm dịu tâm hồn bạn nhé..." """)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494344734121005076/5c535af93368c98666e3c8ee70cd8ee5.gif")
        await ctx.send(embed=embed)

    @commands.command(name="roleinfo")
    async def roleinfo(self, ctx:commands.Context):
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
        await ctx.send(embed=embed)

    @commands.command(name="infolevel")
    async def infolevel(self, ctx:commands.Context):
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
        await ctx.send(embed=embed)
        
    @commands.command(name="ticketrule")
    async def ticketrule(self, ctx:commands.Context):
        embed = discord.Embed(
            title="🎫 HỆ THỐNG TICKET",
            description="""## :handshake: Partner

> Dùng để liên hệ hợp tác giữa các server hoặc trao đổi về Partnership.

**Khi chọn mục này:**

* Vui lòng giới thiệu ngắn về server của bạn.
* Gửi link mời hoặc thông tin cần thiết.
* Trình bày rõ mục đích hợp tác.

:loudspeaker: **Role được thông báo:** <@&1459553975396466880>

## :rotating_light: Report

> Dùng để báo cáo thành viên vi phạm hoặc hành vi không phù hợp.

**Khi chọn mục này:**

* Nêu rõ tên hoặc ID của người bị báo cáo.
* Mô tả chi tiết sự việc.
* Đính kèm bằng chứng (ảnh, video hoặc link tin nhắn) nếu có.

:loudspeaker: **Role được thông báo:** <@&1459555244186013749>


## :tools: Hỗ Trợ

> Dùng để nhận hỗ trợ về server, bot hoặc các vấn đề khác.

**Khi chọn mục này:**

* Mô tả vấn đề bạn cần hỗ trợ
* Cung cấp ảnh chụp màn hình nếu cần.
* Chờ Lễ phản hồi và không spam ping.

:loudspeaker: **Role được thông báo:** <@&1459753366019248209>


# Quy định chung

* Chỉ tạo **01 ticket** cho mỗi vấn đề.
* Chọn **đúng danh mục** trước khi tạo.
* Không spam hoặc tạo ticket với nội dung vô nghĩa.
* Giữ thái độ lịch sự và tôn trọng trong suốt quá trình trao đổi.
* Sau khi vấn đề được giải quyết, ticket sẽ được đóng để giữ hệ thống gọn gàng.
# Hình Phạt
* Tạo Ticket nhảm Mute 3h""",
            color=discord.Color(0xFCB2C5)
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1498547991970320464/341d0e8691a316891bf88a69f2abf90f.jpg?ex=69f18f12&is=69f03d92&hm=8aeeb40e4157c584a3248f5eef3e2b17cde4dfe8eb9e12cfac076d2aa3630cbc&")
        await ctx.send(embed=embed)

    @commands.command(name="partnerrules")
    async def partnerrules(self, ctx:commands.Context):
        embed = discord.Embed(title="Điều kiện Partner", description="""- Server có hoạt động thường xuyên (không dead)
- Server phải 100 Member trở lên
- Phải sử dụng Link Vĩnh Viễn
- Server không có NSFW, Scam,... Những thứ vi phạm tiêu chuẩn cộng đồng
- Trường hợp người đại diện out Server hoặc xóa bài thì Server tụi mình sẽ xóa theo

**__Lưu Ý:__** Server trở về chỉ ping <@&1503409786085965974> để tránh gây phiền và ảnh hưởng Member""", color=discord.Color(0xFCB2C5))
        embed.set_footer(text="Sửa đổi lần cuối 19/06/2026")
        await ctx.delete()
        await ctx.send(embed=embed)

    @commands.command(name="rules")
    async def rules(self, ctx:commands.Context):
        embed = discord.Embed(
            title="ʟᴜậᴛˋˋᴛʀà",
            description='''1. Tôn trọng tất cả thành viên, không xúc phạm, quấy rối hoặc gây mâu thuẫn.

2. Không spam tin nhắn, emoji, sticker, hình ảnh, GIF...

3. Không quảng cáo Server, website, sản phẩm hoặc mạng xã hội nếu chưa được <@&1459554666458386718> cho phép.

4. Không gửi nội dung phản cảm, NSFW, bạo lực hoặc vi phạm Điều khoản dịch vụ của Discord.

5. Không mạo danh người khác, Mod/Admin/Owner hoặc sử dụng tên/avatar nhằm lừa đảo.

6. Không phát tán link độc hại, lừa đảo, virus hoặc các nội dung gây nguy hiểm.

7. Sử dụng đúng kênh chat và đúng mục đích của từng kênh.

8. Khi cần hỗ trợ, hãy tạo Ticket và chọn đúng danh mục. Không spam hoặc tạo nhiều Ticket cùng lúc.

9. Tuân theo hướng dẫn của Mod/Admin/Owner. Nếu không đồng ý với quyết định, hãy bình tĩnh trao đổi qua Ticket.

10. Ban Quản Trị có quyền chỉnh sửa luật và đưa ra quyết định cuối cùng nhằm đảm bảo môi trường thân thiện, công bằng và an toàn cho mọi thành viên.''',
            color=discord.Color(0xFCB2C5)
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494182901976141956/dcd78396326fab10cd9c7b5a3f1e75cf.jpg?ex=69e1adc4&is=69e05c44&hm=fe953a09415d90b08d07ffa527bec2db675721463ec1f4838a38b7cf6a946396&")
        embed2 = discord.Embed(
            description='''# Hình Phạt
Vi phạm lần 1: Warn
Vi phạm lần 2: Mute 1 Ngày
Vi phạm lần 3: Mute 3 Ngày
Vi phạm lần 4: Mute 7 Ngày
Vi phạm lần 5: Mute 14 Ngày
Vi phạm lần 6: Ban Vĩnh Viễn

# Trường Hợp Xử Lí Đặc Biệt

Đăng vid, hình ảnh mang tính chất Chính Trị, Gây Hại, Low Nsfw, Low Gore: Mute 14 Ngày
Đăng vid, hình ảnh mang tính chất Nsfw, Gore: ban vĩnh viễn
Leak thông tin cá nhân: Ban Vĩnh Viễn
Sử dụng acc Clone để tránh Mute, Ban,...: Ban Vĩnh Viễn ( cả chính và Clone)
Acc bị Hack, Scam: Ban Vĩnh Tiễn
**__Lưu Ý__**: 1. <@1307657523926663189> Là **Luật**
2. Những trường hợp nặng dù không được nêu rõ trong luật vẫn xử lí nghêm khắc
3. Luật có thể thay đổi bất cứ lúc nào
4. Mod x2 warn
4. Nếu gặp các Manager Server vi phạm luật thì cứ báo cáo ở https://discord.com/channels/1459553409521684510/1463538921832059001 để được xử lí nhé!''',
            color=discord.Color(0xFCB2C5)
        )
        embed2.set_footer(text="Chúc Bạn Có Thời Gian Vui Vẻ Nha! <3")
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1463886315186684117/1494186163488165919/eb667e1bf9915395a7847f5f5f1230ad.jpg?ex=69e1b0ce&is=69e05f4e&hm=7b1ca98122d541da3d33c02d8835de11d80844c0a2beda5c768c9dd7818f7048&")
        await ctx.send(content="Các bạn đọc luật để tránh bị Warn, Mute hoặc Ban nha<:Zero_Love:1490270183707644025>", embeds=[embed, embed2])

async def setup(bot: commands.Bot):
    await bot.add_cog(DecorateCog(bot))