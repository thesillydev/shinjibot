import json
import typing
import nextcord
import random
from nextcord.ext import commands


class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = nextcord.Intents().all()
    shinji = commands.Bot(intents=intents)

    @commands.command(aliases=["soco", "punch"])
    async def pan(self, ctx, membro: nextcord.Member = None, *, mensagem=" "):
        with open('prefixos.json', 'r') as sus:
            prefixos = json.load(sus)
        prefix = prefixos[str(ctx.guild.id)]
        member = membro.mention
        user = ctx.message.author.mention
        if member == user:
            await ctx.send(f"**Se você quiser se socar(Por alguma razão desconhecida), use `{prefix}socosm`**")
        elif member is None:
            await ctx.send("**Por favor, mencione um usuário que deseja socar.**")
        else:
            with open('nothing_else.json', 'r') as file:
                all_links = json.load(file)
            punch = all_links["punch"]
            soco = random.choice(punch)
            acao = nextcord.Embed(title="Essa deve ter doído... :grimacing:", color=0xe63946,
                                  description=f"{user} socou {member}!\n\n"
                                              f"{mensagem}")
            acao.set_image(url=f"{soco}")
            acao.set_footer(text="Depois dessa vou até ficar quieto...")
            await ctx.send(embed=acao)

    @commands.command(name="socosm")
    async def pan2(self, ctx):
        with open('nothing_else.json', 'r') as file:
            all_links = json.load(file)
        punch = all_links["punch1"]
        soco = random.choice(punch)
        acao = nextcord.Embed(title="O cara tá batendo em si mesmo wtf", color=0xe63946)
        acao.set_image(url=f"{soco}")
        acao.set_footer(text="Enlouqueceu esse pobre coitado...", icon_url=f"{self.bot.user.display_avatar}")
        await ctx.send(embed=acao)

    @commands.command(aliases=["tapa", "slap"])
    async def surappu(self, ctx, member: nextcord.Member = None, *, mensagem=" "):
        membro = member.mention
        user = ctx.message.author.mention
        if member is None:
            await ctx.send("**Por favor, mencione um usuário que deseja dar um tapa.**")
        else:
            with open('nothing_else.json', 'r') as file:
                all_links = json.load(file)
            slap = all_links["slap"]
            tapa = random.choice(slap)
            acao = nextcord.Embed(title="Tome uma, tome duas...", color=0xe63946,
                                  description=f"{user} deu um tapa no {membro}! :grimacing:\n\n"
                                              f"{mensagem}")
            acao.set_image(url=f"{tapa}")
            acao.set_footer(text="Tomou um tapão mesmo eim... Misericórdia...", icon_url=f"{self.bot.user.display_avatar}")
            await ctx.send(embed=acao)

    @commands.command(name="chute")
    async def kikku(self, ctx, member: nextcord.Member = None, *, mensagem=" "):
        membro = member.mention
        user = ctx.message.author.mention
        if member is None:
            await ctx.send("**Por favor, mencione um usuário que deseja dar um chute.**")
        else:
            with open('nothing_else.json', 'r') as file:
                all_links = json.load(file)
            kick = all_links["kick"]
            chute = random.choice(kick)

            acao = nextcord.Embed(title="Toma essa voadora!! :face_with_symbols_over_mouth:", color=0xe63946,
                                  description=f"{user} chutou {membro}!\n"
                                              f"\n"
                                              f"{mensagem}")
            acao.set_image(url=f"{chute}")
            acao.set_footer(text="Na próxima vai ser pra valer!", icon_url=f"{self.bot.user.display_avatar}")
            await ctx.send(embed=acao)

    @commands.command(name="tiro")
    async def shuuto(self, ctx, member: nextcord.Member = None, *, mensagem=" "):
        membro = member.mention
        user = ctx.message.author.mention
        with open('nothing_else.json', 'r') as file:
            all_links = json.load(file)
        shot = all_links["shot"]
        tiro = random.choice(shot)
        if membro == self.bot.user.mention:
            await ctx.send("**No U <a:tiro:1022929989055815730>**\n"
                           "https://cdn.discordapp.com/attachments/968136562"
                           "275651587/1022948566039281664/The_cup_song"
                           "_American_version1080P_60FPS.mp4")
        elif member is None:
            await ctx.send("**Por favor, mencione um usuário que deseja dar um tapa.**")
        elif membro == ctx.author.mention:
            suicide = nextcord.Embed(title=f"{ctx.author.display_name} não aguenta mais viver nesse mundo", color=0xfd1123)
            suicide.set_image(url="https://i.imgur.com/81rN8Sl.gif")
            suicide.set_footer(text="Que mundo cruel nós vivemos...", icon_url=f"{self.bot.user.display_avatar}")
        else:
            acao = nextcord.Embed(title="Morre, sua praga!! <a:tiro:1022929989055815730>", color=0xe63946,
                                  description=f"{user} atirou em {membro}!\n\n"
                                              f"{mensagem}")
            acao.set_image(url=f"{tiro}")
            acao.set_footer(text="Isso foi pouco ainda, essa peste...", icon_url=f"{self.bot.user.display_avatar}")
            await ctx.send(embed=acao)

    @commands.command(aliases=["beijo", "kiss"])
    async def kissu(self, ctx, member: nextcord.Member, *, mensagem=" "):
        with open('prefixos.json', 'r') as sus:
            prefixos = json.load(sus)
        prefix = prefixos[str(ctx.guild.id)]
        membro = member.mention
        user = ctx.message.author.mention
        if membro == user:
            await ctx.send(f"**Se você quiser se beijar(Por alguma razão desconhecida), use `{prefix}beijosm`**")
        else:
            with open('nothing_else.json', 'r') as file:
                all_links = json.load(file)
            kiss = all_links["kiss"]
            beijo = random.choice(kiss)
            acao = nextcord.Embed(title="O amor está no ar!! <a:amorzinho:1022923022186840104>", color=0xe63946,
                                  description=f"{user} beijou {membro}!\n\n"
                                              f"{mensagem}")
            acao.set_image(url=f"{beijo}")
            acao.set_footer(text="Eu também queria alguém para eu beijar assim...")
            await ctx.send(embed=acao)

    @commands.command(name="beijosm")
    async def kissu(self, ctx):
        with open('nothing_else.json', 'r') as file:
            all_links = json.load(file)
        kiss = all_links["kiss1"]
        beijo = random.choice(kiss)
        acao = nextcord.Embed(title="O cara tá beijando a si mesmo wtf", color=0xe63946)
        acao.set_image(url=f"{beijo}")
        acao.set_footer(text="Narcissismo é foda...")
        await ctx.send(embed=acao)

    @commands.command(aliases=["abraço", "hug"])
    async def hangu(self, ctx, member: nextcord.Member, *, mensagem=" "):
        membro = member.mention
        user = ctx.message.author.mention
        with open('nothing_else.json', 'r') as file:
            all_links = json.load(file)
        hug = all_links["hug"]
        abraco = random.choice(hug)
        acao = nextcord.Embed(title="Que bonitinho!! <a:abraco:1022928949040402442>", color=0xe63946,
                              description=f"{user} abraço {membro}!\n\n"
                                          f"{mensagem}")
        acao.set_image(url=f"{abraco}")
        acao.set_footer(text="Eu também queria alguém pra eu abraçar assim...")
        await ctx.send(embed=acao)


def setup(bot):
    bot.add_cog(Actions(bot))
