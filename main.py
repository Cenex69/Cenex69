import discord, time, json, os, random, urllib.request, re, datetime, asyncpraw, tracemalloc
from settings import *
from discord.ui import Button, Select, View
from discord import Member, Guild, Embed, Status, Colour, ButtonStyle
from discord.ext import commands
amtoffivestars = 0
fourstaramt = 0
count = 1
count2 = 1
fourstar = "None"
fivestarstr = None
fourstarstr = "Bennett x0 (maybe ur really unlucky)"
setting = settings()
btstyle = buttonstyle()
ai = ai()
errors = errors()
conf = confirmations()
bot = commands.Bot(setting.prefix(), help_command=None)
try:
    tracemalloc.start()
except:
    pass
finally:
    pass
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10000]:
    print(stat)

@bot.event
async def on_ready():
    print("LOGGED IN AS {0.user}".format(bot))
    await bot.change_presence(status=Status.idle, activity=discord.Game(setting.activity()))


@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, member:Member, reason:str=None):
    toMember = Embed(
       title="Kick",
       description=f"You were kicked by {setting.user(ctx.author)}.",
       colour=Colour.purple()
    )
    toMod = Embed(
        title="Kick",
        description=f"{member} was kicked from this server",
        colour=Colour.purple()
    )
    if reason is None:
        toMember.add_field(name="Reason:", value="No reason provided")
        toMod.add_field(name="Reason:", value="No reason provided")
    else:
        toMember.add_field(name="Reason:", value=reason)
        toMod.add_field(name="Reason:", value=reason)
    toMember.set_footer(text=f"Server: {ctx.guild.name}")
    await member.kick(reason=reason)
    await ctx.author.send(embed=toMod)
    await member.send(embed=toMember)


@commands.has_permissions(ban_members=True)
@bot.command()
async def ban(ctx, member:Member, reason:str=None):
    toMember = Embed(
       title="Ban",
       description=f"You were banned by {setting.user(ctx.author)}.",
       colour=Colour.purple()
    )
    toMod = Embed(
        title="Kick",
        description=f"{member} is banned from this server",
        colour=Colour.purple()
    )
    if reason is None:
        toMember.add_field(name="Reason:", value="No reason provided")
        toMod.add_field(name="Reason:", value="No reason provided")
    else:
        toMember.add_field(name="Reason:", value=reason)
        toMod.add_field(name="Reason:", value=reason)
    toMember.set_footer(text=f"Server: {ctx.guild.name}")
    await member.ban(reason=reason)
    await ctx.author.send(embed=toMod)
    await member.send(embed=toMember)


@commands.has_permissions(administrator=True)
@bot.command()
async def motd(ctx, image_url, title="Meme of the day", description=None):
    channel = bot.get_channel(setting.channel('motd'))
    if description is None:
        membed = Embed(
            title=title,
            colour=Colour.blue()
        )
    else:
        membed = Embed(
            title=title,
            description=description,
            colour=Colour.blue()
        )
    confembed = Embed(
        title="Do you want to post the meme:",
        colour=Colour.blue()
    )
    procembed = Embed(
        title=f"Posted the meme on channel {channel.name}",
        colour=Colour.blue()
    )
    eximbed = Embed(
        title=f"Cancelled meme posting session.",
        colour=Colour.blue()
    )
    btn = Button(label="Proceed", style=ButtonStyle.green)
    btn2 = Button(label="Exit", style=ButtonStyle.red)
    btnd = Button(label="Proceed", style=ButtonStyle.green, disabled=True)
    btn2d = Button(label="Exit", style=ButtonStyle.red, disabled=True)
    confembed.set_image(url=image_url)
    membed.set_image(url=image_url)
    membed.set_footer(text=random.choice(['not rlly that funny lol', 'LOL', 'why tf is this so funny bruh?', 'LMAO okay thats actually funny']))
    miew = View()
    miew.add_item(btn)
    miew.add_item(btn2)
    miew2 = View()
    miew2.add_item(btnd)
    miew2.add_item(btn2d)
    await ctx.channel.purge(limit=1)
    msg = await ctx.author.send(embed=confembed, view=miew)
    async def btn1_callback(interaction):
        await msg.edit(embed=procembed, view=miew2)
        message = await channel.send(embed=membed)
        await message.add_reaction(emoji="😂")
        await message.add_reaction(emoji="😑")

    async def btn2_callback(interaction):
        await msg.edit(embed=eximbed, view=miew2)

    btn.callback = btn1_callback
    btn2.callback = btn2_callback


@bot.command()
async def qotd(ctx, question):
    channel = bot.get_channel(setting.channel('qotd'))
    qembed = Embed(
        title="Question of the day",
        description=question,
        colour=Colour.blue()
    )
    confembed = Embed(
        title="Do you want to post the question:",
        description=question,
        colour=Colour.blue()
    )
    procembed = Embed(
        title=f"Posted the question on channel {channel}",
        colour=Colour.blue()
    )
    exembed = Embed(
        title="Cancelled question posting session.",
        colour=Colour.blue()
    )
    btn1 = Button(label="Proceed", style=btstyle.green())
    btn2 = Button(label="Exit", style=btstyle.red())
    btn3 = Button(label="I forgor 💀", style=btstyle.gray(), disabled=True)
    btn1d = Button(label="Proceed", style=btstyle.green(), disabled=True)
    btn2d = Button(label="Exit", style=btstyle.red(), disabled=True)
    qiew = View()
    qiew.add_item(btn1)
    qiew.add_item(btn2)
    qiew2 = View()
    qiew2.add_item(btn1d)
    qiew2.add_item(btn2d)
    qiew3 = View()
    qiew3.add_item(btn3)
    await ctx.channel.purge(limit=1)
    msg = await ctx.author.send(embed=confembed, view=qiew)
    async def btn1_callback(interaction):
        await msg.edit(embed=procembed, view=qiew2)
        message = await channel.send(embed=qembed, view=qiew3)

    async def btn2_callback(interaction):
        await msg.edit(embed=exembed, view=qiew2)

    btn1.callback = btn1_callback
    btn2.callback = btn2_callback


@commands.has_permissions(administrator=True)
@bot.command()
async def embed(ctx, title=None, description=None):
    if title is None:
        embed = Embed(
            title="Verification",
            description="There are two methods to get verified, one by reacting with :blue_square: and another is by typing >verify.",
            colour=Colour.blue()
        )
    elif description is None:
        embed = Embed(
            title=title,
            description="",
            colour=Colour.blue()
        )
    else:
        embed = Embed(
            title=title,
            description=description,
            colour=Colour.blue()
        )
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)


@commands.has_permissions(administrator=True)
@bot.command()
async def announce(ctx, desc1, desc2=None, desc3=None, desc4=None, desc5=None, desc6=None, desc7=None, desc8=None, desc9=None, desc10=None, desc11=None, desc12=None, desc13=None, desc14=None, desc15=None, desc16=None, desc17=None, desc18=None, desc19=None, desc20=None, desc21=None, desc22=None, desc23=None, desc24=None, desc25=None, desc26=None, desc27=None, desc28=None, desc29=None, desc30=None, desc31=None):
    description = ai.find_desc(desc1, desc2, desc3, desc4, desc5, desc6, desc7, desc8, desc9, desc10, desc11, desc12, desc13, desc14, desc15, desc16, desc17, desc18, desc19, desc20, desc21, desc22, desc23, desc24, desc25, desc26, desc27, desc28, desc29, desc30, desc31)
    if description == "too many words":
        await ctx.channel.purge(limit=1)
        await ctx.author.send(embed=errors.too_many_inputs(30, "announce"))
    btn1 = Button(label="Go ahead", style=btstyle.green())
    btn1d = Button(label="Go ahead", style=btstyle.green(), disabled=True)
    btn2 = Button(label="Go back", style=btstyle.red())
    btn2d = Button(label="Go back", style=btstyle.red(), disabled=True)
    byUSER = Button(label=f"Announcement by: {setting.user(ctx.author)}", disabled=True)
    view1 = View()
    view2 = View()
    view3 = View()
    view1.add_item(btn1)
    view1.add_item(btn2)
    view2.add_item(btn1d)
    view2.add_item(btn2d)
    view3.add_item(byUSER)
    await ctx.channel.purge(limit=1)
    msg = await ctx.author.send(embed=conf.conf(about="announce", desc=description), view=view1)
    title = ai.find_title(description=description, server=ctx.guild)
    announcementembed = Embed(
        title=title,
        description=description,
        colour=Colour.blue()
    )
    async def btncallback(interaction):
        await ctx.send("@everyone")
        await ctx.send(embed=announcementembed, view=view3)
        await msg.edit(embed=conf.procresult(channel=ctx.channel.name, server=ctx.guild.name), view=view2)

    async def btn2callback(interaction):
        await msg.edit(embed=conf.exisult(), view=view2)

    btn1.callback = btncallback
    btn2.callback = btn2callback


@bot.command()
async def meme(ctx):
    reddit = asyncpraw.Reddit(
        client_id=setting.credentials("id"),
        client_secret=setting.credentials("secret"),
        username=setting.credentials("username"),
        user_agent=setting.credentials("agent")
    )
    emload = Embed(
        title="Loading.",
        description=f"{str(bot.user).split('#')[0]} is currently searching for memes. Please be patient {setting.user(ctx.author)}."
    )
    msg = await ctx.send(embed=emload)
    subreddit = await reddit.subreddit("memes")
    allsubs = []
    top = subreddit.hot(limit=150)
    async for submission in top:
        allsubs.append(submission)
    random_sub = random.choice(allsubs)
    name = random_sub.title
    url = random_sub.url
    em = Embed(
        title=name,
        colour=Colour.blue()
    )
    em.set_image(url=url)
    em.set_footer(text=f"Submitted by u/{submission.author}")
    await msg.edit(embed=em)


@bot.command()
async def subreddit(ctx, subreddit):
    reddit = asyncpraw.Reddit(
        client_id=setting.credentials("id"),
        client_secret=setting.credentials("secret"),
        username=setting.credentials("username"),
        user_agent=setting.credentials("agent")
    )
    emload = Embed(
        title="Loading.",
        description=f"Dvalin is searching r/{subreddit}. Please be patient {setting.user(ctx.author)}."
    )
    msg = await ctx.send(embed=emload)
    subreddit = await reddit.subreddit(subreddit)
    allsubs = []
    top = subreddit.hot(limit=150)
    async for submission in top:
        allsubs.append(submission)
    random_sub = random.choice(allsubs)
    name = random_sub.title
    url = random_sub.url
    em = Embed(
    title=name,
    colour=Colour.blue()
    )
    em.set_image(url=url)
    em.set_footer(text=f"Subreddit: r/{subreddit}\nSubmitted by: u/{submission.author}")
    await msg.edit(embed=em)


@bot.command()
async def msg(ctx, user:Member, desc1, desc2=None, desc3=None, desc4=None, desc5=None, desc6=None, desc7=None, desc8=None, desc9=None, desc10=None, desc11=None, desc12=None, desc13=None, desc14=None, desc15=None, desc16=None, desc17=None, desc18=None, desc19=None, desc20=None, desc21=None, desc22=None, desc23=None, desc24=None, desc25=None, desc26=None, desc27=None, desc28=None, desc29=None, desc30=None, desc31=None):
    await user.send(ai.find_desc(desc1, desc2, desc3, desc4, desc5, desc6, desc7, desc8, desc9, desc10, desc11, desc12, desc13, desc14, desc15, desc16, desc17, desc18, desc19, desc20, desc21, desc22, desc23, desc24, desc25, desc26, desc27, desc28, desc29, desc30, desc31))
    await ctx.send("Msg sent")


@bot.command()
async def wish(ctx):
    five_star_gif = "https://images-ext-2.discordapp.net/external/ggZ8CV-6-HWXkbR24vvDNiAcWKMzRMcHzCouO9N6McI/https/i.imgur.com/BV5o91i.gif"
    four_star_gif = "https://images-ext-1.discordapp.net/external/EhNB8Z6ZqgDNsAuekI0YOQdUMOXcfhX3Vg-qmq7yKKc/https/i.imgur.com/nWHBRCJ.gif"
    standard_banner_png = "https://cdn.discordapp.com/attachments/885033730782158930/951726634334052422/standard_banner.png"
    raiden_banner_png = "https://cdn.discordapp.com/attachments/885033730782158930/951728076952326154/raiden_banner.png"
    kokomi_banner_png = "https://cdn.discordapp.com/attachments/885033730782158930/951728194883559454/kokomi.png"
    weapon_banner_png = "https://cdn.discordapp.com/attachments/885033730782158930/951728216459083786/Screenshot_2022-03-11_at_11.23.51_AM.png"
    cool_steel_png = "https://static.wikia.nocookie.net/gensin-impact/images/4/40/Weapon_Cool_Steel_3D.png/revision/latest/scale-to-width-down/579?cb=20201009191834"
    harbinger_png = "https://static.wikia.nocookie.net/gensin-impact/images/2/23/Weapon_Harbinger_of_Dawn_3D.png/revision/latest/scale-to-width-down/550?cb=20201010022249"
    debate_png = "https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Weapon_Debate_Club_3D.png/revision/latest/scale-to-width-down/565?cb=20201010140150"
    white_tassel_png = "https://static.wikia.nocookie.net/gensin-impact/images/f/f0/Weapon_White_Tassel_3D.png/revision/latest/scale-to-width-down/592?cb=20201118022622"
    black_tassel_png = "https://static.wikia.nocookie.net/gensin-impact/images/3/37/Weapon_Black_Tassel_3D.png/revision/latest/scale-to-width-down/601?cb=20201118022448"
    thrilling_tales_png = "https://static.wikia.nocookie.net/gensin-impact/images/3/30/Weapon_Thrilling_Tales_of_Dragon_Slayers_3D.png/revision/latest/scale-to-width-down/436?cb=20201010180555"
    xinyan_png = "https://www.gamespot.com/a/uploads/scale_landscape/1599/15997278/3897720-githumb.jpeg"
    bennett_png = "https://www.siliconera.com/wp-content/uploads/2020/12/genshin-impact-should-you-pull-on-albedo-banner-1.jpg"
    kujou_sara_png = "https://cdn.hobbyconsolas.com/sites/navi.axelspringer.es/public/styles/1200/public/media/image/2021/08/genshin-impact-2453817.jpg?itok=nyWNH4pN"
    beidou_png = "https://assets.gamepur.com/wp-content/uploads/2021/10/23180926/Beidou-e1644819533687.jpg"
    xingqiu_png = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKx2nEcFqjn9w0R-ExdhzM-guTw9hjItgGitmulolutYBAonbZ2AEppHleYwbH4aOL_70&usqp=CAU"
    kokomi_png = "https://assets2.rockpapershotgun.com/genshin-impact-sangonomiya-kokomi.jpg/BROK/resize/1920x1920%3E/format/jpg/quality/80/genshin-impact-sangonomiya-kokomi.jpg"
    raiden_png = "https://www.insidesport.in/wp-content/uploads/2022/01/dsdsfzsdgsg.jpg?w=1024"
    diluc_png = "https://www.alphr.com/wp-content/uploads/2021/04/Diluc-5.png"
    qiqi_png = "https://preview.redd.it/r2kf907juuv71.jpg?width=640&crop=smart&auto=webp&s=bcd9056a1e1d2d4393c0a9ed7a31027435d342a8"
    mona_png = "https://www.siliconera.com/wp-content/uploads/2020/10/Genshin-Impact-Banner.jpg"
    keqing_png = "https://pbs.twimg.com/media/EugPWhxUYAQGQ_w.jpg"
    jean_png = "https://i2.wp.com/www.alphr.com/wp-content/uploads/2021/05/How-to-Play-Jean-in-Genshin-Impact-1.png?resize=1200%2C1052&ssl=1"
    get_cool_steel = Embed(
        title="Wish",
        description="Cool Steel",
        colour=Colour.blue()
    )
    get_cool_steel.set_image(url=cool_steel_png)
    get_harbinger_of_dawn = Embed(
        title="Wish",
        description="Harbinger of Dawn",
        colour=Colour.blue()
    )
    get_harbinger_of_dawn.set_image(url=harbinger_png)
    get_white_tassel = Embed(
        title="Wish",
        description="White Tassel",
        colour=Colour.blue()
    )
    get_white_tassel.set_image(url=white_tassel_png)
    get_black_tassel = Embed(
        title="Wish",
        description="Black Tassel",
        colour=Colour.blue()
    )
    get_black_tassel.set_image(url=black_tassel_png)
    get_debate_club = Embed(
        title="Wish",
        description="Debate Club",
        colour=Colour.blue()
    )
    get_debate_club.set_image(url=debate_png)
    get_thrilling_tales = Embed(
        title="Wish",
        description="Thrilling Tales of Dragon Slayers",
        colour=Colour.blue()
    )
    get_thrilling_tales.set_image(url=thrilling_tales_png)
    get_xinyan = Embed(
        title="Wish",
        description="Xinyan",
        colour=Colour.purple()
    )
    get_xinyan.set_image(url=xinyan_png)
    get_bennett = Embed(
        title="Wish",
        description="Bennett",
        colour=Colour.purple()
    )
    get_bennett.set_image(url=bennett_png)
    get_beidou = Embed(
        title="Wish",
        description="Beidou",
        colour=Colour.purple()
    )
    get_beidou.set_image(url=beidou_png)
    get_kujou = Embed(
        title="Wish",
        description="Kujou Sara",
        colour=Colour.purple()
    )
    get_kujou.set_image(url=kujou_sara_png)
    get_xingqiu = Embed(
        title="Wish",
        description="Xingqiu",
        colour=Colour.purple()
    )
    get_xingqiu.set_image(url=xingqiu_png)
    get_kokomi = Embed(
        title="Wish",
        description=f"Sangnomiya Koko{random.choice(['nut', 'mi'])}",
        colour=Colour.gold()
    )
    get_kokomi.set_image(url=kokomi_png)
    get_raiden = Embed(
        title="Wish",
        description=f"Raiden Sho{random.choice(['', 't'])}gun",
        colour=Colour.gold()
    )
    get_raiden.set_image(url=raiden_png)
    get_qiqi = Embed(
        title="Wish",
        description=f"{random.choice(['ur more unlucky than bennett ngl', 'i think you lost ur 50/50', 'Cheechee sucks', 'pov: you are unlucky'])}",
        colour=Colour.red()
    )
    get_qiqi.set_image(url=qiqi_png)
    get_diluc = Embed(
        title="Wish",
        description=f"{random.choice(['Diluc', 'Dieluke', 'Deelook||[here](https://youtube.com/shorts/HE9tFixFjHg?feature=share)||'])}",
        colour=Colour.gold()
    )
    get_diluc.set_image(url=diluc_png)
    get_mona = Embed(
        title="Wish",
        description=f"Mona",
        colour=Colour.gold()
    )
    get_mona.set_image(url=mona_png)
    get_keqing = Embed(
        title="Wish",
        description=f"{random.choice(['cat', 'Keqing'])}",
        colour=Colour.gold()
    )
    get_keqing.set_image(url=keqing_png)
    get_jean = Embed(
        title="Wish",
        description=f"{random.choice(['Jean', 'Jeaneral', 'yeet'])}",
        colour=Colour.gold()
    )
    get_jean.set_image(url=jean_png)
    selection_embed = Embed(
        title="Wish",
        description="Which banner do you want to wish on?"
    )
    raiden_rerun = Embed(
        title="Wish",
        description="Raiden Shogun Rerun (Limited Banner 1)",
        colour=Colour.dark_purple()
    )
    kokomi_rerun = Embed(
        title="Wish",
        description="Sangnomiya Kokomi Rerun (Limited Banner 2)",
        colour=Colour.blue()
    )
    pull5Star = Embed(
        title="Wish",
        colour=Colour.gold()
    )
    pull4star = Embed(
        title="Wish",
        colour=Colour.purple()
    )
    kokomi_rerun.set_image(url=kokomi_banner_png)
    pull4star.set_image(url=four_star_gif)
    pull5Star.set_image(url=five_star_gif)
    raiden_rerun.set_image(url=raiden_banner_png)
    raiden = Button(label="Raiden Rerun", style=ButtonStyle.primary)
    button1 = Button(label="Wish 10x", style=ButtonStyle.green)
    kokomi = Button(label="Kokomi Rerun", style=ButtonStyle.primary)
    weapon = Button(label="Weapon Banner", style=ButtonStyle.primary)
    standard = Button(label="Standard Banner", style=ButtonStyle.primary)
    skipanimation = Button(label="Skip", style=ButtonStyle.primary)
    exit = Button(label="End interaction", style=ButtonStyle.gray)
    viewtype1 = View()
    viewtype2 = View()
    viewtype3 = View()
    viewtype4 = View()
    viewtype3.add_item(skipanimation)
    viewtype4.add_item(exit)
    viewtype2.add_item(button1)
    viewtype2.add_item(exit)
    viewtype1.add_item(raiden)
    viewtype1.add_item(kokomi)
    viewtype1.add_item(weapon)
    viewtype1.add_item(standard)
    viewtype1.add_item(exit)
    msg = await ctx.send(embed=selection_embed, view=viewtype1)
    async def event_wish_1(interaction):
        await msg.edit(embed=raiden_rerun, view=viewtype2)
        async def raiden_callback(interaction):
            is5Star = random.choice([True, False])
            multiple4Stars = random.choice([True, False])
            if is5Star is True:
                isstandard5 = random.choice([True, False])
                multiple5Stars = random.choice([True, False])
                if isstandard5 is True:
                    if multiple5Stars is True:
                        global amtoffivestars
                        global fivestarstr
                        amtoffivestars = random.randrange(1, 4)
                        fivestar = random.choice(["Diluc", "Qiqi", "Mona", "Keqing", "Jean"])
                        fivestarstr = f"{fivestar} x{amtoffivestars}"
                    else:
                        amtoffivestars = 1
                        fivestar = random.choice(["Diluc", "Qiqi", "Mona", "Keqing", "Jean"])
                        fivestarstr = f"{fivestar} x{amtoffivestars}"
                else:
                    if multiple5Stars is True:
                        amtoffivestars = random.randrange(1, 4)
                        fivestar = "Raiden Shogun"
                        fivestarstr = f"{fivestar} x{amtoffivestars}"
                    else:
                        amtoffivestars = 1
                        fivestar = "Raiden Shogun"
                        fivestarstr = f"{fivestar} x{amtoffivestars}"
            else:
                if multiple4Stars is True:
                    global fourstaramt
                    global fourstarstr
                    global fourstar
                    fourstaramt = random.randrange(1, 3)
                    fourstar = random.choice(['Xinyan', 'Bennett', 'Kujou Sara', 'Beidou', 'Xingqiu'])
                    fourstarstr = f"{fourstar} x{fourstaramt}"
                else:
                    fourstaramt = 1
                    fourstar = random.choice(['Xinyan', 'Bennett', 'Kujou Sara', 'Beidou', 'Xingqiu'])
                    fourstarstr = f"{fourstar} x{fourstaramt}"
            threestar = random.choice(['Cool Steel', 'Harbinger of Dawn', 'Debate Club', 'White Tassel', 'Black Tassel', 'Thrilling Tales of Dragon Slayers'])
            threestar2 = random.choice(
                ['Cool Steel', 'Harbinger of Dawn', 'Debate Club', 'White Tassel', 'Black Tassel',
                 'Thrilling Tales of Dragon Slayers'])
            if threestar == threestar2:
                threestar2 = random.choice(
                    ['Cool Steel', 'Harbinger of Dawn', 'Debate Club', 'White Tassel', 'Black Tassel',
                     'Thrilling Tales of Dragon Slayers'])
            if is5Star is True:
                threestaramt = 10 - (fourstaramt + amtoffivestars)
                amt1 = round(threestaramt / 2)
                amt2 = str(abs(10 - (threestaramt + amt1)))
            else:
                threestaramt = 10 - fourstaramt
                amt1 = round(threestaramt / 2)
                amt2 = str(abs(10 - (threestaramt + amt1)))
            if '-' in amt2:
                amt2 = abs(int(amt2))
            amt1 = int(amt1)
            amt2 = int(amt2)
            if is5Star is True:
                if (int(amt1)+int(amt2))+(fourstaramt+amtoffivestars) != 10:
                    amttochange = 10 - (int(amt1)+int(amt2)+int(fourstaramt)+int(amtoffivestars))
                    whichtochange = random.choice(['amt1', 'amt2'])
                    if whichtochange == "amt1":
                        amt1 += amttochange
                    else:
                        amt2 += amttochange
                else:
                    pass
            else:
                if (int(amt1)+int(amt2))+fourstaramt != 10:
                    amttochange = 10 - (int(amt1)+int(amt2)+int(fourstaramt))
                    whichtochange = random.choice(['amt1', 'amt2'])
                    if whichtochange == "amt1":
                        amt1 += amttochange
                    else:
                        amt2 += amttochange
                else:
                    pass
            threestarstr = f"{threestar} x{amt1}\n{threestar2} x{amt2}"
            syntax = {
                "first": "five star",
                "second": "four star",
                "third": "three star"
            }
            if is5Star is True:
                pull = Embed(
                    title="Wish",
                    description=f"Banner: Raiden Shogun 1st Rerun (1st Character Event Wish Banner)",
                    colour=Colour.blue()
                )
                pull.add_field(name="Five stars:", value=fivestarstr, inline=False)
                pull.add_field(name="Four stars:", value=fourstarstr, inline=False)
                pull.add_field(name="Three stars:", value=threestarstr, inline=False)
                if fivestar == "Diluc":
                    pull.set_footer(text=f"{random.choice(['Deelook||[here](https://youtube.com/shorts/HE9tFixFjHg?feature=share)||', 'you got dieluke nice'])}")
                await msg.edit(embed=pull5Star, view=None)
                time.sleep(6)
                if fivestar == "Diluc":
                    await msg.edit(embed=get_diluc, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan, view=viewtype4)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Mona":
                    await msg.edit(embed=get_mona, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Keqing":
                    await msg.edit(embed=get_keqing, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Jean":
                    await msg.edit(embed=get_jean, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Qiqi":
                    await msg.edit(embed=get_qiqi, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Jean":
                    await msg.edit(embed=get_jean, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Raiden Shogun":
                    await msg.edit(embed=get_raiden, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
            else:
                pull = Embed(
                    title="Wish",
                    description=f"Banner: Raiden Shogun 1st Rerun (1st Character Event Wish Banner)",
                    colour=Colour.blue()
                )
                pull.add_field(name="Four stars:", value=fourstarstr, inline=False)
                pull.add_field(name="Three stars:", value=threestarstr, inline=False)
                await msg.edit(embed=pull4star, view=None)
                time.sleep(6)
                if fourstar == "Xinyan":
                    await msg.edit(embed=get_xinyan)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(2)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
                elif fourstar == "Bennett":
                    await msg.edit(embed=get_bennett)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
                elif fourstar == "Kujou Sara":
                    await msg.edit(embed=get_kujou)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
                elif fourstar == "Beidou":
                    await msg.edit(embed=get_beidou)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
                elif fourstar == "Xingqiu":
                    await msg.edit(embed=get_xingqiu)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
        time.sleep(1)
        await msg.edit(view=viewtype4)
        button1.callback = raiden_callback

    async def limitedbanner2(interaction):
        await msg.edit(embed=kokomi_rerun, view=viewtype2)
        async def kokomi_callback(interaction):
            is5Star = random.choice([True, False])
            multiple4Stars = random.choice([True, False])
            if is5Star is True:
                isstandard5 = random.choice([True, False])
                multiple5Stars = random.choice([True, False])
                if isstandard5 is True:
                    if multiple5Stars is True:
                        global amtoffivestars
                        global fivestarstr
                        amtoffivestars = random.randrange(1, 4)
                        fivestar = random.choice(["Diluc", "Qiqi", "Mona", "Keqing", "Jean"])
                        fivestarstr = f"{fivestar} x{amtoffivestars}"
                    else:
                        amtoffivestars = 1
                        fivestar = random.choice(["Diluc", "Qiqi", "Mona", "Keqing", "Jean"])
                        fivestarstr = f"{fivestar} x{amtoffivestars}"
                else:
                    if multiple5Stars is True:
                        amtoffivestars = random.randrange(1, 4)
                        fivestar = "Sangonomiya Kokomi"
                        fivestarstr = f"{fivestar} x{amtoffivestars}"
                    else:
                        amtoffivestars = 1
                        fivestar = "Sangonomiya Kokomi"
                        fivestarstr = f"{fivestar} x{amtoffivestars}"
            else:
                if multiple4Stars is True:
                    global fourstaramt
                    global fourstarstr
                    fourstaramt = random.randrange(1, 3)
                    fourstar = random.choice(['Xinyan', 'Bennett', 'Kujou Sara', 'Beidou', 'Xingqiu'])
                    fourstarstr = f"{fourstar} x{fourstaramt}"
                else:
                    fourstaramt = 1
                    fourstar = random.choice(['Xinyan', 'Bennett', 'Kujou Sara', 'Beidou', 'Xingqiu'])
                    fourstarstr = f"{fourstar} x{fourstaramt}"
            threestar = random.choice(['Cool Steel', 'Harbinger of Dawn', 'Debate Club', 'White Tassel', 'Black Tassel',
                                       'Thrilling Tales of Dragon Slayers'])
            threestar2 = random.choice(['Cool Steel', 'Harbinger of Dawn', 'Debate Club', 'White Tassel', 'Black Tassel',
                                       'Thrilling Tales of Dragon Slayers'])
            if threestar == threestar2:
                threestar2 = random.choice(['Cool Steel', 'Harbinger of Dawn', 'Debate Club', 'White Tassel', 'Black Tassel',
                                       'Thrilling Tales of Dragon Slayers'])
            if is5Star is True:
                threestaramt = 10 - (fourstaramt+amtoffivestars)
                amt1 = round(threestaramt/2)
                amt2 = 10 - (threestaramt+amt1)
            else:
                threestaramt = 10 - fourstaramt
                amt1 = round(threestaramt/2)
                amt2 = abs(10 - (threestaramt+amt1))
            threestarstr = f"{threestar} x{amt1}\n{threestar2} x{amt2}"
            if is5Star is True:
                pull = Embed(
                    title="Wish",
                    description=f"Banner: Sangonomiya Kokomi 1st Rerun (2nd Character Event Wish Banner)",
                    colour=Colour.blue()
                )
                pull.add_field(name="Five stars:", value=fivestarstr, inline=False)
                pull.add_field(name="Four stars:", value=fourstarstr, inline=False)
                pull.add_field(name="Three stars:", value=threestarstr, inline=False)
                if fivestar == "Diluc"
                    pull.set_footer(text=f"{random.choice(['Deelook||[here](https://youtube.com/shorts/HE9tFixFjHg?feature=share)||', 'you got dieluke nice'])}")
                await msg.edit(embed=pull5Star, view=None)
                time.sleep(6)
                time.sleep(6)
                if fivestar == "Diluc":
                    await msg.edit(embed=get_diluc, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan, view=viewtype4)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Mona":
                    await msg.edit(embed=get_mona, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Keqing":
                    await msg.edit(embed=get_keqing, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Jean":
                    await msg.edit(embed=get_jean, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Qiqi":
                    await msg.edit(embed=get_qiqi, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Jean":
                    await msg.edit(embed=get_jean, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                if fivestar == "Sangnomiya Kokomi":
                    await msg.edit(embed=get_kokomi, view=viewtype4)
                    time.sleep(1)
                    if fourstar == "Xinyan":
                        await msg.edit(embed=get_xinyan)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Bennett":
                        await msg.edit(embed=get_bennett)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Kujou Sara":
                        await msg.edit(embed=get_kujou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Beidou":
                        await msg.edit(embed=get_beidou)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
                    elif fourstar == "Xingqiu":
                        await msg.edit(embed=get_xingqiu)
                        time.sleep(1)
                        if threestar == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            if threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif threestar == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif "thrilling" in threestar2.lower():
                                await msg.edit(embed=get_thrilling_tales)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        elif "thrilling" in threestar.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            if threestar2 == "Harbinger of Dawn":
                                await msg.edit(embed=get_harbinger_of_dawn)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "White Tassel":
                                await msg.edit(embed=get_white_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Black Tassel":
                                await msg.edit(embed=get_black_tassel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            elif threestar2 == "Cool Steel":
                                await msg.edit(embed=get_cool_steel)
                                time.sleep(1)
                                await msg.edit(embed=pull)
                            else:
                                pass
                        else:
                            pass
            else:
                pull = Embed(
                    title="Wish",
                    description=f"Banner: Sangonomiya Kokomi 2nd Rerun (2nd Character Event Wish Banner)",
                    colour=Colour.blue()
                )
                pull.add_field(name="Four stars:", value=fourstarstr, inline=False)
                pull.add_field(name="Three stars:", value=threestarstr, inline=False)
                await msg.edit(embed=pull4star, view=None)
                time.sleep(6)
                if fourstar == "Xinyan":
                    await msg.edit(embed=get_xinyan)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(2)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
                elif fourstar == "Bennett":
                    await msg.edit(embed=get_bennett)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(2)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
                elif fourstar == "Kujou Sara":
                    await msg.edit(embed=get_kujou)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
                elif fourstar == "Beidou":
                    await msg.edit(embed=get_beidou)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
                elif fourstar == "Xingqiu":
                    await msg.edit(embed=get_xingqiu)
                    time.sleep(1)
                    if threestar == "Cool Steel":
                        await msg.edit(embed=get_cool_steel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Harbinger of Dawn":
                        await msg.edit(embed=get_harbinger_of_dawn)
                        time.sleep(1)
                        if threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "White Tassel":
                        await msg.edit(embed=get_white_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif threestar == "Black Tassel":
                        await msg.edit(embed=get_black_tassel)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif "thrilling" in threestar2.lower():
                            await msg.edit(embed=get_thrilling_tales)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    elif "thrilling" in threestar.lower():
                        await msg.edit(embed=get_thrilling_tales)
                        time.sleep(1)
                        if threestar2 == "Harbinger of Dawn":
                            await msg.edit(embed=get_harbinger_of_dawn)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "White Tassel":
                            await msg.edit(embed=get_white_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Black Tassel":
                            await msg.edit(embed=get_black_tassel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        elif threestar2 == "Cool Steel":
                            await msg.edit(embed=get_cool_steel)
                            time.sleep(1)
                            await msg.edit(embed=pull)
                        else:
                            pass
                    else:
                        pass
            await msg.edit(view=viewtype4)
        button1.callback = kokomi_callback

    async def exit_callback(interaction):
        await msg.edit(view=None)

    exit.callback = exit_callback
    raiden.callback = event_wish_1
    kokomi.callback = limitedbanner2


@bot.command()
async def help(ctx):
    nextemoji = "➡"
    backemoji = "⬅"
    nextbutton = Button(style=ButtonStyle.primary, emoji=nextemoji)
    nextdisabled = Button(style=ButtonStyle.primary, emoji=nextemoji, disabled=True)
    backbutton = Button(style=ButtonStyle.primary, emoji=backemoji)
    backdisabled = Button(style=ButtonStyle.primary, emoji=backemoji, disabled=True)
    endbutton = Button(style=ButtonStyle.secondary, label="End Interaction")
    mainpage = Embed(
        title="Help",
        description=f"Click on {backemoji} or {nextemoji} to change pages. To end this interaction click on End Interaction",
        colour=Colour.purple()
    )
    firstpage = Embed(
        title="Help",
        description="This page is for the mod commands.",
        colour=Colour.purple()
    )
    secondpage = Embed(
        title="Help",
        description="This page is for the \'fun\' commands.",
        colour=Colour.purple()
    )
    firstpage.add_field(name="Mod commands:", value=".kick {user:Member} {reason=None}\n.ban {user:Member} {reason=None}\n.announce {description=None}\n.motd {imageurl} {title=None} {description=None}\n.qotd {question}", inline=False)
    secondpage.add_field(name="Fun commands:", value=".wish\n.meme\n.subreddit {subreddit}", inline=False)
    view1d = View()
    view1d2 = View()
    view2d = View()
    viewalldisabled = View()
    view1d.add_item(backdisabled)
    view1d.add_item(nextbutton)
    view1d.add_item(endbutton)
    view1d2.add_item(backbutton)
    view1d2.add_item(nextdisabled)
    view1d2.add_item(endbutton)
    view2d.add_item(backdisabled)
    view2d.add_item(nextdisabled)
    view2d.add_item(endbutton)
    viewalldisabled.add_item(backdisabled)
    viewalldisabled.add_item(nextdisabled)
    msg = await ctx.send(embed=mainpage, view=view1d)

    async def next_page(interaction):
        global count
        count = count+1
        if count == 2:
            await msg.edit(embed=firstpage, view=view1d)
        elif count == 3:
            await msg.edit(embed=secondpage, view=view1d2)

    async def back_page(interaction):
        c = count-1
        if c == 2:
            await msg.edit(embed=firstpage, view=view1d)

    async def end_interaction(interaction):
        await msg.edit(view=viewalldisabled)

    nextbutton.callback = next_page
    backbutton.callback = back_page
    endbutton.callback = end_interaction



async def open_account(user):
    users = await get_wallet_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["primogems"] = 0
    with open('wallets.json', 'w') as f:
        json.dump(users, f)
    return True

async def get_wallet_data():
    with open('wallets.json', 'r') as f:
        users = json.load(f)
    return users


bot.run(setting.token())
tracemalloc.stop()
