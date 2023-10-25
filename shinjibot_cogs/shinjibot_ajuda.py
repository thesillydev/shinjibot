import datetime
import nextcord
import json
import pytz
from shinjibot import prefixo
from nextcord.ext import commands
from nextcord.ext import menus


class CustomButton(menus.ButtonMenuPages, inherit_buttons=False):
    def __init__(self, source, timeout=60):
        super().__init__(source, timeout=timeout)
        self.PREVIOUS_PAGE = "<a:previousbuttonk:1032700205109350531>"
        self.NEXT_PAGE = "<a:nextbuttonk:1032699954701025410>"
        self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE))
        self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE))
        self._disable_unavailable_buttons()


class AjudaFun(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=5)

    async def format_page(self, menu, entries):
        embed = nextcord.Embed(title="Aqui está todos os comandos divertidos(ou não) do bot.", color=0x07efeb,
                               description="Destinado a aquelas pessoas que gostam de "
                                           "zuar seus amigos ou membros do server.")
        for entry in entries:
            embed.add_field(name=f"{entry[0].capitalize()}", value=f"<:replyk:1034136527799861318>{entry[1]}",
                            inline=False)
        embed.set_footer(text=f'Página {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


class AjudaMod(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=5)

    async def format_page(self, menu, entries):
        embed = nextcord.Embed(title="Aqui está todos os comandos de administração do servidor.", color=0x07efeb,
                               description="Destinado aos moderadores e admins do servidor.")
        for entry in entries:
            embed.add_field(name=f"{entry[0].capitalize()}", value=f"<:replyk:1034136527799861318>{entry[1]}",
                            inline=False)
        embed.set_footer(text=f'Página {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


class AjudaUtils(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=4)

    async def format_page(self, menu, entries):
        embed = nextcord.Embed(title="Aqui está todos os comandos de utilidade do servidor.", color=0x07efeb,
                               description="Quer dizer, eu acho, né? Não sei...")
        for entry in entries:
            embed.add_field(name=f"{entry[0].capitalize()}", value=f"<:replyk:1034136527799861318>{entry[1]}",
                            inline=False)
        embed.set_footer(text=f'Página {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = nextcord.Intents.all()
    shinji = commands.Bot(intents=intents)

    @commands.group(name="ajuda", invoke_without_command=True)
    async def ajuda(self, ctx):
        user = ctx.author
        prefix = prefixo(ctx.guild.id)
        hm = nextcord.Embed(title=f"Me chamou, {user.display_name}?", color=0x4682b4,
                            description=f"Se está de olho nos meus commandos, use `{prefix}ajuda "
                                        f"[classe]` para saber como usar os comandos de cada classe!")
        hm.add_field(name="Ações", value="`abraço, beijo, chute, soco, tapa`", inline=False)
        hm.add_field(name="Bio", value="`addbio, amigo, bio, casamento, criarbio, divorciar, solteiro`")
        hm.add_field(name="Diversão", value="`anagrama, copypasta, dado, diga, escolha, eightball, "
                                            "eightballimg, fala, fumo, monke, piadazap, pica, "
                                            "por100, rand, vibe`", inline=False)
        hm.add_field(name="Matemática", value="`calc, fatorial, lernum, raiz`", inline=False)
        hm.add_field(name="Moderação", value="`addrole, apagar, ban, kick, mudarcor, mute, nick, unban, unmute`",
                     inline=False)
        hm.add_field(name="NSFW", value="`fuck, redr34, rule34`", inline=False)
        hm.add_field(name="Utilidade", value="`avatar, clima, cidade, hora, pesquisa, "
                                             "ping, prefixo, reddit, spotify, userinfo, youtube`", inline=False)

        hm.set_thumbnail(url=f"{user.avatar}")
        hm.set_footer(text=f"Solicitado por {user}", icon_url=f"{user.display_avatar}")
        await ctx.send(embed=hm)

    @ajuda.command(name="ações", aliases=["acões", "açoes", "acoes", "actions"])
    async def acoes_em_gif(self, ctx):
        prefix = prefixo(ctx.guild.id)
        ajuda_acoes = {"abraço": "Abraça o usuário que mencionasse.\n"
                                 "Uma ação bem fofinha, eu diria.\n\n"
                                 "Nome alternativo:\n"
                                 "`hug`",
                       "beijo": "Beija o usuário que mencionasse.\n"
                                "O amor é lindo mesmo, né?\n\n"
                                "Nome alternativo:\n"
                                "`kiss`\n"
                                f"Ps: Pod beijar a si mesmo usando {prefix}beijoosm",
                       "chute": "Dá um coice no usuário que mencionasse.\n"
                                "Mas peraí, porque você faria isso? :face_with_raised_eyebrow:\n\n"
                                "Nome alternativo:\n"
                                "`kick`",
                       "soco": "Quebra a cara do usuário que mencionasse.\n"
                               "Virou clube da luta essa porra?\n\n"
                               "Nome alternativo:\n"
                               "`punch`\n"
                               f"Ps: Pode-se socar em si mesmo usando {prefix}socosm",
                       "tiro": "O método mais extremo e que eu não recomendaria usar...\n"
                               "Mata a pessoa que mencionasse no tiro de bala.\n"
                               "Porque você faria isso...?\n\n"
                               "Ps: Sim, você pode atirar em você mesmo..."
                               "Mas eu o sugiro a procurar ajuda médica primeiro..."
                       }
        ajuda_actions = nextcord.Embed(title="Aqui está todas as ações que você pode fazer com seus amigos!",
                                       color=0xd4f7b4,
                                       description="Todos os comandos possuí uma parte opcional "
                                                   f"para você poder expressar como `{prefix}soco [usuário] muito gay` "
                                                   f"ou `{prefix}beijo gostosa`.")
        for ke, va in ajuda_acoes.items():
            ajuda_actions.add_field(name=ke, value=va, inline=False)
        ajuda_actions.set_footer(text=f"Solicitado por {ctx.author}")
        await ctx.send(embed=ajuda_actions)

    @ajuda.command(name="bio")
    async def biografia_lol(self, ctx):
        prefix = prefixo(ctx.guild.id)
        ajuda_biography = {"addbio": "Ferramenta para adicionar as informações "
                                     f"da sua bio, após a criação da mesma usando o `{prefix}criarbio`.\n"
                                     "Os parâmetros disponíveis podem serem vistos usando o addbio.\n"
                                     "Ps: A sequência correta para o uso do addbio é "
                                     "f```{prefix}addbio [parâmetro em letra minúscula]"
                                     "[O que for necessário colocar no parâmetro]```\n",
                           "amigo": "Determina uma melhor amizade com o usuário que mentionastes.\n"
                                    "Para aqueles que querem mostrar a amizade com seu amiguinho para todo mundo ver.\n"
                                    f"Ps: Usar apenas o comando `{prefix}amigo` mostra as seguntes informações:\n\n"
                                    "- Quem é seu melhor amigo.\n"
                                    "- Quando começou a amizade.\n"
                                    "- Quanto tempo são amigos.\n",
                           "bio": "Visualiza a bio que você criou.\n"
                                  "Ps: Esse comando não serve para criar a bio, apenas para visualizar.",
                           "casamento": "Faz uma cerimônia simples para as pessoas que querem se casar(Que fofinhos)!\n"
                                        "Só para os apaixonados :heart:"
                                        f"Ps: Da mesma forma que o comando `{prefix}amigo`, "
                                        f"usando apenas o comando `{prefix}casamento` mostra as seguintes informações:\n\n"
                                        "- Quem é seu cônjuge.\n"
                                        "- Quando começou o casamento.\n"
                                        "- Quanto tempo são casados.\n"
                                        "- Nome do Shipp.",
                           "divorciar": "Cansou de estar com seu cônjuge? Aqui está o comando de divorciar também!\n"
                                        "Nada dura para sempre, né? ;)",
                           "solteiro": "Declara para geral que você não está "
                                       "com ninguém ainda e que está disponível."
                           }
        ajuda_bio = nextcord.Embed(title="Aqui está todos os comandos relacionados ao bio.", colour=0xcc51dd,
                                   description="Para aqueles que querem algo pra customizar.")
        for ke, va in ajuda_biography.items():
            ajuda_bio.add_field(name=ke.capitalize(), value=va, inline=False)
        ajuda_bio.set_footer(text=f"Solicitado por {ctx.author}")
        await ctx.send(embed=ajuda_bio)

    @ajuda.command(name="diversão", aliases=["diversao", "fun"])
    async def entretenimento(self, ctx):
        ajuda_fun = {'8ball': 'Aqui pode me perguntar sobre literalmente qualquer coisa e a vossa '
                              'senhoria, com que vos fala, irá responder usando minha sabedoria '
                              'praticamente ilimitada.\n'
                              '\n'
                              'Nomes alternativos:\n'
                              '`eightball, 8b`\n'
                              'Ps: Esse comando funciona melhor em perguntas de sim ou não, mas '
                              'quem sou eu para estragar sua diversão?',
                     '8ballimg': 'Combine minha sabedoria ilimitada com meu senso de humor merda e '
                                 'aqui está o comando de 8ball por imagem.\n'
                                 'Funciona da mesma maneira que o 8ball, só que dessa vez, eu uso '
                                 'memes para lhe responder.\n'
                                 '\n'
                                 'Nomes alternativos:\n'
                                 '`eightballimg, 8bi`',
                     'anagrama': 'Gera um anagrama aleatório e customizado para você. \n'
                                 'Se você gosta de brincar com as palavras, esse comando é '
                                 'perfeito para ti.',
                     'copypasta': 'Você gostaria de ter um comando onde gere copypastas '
                                  'automáticas porque você é preguiçoso demais para pesquisar as '
                                  'copypastas por si só?\n'
                                  'Então esse é o comando perfeito para você!',
                     'dado': 'Comando simples de dado onde você pode jogar uma quantidade definida '
                             'de dados e também definir a quantidade de lados.\n'
                             'Formato:\n'
                             '```dado [número de dados][número de lados]```',
                     'diga': 'Um comando para fazer eu falar qualquer coisa... Qualquer coisa '
                             'mesmo...\n'
                             'Até "eu gosto do pica" ou algo do tipo.\n'
                             '\n'
                             'Nome alternativo:\n'
                             '`dizer`',
                     'escolha': 'Faça eu escolher entre dois ou mais tópicos.\n'
                                'Um comando ideal caso você seja um cara extremamente indeciso.\n'
                                '\n'
                                'Nome alternativo:\n'
                                '`escolher`',
                     'fala': 'Gera uma mensagem em webhook que simula a pessoa que mencionasse '
                             'falando tal coisa.\n'
                             'Perfeito para zoar com seus amigos e/ou membros do server.\n'
                             '\n'
                             'Nome alternativo:`falar`',
                     'fumo': 'Gera uma gif de fumo(Bonecas de pelúcia chibi) '
                             'pra você...\n'
                             'É, só isso mesmo...',
                     'monke': 'Gera uma gif de macaco para você.\n'
                              'Ótimo pra descrever certas pessoas...',
                     'piadazap': 'Você está procurando uma piada merda pra você mandar no grupo da '
                                 'família?\n'
                                 'Aqui está o comando ideal pra você!\n'
                                 '\n'
                                 'Nome alternativo:\n'
                                 '`piadadozap`\n'
                                 'PS: As piadas em suma maioria são tão ruins que os próprios '
                                 'autores nem tem conhecimento algum de gramática. As exposições à '
                                 'altos niveis de vergonha alheia não são responsabilidade minha e '
                                 'nem do criador.',
                     'pica': 'Um homem de verdade sabe apreciar a pica um do outro e esse comando '
                             'é justamente para isso.\n'
                             'Veja o quão grande é seu pau ou do seu amigo.\n'
                             '||E totalmente não irei fazer um comentário homoerótico sobre seu '
                             'pau...||\n'
                             '\n'
                             'Nomes alternativos:\n'
                             '`penis, pau, rola`',
                     'por100': 'Comando pra dizer o quão seu amigo ou quem mencionasse é tal coisa '
                               'em porcentagem.\n'
                               'Formato:\n'
                               '```por100[usuário][tal coisa]```',
                     'rand': 'Gera um número totalmente E DEFINITIVAMENTE aleatório para você.\n'
                             'Não é como se máquinas não fossem capazes de serem aleatórias... '
                             'né?\n'
                             '\n'
                             'Nomes alternativos:\n'
                             '`random, aleatorio`',
                     'vibe': 'Você gosta daqueles textos de synthwave/vaporwave escrito d  e  s  '
                             's  e    j  e  i  t  o?\n'
                             'Aqui está o comando pra gerar automaticamente pra você.'
                     }
        ke = list(ajuda_fun.keys())
        va = list(ajuda_fun.values())
        data = [tuple([ke[i], va[i]]) for i in range(len(ke))]
        pages = CustomButton(source=AjudaFun(data))
        await pages.start(ctx)

    @ajuda.command(name="matemática", aliases=["matematica", "math"])
    async def mathematicskek(self, ctx):
        ajuda_matematica = {"raiz": 'Calcula a raiz do número e exponente que você adicionou.'
                                    '\nFormato:\n```raiz[número que quer calcular a raiz][expoente da raiz]```\n'
                                    'Caso não coloque o expoente da raiz, irá calcular a raiz quadrada.\n'
                                    'PS: Pode-se calcular a raiz de pi digitando `pi` ou `π`',
                            "lernumero": 'Mostra a posição inicial de como se deve ler tal número.'
                                         '\n\nExemplo:\n```1000000000000000000000000```\nResultado:'
                                         '\n```1.0 septilhão```\nNome alternativo:\n`lernum`',
                            "calcular": 'Uma calculadora onde você pode fazer operações básicas de'
                                        ' matemática e também exponenciação.\nAqui está os sinais que '
                                        'você pode usar:\n\n`+`:  Adição\n`-`:  Subtração\n`*`:  '
                                        'Multiplicação\n`/`:  Divisão(Com decimais)\n`**`: '
                                        'Exponenciação\n`//`: Divisão(Sem decimais)\n\n'
                                        'Formato:```calc[valor 1]{operador}[valor 2]...```'
                                        'Nome alternativo:\n`calc`',
                            "fatorial": 'Calcula o fatorial do número que inserisse.\nNome alternativo:\n`fat`'
                            }
        ajuda_mat = nextcord.Embed(title="Aqui está todos os comandos relacionados a matemática.", colour=0xcc51dd,
                                   description="Destinado aos nerds que são curiosos por matemática ou "
                                               "só aqueles que não sabem calcular quanto é 2 + 2.")
        for ke, va in ajuda_matematica.items():
            ajuda_mat.add_field(name=ke.capitalize(), value=va, inline=False)
        ajuda_mat.set_footer(text=f"Solicitado por {ctx.author}")
        await ctx.send(embed=ajuda_mat)

    @ajuda.command(name="moderação", aliases=["moderacao", "moderacão", "moderaçao", "mod"])
    async def moderacao_lol(self, ctx):
        prefix = prefixo(ctx.guild.id)
        ajuda_mod = {"addrole": "Adiciona um cargo no seu servidor.\n"
                                "Por padrão ele vem com cor branca, "
                                f"mas pode mudar usar o comando `{prefix}mudarcor` "
                                "para mudar a cor do cargo.\n\n"
                                "Permissão necessária: `Gerenciar Cargos`\n"
                                "Nomes Alternativos: `addcargo, criacargo, novocargo, ncargo`",
                     "apagar": "Apaga um número específico de mensagens(Limitado entre 1 e 150 mensagens).\n\n"
                               "Permissão necessária: `Gerenciar Mensagens`\n"
                               "Nomes Alternativos: `deletar, excluir, delete`",
                     "ban": "Bane o usuário mencionado permanentemente."
                            "Use esse comando com moderação. :)\n\n"
                            "Permissão necessária: `Banir Membros`\n",
                     "kick": "Expulsa o usuário mencionado(Mas ainda com a possibilidade dele retornar ao server).\n\n"
                             "Permissão necessária: `Expulsar Membros`\n",
                     "mudarcor": "Muda a cor do cargo mencionado.\n\n"
                                 "Permissão necessária: `Gerenciar Cargos`\n"
                                 "Nomes Alternativos: `corcargo, ccargo`",
                     "mute": "Muta o membro mencionado pelo período que mencionasse(Podendo ir de segundos até dias).\n"
                             f"Formato: ```{prefix}mute [usuario] [tempo][unidade em s, m, h ou d]```\n\n"
                             "Permissão necessária: `Expulsar membros`\n"
                             "Nome Alternativo: `mutar`",
                     "nick": "Muda o nick do usuário mencionado.\n"
                             f"Formato: ```{prefix}nick [usuario] [nick que você quer nomear]```\n\n"
                             "Permissão necessária: `Gerenciar Nicknames`\n"
                             "Nome Alternativo: `mudarnick`",
                     "slowmode": f"Determina o tempo de intervalo entre as mensagens(Mesmo formato do {prefix}mute).\n"
                                 "Muito bom para quem tiver um servidor muito grande.\n\n"
                                 "Permissão necessária: `Gerenciar Mensagens`\n",
                     "unban": "Desbane o usuário usando seu nome e a sua tag.\n\n"
                              "Permissão necessária: `Banir Membros`\n",
                     "unmute": "Desmuta o usuário que mencionasse.\n\n"
                               "Permissão necessária: `Expulsar membros`\n"
                               "Nome Alternativo: `mutar`"
                     }
        ke = list(ajuda_mod.keys())
        va = list(ajuda_mod.values())
        data = [tuple([ke[i], va[i]]) for i in range(len(ke))]
        pages = CustomButton(source=AjudaMod(data))
        await pages.start(ctx)

    @ajuda.command(name="nsfw")
    async def nsfw_lmao(self, ctx):
        prefix = prefixo(ctx.guild.id)
        ajuda_nsfw = {"fuck": "Você quer foder um membro do server? "
                              "Então esse é o comando perfeito pra você!\n"
                              "Apenas aviso que esse é um comando um tanto cringe, "
                              "então não aconselho muito a usá-lo\n\n"
                              "Nomes alternativos: `foder, fuder`",
                      "redr34": "Pega uma imagem de rule34 direto do reddit baseado no que você quer procurar!\n"
                                "Gosta de peitos? Bundas? Paus? Pés?"
                                "Aqui sempre vai ter espaço por qual for o seu fetiche!\n\n"
                                "Nome alternativo: `redditr34`",
                      "rule34": f"Funciona da mesma maneira que o {prefix}redr34, "
                                f"porém ele pega as imagens direto do site do rule34."
                      }
        for ke, va in ajuda_nsfw.items():
            ajuda_nsfw.add_field(name=ke.capitalize(), value=va, inline=False)
        ajuda = nextcord.Embed(title="Aqui está todos os comandos safadinhos...", colour=0xff5426,
                               description="Para você que quer tirar seu tesão...")
        ajuda.set_footer(text=f"Solicitado por {ctx.author}")
        await ctx.send(embed=ajuda)

    @ajuda.command(name="utilidade", alias=["utilidades", "utils"])
    async def utilskek(self, ctx):
        prefix = prefixo(ctx.guild.id)
        ajuda_utils = {"avatar": "Mostra o avatar do usuário que mencionasse.\n"
                                 "Quando não menciona o usuário, mostra o seu avatar.",
                       "addemoji": "Adiciona um emoji para o seu servidor, seja ele animado ou não.\n"
                                   f"Formato: ```{prefix}addemoji [link do emoji] [nome do emoji]```",
                       "clima": "Mostra o clima da cidade que inserisse.\n"
                                "Certifique-se de escrever "
                                "o nome correto para o comando funcionar adequadamente.",
                       "cidade": "Mostra as informações das cidades do brasil baseado nos dados do IBGE\n"
                                 "Ps: É um comando experimental, então pode ignorá-lo.\n\n"
                                 "Nome alternativo: `infocidade`",
                       "pesquisa": "Manda um link que mostra os resultados "
                                   "de pesquisa baseado nos parâmetros que você adicionou.\n\n"
                                   "Nomes alternativos: `pesquisa, search`",
                       "ping": "Mostra o meu tempo de resposta.",
                       "prefixo": "Troca o prefixo atual do server para um personalizado.\n\n"
                                  "Nomes alternativos: `setprefix, mudarprefixo, setp`",
                       "reddit": "Mostra uma imagem aleatória do subreddit que adicionasse.\n"
                                 f"Formato: ```{prefix}reddit [nome do subreddit(sem o r/)] "
                                 "[Parâmetro opcional(hot, top ou new), padrão: hot]```",
                       "spotify": "Mostra as informações da música que o usuário está ouvindo\n"
                                  "Ps: Para funcionar, tem que aparecer a atividade "
                                  "do spotify mostrando a música que ele está ouvindo.",
                       "userinfo": "Mostra as informações do usuário em relação ao server.\n"
                                   "Parâmetros: ``"
                                   "Nomes alternativos: `infouser, uinfo`",
                       "youtube": "Mostra o primeiro link do "
                                  "resultado baseado no que pesquisasse.\n\n"
                                  "Nome alternativo: `yt`"
                       }
        ke = list(ajuda_utils.keys())
        va = list(ajuda_utils.values())
        data = [tuple([ke[i], va[i]]) for i in range(len(ke))]
        pages = CustomButton(source=AjudaUtils(data))
        await pages.start(ctx)


def setup(bot):
    bot.add_cog(Ajuda(bot))
