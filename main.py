import discord, time, json, os, random, urllib.request, re, datetime, asyncpraw
from settings import *
from discord.ui import Button, Select, View
from discord import Member, Guild, Embed, Status, Colour, ButtonStyle
from discord.ext import commands
setting = settings()
ai = ai()
btstyle = buttonstyle()
errors = errors()
conf = confirmations()
bot = commands.Bot(setting.prefix())


@bot.event
async def on_ready():
    print("LOGGED IN AS {0.user}".format(bot))
    await bot.change_presence(status=Status.idle, activity=discord.Game(setting.activity()))


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
    byUSER = Button(label=f"Announced by: {setting.user(ctx.author)}", disabled=True)
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
async def chat(ctx, type=None):
    reddit = asyncpraw.Reddit(
        client_id=setting.credentials("id"),
        client_secret=setting.credentials("secret"),
        username=setting.credentials("username"),
        user_agent=setting.credentials("agent")
    )
    if str(type) == "None":
        hellorandomtext1 = random.choice(['Hallo, ', 'Hi, ', 'Hello, ', 'Hamlo, ', 'Hai, ', 'no greeting for you, '])
        title = hellorandomtext1 + setting.user(ctx.author)
        description = f"{hellorandomtext1.split(',')[0]} {setting.user(ctx.author)}, I am your personal chatbot. Feel free to chat whatever you want with me."
        button1 = Button(label="Hi", style=btstyle.blue())
        button2 = Button(label="Hru?", style=btstyle.blue())
        button3 = Button(label="What do you wanna chat about?", style=btstyle.blue())
        button4 = Button(label="End interaction", style=btstyle.gray())
        button5 = Button(label="Good", style=btstyle.green())
        button6 = Button(label="Average/Okay", style=btstyle.blue())
        button7 = Button(label="Bad", style=btstyle.red())
        button8 = Button(label=f"Check some posts at r/{randsub}", style=btstyle.blue())
        button9 = Button(label="Go to r/cute", style=btstyle.green())
        button10 = Button(label="Next post", style=btstyle.green())
        button11 = Button(label="Go back", style=btstyle.blue())
        button12 = Button(label="Next meme", style=btstyle.blue())
        halloview = View()
        hallo2view = View()
        hruview = View()
        hru2view = View()
        hru3view = View()
        cuteview = View()
        memeview = View()
        wdycaview = View()
        memeview.add_item(button12)
        memeview.add_item(button11)
        memeview.add_item(button4)
        cuteview.add_item(button10)
        cuteview.add_item(button11)
        cuteview.add_item(button4)
        hru3view.add_item(button8)
        hru3view.add_item(button9)
        hru3view.add_item(button4)
        hru2view.add_item(button3)
        hru2view.add_item(button4)
        hruview.add_item(button5)
        hruview.add_item(button6)
        hruview.add_item(button7)
        hruview.add_item(button4)
        halloview.add_item(button1)
        halloview.add_item(button2)
        halloview.add_item(button3)
        halloview.add_item(button4)
        hallo2view.add_item(button2)
        hallo2view.add_item(button3)
        hallo2view.add_item(button4)
        HalloEmbed = Embed(
            title=title,
            description=description,
            colour=Colour.blue()
        )
        HalloEmbed2 = Embed(
            title=f"{random.choice(['Hallo', 'Hello'])} {setting.user(ctx.author)}",
            colour=Colour.blue()
        )
        HruEmbed = Embed(
            title="Question: How are you?",
            description="I'm alright, what about you?",
            colour=Colour.blue()
        )
        HruEmbed2 = Embed(
            title=f"{random.choice(['Nice!', 'Epic.', 'Awesome.', 'empic'])}",
            colour=Colour.green()
        )
        HruEmbed3 = Embed(
            title="That's, kinda bad.",
            description="To lighten your mood up a bit, here are some options.",
            colour=Colour.blue()
        )
        HruEmbed4 = Embed(
            title="Okay cool.",
            description="If you're kinda bored, here are some options to entertain yourself.",
            colour=Colour.blue()
        )
        MainPage = Embed(
            title=f"Hello {setting.user(ctx.author)}!",
            description="If you're kinda bored, pick any one of these options.",
            colour=Colour.blue()
        )
        WDYPAGE = Embed(
            title=f"To keep you entertained, here are some options.",
            colour=Colour.blue()
        )
        HalloEmbed.set_footer(text="correction: not whatever you want, the options i gib u.")
        msg = await ctx.send(embed=HalloEmbed, view=halloview)
        async def btn1_callback(interaction):
            await msg.edit(embed=HalloEmbed2, view=hallo2view)

        async def btn2_callback(interaction):
            await msg.edit(embed=HruEmbed, view=hruview)

        async def good_callback(interaction):
            await msg.edit(embed=HruEmbed2, view=hru2view)

        async def bad_callback(interaction):
            await msg.edit(embed=HruEmbed3, view=hru3view)

        async def average_callback(interaction):
            await msg.edit(embed=HruEmbed4, view=hru3view)

        async def rslashcute(interaction):
            loading = Embed(
                title="Hold on",
                description=f"Wait for some time {setting.user(ctx.author)}. Dvalin is searching r/cute."
            )
            newmsg = await msg.edit(embed=loading, view=None)
            subreddit = await reddit.subreddit(random.choice(['cute', 'cats', 'dogs']))
            allsubs = []
            x = random.choice(['top', 'hot', 'new'])
            if x == 'top':
                subs = subreddit.top(limit=75)
            elif x == 'hot':
                subs = subreddit.hot(limit=250)
            elif x == 'new':
                subs = subreddit.hot(limit=150)
            async for submission in subs:
                allsubs.append(submission)
            random_sub = random.choice(allsubs)
            name = random_sub.title
            url = random_sub.url
            cuteEmbed = Embed(
                title=name,
                colour=Colour.blue()
            )
            cuteEmbed.set_image(url=url)
            cuteEmbed.set_footer(text=f"Posted by {submission.author}.")
            global cutemsg
            cutemsg = await newmsg.edit(embed=cuteEmbed, view=cuteview)

        async def main_page(interaction):
            await msg.edit(embed=MainPage, view=hru3view)

        async def next_post_cute(interaction):
            await type_cute(user=setting.user(ctx.author), msg=cutemsg, button=button10, view=cuteview, reddit=reddit)

        async def end_callback(interaction):
            await msg.edit(view=None)

        button11.callback = main_page
        button9.callback = rslashcute
        button10.callback = next_post_cute
        button4.callback = end_callback
        button6.callback = average_callback
        button1.callback = btn1_callback
        button2.callback = btn2_callback
        button5.callback = good_callback
        button7.callback = bad_callback


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



async def type_cute(user, msg, button, view, reddit):
    loading = Embed(
        title="Hold on",
        description=f"Wait for some time {user}. Dvalin is searching r/cute."
    )
    newmsg = await msg.edit(embed=loading, view=None)
    subreddit = await reddit.subreddit(random.choice(['cute', 'cats', 'dogs']))
    allsubs = []
    x = random.choice(['top', 'hot', 'new'])
    if x == 'top':
        subs = subreddit.top(limit=75)
    elif x == 'hot':
        subs = subreddit.hot(limit=250)
    elif x == 'new':
        subs = subreddit.hot(limit=150)
    async for submission in subs:
        allsubs.append(submission)
    random_sub = random.choice(allsubs)
    name = random_sub.title
    url = random_sub.url
    cuteEmbed = Embed(
        title=name,
        colour=Colour.blue()
    )
    cuteEmbed.set_image(url=url)
    cuteEmbed.set_footer(text=f"Posted by {submission.author}.")
    cutemsg = await newmsg.edit(embed=cuteEmbed, view=view)

    async def next_post_cute(interaction):
        await type_cute(user=user, msg=cutemsg, button=button, view=view, reddit=reddit)

    button.callback = next_post_cute


async def randsub():
    return random.choice(['ksi', 'genshinimpact', 'technicallythetruh', 'gtaonline', 'discordapp', 'dvalinbot', 'askreddit', 'entitledparents', 'facepalm', 'hardware', 'history', 'humor', 'iphone', 'apple'])


bot.run(setting.token())
