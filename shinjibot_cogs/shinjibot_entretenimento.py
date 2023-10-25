import json
import pprint
import typing
import nextcord
import requests
import asyncpraw
import random
from bs4 import BeautifulSoup as Bs
from nextcord.colour import Color
from nextcord.ext import commands
from shinjibot import prefixo


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = nextcord.Intents().all()
    shinji = commands.Bot(intents=intents)

    @commands.Cog.listener(name="on_message")
    async def let_me_see(self, message):
        dict1 = {}
        if message.content.lower() == "mostre-me os comandos":
            commands1 = self.get_commands()
            for item in commands1:
                dict1.update({item.name: item.description})
            pprint.pprint(dict1)

    @commands.command(name="dado", description="Comando simples de dado onde você pode jogar uma quantidade "
                                               "definida de dados e também definir a quantidade de lados.\n"
                                               "Formato:\n"
                                               f"```dado [número de dados][número de lados]```")
    async def randomvalue(self, ctx, quantidade=1, dado=6, add=0):
        lista = []
        concordancia, addup, addupsum = "", "", ""
        if quantidade <= 0:
            await ctx.send(f"**Não se pode lançar {quantidade} dados... Isso nem faz sentido!**")
        elif dado < 3:
            await ctx.send("**Não existe dados com menos de= 3 lados! Tente novamente!**")
        elif dado > 100:
            await ctx.send(f"**Não existe dados com {dado} lados!**")
        elif quantidade > 150:
            lol = nextcord.Embed(title="Por favor, tenha misericórdia dos programadores!",
                                 color=0xffb6b6,
                                 description="Eu posso trabalhar com quantos dados quiser mas o PC do "
                                             "meu criador não!\n"
                                             "Se usar números maiores que isso, o PC dele explode!\n"
                                             "||Brincadeira, é só pra não ficar grande pra caralho mesmo||")
            lol.set_image(url="https://c.tenor.com/2tmFzIpCJTYAAAAd/shinji-shinji-ikari.gif")
            await ctx.send(embed=lol)
        else:
            for num in range(1, (int(quantidade) + 1)):
                rando = random.randint(1, (int(dado)))
                lista.append(rando)
            soma = sum(lista)

            if quantidade == 1:
                concordancia += "dado"
            else:
                concordancia += "dados"

            if add == 0:
                addup += f"{lista}"
                addupsum += f"{soma}"
            elif add < 0:
                addup += f"{lista} - {abs(add)}"
                addupsum += f"{soma + add}"
            else:
                addup += f"{lista} + {add}"
                addupsum += f"{soma + add}"

            await ctx.send(f":game_die: | Você rodou {quantidade} {concordancia} "
                           f"de {dado} lados e conseguiu: **{soma}**!\n"
                           f":face_with_monocle: | `{addupsum}` >> {addup}")

    @commands.command(name="rand", aliases=["random", "aleatorio"], description="Gera um número totalmente E DEFINITIVAMENTE aleatório para você.\n"
                                                                                "Não é como se máquinas não fossem capazes de serem aleatórias... né?\n\n"
                                                                                "Nomes alternativos:\n"
                                                                                "`random, aleatorio`")
    async def numeroaleatorio(self, ctx, num1=20):
        aleatorio = random.randint(0, int(num1))
        await ctx.send(f"Seu número aleatório é: **{aleatorio}**")

    @commands.command(name="escolha", aliases=["escolher"], description="Faça eu escolher entre dois ou mais tópicos.\n"
                                                                        "Um comando ideal caso você seja um cara extremamente indeciso.\n\n"
                                                                        "Nome alternativo:\n"
                                                                        "`escolher`")
    async def unidunite(self, ctx, *, mensagem):
        msgm = mensagem.split(" ")
        if len(msgm) == 1:
            await ctx.send("**Preciso de pelo menos 2 itens para escolher!**")
        else:
            randoll = random.choice(msgm)
            await ctx.send(f"Eu escolho: **{randoll}**")

    @commands.command(name="fala", aliases=["falar"], description="Gera uma mensagem em webhook que simula a "
                                                                  "pessoa que mencionasse falando tal coisa.\n"
                                                                  "Perfeito para zoar com seus amigos e/ou membros do server.\n\n"
                                                                  "Nome alternativo:"
                                                                  "`falar`")
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def mandar_messagem(self, ctx, membro: nextcord.Member = None, *, mensagem=None):
        if membro is None:
            await ctx.send(f'**Tem que marcar um membro para isso funcionar, comédia!**')
        elif mensagem is None:
            await ctx.send(f'**Insira uma mensagem aqui, comédia...**')
        else:
            await ctx.message.delete()
            webhook = await ctx.channel.create_webhook(name=membro.display_name)
            await webhook.send(str(mensagem), username=membro.display_name, avatar_url=membro.display_avatar)

    @commands.command(name="diga", aliases=["dizer"], description="Um comando para fazer eu falar qualquer coisa... Qualquer coisa mesmo...\n"
                                                                  """Até "eu gosto do pica" ou algo do tipo.\n\n"""
                                                                  "Nome alternativo:\n"
                                                                  "`dizer`")
    async def fala_alguma_coisa(self, ctx, *, mensagem):
        await ctx.message.delete()
        await ctx.send(mensagem)

    @commands.command(name="8ball", aliases=["eightball", "8b"], description="Aqui pode me perguntar sobre literalmente qualquer coisa e a vossa senhoria, "
                                                                             "com que vos fala, irá responder usando minha sabedoria praticamente ilimitada.\n\n"
                                                                             "Nomes alternativos:\n"
                                                                             "`eightball, 8b`\n"
                                                                             "Ps: Esse comando funciona melhor em perguntas de sim ou não, "
                                                                             "mas quem sou eu para estragar sua diversão?")
    async def oitobola(self, ctx, *, mensagem):
        if mensagem.endswith("?"):
            pctg = random.choice(range(0, 101))
            lst_rspts = ["Sim!", "Não!", "Talvez...", "Não Sei.", "Sei lá...", "Não entendi :face_with_raised_eyebrow:",
                         f"Existe uma possibilidade de {pctg}% de que isto seja verdade...",
                         f"Existe uma possibilidade de {pctg}% de que isto seja mentira...",
                         "Poderia repetir, por favor?", "Estou meio confuso...", "Faça uma pergunta mais coerente!",
                         "Amogus!", "Meio sus isso aí...", "Confia.", "Achei verídico!", "Me parece falso...",
                         "Não faça essas perguntas insolentes denovo! :face_with_symbols_over_mouth:",
                         "Meu cachorro diz que sim!", "Meu cachorro diz que não!", "Nada a declarar!",
                         "Pergunta lá no Posto Ipiranga!", "A mimir... :sleeping:", "Foda-se!",
                         "Eu não sei e nem quero saber!", "Tô nem aí...", "Tô pouco me fudendo, honestamente...",
                         "Só se for o cu da tua mãe!", "Que porra de pergunta é essa?", "42, eu acho.", "haha sex funny.",
                         "kkkkkkkkkkkkkkkkkkkkkkkkkkk", "Acho que você está fora de si.", "Quem? Te perguntou...",
                         "Não foi isso que sua mãe disse pra mim quando eu tava com ela na cama ontem",
                         """⠀⠀⠀⠀- ⣠⠤⠖⠚⠛⠉⠛⠒⠒⠦⢤
⠀⠀⠀⠀⣠⠞⠁⠀⠀⠠⠒⠂⠀⠀⠀⠀⠀⠉⠳⡄
⠀⠀⠀⢸⠇⠀⠀⠀⢀⡄⠤⢤⣤⣤⡀⢀⣀⣀⣀⣹⡄
⠀⠀⠀⠘⢧⠀⠀⠀⠀⣙⣒⠚⠛⠋⠁⡈⠓⠴⢿⡿⠁
⠀⠀⠀⠀⠀⠙⠒⠤⢀⠛⠻⠿⠿⣖⣒⣁⠤⠒⠋
⠀⠀⠀⠀⠀⢀⣀⣀⠼⠀⠈⣻⠋⠉⠁
⠀⠀⠀⡴⠚⠉⠀⠀⠀⠀⠀⠈⠀⠐⢦
⠀⠀⣸⠃⠀⡴⠋⠉⠀⢄⣀⠤⢴⠄⠀⡇
⠀⢀⡏⠀⠀⠹⠶⢀⡔⠉⠀⠀⣼⠀⠀⡇
⠀⣼⠁⠀⠙⠦⣄⡀⣀⡤⠶⣉⣁⣀⠘
⢀⡟⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⣽
⢸⠇⠀⠀⠀⢀⡤⠦⢤⡄⠀⠀⡟
⢸⠀⠀⠀⠀⡾⠀⠀⠀⡿⠀⠀⣇⣀⣀
⢸⠀⠀⠈⠉⠓⢦⡀⢰⣇⡀⠀⠉⠀⠀⣉⠇
⠈⠓⠒⠒⠀⠐⠚⠃⠀⠈⠉⠉⠉⠉⠉⠁""",
                         """⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠋⠈⠀⠀⠀⠀⠐⠺⣖⢄⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⢀⡆⠀⠀⠀⢋⣭⣽⡚⢮⣲⠆⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⡼⠀⠀⠀⠀⠈⠻⣅⣨⠇⠈⠀⠰⣀⣀⣀⡀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⢷⣶⠶⣃⢀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⠈⠓⠚⢸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢀⡠⠀⡄⣀⠀⠀⠀⢻⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠐⠉⠀⠀⠙⠉⠀⠠⡶⣸⠁⠀⣠⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣦⡆⠀⠐⠒⠢⢤⣀⡰⠁⠇⠈⠘⢶⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠠⣄⣉⣙⡉⠓⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⣀⠀⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"""]
            respostas = random.choice(lst_rspts)
            resposta = nextcord.Embed(title="Oito bola :8ball:", color=0xff5b80,
                                      description=f"{ctx.message.author.mention} perguntou:\n")
            resposta.add_field(name="Questão", value=f"{mensagem}", inline=False)
            resposta.add_field(name="Resposta", value=f"{respostas}", inline=False)
            await ctx.send(embed=resposta)
        else:
            await ctx.send("**Perguntas terminam com ponto de interrogação.**")

    @commands.command(name="8ballimg", aliases=["eightballimg", "8bi"], description="Combine minha sabedoria ilimitada com meu senso de "
                                                                                    "humor merda e aqui está o comando de 8ball por imagem.\n"
                                                                                    f"Funciona da mesma maneira que o 8ball, "
                                                                                    "só que dessa vez, eu uso memes para lhe responder.\n\n"
                                                                                    "Nomes alternativos:\n"
                                                                                    "`eightballimg, 8bi`")
    async def oitobolaimagem(self, ctx, *, mensagem):
        if mensagem.endswith("?"):
            with open('nothing_else.json', 'r') as file:
                all_links = json.load(file)
            lista_imagem = all_links["lista_imagem"]
            respostas = random.choice(lista_imagem)
            resposta = nextcord.Embed(title="Oito bola :8ball:", color=0xff5b80,
                                      description=f"{ctx.message.author.mention} perguntou:\n"
                                                  f"**Questão**\n"
                                                  f"{mensagem}\n"
                                                  f"**Resposta**")
            resposta.set_image(url=f"{respostas}")
            await ctx.send(embed=resposta)
        else:
            await ctx.send("**Perguntas terminam com ponto de interrogação.**")

    @commands.command(name="anagrama", description="Gera um anagrama aleatório e customizado para você. \n"
                                                   "Se você gosta de brincar com as palavras, esse comando é perfeito para ti.")
    async def anaguramu(self, ctx, *, mensagem: str = None):
        if mensagem is None:
            await ctx.send("**Qual palavra deseja fazer um anagrama?**")
        else:
            anagrama = string_utils.shuffle(mensagem)
            await ctx.send(f"O anagrama escolhido de {mensagem} foi: **{anagrama}**.\n"
                           f"Existem mais `{(math.factorial(len(list(anagrama))) - 1)}`"
                           f" possiveis anagramas para essa palavra!")

    @commands.command(name="monke", description="Gera uma gif de macaco para você.\n"
                                                "Ótimo pra descrever certas pessoas...")
    async def saru(self, ctx):
        with open("nothing_else.json", "r") as data:
            all_links = json.load(data)
        monkey = all_links["monkey"]
        macaco = random.choice(monkey)
        acao = nextcord.Embed(title="Aqui está a sua gif de macaco, senhor... :monkey: ", color=0xe63946)
        acao.set_image(url=f"{macaco}")
        acao.set_footer(text=f"Solicitado pelo mamaco {ctx.author}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.send(embed=acao)

    @commands.command(name="fumo", description="Gera uma gif de fumo(Bonecas de pelúcia chibi, geralmente de Touhou) pra você...\n"
                                               "É, só isso mesmo...")
    async def fumo_plush(self, ctx):
        with open("nothing_else.json", "r") as data:
            all_links = json.load(data)
        fumo = all_links["fumo"]
        plushie = random.choice(fumo)
        acao = nextcord.Embed(title="Aqui está a sua gif de fumo, senhor... :face_with_monocle: ", color=0xe63946)
        acao.set_image(url=f"{plushie}")
        acao.set_footer(text=f"Solicitado pelo weeb {ctx.author}",
                        icon_url=f"{ctx.author.display_avatar}")
        await ctx.send(embed=acao)

    @commands.command(name="por100", description="Comando pra dizer o quão seu amigo ou quem mencionasse é tal coisa em porcentagem.\n"
                                                 f"Formato:\n"
                                                 f"```por100[usuário][tal coisa]```")
    async def porcentagemlol(self, ctx, membro: nextcord.Member, *, mensagem):
        randomizado = random.randint(0, 100)
        value = ""
        check_member = ""
        if membro == ctx.author:
            value += "Você mesmo, lol"
            check_member += "Você"
        else:
            value += f"{ctx.author.mention}"
            check_member += f"{membro.mention}"
        por100 = nextcord.Embed(title="Resultado!", color=0x9163b1,
                                description=f"{check_member} é **{randomizado}%** {mensagem}!!")
        por100.add_field(name="Solicitado por:", value=value)
        por100.set_thumbnail(url=f"{membro.display_avatar}")
        por100.set_footer(text="Confia no pai!", icon_url=f"{self.bot.user.display_avatar}")
        await ctx.send(embed=por100)

    @commands.command(name="vibe", description="Você gosta daqueles textos de synthwave/vaporwave escrito d  e  s  s  e    j  e  i  t  o?\n"
                                               "Aqui está o comando pra gerar automaticamente pra você.")
    async def synthwave(self, ctx, *, mensagem):
        alphabet_distance = ord('Ａ') - ord('A')
        new_text = ''
        for char in mensagem:
            pos_norm_char = ord(char)
            if ord('!') <= pos_norm_char <= ord('~'):
                char = chr(pos_norm_char + alphabet_distance)
            new_text += char
        await ctx.send(new_text)

    @commands.command(name="piadazap", aliases=["piadadozap"], description="Você está procurando uma piada merda pra você mandar no grupo da família?\n"
                                                                           "Aqui está o comando ideal pra você!\n\n"
                                                                           "Nome alternativo:\n"
                                                                           "`piadadozap`\n"
                                                                           "PS: As piadas em suma maioria são tão ruins que os próprios autores nem tem conhecimento algum de gramática. "
                                                                           "As exposições à altos niveis de vergonha alheia não são responsabilidade minha e nem do criador.")
    async def mandar_piada_ruim(self, ctx):
        def piadas_do_zap():
            resultado = []
            index = random.randint(1, 100)
            lol = requests.get(f"https://www.piadas.com.br/piadas/curtas?page={index}")
            sus = Bs(lol.content, "html.parser")
            sus1 = sus.find("div").find("div").find("div").find("div", id="main-wrapper")
            sus2 = sus1.find("div").find("div").find_all("div")
            sus3 = sus2[5].find("main")
            sus4 = sus3.find_all("div")[2].find("div").find("div").find("div").find("div").find_all("div")
            for item in sus4:
                if str(item).startswith("""<div class="text-content field field--name-body 
                field--type-text-with-summary field--label-hidden field__item"""):
                    amogus = str(item).replace("""<div class="text-content field field--name-body 
                    field--type-text-with-summary field--label-hidden field__item">""", "")
                    amogus1 = amogus.replace("<p>", "").replace("</p>", "").replace("<br/>", "\n").replace("</div>", "")
                    resultado.append(amogus1)
            print(len(resultado))
            return random.choice(resultado)

        zapzap = nextcord.Embed(title="Se liga só nessa piada muito engraçada :rofl: :rofl: "
                                      ":rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: "
                                      ":rofl: :rofl: :ok_hand:", color=Color.random(),
                                description=f"{piadas_do_zap()}")
        zapzap.set_image(url="https://c.tenor.com/xEaOQBLkl2cAAAAd/atumalaca-risada.gif")
        zapzap.set_thumbnail(url="https://cdn3.emoji.gg/emojis/9223-kekexplode.gif")
        zapzap.set_footer(text="Essa é pra mandar no zipzop!", icon_url="https://cdn3.emoji.gg/emojis/1579-laughing-off.png")
        await ctx.send(embed=zapzap)

    @commands.command(name="copypasta", description="Você gostaria de ter um comando onde gere copypastas "
                                                    "automáticas porque você é preguiçoso demais para "
                                                    "pesquisar as copypastas por si só?\n"
                                                    "Então esse é o comando perfeito para você!")
    async def mandar_copypasta(self, ctx):
        with open("nothing_else.json", "r") as data:
            all_links = json.load(data)
        random_post = []
        red = asyncpraw.Reddit(client_id=all_links["client_id"], client_secret=all_links["client_secret"], user_agent=all_links["user_agent"])
        subred = await red.subreddit("copypastabr")
        quente = subred.top(limit=600)
        posts = [post async for post in quente]
        for i in range(0, len(posts)):
            if len(posts[i].selftext) <= 2000:
                random_post.append({posts[i].title: posts[i].selftext.replace("&#x200B;", "")})
        post1 = random.choice(random_post)
        titulo = list(post1.keys())[0]
        copypasta = post1[list(post1.keys())[0]]
        if titulo in copypasta:
            coppy = nextcord.Embed(title=f"Saindo uma copypasta direto do forno hmmm...", color=nextcord.Color.random(),
                                   description=f"{copypasta}")
            coppy.set_thumbnail(url="https://i.kym-cdn.com/photos/images/original/000/005/713/copypasta.jpg")
            coppy.set_footer(text=f"Solicitado por {ctx.author}", icon_url=f"{ctx.author.display_avatar}")
            await ctx.send(embed=coppy)
        else:
            coppy = nextcord.Embed(title=f"Saindo uma copypasta direto do forno hmmm...", color=nextcord.Color.random(),
                                   description=f"**{titulo}**\n\n"
                                               f"{copypasta}")
            coppy.set_thumbnail(url="https://i.kym-cdn.com/photos/images/original/000/005/713/copypasta.jpg")
            coppy.set_footer(text=f"Solicitado por {ctx.author}", icon_url=f"{ctx.author.display_avatar}")
            await ctx.send(embed=coppy)

    @commands.command(name="pica", aliases=["penis", "pau", "rola"], description="Um homem de verdade sabe apreciar a "
                                                                                 "pica um do outro e esse comando é justamente para isso.\n"
                                                                                 "Veja o quão grande é seu pau ou do seu amigo.\n"
                                                                                 "||E totalmente não irei fazer um comentário homoerótico sobre seu pau...||\n\n"
                                                                                 "Nomes alternativos:\n"
                                                                                 "`penis, pau, rola`")
    async def medir_penis(self, ctx, member: typing.Optional[str]):
        rdm = random.randint(0, 25)
        mensagem = ["Caralho, o cara não tem pinto kkkkkkkkkkkk",
                    "Pequinininho...Serve só pra mijar mesmo...",
                    "Não é grande mas dá pra aproveitar...",
                    "Belo pênis, amigo...",
                    "Oloko, dá pra catar manga com a tua pica...",
                    "Taporra, vai achar petróleo com isso aí?"]

        def mens(valor):
            return mensagem[valor // 5]

        member_type = ""
        if member is None:
            member_type += f"{ctx.author.display_name}"
        else:
            membro = member.replace("<@", "").replace(">", "")
            user = await ctx.guild.fetch_member(int(membro))
            member_type += f"{user.display_name}"
        pica = nextcord.Embed(title=f"Vamos ver o tamanho do pênis do {ctx.author.display_name}...", color=0x6305f4,
                              description=f"8{'=' * rdm}D\n")
        pica.set_footer(text=f"{mens(rdm)}")
        await ctx.send(embed=pica)


def setup(bot):
    bot.add_cog(Fun(bot))
