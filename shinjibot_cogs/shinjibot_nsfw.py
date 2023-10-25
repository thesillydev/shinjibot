import json
import typing
import random
import nextcord
import asyncpraw
import requests
from bs4 import BeautifulSoup as Bs
from nextcord.ext import commands
from rule34Py import rule34Py
from shinjibot import links


def pornhub_link(query: str):
    url_extent = query.lower().replace(" ", "+")
    response = requests.get(f"https://pt.pornhub.com/video/search?search={url_extent}")
    if response.status_code == 404:
        return "Sem Resultados"
    else:
        page = Bs(response.content, 'html.parser')
        search_quantity = page.find("div", class_="showingCounter").text.lstrip().replace("Mostrar 1-32 de ", "")
        i = random.randint(1, int(search_quantity) // 32)
        real_response = requests.get(f"https://pt.pornhub.com/video/search?search={url_extent}&page={i}")
        real_page = Bs(real_response.content, 'html.parser')
        search = real_page.find("div", class_="sectionWrapper")
        search_results = search.find_all("li", class_="pcVideoListItem")
        links1, links2, links3 = [], [], []
        for item in search_results:
            links1.append(item.find_next('a'))
            links2.append(item.find_next('div', class_="usernameWrap").text.lstrip())
            links3.append(item.find_next("div", class_="videoDetailsBlock"))
        i = random.randint(0, (len(links1) - 1))
        info = {"Nome": links1[i].find("img").get("alt"),
                "Duração": links1[i].find("var", class_="duration").text,
                "Autor": links2[i].rstrip(),
                "Views": links3[i].find("span", class_="views").text.replace('Visualiz.', 'views').rstrip(),
                "Quando Foi Postado": links3[i].find("var", class_="added").text,
                "Link do Vídeo": f"https://pt.pornhub.com{links1[i].get('href')}",
                "Thumbnail": links1[i].find("img").get("src")}
        return info


class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = nextcord.Intents().all()
    shinji = commands.Bot(intents=intents)

    @commands.command(name="pornhub")
    async def pronhub(self, ctx, *, mensagem):
        if ctx.channel.name.lower() not in ["nsfw", "hentai", "porn"] and ctx.channel.is_nsfw() is False:
            pare = nextcord.Embed(title="Um momento amigo...", color=0xff0000,
                                  description="Esse é um comando NSFW e só deve ser usado em canais destinados "
                                              "ao envio de conteúdo adulto...\n\n"
                                              "Mas aqui está a foto do pinto duro que você pediu ontem no privado...\n"
                                              "||Você deveria foder humanos, não robôs... :flushed:||")
            pare.set_image(url="https://www.ahnegao.com.br/wp-content/uploads/2019/02/pinto.jpg")
            await ctx.send(embed=pare)
        else:
            resultado = pornhub_link(mensagem)
            if resultado == "Sem Resultados":
                await ctx.send("**Não existe resultados para a sua pesquisa! Tente novamente!")
            else:
                embed = nextcord.Embed(title=f"Aqui está o resultado de {mensagem.title()}!")
                for item in resultado.keys():
                    if item != "Thumbnail":
                        if item == "Link do Video":
                            embed.add_field(name=item, value=f"[Link do {resultado['Nome']}]({resultado['Link do Vídeo']})")
                        embed.add_field(name=item, value=resultado[item], inline=False)
                embed.set_image(url=resultado["Thumbnail"])
                await ctx.send(embed=embed)
                print("Enviado com sucesso")

    @commands.command(name="rule34")
    async def hihihi(self, ctx, *, mensagem):
        if ctx.channel.name.lower() not in ["nsfw", "hentai", "porn"] and ctx.channel.is_nsfw() is False:
            pare = nextcord.Embed(title="Um momento amigo...", color=0xff0000,
                                  description="Esse é um comando NSFW e só deve ser usado em canais destinados "
                                              "ao envio de conteúdo adulto...\n\n"
                                              "Mas aqui está a foto do pinto duro que você pediu ontem no privado...\n"
                                              "||Você deveria foder humanos, não robôs... :flushed:||")
            pare.set_image(url="https://www.ahnegao.com.br/wp-content/uploads/2019/02/pinto.jpg")
            await ctx.send(embed=pare)
        else:
            r34_py = rule34Py()
            msg = "_".join(mensagem)
            result_search = r34_py.search([msg.lower()], limit=1000)
            if not result_search:
                await ctx.send("**Opa... parece que algo deu errado, não foi?**\n\n"
                               "A provável razão de não ter mostrado o resultado "
                               "foi porque você não digitou a tag corretamente...\n"
                               "Na dúvida, vá no https://rule34.xxx e tente ver como está a tag "
                               "e escreva ela sem o uso do underline...")
            else:
                r34 = nextcord.Embed(title=f"Aqui está o resultado de: "
                                           f"{' '.join([mensagem[i].capitalize() for i in range(0, len(mensagem))])}",
                                     color=0x75ca5b, description="Aproveite a punheta...")
                r34.set_image(url=f"{result_search[random.randint(0, len(result_search))].image}")
                r34.set_footer(text=f"Solicitado pelo punheteiro assumido: {ctx.author}",
                               icon_url=f"{ctx.author.display_avatar}")
                await ctx.send(embed=r34)

    @commands.command(aliases=["redditr34", "redr34"])
    async def hihihired(self, ctx, *, pesquisa="sex"):
        red = asyncpraw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        random_post = []
        if ctx.channel.name not in ["nsfw", "hentai", "porn"] and ctx.channel.is_nsfw() is False:
            pare = nextcord.Embed(title="Um momento amigo...", color=0xff0000,
                                  description="Esse é um comando NSFW e só deve ser usado em canais destinados "
                                              "ao envio de conteúdo adulto...\n\n"
                                              "Mas aqui está a foto do pinto duro que você pediu ontem no privado...\n"
                                              "||Você deveria foder humanos, não robôs... :flushed:||")
            pare.set_image(url="https://www.ahnegao.com.br/wp-content/uploads/2019/02/pinto.jpg")
            await ctx.send(embed=pare)
        else:
            subred = await red.subreddit("rule34+hentai+thick_hentai+HENTAI_GIF+Yiff+westernhentai", fetch=True)
            posts = [post async for post in
                     subred.search(pesquisa)]
            for i in range(0, len(posts)):
                if posts[i].url.endswith(("jpg", "png", "jpeg", "gif")):
                    random_post.append(posts[i].url)
            if not random_post:
                await ctx.send("**Opa... parece que algo deu errado, não foi?**\n\n"
                               "A provável razão de não ter mostrado o resultado "
                               "foi porque o resultado da sua pesquisa não existe!\n"
                               "Esse comando pega os posts de 6 subreddits diferentes para "
                               "ter uma diversidade maior de conteúdo e às vezes, quando "
                               "pesquisa algo muito específico de um sub, pode acabar não aparecendo resultados...\n"
                               "Tente novamente ou deixe a sua pesquisa mais simplificada!\n\n"
                               "Se não souber como procurar por resultados no reddit, use "
                               "`https://www.reddit.com/[o sub que quer pegar]/search/?"
                               "q=[o que quer pesquisar]&restrict_sr=1&sr_nsfw=1`\n"
                               "Como por exemplo: https://www.reddit.com/r/rule34/"
                               "search/?q=big%20boobs&restrict_sr=1&sr_nsfw=1 (%20 é o indicador de espaço)\n\n"
                               "||Os subreddits são r/rule34, r/hentai, r/thick_hentai, "
                               "r/hentai_gif, r/yiff e r/westernhentai||")
            else:
                resultado = random_post[random.randint(0, len(random_post))]
                reddit18 = nextcord.Embed(title=f"Aqui está o resultado de: "
                                          f"{pesquisa.capitalize()}",
                                          color=0xff4300, description="Aproveite a punheta...")
                reddit18.set_image(url=f"{resultado}")
                reddit18.set_footer(text=f"Solicitado pelo punheteiro "
                                         f"assumido: {ctx.author}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.send(embed=reddit18)
                await red.close()

    @commands.command(aliases=["fuck", "foder", "fuder"])
    async def imoralidades(self, ctx, member: nextcord.Member, *, mensagem=" "):
        membro = member.mention
        user = ctx.message.author.mention
        duck = links("duck")
        se7 = random.choice(duck)
        if ctx.channel.name.lower() not in ["nsfw", "hentai", "porn"] or ctx.channel.is_nsfw():
            pare = nextcord.Embed(title="Um momento amigo...", color=0xff0000,
                                  description="Esse é um comando NSFW e só deve ser usado em canais destinados "
                                              "ao envio de conteúdo adulto...\n\n"
                                              "Mas aqui está a foto do pinto duro que você pediu ontem no privado...\n"
                                              "||Você deveria foder humanos, não robôs... :flushed:||")
            pare.set_image(url="https://www.ahnegao.com.br/wp-content/uploads/2019/02/pinto.jpg")
            await ctx.send(embed=pare)
        else:
            acao = nextcord.Embed(title="Eita que tesão danado...", color=0xe63946,
                                  description=f"{user} fodeu {membro}! :hot_face:\n"
                                              f"\n"
                                              f"{mensagem}")
            acao.set_image(url=f"{se7}")
            acao.set_footer(text="Ficar segurando vela pra vocês dois não dá pra mim...")
            await ctx.send(embed=acao)


def setup(bot):
    bot.add_cog(Nsfw(bot))
