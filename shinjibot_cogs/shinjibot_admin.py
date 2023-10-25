import json
import typing
import nextcord
from nextcord.ext import commands
from shinjibot import prefixo


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = nextcord.Intents().all()
    shinji = commands.Bot(intents=intents)

    @commands.command(name="apagar", aliases=["deletar", "excluir", "delete"], pass_context=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def apagar_mensagens(self, ctx, quantidade: int = 0):
        if ctx.author.guild_permissions.manage_messages is False:
            await ctx.channel.send(f"{ctx.author.name}, você precisa de permissão para "
                                   f"**Apagar Mensagens** para poder usar esse comando!")
        else:
            if quantidade < 1 or quantidade > 150:
                await ctx.send('Você só pode apagar entre 1 e 150 mensagens!')
            else:
                msg = ""
                if quantidade == 1:
                    msg += "1 mensagem"
                else:
                    msg += f"{quantidade} mensagens"
                await ctx.channel.purge(limit=quantidade + 1)
                await ctx.channel.send(f"{msg} foram apagadas com sucesso!")

    @apagar_mensagens.error
    async def apagar_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa apagar mensagens, "
                           f"por favor ative a permissão `Gerenciar Mensagens`!")

    @commands.command(name="nick", aliases=["mudarnick"])
    @commands.bot_has_permissions(manage_nicknames=True)
    async def mudar_nickname(self, ctx, member: nextcord.Member, *, nickname):
        if ctx.message.author.guild_permissions.manage_nicknames is False:
            await ctx.send(f"Eu tô ligado nesse seu joguinho, {ctx.author.name}...\n"
                           f"Precisa de autorização para **Gerenciar Apelidos** para que possa usar esse comando...")
        elif member == ctx.guild.owner:
            await ctx.send("**Boa tentativa...\n"
                           "É impossível mudar o nickesse usuário porque ele é o dono do server...**")
        else:
            await ctx.message.delete()
            await member.edit(nick=nickname)

    @mudar_nickname.error
    async def nickname_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa mudar a cor dos cargos, "
                           f"por favor ative a permissão `Gerenciar Apelidos`!")

    @commands.command(name="mute", aliases=["mutar"])
    @commands.bot_has_permissions(manage_roles=True)
    async def mutar_pessoas(self, ctx, membro: nextcord.Member = None,
                            tempo=5, var="m", *, motivo="Aparentemente sem motivo..."):
        guild = ctx.guild
        role = nextcord.utils.get(ctx.guild.roles, name="Mutado")
        if ctx.message.author.guild_permissions.kick_members is False:
            await ctx.send(f"{ctx.author.name}, você acha que esse server é só putaria e cachorrada?\n"
                           f"Você precisa de permissão para **Mutar Membros** para poder usar esse comando!")
        elif membro is None:
            await ctx.send("**Mencione o usuário para que eu possa mutar...**")
        elif membro == ctx.guild.owner:
            await ctx.send("**É impossível mutar esse usuário porque ele é o dono do server...**")
        elif membro.id == ctx.author.id:
            await ctx.send("**Um momento amigo... Você não pode se mutar...**")
        else:
            if role is None:
                role = await guild.create_role(name="Mutado")
                for channel in guild.channels:
                    await channel.set_permissions(role, speak=False, send_messages=False)
                await ctx.send("**Configurações feitas com sucesso... Agora pode mutar de vez**")
            else:
                if var not in ["s", "m", "h", "d"]:
                    await ctx.send("**Chave invalida! As chaves válidas são: `[s, m, h, d]`**")
                else:
                    if role in membro.roles:
                        await ctx.send("**Você já mutou esse usuário!**")
                    else:
                        n = ""
                        if var == "m":
                            n += "minutos"
                        elif var == "h":
                            n += "horas"
                        elif var == "d":
                            n += "dias"
                        elif var == "s":
                            n += "segundos"
                        mutadolol = nextcord.Embed(title=f"__Mutado!__ <a:mutadolol:1052982357700911164>", color=0xff6754,
                                                   description="Parece que alguém aqui não foi muito amigável...")
                        mutadolol.add_field(name="Quem foi mutado?", value=f"{membro.name}", inline=False)
                        mutadolol.add_field(name="Quem mutou?", value=f"{ctx.author.name}", inline=False)
                        mutadolol.add_field(name="Quanto tempo de mute?", value=f"{tempo} {n}", inline=False)
                        mutadolol.add_field(name="Qual motivo? ", value=f"{motivo}", inline=False)
                        mutadolol.set_thumbnail(url=ctx.author.display_avatar)
                        mutadolol.set_footer(text="Não submestime os mods!", icon_url=f"{self.bot.user.display_avatar}")
                        await ctx.send(embed=mutadolol)
                        await membro.add_roles(role)
                        if var == "s":
                            await asyncio.sleep(tempo)

                        elif var == "m":
                            await asyncio.sleep(tempo * 60)

                        elif var == "h":
                            await asyncio.sleep(tempo * 3600)

                        elif var == "d":
                            await asyncio.sleep(tempo * 86400)
                        await membro.remove_roles(role)
                        await ctx.send(f"{membro.mention} foi desmutado!")

    @mutar_pessoas.error
    async def mutar_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa mutar membros, "
                           f"por favor ative a permissão `Gerenciar Cargos`!")

    @commands.command(aliases=["unmute", "desmutar"])
    @commands.bot_has_permissions(manage_roles=True)
    async def desmutar_pessoas(self, ctx, membro: nextcord.Member = None):
        guild = ctx.guild
        role = nextcord.utils.get(guild.roles, name="Mutado")
        if ctx.message.author.guild_permissions.kick_members is False:
            await ctx.send(f"**{ctx.author.name}, você não pode desmutar membros assim como não pode mutar eles...**")
        elif membro is None:
            await ctx.send("**Mencione o usuário para que eu possa desmutar...**")
        elif role not in membro.roles:
            await ctx.send("**Ele não estava mutado ou já foi desmutado antes...**")
        else:
            if role:
                await membro.remove_roles(role)
                await ctx.send(f"{membro.mention} foi desmutado!")

    @desmutar_pessoas.error
    async def desmutar_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa desmutar membros, "
                           f"por favor ative a permissão `Gerenciar Cargos`!")

    @commands.command(name="addrole", aliases=["addcargo", "criacargo", "novocargo", "ncargo"], pass_context=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def criar_carginho(self, ctx, *, name):
        if ctx.author.guild_permissions.manage_roles is False:
            await ctx.send(f"{ctx.author.name}, você precisa de autorização para "
                           f"**Gerenciar Cargos** para poder usar esse comando!")
        else:
            guild = ctx.guild
            await guild.create_role(name=f"{name}")
            await ctx.send(f"**Cargo chamado `{name}` criado com sucesso!**")

    @criar_carginho.error
    async def criar_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa criar cargos, "
                           f"por favor ative a permissão `Gerenciar Cargos`!")

    @commands.command(name="mudarcor", aliases=["corcargo", "ccargo"])
    @commands.bot_has_permissions(manage_roles=True)
    async def mudar_cor_carginho(self, ctx, name: nextcord.Role, *, cor: typing.Optional[str]):
        prefix = prefixo(ctx.guild.id)
        cargo = name.mention
        role = nextcord.utils.get(ctx.guild.roles, name=f"{name.name}")
        if ctx.author.guild_permissions.manage_roles is False:
            await ctx.send(f"{ctx.author.name}, você precisa de autorização para "
                           f"**Gerenciar Cargos** para poder usar esse comando!")
        elif cor is None:
            await role.edit(color=nextcord.Colour.random())
            await ctx.send("Já que você não disse o nome de uma cor, eu mesmo coloquei a cor para ti... ;)")
        else:
            if cor == "Amarelo":
                await role.edit(color=nextcord.Colour.yellow())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Azul":
                await role.edit(color=nextcord.Colour.blue())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Azul Escuro":
                await role.edit(color=nextcord.Colour.dark_blue())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Blurple":
                await role.edit(color=nextcord.Colour.blurple())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Cinza":
                await role.edit(color=nextcord.Colour.light_gray())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Cinza Claro":
                await role.edit(color=nextcord.Colour.lighter_gray())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Cinza Escuro":
                await role.edit(color=nextcord.Colour.dark_gray())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Discord":
                await role.edit(color=nextcord.Colour.og_blurple())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Dourado":
                await role.edit(color=nextcord.Colour.gold())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Laranja":
                await role.edit(color=nextcord.Colour.orange())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Laranja Escuro":
                await role.edit(color=nextcord.Colour.dark_orange())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Magenta":
                await role.edit(color=nextcord.Colour.magenta())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Magenta Claro":
                await role.edit(color=nextcord.Colour.fuchsia())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Magenta Escuro":
                await role.edit(color=nextcord.Colour.dark_magenta())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Roxo":
                await role.edit(color=nextcord.Colour.purple())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Roxo Escuro":
                await role.edit(color=nextcord.Colour.dark_purple())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Preto":
                await role.edit(color=nextcord.Colour.dark_theme())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Verde":
                await role.edit(color=nextcord.Colour.green())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Verde Claro":
                await role.edit(color=nextcord.Colour.brand_green())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Verde Escuro":
                await role.edit(color=nextcord.Colour.dark_green())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Vermelho":
                await role.edit(color=nextcord.Colour.red())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            elif cor == "Vermelho Escuro":
                await role.edit(color=nextcord.Colour.dark_red())
                await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
            else:
                if cor.startswith("#"):
                    cor1 = cor.lstrip("#")
                    cor2 = tuple(int(cor1[i:i + 2], 16) for i in (0, 2, 4))
                    await role.edit(color=nextcord.Colour.from_rgb(cor2[0], cor2[1], cor2[2]))
                    await ctx.send(f"O cargo {cargo} teve sua cor mudada com sucesso!")
                else:
                    colorido = nextcord.Embed(title="Cor inválida!", color=nextcord.Colour.og_blurple(),
                                              description=f"Use `{prefix}ajuda mudarcor` para saber como "
                                                          f"funciona esse comando!\n"
                                                          f"Lá também possui as informações de como mudar "
                                                          f"a cor do cargo usando hexadecimal!")
                    await ctx.send(embed=colorido)

    @mudar_cor_carginho.error
    async def mudar_cor_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa mudar a cor dos cargos, "
                           f"por favor ative a permissão `Gerenciar Cargos`!")

    @commands.command(name="kick")
    @commands.bot_has_permissions(kick_members=True)
    async def kickar_pessoas(self, ctx, membro: nextcord.Member, *, reason: typing.Optional[str]):
        if ctx.author.guild_permissions.kick_members is False:
            await ctx.send("Você tá pensando que isso é palhaçada? Você precisa de "
                           "autorização para **Expulsar Membros** para realizar esse comando!")
        elif membro == ctx.author:
            await ctx.send("Você não pode se expulsar... :face_with_raised_eyebrow:")
        elif membro == ctx.guild.owner:
            await ctx.send("**É impossível expulsar esse usuário porque ele é o dono do server...**")
        else:
            if membro not in ctx.guild.members:
                await ctx.send("**Esse membro não existe nesse servidor!**")
            else:
                rs = ""
                if reason is None:
                    rs += "Sem motivo aparente"
                else:
                    rs += reason
                kickado = nextcord.Embed(title=f"Você foi expulso do server {ctx.guild} por {ctx.author}", color=0xff0000)
                kickado.add_field(name="Motivo:", value="rs", inline=False)
                kickado.set_image(url="https://gifimage.net/wp-content/uploads/2018/06/"
                                      "team-rocket-blasting-off-again-gif-8.gif")
                await membro.send(embed=kickado)
                await membro.kick()
                kickadolol = nextcord.Embed(title=f"__Expulso!__ <:kickadolol:1052992947815190528>", color=0xff6754,
                                            description="Parece que alguém aqui fez uma bronca e tanto...")
                kickadolol.add_field(name="Quem foi expulso:", value=f"{membro.name}#{membro.discriminator}", inline=False)
                kickadolol.add_field(name="Quem expulsou:", value=f"{ctx.author.mention}", inline=False)
                kickadolol.add_field(name="Qual motivo:", value=f"{rs}", inline=False)
                kickadolol.set_footer(text="Não submestime os mods!", icon_url=f"{self.bot.user.display_avatar}")
                await ctx.send(embed=kickadolol)

    @kickar_pessoas.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa expulsar membros, "
                           f"por favor ative a permissão `Expulsar Membros`!")

    @commands.command(name="ban")
    @commands.bot_has_permissions(ban_members=True)
    async def banir_pessoas(self, ctx, membro: nextcord.Member = None, *, motivo=None):
        if ctx.author.guild_permissions.ban_members is False:
            await ctx.send("**Você tá pensando que isso é palhaçada?**\n"
                           "Você precisa de autorização para `Banir Membros` para realizar esse comando!")
        elif membro == ctx.author:
            await ctx.send("**Você não pode se banir...**\n"
                           "Porque caralhos iria fazer isso? :face_with_raised_eyebrow:")
        elif membro is None:
            await ctx.send("**Mencione o usuário para que eu possa banir...**")
        elif membro == ctx.guild.owner:
            await ctx.send("**É impossível banir esse usuário porque ele é o dono do server...**")
        else:
            if membro not in ctx.guild.members:
                await ctx.send("**Esse usuário ou já foi banido ou não está dentro do server**")
            else:
                if motivo is None:
                    motivo = "Sem motivo aparente"
                banido = nextcord.Embed(title=f"Você foi banido do {ctx.guild.name}", colour=0x000000)
                banido.add_field(name="Motivo", value=f"{motivo}")
                banido.set_image(url="https://media.tenor.com/RxqqK6mWr2AAAAAM/cryptoon-goonz-cryptoongoonz-ban.gif")
                banido.set_footer(text="Se deu mal, cara...")
                await membro.send(embed=banido)
                await membro.ban()
                banidolol = nextcord.Embed(title=f"{membro} foi banido!\n", color=0xff0000,
                                           description=f"Foi punido justamente pelos crimes cometidos no server {ctx.guild}!")
                banidolol.add_field(name="Quem foi banido?", value=f"{membro.name}#{membro.discriminator}", inline=False)
                banidolol.add_field(name="Quem baniu?", value=f"{ctx.author.mention}", inline=False)
                banidolol.add_field(name="Qual motivo?", value=f"{motivo}", inline=False)
                banidolol.set_footer(text="Não submestime os mods!", icon_url=f"{ctx.author.display_avatar}")
                await ctx.send(embed=banidolol)

    @banir_pessoas.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa banir membros, "
                           f"por favor ative a permissão `Banir Membros`!")

    @commands.command(name="unban")
    async def desbanir_pessoas(self, ctx, *, member):
        if ctx.author.guild_permissions.ban_members is False:
            await ctx.send(f"**{ctx.author.name}, você não pode desbanir membros assim como não pode banir eles...**")
        elif member.split("#") == [ctx.author.name, ctx.author.discriminator]:
            await ctx.send(f"**{ctx.author.name}, você não está banido e... você não pode se banir wtf...**")
        else:
            banidos = await ctx.guild.bans().flatten()
            nome, hashtag = member.split("#")
            for bans in banidos:
                usuario = bans.user
                if [usuario.name, usuario.discriminator] == [nome, hashtag]:
                    await ctx.guild.unban(usuario)
                    desbanidolol = nextcord.Embed(title=f"{usuario} foi desbanido!", color=0xff0000,
                                                  description=f"Ele foi revogado dos seus crimes contra o "
                                                              f"servidor {ctx.guild}...\n"
                                                              f"Espero que ele não vacile denovo!")
                    desbanidolol.set_image(url="https://c.tenor.com/ctSeX23vr98AAAAM/shinji-shinji-ikari.gif")
                    desbanidolol.set_footer(text="Não submestime os mods!", icon_url=f"{self.bot.user.display_avatar}")
                    await ctx.send(embed=desbanidolol)

    @desbanir_pessoas.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa desbanir membros, "
                           f"por favor ative a permissão `Banir Membros`!")

    @commands.command(name="slowmode")
    async def setdelay(self, ctx, n: int, var: str):
        if ctx.author.guild_permissions.manage_messages:
            if n > 0:
                if var == "m":
                    await ctx.channel.edit(slowmode_delay=n * 60)
                elif var == "h":
                    await ctx.channel.edit(slowmode_delay=n * 3600)
                elif var == "d":
                    await ctx.channel.edit(slowmode_delay=n * 86400)
                else:
                    await ctx.channel.edit(slowmode_delay=n)
            elif n == 0 and var == "":
                await ctx.send("**Slowmode desabilitado!**")
        else:
            await ctx.send("**Você não tem permissão para usar esse comando!**")

    @setdelay.error
    async def delay_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Não tenho as permissões necessárias para realizar esse comando...\n"
                           f"Se deseja que eu possa usar o comando de slowmode, "
                           f"por favor ative a permissão `Gerenciar Mensagens`!")


def setup(bot):
    bot.add_cog(Admin(bot))
