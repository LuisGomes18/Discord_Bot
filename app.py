from datetime import datetime
from typing import Optional
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

try:
    with open("token.txt", "r", encoding="utf-8") as dados:
        token = dados.read()
except FileNotFoundError:
    print("Arquivo não encontrado!")
    exit(1)
except Exception as erro:
    print(f"Ocorreu um erro: {str(erro)}")
    exit(1)


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"\n\nLogged in as {bot.user.name}\n\n")
    bot.started_at = datetime.utcnow()


@bot.command()
async def ping(ctx):
    print(f"{ctx.author} acabou de usar comando (ping) no server {ctx.guild.name}")
    await ctx.send("Pong!")


@bot.command()
async def sobre(ctx):
    print(f"{ctx.author} acabou de usar comando (sobre) no server {ctx.guild.name}")
    bot_member = ctx.guild.get_member(bot.user.id)
    bot_user = ctx.bot.user
    entry_date = bot_member.joined_at.strftime("%Y-%m-%d %H:%M")
    creation_date = bot_user.created_at.strftime("%Y-%m-%d %H:%M")

    await ctx.send(
        f"""
{ctx.author.mention} eu sou um bot criado pelo Lucas Gomes
    Entrei no servidor em: {entry_date} UTC
    Foi criado em: {creation_date} UTC
"""
    )


@bot.command()
async def uptime(ctx: commands.Context) -> discord.Message:
    print(f"{ctx.author} acabou de usar comando (uptime) no server {ctx.guild.name}")
    uptime_delta = datetime.utcnow() - bot.started_at
    hours, remainder = divmod(int(uptime_delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours} horas, {minutes} minutos, {seconds} segundos"

    await ctx.send(f"Estou online há {uptime_str}")


@bot.command()
async def perfil(ctx):
    print(f"{ctx.author} acabou de usar comando (perfil) no server {ctx.guild.name}")
    author = ctx.author
    entry_date = author.joined_at.strftime("%Y-%m-%d %H:%M")
    creation_date = author.created_at.strftime("%Y-%m-%d %H:%M")
    roles = ", ".join([role.name for role in author.roles[1:]])

    await ctx.send(
        f"""
{ctx.author.mention} seu perfil é:
    Nome: {author}
    Criação: {creation_date}
    Entrada: {entry_date}
    Cargos: {roles}
"""
    )


@bot.command()
@commands.guild_only()
@commands.has_guild_permissions(ban_members=True)
@commands.bot_has_guild_permissions(ban_members=True)
async def ban(
    ctx: commands.Context, member: discord.Member, *, reason: str = None  # type: ignore
) -> Optional[discord.Message]:
    if ctx.guild is None or isinstance(ctx.author, discord.User):
        return
    mention = ctx.author.mention
    if ctx.guild.owner == member:
        return await ctx.send(f"{mention} você não pode banir o dono do servidor!")
    elif member == ctx.author:
        return await ctx.send(f"{mention} você não pode se banir!")
    elif member == ctx.guild.me:
        return await ctx.send(f"{mention} eu não posso me banir!")
    elif ctx.author.top_role <= member.top_role:
        return await ctx.send(
            f"{mention} você não pode banir alguém com o mesmo cargo ou maior que o seu!"
        )
    try:
        await ctx.guild.ban(member, reason=reason)
    except discord.errors.Forbidden:
        return await ctx.send("Eu não tenho permissão para banir esse membro!")
    except discord.errors.HTTPException:
        return await ctx.send("Ocorreu um erro ao banir esse membro!")
    else:
        ban_message = f"{member.mention} foi banido por {ctx.author.mention}!"
        if reason:
            ban_message += f" Motivo: {reason}"
        await ctx.send(ban_message)


@bot.command()
@commands.guild_only()
@commands.has_guild_permissions(kick_members=True)
@commands.bot_has_guild_permissions(kick_members=True)
async def kick(
    ctx: commands.Context, member: discord.Member, *, reason: str = None  # type: ignore
) -> Optional[discord.Message]:
    if ctx.guild is None or isinstance(ctx.author, discord.User):
        return
    mention = ctx.author.mention
    if ctx.guild.owner == member:
        return await ctx.send(f"{mention} você não pode kickar o dono do servidor!")
    elif member == ctx.author:
        return await ctx.send(f"{mention} você não pode se kickar!")
    elif member == ctx.guild.me:
        return await ctx.send(f"{mention} eu não posso me kickar!")
    elif ctx.author.top_role <= member.top_role:
        return await ctx.send(
            f"{mention} você não pode kickar alguém com o mesmo cargo ou maior que o seu!"
        )
    try:
        await ctx.guild.kick(member, reason=reason)
    except discord.errors.Forbidden:
        return await ctx.send("Eu não tenho permissão para kickar esse membro!")
    except discord.errors.HTTPException:
        return await ctx.send("Ocorreu um erro ao kickar esse membro!")
    else:
        kick_message = f"{member.mention} foi kickado por {ctx.author.mention}!"
        if reason:
            kick_message += f" Motivo: {reason}"
        await ctx.send(kick_message)


@bot.command()
async def ajuda(ctx):
    print(f"{ctx.author} acabou de usar comando (ajuda) no server {ctx.guild.name}")

    await ctx.send(
        f"""{ctx.author.mention} os comando que tenho são:\n
**Comandos de informação**
```!ping - para testar se estou online
!uptime - para ver a quanto tempo estou online
!sobre - para saber mais sobre mim
!perfil - para ver seu perfil
!ajuda - para ver os comandos que tenho```

**Comandos de Moderação**
```!ban - para banir um membro
!kick - para kickar um membro
```
""")


bot.run(token)
