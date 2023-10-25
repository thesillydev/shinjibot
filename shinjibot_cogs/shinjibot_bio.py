import json
import typing
import nextcord
import asyncio
import humanize
import random
import pymongo
from nextcord.errors import HTTPException
from shinjibot_cogs.shinjibot_ajuda import CustomButton
from shinjibot import prefixo
from datetime import datetime, timedelta
from nextcord.ext import commands, menus


class Addbio(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=5)

    async def format_page(self, menu, entries):
        embed = nextcord.Embed(title="Parece que está com dúvida, amigão...",
                               description=f"Para poder usar o comando addbio, tem que seguir esse formato:\n"
                                           f"```(prefixo)addbio [parâmetro em letra minúscula] "
                                           f"[O que for necessário colocar no parâmetro]```\n"
                                           f"Aqui está a lista de parâmetros que você pode trabalhar: ",
                               color=0x7512f4)
        for entry in entries:
            embed.add_field(name=f"{entry[0].capitalize()}", value=f"{entry[1]}",
                            inline=False)
        embed.set_footer(text=f'Página {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


class Biografia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = nextcord.Intents().all()
    shinji = commands.Bot(intents=intents)

    @commands.command(name="criarbio")
    async def biografialol(self, ctx):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        biografia = {
            "Server": [{server: {"Usuários": [{user: {"<a:verificado:1025410680553209977> Título": "Desconhecido",
                                                      ":name_badge: Nome": "Desconhecido",
                                                      "<:calendar1:1025419787515461662> Data de Nascimento": "Desconhecido",
                                                      "<:kidlol:1027187486184714290> Idade": "Desconhecido",
                                                      "<a:muchlovexd:1027188280699125814> Estado Civil": "Desconhecido",
                                                      "<a:abraco:1022928949040402442> Melhor Amigo": "Desconhecido",
                                                      "<:dunnolol:1027194243262992425> Gênero": "Desconhecido",
                                                      "<:amoguslgbt:1025434368199634995> Sexualidade": "Desconhecido",
                                                      "<a:dance:1025419262426361988> Descrição": "Desconhecido",
                                                      "Imagem": "Desconhecido"}}]}}]}
        if not data:
            with open("bio.json", "w") as bi:
                json.dump(biografia, bi, indent=4, ensure_ascii=False)
            await ctx.send("A sua base de bio foi criada com sucesso!! \n"
                           f"Para poder adicionar as suas informações de bio, use `{prefix}addbio`!!")
        elif server not in [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]:
            data["Server"] += [
                {server: {"Usuários": [
                    {user: {"<a:verificado:1025410680553209977> Título": "Desconhecido",
                            ":name_badge: Nome": "Desconhecido",
                            "<:calendar1:1025419787515461662> Data de Nascimento": "Desconhecido",
                            "<:kidlol:1027187486184714290> Idade": "Desconhecido",
                            "<a:muchlovexd:1027188280699125814> Estado Civil": "Desconhecido",
                            "<a:abraco:1022928949040402442> Melhor Amigo": "Desconhecido",
                            "<:dunnolol:1027194243262992425> Gênero": "Desconhecido",
                            "<:amoguslgbt:1025434368199634995> Sexualidade": "Desconhecido",
                            "<a:dance:1025419262426361988> Descrição": "Desconhecido",
                            "Imagem": "Desconhecido"}}]}}]
            with open("bio.json", "w+") as bi:
                json.dump(data, bi, indent=4, ensure_ascii=False)
            await ctx.send("A sua base de bio foi criada com sucesso!! \n"
                           f"Para poder adicionar as suas informações de bio, use `{prefix}addbio`!!")
        else:
            if user in [list(data["Server"][list_of_servers.index(str(server))][str(server)][
                                 "Usuários"][i].keys())[0] for i in range(len(data["Server"][
                                 list_of_servers.index(str(server))][str(server)]["Usuários"]))]:
                await ctx.send(f"Você já criou a sua base de bio!\n"
                               f"Para checar sua bio, use `{prefix}bio`\n"
                               f"E para adicionar as suas informações de bio, use `{prefix}addbio`")
            else:
                with open("bio.json", "r") as bio:
                    data = json.load(bio)
                data["Server"][list_of_servers.index(server)][server]["Usuários"].append(
                    {user: {"<a:verificado:1025410680553209977> Título": "Desconhecido",
                            ":name_badge: Nome": "Desconhecido",
                            "<:calendar1:1025419787515461662> Data de Nascimento": "Desconhecido",
                            "<:kidlol:1027187486184714290> Idade": "Desconhecido",
                            "<a:muchlovexd:1027188280699125814> Estado Civil": "Desconhecido",
                            "<a:abraco:1022928949040402442> Melhor Amigo": "Desconhecido",
                            "<:dunnolol:1027194243262992425> Gênero": "Desconhecido",
                            "<:amoguslgbt:1025434368199634995> Sexualidade": "Desconhecido",
                            "<a:dance:1025419262426361988> Descrição": "Desconhecido",
                            "Imagem": "Desconhecido"}})
                with open("bio.json", "w") as bi:
                    json.dump(data, bi, indent=4, ensure_ascii=False)
                await ctx.send("A sua base de bio foi criada com sucesso!! \n"
                               f"Para poder adicionar as suas informações de bio, use `{prefix}addbio`!!")

    @commands.command(name="amigo")
    async def amizade_da_bio(self, ctx, membro: typing.Optional[str]):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        member = ctx.message.raw_mentions
        now = datetime.now()
        real_now = datetime.strftime(now, "%d/%m/%Y %H:%M:%S")
        if user in list_of_users:
            if member:
                if f"<@{member[0]}>" == membro:
                    users[list_of_users.index(user)][user][
                        "<a:abraco:1022928949040402442> Melhor Amigo"] = f"{membro} {real_now}"
                    await ctx.send("**Opa, parece que temos uma nova amizade por aqui!**\n"
                                   f"Para checar sua bio, use o comando `{prefix}bio`")
                else:
                    await ctx.send("**Por favor, mencione a pessoa que deseja iniciar uma melhor amizade**")
            else:
                if users[list_of_users.index(user)][user][
                    "<a:abraco:1022928949040402442> Melhor Amigo"] != "Desconhecido":
                    info = users[list_of_users.index(user)][user][
                        '<a:abraco:1022928949040402442> Melhor Amigo'].split()
                    humanize.i18n.activate("pt_BR")
                    no = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
                    now = datetime.strptime(no, "%d/%m/%Y %H:%M:%S")
                    birthdate = datetime.strptime(f"{info[1]} {info[2]}", "%d/%m/%Y %H:%M:%S")
                    delta = now - birthdate
                    resultado = []
                    if delta.days >= 1:
                        no1 = datetime.strftime(datetime.now(), "%d/%m/%Y")
                        now1 = datetime.strptime(no1, "%d/%m/%Y")
                        birthdate1 = datetime.strptime(f"{info[1]}", "%d/%m/%Y")
                        delta1 = now1 - birthdate1
                        resultado.append(humanize.precisedelta(delta1))
                    else:
                        resultado.append(humanize.precisedelta(delta))

                    amizade = nextcord.Embed(title="Sistema de amizade! <:zica:1022922248073519104>",
                                             color=0xf295d4)
                    amizade.set_thumbnail(url=f"{ctx.author.display_avatar}")
                    amizade.add_field(name="Melhor Amigo", value=f"{info[0]}", inline=False)
                    amizade.add_field(name="Data de início da amizade", value=info[1], inline=False)
                    amizade.add_field(name="Duração da amizade", value=resultado[0], inline=False)
                    amizade.set_footer(
                        text=f"Caso não apareça as informações de forma correta, "
                             f"verifique se você marcou a pessoa corretamente usando o comando {prefix}amigo.")
                    await ctx.send(embed=amizade)
            with open("bio.json", "w") as bi:
                json.dump(data, bi, indent=4, ensure_ascii=False)
        else:
            await ctx.send(
                f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @commands.command(name="casamento", aliases=["marry"])
    async def casamento_da_bio(self, ctx, member: typing.Optional[str]):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        membro = await commands.MemberConverter().convert(ctx, member[2:-1])
        mentions = ctx.message.raw_mentions
        if member is None:
            await ctx.send("**Por favor, marque a pessoa com que você deseja casar!**")
        else:
            if user in list_of_users:
                if mentions:
                    gender_check, gender_check_user = "", ""
                    try:
                        gender_check += users[list_of_users.index(f"{membro.name}({membro.id})")][
                            f"{membro.name}({membro.id})"]["<:dunnolol:1027194243262992425> Gênero"]
                    except TypeError:
                        await ctx.send(
                            "**Não pode se casar com aguém que não definiu seu gênero... "
                            "Vai se casar com um bot?** :face_with_raised_eyebrow:")
                    try:
                        gender_check_user += users[list_of_users.index(user)][user][
                            "<:dunnolol:1027194243262992425> Gênero"]
                    except TypeError:
                        await ctx.send("**Precisa informar seu gênero antes de se casar!**")

                    def termo_de_casal():
                        lista = [gender_check_user, gender_check]
                        if "Homem :male_sign:" in lista:
                            lista.remove("Homem :male_sign:")
                            lista.append("Marido")
                            if "Mulher :female_sign:" in lista:
                                lista.remove("Mulher :female_sign:")
                                lista.append("Esposa")
                                if "Não Binário <:non_binary:1022653462909030440>" in lista:
                                    lista.remove("Não Binário <:non_binary:1022653462909030440>")
                                    lista.append("Cônjuge")
                        if "Mulher :female_sign:" in lista:
                            lista.remove("Mulher :female_sign:")
                            lista.append("Esposa")
                            if "Não Binário <:non_binary:1022653462909030440>" in lista:
                                lista.remove("Não Binário <:non_binary:1022653462909030440>")
                                lista.append("Cônjuge")
                        else:
                            lista.remove("Não Binário <:non_binary:1022653462909030440>")
                            lista.append("Cônjuge")
                        return lista

                    if f"{membro.name}({membro.id})" not in list_of_users:
                        await ctx.send("**A pessoa com quem você quer se casar não criou uma bio ainda.**\n"
                                       f"Peça para ela usar o comando `{prefixo(ctx.guild.id)}` para que possam se casar.")
                    else:
                        if user in list_of_users:
                            membro1 = list(users[list_of_users.index(f"{membro.name}({membro.id})")].keys())[0] \
                                .replace(f"{membro.name}(", "").replace(")", "")
                            membro2 = \
                            users[list_of_users.index(f"{membro.name}({membro.id})")][f"{membro.name}({membro.id})"][
                                "<a:muchlovexd:1027188280699125814> Estado Civil"]
                            marcar = await commands.MemberConverter().convert(ctx, membro1)
                            pronome = ""
                            if gender_check_user.startswith("Homem"):
                                pronome += "ele"
                            elif gender_check_user.startswith("Mulher"):
                                pronome += "ela"
                            else:
                                pronome += "elu"
                            if membro2 != f"Casado com {membro.mention}" and membro2 != "Desconhecido":
                                await ctx.send("Ei... O que... Você está fazendo...? Você já é uma pessoa casada...")
                                await asyncio.sleep(3)
                                await marcar.send(
                                    f"Ei, uhhh... Não sou de me meter em história de casal, mas infelizmente eu vi o {ctx.author} querendo se casar com {membro}...\n"
                                    f"Se você quiser terminar com {pronome}, não hesite em usar `[prefixo do server]divorciar`!")
                            elif membro2 == f"Casado com {membro.mention}":
                                await ctx.send(f"**Você já está casado com {membro.mention}!**")
                            elif membro2 == "Desconhecido":
                                if membro.name == self.bot.user.name:
                                    nani = nextcord.Embed(title="P-peraí, m-mas porque se casaria comigo?",
                                                          color=0xf24193,
                                                          description="Eu sou apenas um robô...\n"
                                                                      "Não posso me casar com você...")
                                    nani.set_image(url=f"{blush1[random.choice(range(len(blush1)))]}")
                                    await ctx.send(embed=nani)
                                elif membro.name == user:
                                    credo = nextcord.Embed(title="Credo... Você não pode se casar consigo mesmo...\n"
                                                                 "Porque caralhos você faria isso?", colour=0xf6b2d6,
                                                           description="Vai arranjar um parceiro ao menos, seu narcisista do caralho... <:disgustingcringe:1030482957821034517>")
                                    credo.set_image(
                                        url="https://media.tenor.com/HzZIzXahdw0AAAAM/one-punch-man-saitama.gif")
                                    await ctx.send(embed=credo)
                                else:
                                    mens, artigo = "", ""
                                    if gender_check_user.startswith("Homem"):
                                        mens += "marido"
                                        artigo += "á-lo"
                                    elif gender_check_user.startswith("Mulher"):
                                        mens += "esposa"
                                        artigo += "á-la"
                                    elif gender_check_user.startswith("Não"):
                                        mens += "cônjuge"
                                        artigo += "ar"
                                    await ctx.send(
                                        f"""{membro.mention}, você aceita {ctx.author.mention} como seu legítimo {mens}
                e promete am{artigo} e respeit{artigo}:
        
                Na alegria e na tristeza,
                Na saúde e na doença,
                Na riqueza e na pobreza,
                Por todos os dias das suas vida
                Até que a morte os separe?""")

                                    def check_this(m):
                                        return m.author == membro and m.content.lower().startswith(("sim", "não"))

                                    try:
                                        with open("nothing_else.json") as dat:
                                            all_links = json.load(dat)
                                        kiss1 = all_links["kiss"]
                                        msg = await self.bot.wait_for("message", timeout=30, check=check_this)
                                        if msg.content.lower().startswith('sim'):
                                            marry = nextcord.Embed(
                                                title=f"Então eu vos declaro {termo_de_casal()[0]} e {termo_de_casal()[1]}!",
                                                color=0xb1b1f3,
                                                description=f"Pode beijar-vos agora!")
                                            marry.set_image(url=f"{kiss1[random.choice(range(len(kiss1)))]}")
                                            await ctx.send(embed=marry)
                                            users[list_of_users.index(user)][
                                                user]["<a:muchlovexd:1027188280699125814> Estado Civil"] = \
                                                f"Casado com {membro.mention} <a:amorzinho:1022923022186840104> {datetime.now()}"
                                            users[list_of_users.index(f"{membro.name}({membro.id})")][
                                                f"{membro.name}({membro.id})"][
                                                "<a:muchlovexd:1027188280699125814> Estado Civil"] = \
                                                f"Casado com {ctx.author.mention} <a:amorzinho:1022923022186840104> {datetime.now()}"
                                            with open("bio.json", "w") as bi:
                                                json.dump(data, bi, indent=4, ensure_ascii=False)
                                    except asyncio.TimeoutError:
                                        await ctx.send(f"**Sinto muito, {ctx.author.mention}...**\n"
                                                       f"Parece que você levou um fora de {membro.mention}. <:sadhug:1030468652182536262>")
                else:
                    info = users[list_of_users.index(user)][user][
                        "<a:muchlovexd:1027188280699125814> Estado Civil"].split()
                    humanize.i18n.activate("pt_BR")
                    no = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
                    now = datetime.strptime(no, "%d/%m/%Y %H:%M:%S")
                    birthdate = datetime.strptime(f"{info[3]} {info[4]}", "%d/%m/%Y %H:%M:%S")
                    delta = now - birthdate
                    resultado = []
                    if delta.days >= 1:
                        no1 = datetime.strftime(datetime.now(), "%d/%m/%Y")
                        now1 = datetime.strptime(no1, "%d/%m/%Y")
                        birthdate1 = datetime.strptime(f"{info[3]}", "%d/%m/%Y")
                        delta1 = now1 - birthdate1
                        resultado.append(humanize.precisedelta(delta1))
                    else:
                        resultado.append(humanize.precisedelta(delta))
                    name1 = await commands.MemberConverter().convert(ctx, info[2][2:-1])
                    username = name1.display_name
                    authorname = ctx.author.display_name

                    amizade = nextcord.Embed(title="Sistema de amizade! <:zica:1022922248073519104>",
                                             color=0xf295d4)
                    amizade.set_thumbnail(url=f"{ctx.author.display_avatar}")
                    amizade.add_field(name="Casado com", value=f"{info[2]}", inline=False)
                    amizade.add_field(name="Data do Início do Casamento", value=info[3], inline=False)
                    amizade.add_field(name="Duração do casamento", value=resultado[0], inline=False)
                    amizade.add_field(name="Nome do shipp",
                                      value=f"{authorname[:len(authorname) // 2 + 1]}{username[len(username) // 2:].lower()}",
                                      inline=False)
                    amizade.set_footer(
                        text=f"Caso não apareça as informações de forma correta, "
                             f"verifique se você marcou a pessoa corretamente usando o comando {prefix}casamento.")
                    await ctx.send(embed=amizade)
                with open("bio.json", "w") as bi:
                    json.dump(data, bi, indent=4, ensure_ascii=False)
            else:
                await ctx.send(
                    f"**Para poder se casar primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @commands.command(name="solteiro")
    async def solteiro_da_bio(self, ctx):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        if user in list_of_users:
            users[list_of_users.index(user)][user][
                "<a:muchlovexd:1027188280699125814> Estado Civil"] = "Solteiro " \
                                                                     "<:foreveralone:1023034415061930036>"
            await ctx.send("Parece que temos um solteiro entre nós...\n"
                           f"Para checar sua bio, use o comando `{prefix}bio`")
            with open("bio.json", "w") as bi:
                json.dump(data, bi, indent=4, ensure_ascii=False)
        else:
            await ctx.send(
                f"**Para poder adicionar as "
                f"informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @commands.command(name="divorciar", aliases=["divorcio", "divórcio", "divorce"])
    async def divorcio_da_bio(self, ctx):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        if user in list_of_users:
            estado_civil = users[list_of_users.index(user)][user][
                "<a:muchlovexd:1027188280699125814> Estado Civil"]
            if estado_civil.startswith("Casado"):
                users[list_of_users.index(user)][user][
                    "<a:muchlovexd:1027188280699125814> Estado Civil"] = "Divorciado <a:sadmoment:1051191106043379712>"
                await ctx.send("Uma pena que tenham que se separar...")
            with open("bio.json", "w") as bi:
                json.dump(data, bi, indent=4, ensure_ascii=False)
        else:
            await ctx.send(
                f"**Para poder adicionar as "
                f"informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @commands.command(name="bio")
    async def biolol(self, ctx, membro: typing.Optional[str]):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        try:
            if membro is None:
                items1 = users[list_of_users.index(user)]
                all_values = {k: v for k, v in items1[user].items() if v != "Desconhecido"}
                if user in list_of_users:
                    if not all_values:
                        vazio = nextcord.Embed(title="Wow, look! Nothing!",
                                               description=f"Se quiser ver algo além do próprio vazio, "
                                                           f"não se esqueça de usar `{prefix}addbio`", color=0x111111)
                        vazio.set_image(url="https://media.tenor.com/W89Ibr-XOTUAAAAC/dhmis-donthugmeimscared.gif")
                        await ctx.send(embed=vazio)
                    else:
                        biografia = nextcord.Embed(title=f"Perfil do Usuário do {ctx.author} :detective:",
                                                   description=f"Solictado por {ctx.author.mention}", color=0x7429f4)
                        for item in all_values.keys():
                            if item != "Imagem":
                                if item not in ["<a:abraco:1022928949040402442> Melhor Amigo",
                                                "<a:muchlovexd:1027188280699125814> Estado Civil"]:
                                    biografia.add_field(name=item, value=all_values[item], inline=False)
                                else:
                                    if item == "<a:abraco:1022928949040402442> Melhor Amigo":
                                        biografia.add_field(name=item, value=all_values[item].split()[0], inline=False)
                                    else:
                                        if items1[user]["<a:muchlovexd:1027188280699125814> Estado Civil"].startswith(
                                                "Casado"):
                                            lst = all_values[item].split()
                                            new_lst = [lst[i] for i in range(len(lst)) if
                                                       i not in [(len(lst) - 2), (len(lst) - 1)]]
                                            biografia.add_field(name=item, value=" ".join(new_lst), inline=False)
                            else:
                                biografia.add_field(name=item, value=all_values[item], inline=False)
                        if "Imagem" not in list(all_values.keys()):
                            biografia.set_image(url="https://media.tenor.com/51xvC35-fDEAAAAC/manhunt.gif")
                        else:
                            biografia.set_image(url=f"{list(all_values.values())[-1]}")
                        biografia.set_thumbnail(url=f"{ctx.author.display_avatar}")
                        await ctx.send(embed=biografia)
                else:
                    await ctx.send(
                        f"**Para poder visualizar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")
            else:
                member = await commands.MemberConverter().convert(ctx, membro[2:-1])
                if f"{member.name}({member.id})" not in list_of_users:
                    await ctx.send("**Esse membro não possui uma bio!**\n"
                                   f"Peça para ele criar a bio usando o comando `{prefix}criarbio` "
                                   f"antes de poder ver a bio dele.")
                else:
                    items1 = users[list_of_users.index(f"{member.name}({member.id})")]
                    all_values = {k: v for k, v in items1[f"{member.name}({member.id})"].items() if v is not None}
                    if not all_values:
                        vazio = nextcord.Embed(title="Wow, look! Nothing!",
                                               description=f"Se quiser ver algo além do próprio vazio, "
                                                           f"não se esqueça de usar `{prefix}addbio`", color=0x111111)
                        vazio.set_image(url="https://media.tenor.com/W89Ibr-XOTUAAAAC/dhmis-donthugmeimscared.gif")
                        await ctx.send(embed=vazio)
                    else:
                        biografia = nextcord.Embed(title=f"Perfil do Usuário do {member} :detective:",
                                                   description=f"Solictado por {ctx.author.mention}", color=0x7429f4)
                        for item in all_values.keys():
                            if item != "Imagem":
                                if item not in ["<a:abraco:1022928949040402442> Melhor Amigo",
                                                "<a:muchlovexd:1027188280699125814> Estado Civil"]:
                                    biografia.add_field(name=item, value=all_values[item], inline=False)
                                else:
                                    if item == "<a:abraco:1022928949040402442> Melhor Amigo":
                                        biografia.add_field(name=item, value=all_values[item].split()[0], inline=False)
                                    else:
                                        if items1[user]["<a:muchlovexd:1027188280699125814> Estado Civil"].startswith(
                                                "Casado"):
                                            lst = all_values[item].split()
                                            new_lst = [lst[i] for i in range(len(lst)) if
                                                       i not in [(len(lst) - 2), (len(lst) - 1)]]
                                            biografia.add_field(name=item, value=" ".join(new_lst), inline=False)
                            else:
                                biografia.add_field(name=item, value=all_values[item], inline=False)
                        if "Imagem" not in list(all_values.keys()):
                            biografia.set_image(url="https://media.tenor.com/51xvC35-fDEAAAAC/manhunt.gif")
                        else:
                            biografia.set_image(url=f"{list(all_values.values())[-1]}")
                        biografia.set_thumbnail(url=f"{member.display_avatar}")
                        await ctx.send(embed=biografia)
        except ValueError:
            await ctx.send(f"Você deve criar uma bio usando o "
                           f"comando `{prefix}criarbio` antes de usar esses comandos.")

    @commands.group(name="addbio", invoke_without_command=True)
    async def addbio(self, ctx):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        ajuda_addbio = {"Título": "Uma mini descrição do usuário limitado a 42 caracteres.",
                        "Nome": "O nome que o usuário prefere ser chamado:\n\n"
                                "Se prefere ser chamado pelo seu nickname, use [nick].\n"
                                "Se prefere ser chamado pelo username, use [username].\n"
                                "Caso contrário, pode colocar o nome que quiser.\n\n"
                                "Atenção: Ele é limitado a 32 caracteres, assim como o Discord.",
                        "Nascimento": "A data de nascimento do usuário no formato DD/MM/YYYY"
                                      "(Ele preenche o campo da idade automaticamente)\n\n"
                                      "Atenção: Ele não aceita falsas datas de "
                                      "nascimento de pessoas mais velhas que 100 anos.\n"
                                      "Exemplo:\n\n"
                                      "`04/02/69(Ao invés disso, digite 04/02/1969, "
                                      "se quiser fazer essa piadinha de haha 69 sexo haha)`",
                        "Status": "Define se ele está solteiro ou não.\n"
                                  f"Para casar, use `{prefix}casar` e marcar a "
                                  "pessoa que quer casar dentro do server.\n"
                                  f"Para definir que está solteiro, use `{prefix}solteiro`.\n"
                                  f"Ps: Se quiser divorciar, use o comando `{prefix}divorciar.`",
                        "Amigo": "Declara quem você tem mais amizade dentro do server "
                                 f"usando o comando {prefix}amigo.",
                        "Gênero": "Declara sua identidade de gênero.\n"
                                  "Aqui está os parâmetros que pode usar:\n\n"
                                  "- Homem :male_sign:\n"
                                  "- Mulher :female_sign:\n"
                                  "- Homem Trans :transgender_flag: :male_sign:\n"
                                  "- Mulher Trans :transgender_flag: :female_sign:\n"
                                  "- Não-Binário <:non_binary:1022653462909030440>",
                        "Sexualidade": "Declara suas preferências sexuais.\n"
                                       "Aqui está os parâmetros que pode usar:\n\n"
                                       "- Hétero <:straight_flag:1022652639877550154>\n"
                                       "- Gay <:gay_flag:1022652722018787368>\n"
                                       "- Lésbica <:lesbian_flag:1022652805422526484>\n"
                                       "- Bissexual <:bisexual_flag:1022652888843030569>\n"
                                       "- Panssexual <:pansexual_flag:1022652943754870914>\n"
                                       "- Assexual <:asexual_flag:1022653021974437930>\n",
                        "Descrição": "Área para colocar o que possa descrever pelo um pouco sobre você.\n"
                                     "Limitado a 1024 caracteres devido a limitação de caracteres do discord.",
                        "Imagem": "Insere uma imagem para deixar sua bio bonita, ou engraçada, ou que seja; "
                                  "desde que sirva para decorar sua bio."
                        }
        try:
            if user in list_of_users:
                ke = list(ajuda_addbio.keys())
                va = list(ajuda_addbio.values())
                data = [tuple([ke[i], va[i]]) for i in range(len(ke))]
                pages = CustomButton(source=Addbio(data))
                await pages.start(ctx)
            else:
                await ctx.send(
                    f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")
        except ValueError:
            await ctx.send(f"Você deve criar uma bio usando o "
                           f"comando `{prefix}criarbio` antes de usar esses comandos.")

    @addbio.command(name="título", aliases=["titulo"])
    async def titulo_da_bio(self, ctx, *, mensagem):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        if user in list_of_users:
            if len(mensagem) > 42:
                await ctx.send("**Você não pode colocar mais que 42 caracteres "
                               "na título da bio.\n\n**"
                               "Tem que ser resumido em uma linha só.")
            else:
                if user in list_of_users:
                    users[list_of_users.index(user)][user][
                        "<a:verificado:1025410680553209977> Título"] = mensagem
                with open("bio.json", "w") as bi:
                    json.dump(data, bi, indent=4, ensure_ascii=False)
                await ctx.send(f"**Título `{mensagem}` adicionado com sucesso!**\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
        else:
            await ctx.send(
                f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @addbio.command(name="nome")
    async def nome_da_bio(self, ctx, *, mensagem):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        if user in list_of_users:
            if len(mensagem) > 32:
                await ctx.send("**Você não pode colocar mais que 32 caracteres "
                               "no nome da bio.\n\n**"
                               "Assim como não pode fazer isso renomeando seu nickname, "
                               "também não pode fazer isso na bio.")
            else:
                if user in list_of_users:
                    if mensagem == "nick":
                        users[list_of_users.index(user)][user][":name_badge: Nome"] = ctx.author.display_name
                        await ctx.send(f"**Nome {ctx.author.display_name} adicionado com sucesso!**\n"
                                       f"Para checar sua bio, use o comando `{prefix}bio`")
                    elif mensagem == "username":
                        users[list_of_users.index(user)][user][":name_badge: Nome"] = ctx.author.name
                        await ctx.send(f"**Nome {ctx.author.name} adicionado com sucesso!**\n"
                                       f"Para checar sua bio, use o comando `{prefix}bio`")
                    else:
                        users[list_of_users.index(user)][user][":name_badge: Nome"] = mensagem
                        await ctx.send(f"**Nome {mensagem} adicionado com sucesso!**\n"
                                       f"Para checar sua bio, use o comando `{prefix}bio`")
                with open("bio.json", "w") as bi:
                    json.dump(data, bi, indent=4, ensure_ascii=False)
        else:
            await ctx.send(
                f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @addbio.command(name="nascimento")
    async def nascimento_da_bio(self, ctx, datas):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        if user in list_of_users:
            try:
                now = str(datetime.date(datetime.now()))
                day = now[-2:]
                month = now[-5:-3]
                year = now[:4]
                now1 = f"{day}/{month}/{year}"
                real_now = datetime.strptime(now1, "%d/%m/%Y")
                day1 = datas[:2]
                month1 = datas[3:5]
                year1 = datas[6:]
                real_data = f"{day1}/{month1}/{year1}"
                real_data1 = datetime.strptime(real_data, "%d/%m/%Y")
                unix = real_now - real_data1
                if user in list_of_users:
                    if unix.days > 36500:
                        await ctx.send("**Não pode colocar datas de pessoas mais velhas que 100 anos.**\n"
                                       "Esse comando permite que as pessoas coloquem até 1000 anos de idade, "
                                       "porém, ninguém vive mais de 100 anos e usa o discord.")
                    else:
                        users[list_of_users.index(user)][user][
                            "<:calendar1:1025419787515461662> Data de Nascimento"] = datas
                        users[list_of_users.index(user)][user][
                            "<:kidlol:1027187486184714290> Idade"] = f"{unix.days // 365} anos"
                        with open("bio.json", "w") as bi:
                            json.dump(data, bi, indent=4, ensure_ascii=False)
                        await ctx.send("**Data de nascimento adicionado com sucesso.**\n"
                                       f"Para checar sua bio, use o comando `{prefix}bio`")
            except ValueError:
                error = nextcord.Embed(title="Você está trabalhando com o valor errado", color=0xff1414,
                                       description="Esse comando utiliza o método padrão de "
                                                   "classificar datas(DD/MM/YYYY).\n"
                                                   "Qualquer valor que colocar como parâmetro que "
                                                   "não siga esse formato será considerado inválido.")
                await ctx.send(embed=error)
        else:
            await ctx.send(
                f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @addbio.command(name="gênero", aliases=["genero"])
    async def genero_da_bio(self, ctx, *, gender):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        if user in list_of_users:
            if gender.lower() == "homem":
                users[list_of_users.index(user)][user]["<:dunnolol:1027194243262992425> Gênero"] = "Homem :male_sign:"
                await ctx.send(f"Gênero **Homem :male_sign:** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            elif gender.lower() == "mulher":
                users[list_of_users.index(user)][user][
                    "<:dunnolol:1027194243262992425> Gênero"] = "Mulher :female_sign:"
                await ctx.send(f"Gênero **Mulher :female_sign:** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            elif gender.lower() == "homem trans":
                users[list_of_users.index(user)][user][
                    "<:dunnolol:1027194243262992425> Gênero"] = "Homem Trans :male_sign: :transgender_flag:"
                await ctx.send(f"Gênero **Homem Trans :male_sign: :transgender_flag:** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            elif gender.lower() == "mulher trans":
                users[list_of_users.index(user)][user][
                    "<:dunnolol:1027194243262992425> Gênero"] = "Mulher Trans :female_sign: :transgender_flag:"
                await ctx.send(f"Gênero **Mulher Trans :female_sign: :transgender_flag:** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            elif gender.lower() in ["não binário", "nao binário", "não binario", "nao binario", "enby", "nb"]:
                users[list_of_users.index(user)][user][
                    "<:dunnolol:1027194243262992425> Gênero"] = "Não Binário <:non_binary:1022653462909030440>"
                await ctx.send(f"Gênero **Não Binário <:non_binary:1022653462909030440>** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            elif gender.lower() in ["helicóptero de ataque", "helicoptero de ataque"]:
                texto = """Isso que me contou foi uma piada? Nem parece.
Sua piada é tão ruim que eu teria preferido que a piada passasse pela minha cabeça e você desistisse de me contar a piada novamente.
Para ser honesto, esta é uma tentativa horrível de tentar tirar uma risada de mim.
Nem uma risada, nem um haha, nem mesmo uma sutil explosão de ar saindo do meu esôfago.
A ciência diz que antes de você rir, seu cérebro prepara os músculos do rosto, mas eu nem senti a menor contração.
0/10 essa piada é tão ruim que não posso acreditar que alguém legalmente permitiu que você fosse criativo.
A quantidade de poder cerebral que você deve ter colocado nessa piada tem o potencial de abastecer todas as casas da Terra.
Vá ter uma personalidade decente e aprenda a fazer piadas ou leia um livro.
Eu não estou dizendo isso para ser engraçado, eu realmente quero dizer que isso é apenas uma vergonha na comédia.
Você sozinho matou o humor e todos os atos cômicos do planeta.
Estou tão desapontado que a sociedade tenha falhado como um todo em ser capaz de ensiná-lo a ser engraçado.
Honestamente, se eu colocasse todo o meu poder e tempo para tentar tornar sua piada engraçada, seria necessário que o próprio Einstein construísse um dispositivo para me prender, para que eu pudesse estar conectado à energia de um bilhão de estrelas para fazê-lo, e mesmo assim tudo que a piada iria receber das pessoas é uma gargalhada muito sutil.
Você tem sorte de eu ainda ter a menor empatia por você depois de contar essa piada, caso contrário eu teria cometido todos os crimes de guerra do livro apenas para evitar que você tentasse qualquer tipo de humor novamente.
Devemos colocar essa piada nos livros didáticos para que as gerações futuras possam ser cautelosas em se tornar um fracasso cômico absoluto.
Estou desapontado, magoado e totalmente ofendido por meu precioso tempo ter sido desperdiçado em meu cérebro entendendo essa piada.
No tempo que levei eu estava planejando ajudar crianças que ficaram órfãs, mas por causa disso você gastou meu tempo explicando a integridade obscena de sua terrível tentativa de comédia.
Agora essas crianças estão sofrendo sem comer e não há ninguém para culpar além de você.
"""
                embed_var = nextcord.Embed(title="O que foi isso?",
                                           description=texto,
                                           color=0x8d62f6)
                await ctx.channel.send(embed=embed_var)
            else:
                await ctx.send(f"**Tag inválida!** Confira todos os parâmetros "
                               f"que pode usar com o comando `{prefix}addbio`")
            with open("bio.json", "w") as bi:
                json.dump(data, bi, indent=4, ensure_ascii=False)
        else:
            await ctx.send(
                f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @addbio.command(name="sexualidade", aliases=["sexo"])
    async def sexualidade_da_bio(self, ctx, sexuality):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        if user in list_of_users:
            if sexuality.lower() in ["hétero", "hetero"]:
                users[list_of_users.index(user)][user][
                    "<:amoguslgbt:1025434368199634995> Sexualidade"] = "Hétero <:straight_flag:1022652639877550154>"
                await ctx.send(f"Sexualidade **Hétero <:straight_flag:1022652639877550154>** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            elif sexuality.lower() == "gay":
                users[list_of_users.index(user)][user][
                    "<:amoguslgbt:1025434368199634995> Sexualidade"] = "Gay <:gay_flag:1022652722018787368>"
                await ctx.send(f"Sexualidade **Gay <:gay_flag:1022652722018787368>** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            elif sexuality.lower() in ["lesbica", "lésbica"]:
                users[list_of_users.index(user)][user][
                    "<:amoguslgbt:1025434368199634995> Sexualidade"] = "Lésbica <:lesbian_flag:1022652805422526484>"
                await ctx.send(f"Sexualidade **Lésbica <:lesbian_flag:1022652805422526484>** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            elif sexuality.lower() in ["bissexual", "bisexual", "bi"]:
                users[list_of_users.index(user)][user][
                    "<:amoguslgbt:1025434368199634995> Sexualidade"] = "Bissexual <:bisexual_flag:1022652888843030569>"
                await ctx.send(
                    f"Sexualidade **Bissexual <:bisexual_flag:1022652888843030569>** adicionado com sucesso!\n"
                    f"Para checar sua bio, use o comando `{prefix}bio`")
            elif sexuality.lower() in ["panssexual", "pansexual", "pan"]:
                users[list_of_users.index(user)][user][
                    "<:amoguslgbt:1025434368199634995> Sexualidade"] = "Panssexual <:pansexual_flag:1022652943754870914>"
                await ctx.send(
                    f"Sexualidade **Panssexual <:pansexual_flag:1022652943754870914>** adicionado com sucesso!\n"
                    f"Para checar sua bio, use o comando `{prefix}bio`")
            elif sexuality.lower() in ["assexual", "asexual"]:
                users[list_of_users.index(user)][user][
                    "<:amoguslgbt:1025434368199634995> Sexualidade"] = "Assexual <:asexual_flag:1022653021974437930>"
                await ctx.send(f"Sexualidade **Assexual <:asexual_flag:1022653021974437930>** adicionado com sucesso!\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            with open("bio.json", "w") as bi:
                json.dump(data, bi, indent=4, ensure_ascii=False)
        else:
            await ctx.send(
                f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @addbio.command(name="descrição", aliases=["descricão", "descriçao", "descricao"])
    async def descricao_da_bio(self, ctx, *, mensagem):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        if user in list_of_users:
            if len(mensagem) > 1981:
                await ctx.send("**Você não pode colocar mais que 2000 caracteres "
                               "na descrição da bio.\n\n**"
                               "Pra que tudo isso...?")
            else:
                if user in list_of_users:
                    users[list_of_users.index(user)][user][
                        "<a:dance:1025419262426361988> Descrição"] = mensagem
                with open("bio.json", "w") as bi:
                    json.dump(data, bi, indent=4, ensure_ascii=False)
                await ctx.send(f"**Descrição adicionada com sucesso!**\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
        else:
            await ctx.send(
                f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")

    @addbio.command(name="imagem")
    async def imagem_da_bio(self, ctx, image):
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        prefix = prefixo(ctx.guild.id)
        user = f"{ctx.author.name}({ctx.author.id})"
        server = str(ctx.guild.id)
        list_of_servers = [list(data["Server"][i].keys())[0] for i in range(len(data["Server"]))]
        users = data["Server"][list_of_servers.index(str(server))][str(server)]["Usuários"]
        list_of_users = [list(users[i].keys())[0] for i in range(len(users))]
        ext = (".gif", ".png", ".jpg", ".jpeg")
        with open("bio.json", "r") as bio:
            data = json.load(bio)
        if user in list_of_users:
            if image.endswith(ext) or image.endswith(".mp4") is False:
                users[list_of_users.index(user)][user]["Imagem"] = image
                with open("bio.json", "w") as bi:
                    json.dump(data, bi, indent=4, ensure_ascii=False)
                await ctx.send(f"**Imagem adicionada com sucesso!**\n"
                               f"Para checar sua bio, use o comando `{prefix}bio`")
            else:
                await ctx.send("**Formato inválido de imagem.**\n"
                               "Só posso mandar arquivos em `.gif, .png, .jpg e .jpeg`!\n"
                               "Além disso, certique-se que você tenha mandado "
                               "a url da imagem, não a imagem em si.")
        else:
            await ctx.send(
                f"**Para poder adicionar as informações da sua bio, primeiro você precisa criar uma bio com o `{prefix}criarbio`!**")


def setup(bot):
    bot.add_cog(Biografia(bot))
