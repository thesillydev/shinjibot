import asyncio
import nextcord
import json
import os
import math
import random
import pymongo
import time
from num2words import num2words
from nextcord.ext import commands, tasks
from datetime import timedelta
from math import pi


def determinar_prefixo(client, message):
    try:
        with open('prefixos.json', 'r') as sus:
            prefixos = json.load(sus)

        return prefixos[str(message.guild.id)]
    except KeyError:
        with open('prefixos.json', 'r') as sus:
            prefixos = json.load(sus)

        prefixos[str(message.guild.id)] = '//'

        with open('prefixos.json', 'w') as f:
            json.dump(prefixos, f, indent=4)
        return "//"


def prefixo(guild):
    with open('prefixos.json', 'r') as sus:
        prefixos = json.load(sus)
    prefix = prefixos[str(guild)]
    return prefix


def links(key):
    with open('nothing_else.json', 'r') as file:
        all_links = json.load(file)
    return all_links[str(key)]


intents = nextcord.Intents().all()
shinji = commands.Bot(command_prefix=determinar_prefixo, intents=intents)


@tasks.loop(minutes=20)
async def changepresence():
    game = ["Amogus ඞ",
            "Bobox é muito bom!",
            "Se liga na minha skin de 1000000 bobux!",
            "ORA ORA ORA ORA ORA ORA ORA ORA",
            "Carai, esse joguinho com dubstep é mó daora kkkkk",
            "Joguinho de ritmokkkkkkkkkkkkkkkkkkkkkkkkk",
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "I like your cut G",
            "SMONGUAI WAM WAM WAM WAM WAM WAM",
            "Essa menininha de Spy x Family é muito fofa",
            "F VereBot",
            "Jesse, stop smelling my balls",
            "Haha Sus Amogus",
            "Drop like it's hot",
            "Algo totalmente não relacionado a sus amogus haha",
            "Metal rocks muito loco hardcore pesadão pauleira",
            "Vaporwave não é gênero musical",
            "Fuck you, I'm Broly",
            "Ainda vai ter mais comandos pela frente, relaxa",
            "Finna Jerk It",
            "O meu criador é muito cringe",
            "We do a little trolling",
            "Eu sou aroace, sai daqui!",
            "Cum bucket"]
    type1 = range(0, 4)
    await shinji.change_presence(activity=nextcord.Activity(name=random.choice(game), type=random.choice(type1)))


@tasks.loop(seconds=1)
async def mongodb():
    time1 = os.path.getmtime(r"C:\Users\mahir\PycharmProjects\Teste\venv\projetos\bio.json")
    client = pymongo.MongoClient(links("mongodb"))
    db = client["shinjibot"]
    bio = db["bio"]
    while True:
        with open("bio.json", "r") as sus:
            bio1 = json.load(sus)
        new_time = os.path.getmtime(r"C:\Users\mahir\PycharmProjects\Teste\venv\projetos\bio.json")
        if new_time != time1:
            bio.delete_many({})
            bio.insert_one(bio1)


@shinji.event
async def on_ready():
    await shinji.wait_until_ready()
    if not changepresence.is_running():
        changepresence.start()
    if not mongodb.is_running():
        mongodb.start()
    print(f"{shinji.user} está conectado no discord!")


@shinji.event
async def on_guild_join(guild):
    with open('prefixos.json', 'r') as sus:
        prefixos = json.load(sus)

    prefixos[str(guild.id)] = "//"

    with open('prefixos.json', 'w') as sus:
        json.dump(prefixos, sus, indent=4)


@shinji.listen(name="on_message")
async def idklol(msg):
    if shinji.user.mentioned_in(msg):
        if msg.content != shinji.user.mention:
            pass
        else:
            await msg.channel.send(f"**Eae, {msg.author.name}! Suave?**\n"
                                   f"Se está procurando saber sobre os meus comandos, use `{prefixo(msg.guild.id)}ajuda`\n"
                                   f"Caso queira mudar meu prefixo, use `{prefixo(msg.guild.id)}prefixo [prefixo que deseja mudar]`")


@shinji.event
async def on_message(msgm):
    with open('nothing_else.json', 'r') as file:
        all_links = json.load(file)
    amogus = all_links["amogus"]
    if msgm.content.lower() in ["sus", "sussy baka", "sussy", "sussy bak"] and msgm.content != "SUS":
        sussus = nextcord.Embed(title="Amogus <:amogus:1022951116905914420>", color=0xff2727)
        sussus.set_image(url=f"{random.choice(amogus)}")
        await msgm.channel.send(embed=sussus)
    elif msgm.content.lower() == "among us?":
        await msgm.channel.send("https://cdn.discordapp.com/attachments/553991220469170240/"
                                "983773923940372570/976f034af1b88cdd1b4fda19fc9668a571c6db"
                                "e11edd2e1822d363a312dd0a35_1.mp4")
    elif msgm.content == "SUS":
        amogus1 = all_links["amogus1"]
        sussus4 = nextcord.Embed(title="Sistema Único de Saúde??? Meio sus isso ai...", color=0xff2727)
        sussus4.set_image(url=f"{random.choice(amogus1)}")
        await msgm.channel.send(embed=sussus4)
    await shinji.process_commands(msgm)


@shinji.command(name="ping", description="Mostra a latência do bot em milissegundos.")
async def get_ping(ctx):
    await ctx.send(f":ping_pong: | **Pong!** \n\n"
                   f"Latência do bot: **{round(shinji.latency * 1000, 2)}** ms")


@shinji.command(aliases=["calcular"])
async def calc(ctx, operador, *numero):
    if len(str(eval(operador))) > 1334:
        lol = nextcord.Embed(title="Por favor, tenha misericórdia dos programadores!",
                             color=0xffb6b6,
                             description="Eu posso trabalhar com números grandes mas o "
                                         "PC do meu criador não!\n")
        lol.set_image(url="https://c.tenor.com/2tmFzIpCJTYAAAAd/shinji-shinji-ikari.gif")
        lol.set_footer(text="Brincadeira, é só limitação do discórdia mesmo.", icon_url=f"{shinji.user.display_avatar}")
        await ctx.send(embed=lol)
    else:
        f"{operador}".join(numero)
        calculo = nextcord.Embed(title="Calculadora", colour=0x7289da)
        calculo.add_field(name="Expressão:", value=f"{operador}")
        calculo.add_field(name="Resultado:", value=f"{eval(operador):,}")
        calculo.set_thumbnail(url="https://i.imgur.com/y47M56i.jpg")
        await ctx.send(embed=calculo)


@shinji.command(aliases=["fat"])
async def fatorial(ctx, num: int):
    resultado = 1
    for ene in range(1, num + 1):
        resultado = resultado * ene
    lst = list(str(resultado))
    lt = len(lst)
    if num == 0 or num == 1:
        await ctx.send("Fatorial de 0 e 1 vale 1!")
    elif num < 0:
        await ctx.send("**Honestamente...Você iria se endoidar se você visse fatoriais negativos!** \n"
                       "**Então só esquece e finge que não tentou fazer isso, lol**")
    elif lt >= 1970:
        cu = nextcord.Embed(title="Wow, calma lá amigão...", color=0xffb6b6,
                            description="O resultado dessa porra é muito maior "
                                        "do que o limite de caracteres que pode enviar mensagens pelo discord...\n"
                                        "Tá querendo explodir o PC de quem?")
        cu.set_image(url="https://c.tenor.com/LTiJbb3yRM4AAAAM/evangelion-anime.gif")
        await ctx.send(embed=cu)
    else:
        await ctx.send(f"O fatorial de {num} vale: **{resultado}**")


@shinji.command(name="raiz")
async def raizcuadrada(ctx, numero: str, raiz=2):
    if str(numero) in ["pi", "π"]:
        if raiz == 2:
            valor = math.sqrt(int(math.pi))
            await ctx.send(f"A raiz quadrada de pi é proximadamente: **{round(valor, 2)}**")
        else:
            valor = int(math.pi) ** (1 / int(raiz))
            await ctx.send(f"A raiz de expoente {raiz} de pi é aproximadamente: **{round(valor, 2)}**")
    else:
        if raiz == 2:
            valor = math.sqrt(int(numero))
            if round(valor, 2) == int(valor):
                await ctx.send(f"A raiz quadrada de {numero} é: **{int(valor)}**")
            else:
                await ctx.send(f"A raiz quadrada de {numero} é aproximadamente: **{round(valor, 2)}**")
        else:
            valor = int(numero) ** (1 / int(raiz))
            if round(valor, 2) == int(valor):
                await ctx.send(f"A raiz quadrada de {numero} é: **{int(valor)}**")
            else:
                await ctx.send(f"A raiz de expoente {raiz} do número {numero} é aproximadamente: **{round(valor, 2)}**")
        print(numero)


@shinji.command(aliases=["lernumero"])
async def lernum(ctx, numero: str):
    try:
        numero_real = numero.replace(',', '')
        ler_numero = nextcord.Embed(title="Leitor de números", colour=0x67d3cc)
        ler_numero.add_field(name="Número:", value=f"{numero_real}")
        ler_numero.add_field(name="Como se lê:", value=f"{num2words(numero_real, lang='pt_BR').capitalize()}")
        await ctx.send(embed=ler_numero)
    except OverflowError:
        await ctx.send("**Por questões de limitações, é impossível ler números maiores ou iguais a 1 quintilhão.**")


@shinji.group(name="anon", invoke_without_command=True)
async def anon(ctx, *, message):
    prefix = prefixo(ctx.guild.id)
    with open('anon.json', 'r') as sus:
        anon1 = json.load(sus)
    if str(ctx.guild.id) not in anon1.keys():
        await ctx.send(f"**Você precisa usar `{prefix} anon config` antes de usar esse comando!**")
    else:
        chan = nextcord.utils.get(ctx.guild.channels, id=int(anon1[f"{ctx.guild.id}"]))
        await ctx.channel.purge(limit=1)
        await chan.send(message)


@anon.command(name="config")
async def anonimo_config(ctx):
    prefix = prefixo(ctx.guild.id)
    channels = []
    with open('anon.json', 'r') as sus:
        anon1 = json.load(sus)
    if str(ctx.guild.id) in anon1.keys():
        await ctx.send(f"**Você já configurou esse servidor e "
                       f"as mensagens estão sendo enviadas no canal <#{anon1[str(ctx.guild.id)]}>!**")
    else:
        await ctx.send("**Mencione o canal que deseja que envie as mensagens anônimas**")
        for channel in ctx.guild.text_channels:
            channels.append(f"<#{channel.id}>")

        def check_this(m):
            return m.author == ctx.author and m.content in channels

        try:
            msg = await shinji.wait_for("message", timeout=30, check=check_this)
            if msg.content in channels:
                anon1[ctx.guild.id] = f'{msg.content.replace("<#", "").replace(">", "")}'
                with open('anon.json', 'w') as f:
                    json.dump(anon1, f, indent=4)
                await ctx.send(f"**Canal {msg.content} foi adicionado com sucesso!**\n"
                               "A partir de agora, todas as "
                               f"mensagens usando o comando `{prefix}anon` "
                               f"serão enviadas no canal {msg.content}!")
            else:
                await ctx.send("amogus")
        except asyncio.TimeoutError:
            await ctx.send("Demorasse demais! Tô vazando...")


for filename in os.listdir('shinjibot_cogs'):
    if filename.endswith('.py'):
        shinji.load_extension(f'shinjibot_cogs.{filename[:-3]}')

shinji.run("OTQyODYxNTEwOTMyMzI0Mzcy.GwJ_JP.8J4Na5lpzDHMrXzxYopd262_3kJ-pZpe44f-zc")
