import discord, json, requests, os, asyncio
from discord.ext import commands
from bs4 import BeautifulSoup as bs

with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    prefix = data["PREFIX"]
    id = data["ID"]
    a2f = data["A2F"]

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = prefix, intents=intents)
bot.remove_command('help')

def get_qrcode(id):
    qrcode = requests.get(f"https://www.authenticatorapi.com/pair.aspx?AppName=EBOT&AppInfo=Verif&SecretCode=ReToken_{id}")
    soupe = bs(qrcode.content, "html.parser")
    images = soupe.find_all("img")
    for image in images:
        image_src = image["src"]
        return image_src

def verif_code(id, code):
    verif = requests.get(f"https://www.authenticatorapi.com/Validate.aspx?Pin={code}&SecretCode=ReToken_{id}")
    return verif.text

@bot.command()
async def retoken(ctx):
    if ctx.author.id == id:

        if a2f == "Y":
            embed = discord.Embed(title="Verification | Google Authenticator", description="Scanner le Qrcode si se n'est pas déjà fait, puis entrer le code de google auth.")
            qrcode = get_qrcode(ctx.author.id)
            embed.set_thumbnail(url=qrcode)
            a = await ctx.author.send(embed=embed)

            embedT = discord.Embed(title="Verification | Google Authenticator", description="Vous avez entrer le bon code, j'ai regen le token du bot donc un message officiel de discord vous a été envoyer.")
            embedT.set_thumbnail(url="https://play-lh.googleusercontent.com/oMv9o-L-mNKdyL3Hp6fvNwrhAyIYB1iP3p644hxN03oFU0R2oevnmxmCLF6FewjzZXU")

            embedF = discord.Embed(title="Verification | Google Authenticator", description="Vous avez entrer un code invalide.")
            embedF.set_thumbnail(url="https://play-lh.googleusercontent.com/oMv9o-L-mNKdyL3Hp6fvNwrhAyIYB1iP3p644hxN03oFU0R2oevnmxmCLF6FewjzZXU")

            def check(m):
                return m.author == ctx.author

            try:
                message = await bot.wait_for('message', timeout= 60.0, check= check)
            except asyncio.TimeoutError:
                await ctx.message.delete()
                await a.delete()
                return
            else:
                result = verif_code(ctx.author.id, message.content)
                await ctx.message.delete()
                if result == "True":
                    await ctx.send(embed=embedT)
                    os.system(f"python github.py --name {bot.user.name} --token {token}")
                else:
                    await a.edit(embed=embedF)
        else:
            os.system(f"python github.py --name {bot.user.name} --token {token}")
            await ctx.send("Token regen.")
    else:
        await ctx.send("Vous avez pas la perm. d'utiliser cette commande.")

bot.run(token)