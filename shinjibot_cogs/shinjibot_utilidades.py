import asyncpraw
import nextcord
import random
import re
import urllib
from urllib import parse, request
import translate
import typing
import spotipy
from shinjibot import links
from bs4 import BeautifulSoup as Bs
from spotipy.oauth2 import SpotifyClientCredentials
from translate import Translator
from datetime import datetime, timedelta
from nextcord.ext import commands
from nextcord import Spotify as Listening
from nextcord import Color
from ibge.localidades import *


class Utilidade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = nextcord.Intents.all()
    shinji = commands.Bot(intents=intents)

    @commands.command(name="prefixo", aliases=["setprefix", "mudarprefixo", "setp"])
    @commands.has_permissions(manage_guild=True)
    async def mudar_prefixo_lol(self, ctx, prefix=None):
        if prefix is None:
            pass
        else:
            with open('prefixos.json', 'r') as sus:
                prefixos = json.load(sus)
            prefixos[str(ctx.guild.id)] = prefix
            with open('prefixos.json', 'w') as sus:
                json.dump(prefixos, sus, indent=4)
            await ctx.send(f"Prefixo alterado para `{prefix}` com sucesso!")

    @commands.command()
    async def avatar(self, ctx, member: typing.Optional[str]):
        member_info, member_image = "", ""
        if member is None:
            member_info += f"{ctx.author}"
            member_image += f"{ctx.author.display_avatar}"
        else:
            membro = member.replace("<@", "")
            user = await ctx.guild.fetch_member(int(membro.replace(">", "")))
            member_info += f"{user}"
            member_image += f"{user.display_avatar}"
        ava = nextcord.Embed(title=f"Avatar: {member_info}", color=0xb7b6f9,
                             description=f"Solicitado por {ctx.author.mention}")
        ava.set_image(url=f"{member_image}")

    @commands.command(name="userinfo", aliases=["infouser", "uinfo"])
    async def infousuario(self, ctx, member: nextcord.Member = None):
        membro = ""
        if member is None:
            membro += f"{ctx.author}"
            member = ctx.author
        else:
            membro += f"{await ctx.guild.fetch_member(int(member.id))}"
        user = ctx.author
        cria = member.created_at
        junta = member.joined_at
        criado = cria - timedelta(hours=3)
        juntou = junta - timedelta(hours=3)
        infouser = nextcord.Embed(title=f"Informações do {membro}", color=0xcaeff4)
        infouser.add_field(name=":id: | **ID:**", value=f"{member.id}", inline=False)
        infouser.add_field(name=":restroom: | **Apelido:**", value=f"{member.display_name}", inline=False)
        infouser.add_field(name=":house: | **Server onde se reside:**", value=f"{member.guild}", inline=False)
        infouser.add_field(name=":sleeping: | **Status:**", value=f"{str(member.status).capitalize()}", inline=False)
        msg, msg1, msg2 = "", "", ""
        if member.bot is True:
            msg += "Sim"
        else:
            msg += "Não"
        infouser.add_field(name=":robot: | **É bot?**", value=msg, inline=False)
        if member.guild_permissions.administrator is True:
            msg1 += "Sim"
        else:
            msg1 += "Não"
        infouser.add_field(name=":detective: | **É admin?**", value=msg1, inline=False)
        if member.is_on_mobile() is True:
            msg2 += "Sim"
        else:
            msg2 += "Não"
        infouser.add_field(name=":mobile_phone: | **É usuário mobile?**", value=msg2, inline=False)
        infouser.add_field(name=":man: | **Data de criação da conta:**",
                           value=f"{criado.strftime('%d/%m/%y %H:%M:%S')}", inline=False)
        infouser.add_field(name=":computer: | **Juntou-se ao server:**",
                           value=f"{juntou.strftime('%d/%m/%y %H:%M:%S')}", inline=False)
        roles = []
        for i in member.roles:
            if i.name != "@everyone":
                roles.append(i.mention)
        infouser.add_field(name="<a:verificado:1025410680553209977> | **Cargos**", value=", ".join(roles), inline=False)
        infouser.set_thumbnail(url=f"{member.display_avatar}")
        infouser.set_footer(text=f"Solicitado por {user}")
        await ctx.send(embed=infouser)

    @commands.command(name="pesquisar", aliases=["pesquisa", "search"])
    async def searche(self, ctx, *, mensagem):
        membro = ctx.message.author
        url = "https://www.google.com.br/search?q="
        msgm = mensagem.split(' ')
        msg = "+".join(msgm)
        google = url + msg
        search = nextcord.Embed(title="Pesquisa Google")
        search.add_field(name="Pesquisa:", value=f"{mensagem}\n")
        search.add_field(name="Link:", value=f"{google}")
        search.set_thumbnail(url=f"{membro.display_avatar}")
        search.set_footer(text=f"Solicitado por {membro}")
        await ctx.send(embed=search)

    @commands.command(name="reddit")
    async def pegar_post_do_reddit(self, ctx, sub: typing.Optional[str] = "comedynecrophilia",
                                   sort: typing.Optional[str] = "hot"):
        red = asyncpraw.Reddit(client_id=links("client_id"), client_secret=links("client_secret"), user_agent=links("user_agent"))
        random_post = []
        subs = []
        result = None
        time_filter = ""
        formats = ("jpg", "png", "jpeg", "gif", "gifv")
        async for sb in red.subreddits.search_by_name(sub):
            subs.append(sb)
        subred = await red.subreddit(sub, fetch=True)
        if sub in subs:
            if subred.over18 is False:
                if sort == "hot":
                    result = subred.hot(limit=100)
                elif sort.startswith("top"):
                    result = subred.top(limit=100, time_filter=random.choice(["all", "year", "month"]))
                elif sort == "new":
                    result = subred.new(limit=100)
                posts = [post async for post in result]
                for i in range(0, len(posts)):
                    random_post.append(posts[i])
                post_sub = random.choice(random_post)
                if post_sub.url.startswith("https://www.reddit.com/gallery") is False:
                    if post_sub.url.endswith(formats):
                        reddit9 = nextcord.Embed(title=f"Aqui está o resultado da "
                                                       f"imagem do sub `r/{sub}`", color=0xff8700,
                                                 description="Informações do post:\n")
                        reddit9.add_field(name="Nome do Autor:", value=f"{post_sub.author}", inline=False)
                        reddit9.add_field(name="Título do Post:", value=f"{post_sub.title}", inline=False)
                        reddit9.add_field(name="Karma:", value=f"{post_sub.score} upvotes", inline=False)
                        reddit9.set_image(url=f"{post_sub.url}")
                        reddit9.set_footer(text=f"Solicitado por {ctx.author}",
                                           icon_url=f"{ctx.author.display_avatar}")
                        await ctx.send(embed=reddit9)
                    else:
                        await ctx.send(f"Aqui está o resultado do post do sub `r/{sub}`:\n\n"
                                       f"**Nome do Autor:** {post_sub.author}\n"
                                       f"**Título do Post:** {post_sub.title}\n"
                                       f"**Karma:** {post_sub.score} upvotes\n"
                                       f"**Post:**\n"
                                       f"{post_sub.url}")
                await red.close()
            else:
                if ctx.channel.name.lower() not in ["nsfw", "hentai", "porn"] or ctx.channel.is_nsfw():
                    pare = nextcord.Embed(title="Um momento amigo...", color=0xff0000,
                                          description="Apesar desse comando permitir mostrar posts "
                                                      "de subreddits NSFW, esses "
                                                      "posts devem ficar em canais destinados ao "
                                                      "envio de conteúdo adulto...\n\n"
                                                      "Mas aqui está uma imagem de sapos fofinhos: ")
                    pare.set_image(url="https://i.imgur.com/A7a25VD.jpg")
                    await ctx.send(embed=pare)
                else:
                    if sort == "hot":
                        result = subred.hot(limit=100)
                    elif sort.startswith("top"):
                        result = subred.top(limit=100, time_filter=random.choice(["all", "year", "month"]))
                    elif sort == "new":
                        result = subred.new(limit=100)
                    posts = [post async for post in result]
                    for i in range(0, len(posts)):
                        random_post.append(posts[i])
                    post_sub = random.choice(random_post)
                    if post_sub.url.startswith(("https://www.reddit.com/gallery", "https://redgifs.com/")) is False:
                        if post_sub.url.endswith(formats):
                            reddit9 = nextcord.Embed(title=f"Aqui está o resultado da "
                                                           f"imagem do sub `r/{sub}`", color=0xff8700,
                                                     description="Informações do post:\n\n"
                                                                 f"**Nome do Autor:** {post_sub.author}\n"
                                                                 f"**Título do Post:** {post_sub.title}\n"
                                                                 f"**Karma:** {post_sub.score} upvotes")
                            reddit9.set_image(url=f"{post_sub.url}")
                            reddit9.set_footer(text=f"Solicitado por {ctx.author}",
                                               icon_url=f"{ctx.author.display_avatar}")
                            await ctx.send(embed=reddit9)
                        else:
                            await ctx.send(f"Aqui está o resultado do post do sub `r/{sub}`:\n\n"
                                           f"**Nome do Autor:** {post_sub.author}\n"
                                           f"**Título do Post:** {post_sub.title}\n"
                                           f"**Karma:** {post_sub.score} upvotes\n"
                                           f"**Post:**\n"
                                           f"{post_sub.url}")
                    await red.close()
        else:
            await ctx.send("**Opa... parece que algo deu errado, não foi?**\n\n"
                           "A provável razão de não ter mostrado o resultado "
                           "foi porque o resultado da sua pesquisa não existe!\n"
                           "Tenha certeza que colocou o nome do subreddit "
                           "certinho (sem o r/) e tente novamente!\n\n"
                           "Se não souber como procurar por resultados no reddit, use "
                           "`https://www.reddit.com/[o sub que quer pegar]/search/?"
                           "q=[o que quer pesquisar]`.\n"
                           "Como por exemplo: https://www.reddit.com/r/memes/search/"
                           "?q=sussy%20baka&restrict_sr=1&sr_nsfw= (%20 é o indicador de espaço)")

    @commands.command(name="spotify")
    async def mostrar_musica(self, ctx, membro: typing.Optional[str]):
        with open('nothing_else.json', 'r') as file:
            all_links = json.load(file)
        cid = all_links["cid"]
        secret = all_links["secret"]
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        if membro is None:
            membro = ctx.author
        else:
            user = membro.replace("<@", "")
            membro = await ctx.guild.fetch_member(int(user.replace(">", "")))
        for act in membro.activities:
            if isinstance(act, Listening):
                musica = act.track_url
                track = sp.audio_features(musica)[0]
                keys = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
                scale = ["Menor", "Maior"]
                seconds = round(track['duration_ms'] / 1000)
                if seconds >= 60:
                    minutes = seconds // 60
                    rest = round(seconds) - 60 * minutes
                    if rest < 10:
                        time = f"{minutes}:0{rest}"
                    else:
                        time = f"{minutes}:{rest}"
                else:
                    if seconds < 10:
                        time = f"0:0{seconds}"
                    else:
                        time = f"0:{seconds}"
                bpm = round(track['tempo'])
                if bpm == 0:
                    tempo = "Desconhecido"
                else:
                    tempo = round(track['tempo'])
                spot = nextcord.Embed(title=f"Vamos ver o que {membro.name} está ouvindo...", color=0x60f267)
                spot.add_field(name="Nome do Artista:", value=act.artist, inline=False)
                spot.add_field(name="Nome da música:", value=act.title, inline=False)
                spot.add_field(name="Tonalidade:", value=f"{keys[track['key']]} {scale[track['mode']]}", inline=False)
                spot.add_field(name="BPM:", value=f"{tempo}", inline=False)
                spot.add_field(name="Duração:", value=time, inline=False)
                spot.add_field(name="Album:", value=act.album, inline=False)
                spot.add_field(name="Link da música:", value=act.track_url, inline=False)
                spot.add_field(name="Album cover: ", value=f"[Download]({act.album_cover_url})")
                spot.set_image(url=f"{act.album_cover_url}")
                spot.set_footer(text=f"Solicitado por {ctx.author}", icon_url=f"{ctx.message.author.display_avatar}")
                await ctx.send(embed=spot)

    @commands.command(aliases=["youtube", "yt"])
    async def youtoba(self, ctx, *, search):
        olhando_pesquisa = urllib.parse.urlencode({"search_query": search})
        conteudo_htm = urllib.request.urlopen("https://www.youtube.com/results?" + olhando_pesquisa)
        conteudo_resultado = conteudo_htm.read().decode()
        resultado = re.findall(r'/watch\?v=(\S{11})', conteudo_resultado)
        await ctx.send("https://www.youtube.com/watch?v=" + resultado[0])

    @commands.command(name="clima")
    async def weather(self, ctx, *, cidade=None):
        if cidade is None:
            await ctx.send("**Insira um local para que eu possa trabalhar corretamente!**")
        else:
            api = "24a0e1a3f71f5db0e5cb6369c4da2d67"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            nome_cidade = cidade
            url_completo = base_url + "appid=" + api + "&q=" + nome_cidade
            lol = requests.get(url_completo)
            result = lol.json()
            channel = ctx.message.channel
            if result["cod"] != "404":
                pais = result['sys']['country']
                main = result['weather'][0]['main']
                descricao = result['weather'][0]['description']
                vento = result['wind']['speed']
                umidade = result['main']['humidity']
                pressao = result['main']['pressure']
                temperatura_celsius = round(result['main']['temp'] - 273.15, 1)
                sensacao = round(result['main']['feels_like'] - 273.15, 1)
                trans = translate.Translator("pt-br")
                traduzir = Translator.translate(trans, descricao)
                clim = nextcord.Embed(title=f"Clima de {nome_cidade}, {pais}", color=0xf66734,
                                      timestamp=datetime.now())
                clim.add_field(name="Clima", value=f"**{traduzir}**", inline=False)
                clim.add_field(name="Temperatura", value=f"**{temperatura_celsius}°C**", inline=False)
                clim.add_field(name="Sensação", value=f"**{sensacao}°C**", inline=False)
                clim.add_field(name="Umidade", value=f"**{umidade}%**", inline=False)
                clim.add_field(name="Vento", value=f"**{round(vento * 1.6, 2)} km/h**", inline=False)
                clim.add_field(name="Pressão atmosférica", value=f"**{pressao} hPa**", inline=False)
                clim.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                clim.set_footer(text=f"Solicitado por {ctx.message.author}")
                await channel.send(embed=clim)
            else:
                await channel.send("**Cidade não encontrada!**\n"
                                   "**Por favor tente novamente!**")

    @commands.command(aliases=["cidade", "infocidade"])
    async def mostrar_informations_da_cidade(self, ctx, *, city: typing.Optional[str]):
        data = Municipios()
        if city is None:
            await ctx.send("**Informe o nome da cidade que deseja trabalhar!!**")
        elif city.lower() not in [str(data.getNome()[i]).lower() for i in range(data.count())]:
            await ctx.send("**Não existe uma cidade no Brasil com esse nome!!\n"
                           "Tente novamente...**")
        else:
            cidade2 = city.lower()
            cidade3 = cidade2.split(" ")
            cidade4 = " ".join(cidade3)
            cidade1 = "-".join(cidade3)
            state = Municipio(cidade4)
            estado = state.getUF()
            page = requests.get(f"https://www.ibge.gov.br/cidades-e-estados/{str(estado).lower()}/{cidade1}.html")
            soup = Bs(page.content, 'html.parser')
            s = soup.find('div', id="responseMunicipios", class_="quick-facts-resultados pure-u-1")
            lines = s.find_all('p')
            informations = []
            for line in lines:
                informations.append(str(line.text))
            p = informations[3].split(" ")
            p1 = []
            for i in range(0, (len(p) - 1)):
                p2 = p[i].capitalize()
                p1.append(p2)
            p3 = p[len(p) - 1].replace("\xa0\xa0\xa0[2021]", "")
            p4 = p3.capitalize()
            p1.append(p4)
            prefeito = " ".join(p1)
            grana = ''.join([informations[23][i] for i in range(len(informations[23]) - 9)
                             if informations[23].endswith("\xa0\xa0\xa0[2019]")])
            cidade4 = [cidade3[i].title() for i in range(0, len(cidade3)) if
                       cidade3[i] not in ["e", "de", "do", "das", "dos"]]
            cidade = " ".join(cidade4)
            info = nextcord.Embed(title=f"Informações da cidade de {cidade}, {estado.upper()}", color=0x60e183,
                                  description="Apenas cidades localizadas no Brasil!\n")
            info.add_field(name="Nome da Cidade:", value=cidade, inline=False)
            info.add_field(name="Nome do Estado:", value=state.getDescricaoUF(), inline=False)
            info.add_field(name="Área Territorial:",
                           value=informations[7].replace("\xa0\xa0\xa0[2021]", ""), inline=False)
            info.add_field(name="População:", value=informations[9].replace("\xa0\xa0\xa0[2021]", ""), inline=False)
            info.add_field(name="Densidade Demográfica:",
                           value=informations[11].replace("\xa0\xa0\xa0[2010]", ""), inline=False)
            info.add_field(name="IDHM(Índice de Desenvolvimento Humano Municipal):",
                           value=informations[15].replace("\xa0\xa0\xa0[2010]", ""), inline=False)
            info.add_field(name="PIB Per Capita", value=grana, inline=False)
            info.add_field(name="Prefeito", value=prefeito.replace("De", "de"), inline=False)
            info.set_thumbnail(url="https://logodownload.org/wp-content/uploads/2018/02/ibge-logo-1.png")
            info.set_footer(text=f"Solicitado por {ctx.author}",
                            icon_url=f"{ctx.author.display_avatar}")
            await ctx.send(embed=info)

    @commands.command(name="addemoji")
    async def addemojilol(self, ctx, name, url):
        try:
            response = requests.get(url)
            if url.endswith((".gif", ".png", ".jpg", ".jpeg")):
                emoji = await ctx.guild.create_custom_emoji(name=name, image=response.content)
                if emoji.animated:
                    await ctx.send(f"**Emoji `:{emoji.name}:` adicionado com sucesso!** <a:{emoji.name}:{emoji.id}>")
                else:
                    await ctx.send(f"**Emoji `:{emoji.name}:` adicionado com sucesso!** <:{emoji.name}:{emoji.id}>")
            else:
                await ctx.send("Invalid image type. Only PNG, JPEG and GIF are supported.")
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema,
                requests.exceptions.ConnectionError, nextcord.errors.HTTPException):
            await ctx.send("**URL ou nome de emoji inválido!**\n"
                           "Verifique a URL da imagem que você mandou, veja se possuí "
                           "algum erro e tente novamente.\n"
                           "Também verifique o nome do emoji que escolheu, "
                           "já que ele só suporta caracteres ASCII.")

    @commands.command(name="verid")
    async def seila(self, ctx):
        for item in ctx.guild.emojis:
            await ctx.send(f"\\{item}")


def setup(bot):
    bot.add_cog(Utilidade(bot))
