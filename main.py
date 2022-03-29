import discord, time, json, os, random, urllib.request, re, datetime, asyncpraw, tracemalloc
from settings import *
from discord.ui import Button, Select, View
from discord import Member, Guild, Embed, Status, Colour, ButtonStyle
from discord.ext import commands
setting = settings()
btstyle = buttonstyle()
ai = ai()
errors = errors()
conf = confirmations()
bot = commands.Bot(setting.prefix(), help_command=None)
tracemalloc.start()
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10000]:
    print(stat)

@bot.event
async def on_ready():
    print("LOGGED IN AS {0.user}".format(bot))
    await bot.change_presence(status=Status.idle, activity=discord.Game(setting.activity()))



@bot.command()
async def count(ctx, till):
    for x in range(int(till)+1):
        if x == 0:
            pass
        else:
            await ctx.send(x)


@bot.command()
async def poll(ctx, type="END_RESULT"):
    if ctx.author.display_name == "canadian aether":
        if type == "END_RESULT":
            embed = Embed(
                title="How much did you get in exams?",
                description="Use kaz react HISTORY and submit your answers.",
                colour=Colour.blue()
            )
            await ctx.send("@everyone",embed=embed)
    else:
        await ctx.send("this command is not for you")


@bot.command()
async def react(ctx, poll=None):
    a1 = Button(label="10", style=ButtonStyle.red)
    a2 = Button(label="20", style=ButtonStyle.red)
    a3 = Button(label="30", style=ButtonStyle.red)
    a4 = Button(label="40", style=ButtonStyle.primary)
    a5 = Button(label="50", style=ButtonStyle.primary)
    a6 = Button(label="60", style=ButtonStyle.primary)
    a7 = Button(label="70", style=ButtonStyle.primary)
    a8 = Button(label="80", style=ButtonStyle.green)
    a9 = Button(label="90", style=ButtonStyle.green)
    a10 = Button(label="100", style=ButtonStyle.green)
    view1 = View()
    view1.add_item(a1)
    view1.add_item(a2)
    view1.add_item(a3)
    view1.add_item(a4)
    view1.add_item(a5)
    view1.add_item(a6)
    view1.add_item(a7)
    view1.add_item(a8)
    view1.add_item(a9)
    view1.add_item(a10)
    marksembed = Embed(
        description="How much marks did you get?",
        colour=Colour.blue()
    )
    marksembed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar.url)
    ty = Embed(
        description="Thanks for answering!",
        colour=Colour.blue()
    )
    ty.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar.url)
    eror = Embed(
        description="You have already answered to this poll.",
        colour=Colour.blue()
    )
    eror.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar.url)
    marksembed.set_footer(text="the information will be deleted after the poll ends")
    await open_poll_account(ctx.author)
    users = await get_poll_data()
    if poll is None:
        await ctx.send("hey enter the arguments first don\'t be an idiot ||error: var code was not answered||")
    elif "his" in str(poll).lower():
        if users[str(ctx.author.id)]["has_answered"] == "False":
            msg = await ctx.send(embed=marksembed, view=view1)
            async def callback1(interaction):
                users[str(ctx.author.id)]["answer"] = 10
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback2(interaction):
                users[str(ctx.author.id)]["answer"] = 20
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback3(interaction):
                users[str(ctx.author.id)]["answer"] = 30
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback4(interaction):
                users[str(ctx.author.id)]["answer"] = 40
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback5(interaction):
                users[str(ctx.author.id)]["answer"] = 50
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback6(interaction):
                users[str(ctx.author.id)]["answer"] = 60
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback7(interaction):
                users[str(ctx.author.id)]["answer"] = 70
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback8(interaction):
                users[str(ctx.author.id)]["answer"] = 80
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback9(interaction):
                users[str(ctx.author.id)]["answer"] = 90
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            async def callback10(interaction):
                users[str(ctx.author.id)]["answer"] = 100
                users[str(ctx.author.id)]["has_answered"] = "True"
                with open('polls_active.json', 'w') as f:
                    json.dump(users, f)
                await msg.edit(embed=ty, view=None)
            a1.callback = callback1
            a2.callback = callback2
            a3.callback = callback3
            a4.callback = callback4
            a5.callback = callback5
            a6.callback = callback6
            a7.callback = callback7
            a8.callback = callback8
            a9.callback = callback9
            a10.callback = callback10
        elif users[str(ctx.author.id)]["has_answered"] == "True":
            await ctx.send(embed=eror, view=None)
    else:
        await ctx.send(f"Incorrect code given: {poll}\n**Active codes:**\nHISTORY\n**Inactive codes:**\nMARKS\nPHYSICS\nCHEMISTRY\nMATHS\nLANGUAGE\nBIOLOGY\nCOMPUTERS\nHINDI")


async def open_poll_account(user):
    users = await get_poll_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["answer"] = 0
        users[str(user.id)]["has_answered"] = "False"
    with open('polls_active.json', 'w') as f:
        json.dump(users, f)


async def get_poll_data():
    with open('polls_active.json', 'r') as f:
        data = json.load(f)
    return data



@bot.command()
async def clear(ctx, amount:int):
    await ctx.channel.purge(limit=int(amount))
    await ctx.send(f"Cleared {amount} messages")
    await ctx.channel.purge(limit=1)


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
        message = await ctx.send(embed=qembed, view=qiew3)

    async def btn2_callback(interaction):
        await msg.edit(embed=exembed, view=qiew2)

    btn1.callback = btn1_callback
    btn2.callback = btn2_callback


@bot.command()
async def rules(ctx):
    embed = Embed(
        description=f"not following the rules will result [in]({random.choice(['https://youtu.be/dQw4w9WgXcQ', 'https://youtu.be/XUI7jECVuI4', 'https://youtu.be/ZSzINfPlVLY'])})",
        colour=Colour.blue()
    )
    embed.add_field(name="Rules", value="**1.** Don't be a prick.\n**2**. Use channels for the proper purpose and not like a prick\n**3**. Don't swear unneccesarily like a prick, unless it's against Aurko.\n**4.** Don't do drugs like a prick\n**5.** No discriminatory slurs\n**6.** DON'T BE A KLEPTOMANIAC.\n**7.** REMEMBER RULE 11.\n**8.** Don't be a prick.\n**9.** Don't post nsfw stuff like a prick and a pervert.\n**10.** Do NOT config server settings like a prick\n**11.** Don't be a prick ")
    embed.set_footer(text="also don't be a prick.")
    await ctx.send(embed=embed)


@bot.command()
async def question(ctx, desc1, desc2=None, desc3=None, desc4=None, desc5=None, desc6=None, desc7=None, desc8=None, desc9=None, desc10=None, desc11=None, desc12=None, desc13=None, desc14=None, desc15=None, desc16=None, desc17=None, desc18=None, desc19=None, desc20=None, desc21=None, desc22=None, desc23=None, desc24=None, desc25=None, desc26=None, desc27=None, desc28=None, desc29=None, desc30=None, desc31=None):
    description = ai.find_desc(desc1, desc2, desc3, desc4, desc5, desc6, desc7, desc8, desc9, desc10, desc11, desc12,
                              desc13, desc14, desc15, desc16, desc17, desc18, desc19, desc20, desc21, desc22, desc23,
                              desc24, desc25, desc26, desc27, desc28, desc29, desc30, desc31)
    await ctx.channel.purge(limit=1)
    announcementembed = Embed(
        title="Question",
        description=description,
        colour=Colour.blue()
    )
    await ctx.send(embed=announcementembed)



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
    thirdpage = Embed(
        title="Help",
        description="This page is for the important commands."
    )
    firstpage.add_field(name="Mod commands:", value="kaz kick {user:Member} {reason=None}\nkaz ban {user:Member} {reason=None}\nkaz announce {description=None}\nkaz motd {imageurl} {title=None} {description=None}\nkaz qotd {question}", inline=False)
    secondpage.add_field(name="Fun commands:", value="kaz meme\nkaz subreddit {subreddit}\nkaz question {question}", inline=False)
    thirdpage.add_field(name="Important Commands:", value="kaz rules\nkaz ask (expires on the 3rd of April)")
    view1d = View()
    view1d2 = View()
    view2d = View()
    view0d = View()
    view0d.add_item(backbutton)
    view0d.add_item(nextbutton)
    view0d.add_item(endbutton)
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
            await msg.edit(embed=secondpage, view=view0d)
        elif count == 4:
            await msg.edit(embed=thirdpage, view=view1d2)

    async def back_page(interaction):
        c = count-1
        if c == 2:
            await msg.edit(embed=firstpage, view=view1d)
        elif c == 3:
            await msg.edit(embed=secondpage, view=view0d)

    async def end_interaction(interaction):
        await msg.edit(view=viewalldisabled)

    nextbutton.callback = next_page
    backbutton.callback = back_page
    endbutton.callback = end_interaction



bot.run(setting.token())
tracemalloc.stop()
