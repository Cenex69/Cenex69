import discord, random
from runner import *
class settings:
    def __init__(self):
        pass

    def prefix(self, override=None):
        if override is None:
            self.prefix = "."
        else:
            self.prefix = str(override)
        return self.prefix

    def token(self):
        self.token = "not for u."
        return self.token


    def activity(self):
        self.activity = ".help"
        return self.activity

    def user(self, mbr):
        user = str(str(mbr).split('#')[0])[0].upper() + str(str(mbr).split('#')[0])[1:]
        if '_' in user:
            user = user.split('_')[0]
        elif ' ' in user:
            user = user.split(' ')[0]
        elif '-' in user:
            user = user.split('-')[0]
        elif '.' in user:
            user = user.split('.')[0]
        else:
            pass
        return user

    def channel(self, channel_name):
        if channel_name == "motd":
            return 943877951915708486
        elif channel_name == "qotd":
            return 943877974942420992
        else:
            print("Wrong channel name.")

    def credentials(self, type="password"):
        if type == "password":
            return "not for u"
        elif type == "username":
            return "not for u"
        elif type == "id":
            return "not for u"
        elif type == "secret":
            return "not for u"
        elif type == "agent":
            return "not for u"



class ai:
    def __init__(self):
        return "ah yes \'artifical inteligence\'"

    def find_no(self, number):
        self.number = number
        if 'k' in number:
            split = int(str(number).split('k')[0])
            x = split * 1000
            return int(x)
        elif 'm' in number:
            split = int(str(number).split('m')[0])
            x = split * 1000000
            return int(x)
        elif 'b' in number:
            split = int(str(number).split('b')[0])
            x = split * 1000000000
            return int(x)
        else:
            print(int(number))
            return int(number)

    def find_title(self, description:str, server):
        if "welcome" in description.lower():
            self.title = f"Welcome to {server.name}"
        elif "verif" in description.lower():
            self.title = f"About verification"
        elif "mod" in description.lower():
            self.title = f"About moderation"
        elif "updat" in description.lower():
            self.title = f"New Update"
        else:
            self.title = f"Announcement"
        return self.title

    def find_desc(self, desc1, desc2=None, desc3=None, desc4=None, desc5=None, desc6=None, desc7=None, desc8=None, desc9=None, desc10=None, desc11=None, desc12=None, desc13=None, desc14=None, desc15=None, desc16=None, desc17=None, desc18=None, desc19=None, desc20=None, desc21=None, desc22=None, desc23=None, desc24=None, desc25=None, desc26=None, desc27=None, desc28=None, desc29=None, desc30=None, desc31=None):
        if desc2 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]}"
        elif desc3 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2}"
        elif desc4 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3}"
        elif desc5 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4}"
        elif desc6 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5}"
        elif desc7 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6}"
        elif desc8 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7}"
        elif desc9 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8}"
        elif desc10 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9}"
        elif desc11 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10}"
        elif desc12 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11}"
        elif desc13 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12}"
        elif desc14 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13}"
        elif desc15 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14}"
        elif desc16 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15}"
        elif desc17 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16}"
        elif desc18 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17}"
        elif desc19 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18}"
        elif desc20 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19}"
        elif desc21 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20}"
        elif desc22 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21}"
        elif desc23 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22}"
        elif desc24 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22} {desc23}"
        elif desc25 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22} {desc23} {desc24}"
        elif desc26 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22} {desc23} {desc24} {desc25}"
        elif desc27 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22} {desc23} {desc24} {desc25} {desc26}"
        elif desc28 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22} {desc23} {desc24} {desc25} {desc26} {desc27}"
        elif desc29 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22} {desc23} {desc24} {desc25} {desc26} {desc27} {desc28}"
        elif desc30 is None:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22} {desc23} {desc24} {desc25} {desc26} {desc27} {desc28} {desc29}"
        elif desc31 is not None:
            msg = "too many words"
            return msg
        else:
            description = f"{str(desc1)[0].upper() + str(desc1)[1:]} {desc2} {desc3} {desc4} {desc5} {desc6} {desc7} {desc8} {desc9} {desc10} {desc11} {desc12} {desc13} {desc14} {desc15} {desc16} {desc17} {desc18} {desc19} {desc20} {desc21} {desc22} {desc23} {desc24} {desc25} {desc26} {desc27} {desc28} {desc29} {desc30}"
        return description


class buttonstyle:
    def __init__(self):
        pass

    def blue(self):
        return 1

    def gray(self):
        return 2

    def green(self):
        return 3

    def red(self):
        return 4

    def url(self):
        return 5



class confirmations:
    def __init__(self):
        pass

    def conf(self, about:str, desc:str):
        if about == "announce":
            self.conf_type = "ANNOUNCEMENT"
        elif about == "verify":
            self.conf_type = "VERIFICATION"
        else:
            print('you dork why didnt you type the correct thing im ashamed of u')
        if self.conf_type == "ANNOUNCEMENT":
            self.anounc = discord.Embed(
                title="Confirmation",
                description=f"Do you want to announce '{desc}'?",
                colour=discord.Colour.blue()
            )
            return self.anounc

    def procresult(self, channel, server):
        channel = str(channel)[0].upper()+str(channel)[1:]
        server = str(server)[0].upper()+str(server)[1:]
        if '-' in channel:
            channel = channel.replace('-', ' ')
        if self.conf_type == "ANNOUNCEMENT":
            self.result = discord.Embed(
                title="Success",
                description=f"Posted the announcement on {channel} at {server}",
                colour=discord.Colour.blue()
            )
        return self.result

    def exisult(self):
        if self.conf_type == "ANNOUNCEMENT":
            self.result = discord.Embed(
                title="Cancelled the announcement",
                colour=discord.Colour.blue()
            )
        return self.result

class errors:
    def __init__(self):
        pass

    def too_many_inputs(self, amount:int, command):
        self.too_many_inputs = discord.Embed(
            title="Error",
            description=f"The maximum word limit for the {command} command is {amount}. Any more than {amount} will result an error like this one.",
            colour=discord.Colour.blue()
        )
        return self.too_many_inputs
