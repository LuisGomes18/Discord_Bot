import mysql.connector
from datetime import *
import pytz
import asyncio
import random
from googletrans import Translator
import requests
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import *

mydb = mysql.connector.connect(
    host="IP do banco de dados",
    user="Usuario do banco de dados",
    password="Password do banco de dados",
    database="Nome da database do banco de dados"
)

cursor = mydb.cursor()

token = buscar_token(cursor)
prefixo = carregar_prefixo(cursor)
id_boas_vindas = carregar_boas_vindas(cursor)
id_despedidas = carregar_despedidas(cursor)
api_key = carregar_api_key(cursor)

intents = discord.Intents.all()
bot = commands.Bot("??", intents=intents)
start_time = datetime.now(pytz.utc).replace(microsecond=0)


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Comando não encontrado!')


@bot.event
async def warm_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Desculpe, você não tem permissão para usar este comando.")


@bot.event
async def on_member_join(member):
    if id_boas_vindas is not None:
        canal_boas_vindas = bot.get_channel(id_boas_vindas)
        if canal_boas_vindas:
            try:
                role = discord.utils.get(member.guild.roles, name="Bot's  Recem Chegados")
                if role:
                    await member.add_roles(role)
                    mensagem_boas_vindas = f"Bem-vindo {member.mention}!"
                    await canal_boas_vindas.send(mensagem_boas_vindas)
            except Exception as e:
                print(f"Erro ao adicionar cargo ou enviar mensagem de boas-vindas: {e}")


@bot.event
async def on_member_remove(member):
    if id_despedidas is not None:
        canal_despedidas = bot.get_channel(id_despedidas)
        if canal_despedidas:
            mensagem_despedida = f"Até logo {member.name}!"
            await canal_despedidas.send(mensagem_despedida)


@bot.command()
async def ajuda(ctx):
    embed = discord.Embed(
        title='Comandos Disponíveis',
        description='Lista de comandos disponíveis:',
        color=discord.Color.green()
    )
    embed.add_field(name='!ping', value='Comando para saber se bot esta online', inline=False)
    embed.add_field(name='!uptime', value='Comando para saber quanto tempo o bot esta online', inline=False)
    embed.add_field(name='!boas_vindas', value='Define o canal de boas vindas', inline=False)
    embed.add_field(name='!despedidas', value='Define o canal de despedidas', inline=False)
    embed.add_field(name='!purge', value='Apaga certo numero de mensagem definidas pelo usuario', inline=False)
    embed.add_field(name='!dar_cargo', value='Atribui um cargo ao usuario', inline=False)
    embed.add_field(name='!remover_cargo', value='Remove um cargo do usuario', inline=False)
    embed.add_field(name='!ajuda', value='Mostra esta mensagem de ajuda', inline=False)
    embed.add_field(name='!ban', value='Da ban ao usuario', inline=False)
    embed.add_field(name='!unban', value='Remove a ban do usuario', inline=False)
    embed.add_field(name='!mute', value='Muta o usuario', inline=False)
    embed.add_field(name='!unmute', value='Desmuta o usuario', inline=False)
    embed.add_field(name='!kick', value='Kick usuario', inline=False)
    embed.add_field(name='!info', value='Mostar as informações do bot', inline=False)
    embed.add_field(name='!timeout', value='Silencia o usuario', inline=False)
    embed.add_field(name='!rps', value='Jogar pedra, papel ou tessoura com o usuario', inline=False)
    embed.add_field(name='!cara_coroa', value='Joga cara ou coroa com o usuario', inline=False)
    embed.add_field(name='!dado', value='Jogar o dado', inline=False)
    embed.add_field(name='!traducao', value='Traduz o texto', inline=False)
    embed.add_field(name='!tempo', value='Mostra o tempo', inline=False)
    embed.set_footer(text=f'Comando executado por {ctx.author.name}', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    await ctx.send('Pong')


@bot.command()
async def uptime(ctx):
    current_time = datetime.now(pytz.utc).replace(microsecond=0)
    uptime = current_time - start_time
    await ctx.send(f'O bot está online há: {uptime}')


@bot.command()
async def boas_vindas(ctx, id: int):
    id_boas_vindas = id
    guardar_id_boas_vindas(mydb, cursor, id_boas_vindas)
    await ctx.send(f'O ID do canal de boas vindas agora é {id_boas_vindas}')


@bot.command()
async def despedidas(ctx, id: int):
    id_despedidas = id
    guardar_id_despedidas(mydb, cursor, id_despedidas)
    await ctx.send(f'O ID do canal de despedidas agora é {id}')


@bot.command()
async def api_tempo(ctx, *, api_key: str):
    api = api_key
    guardar_api_key(mydb, cursor, api)
    await ctx.send(f'A key para API de tempo agora é {api_key}')


@bot.command()
@has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} mensagens foram excluídas neste canal.', delete_after=5)


@bot.command()
@has_permissions(manage_roles=True)
async def dar_cargo(ctx, member: discord.Member, role: discord.Role):
    if member == bot.user:
        await ctx.send("Desculpe, não posso atribuir cargos a mim mesmo.")
        return
    if ctx.author.top_role.position <= role.position:
        await ctx.send("Você não tem permissão para atribuir esse cargo.")
        return
    if ctx.author.top_role.position <= member.top_role.position:
        await ctx.send("Você não pode atribuir um cargo a alguém com um cargo superior ou igual ao seu.")
        return

    await member.add_roles(role)
    await ctx.send(f'O cargo {role.name} foi dado a {member.mention}.')


@bot.command()
@has_permissions(manage_roles=True)
async def remover_cargo(ctx, member: discord.Member, role: discord.Role):
    if member == bot.user:
        await ctx.send("Desculpe, não posso atribuir cargos a mim mesmo.")
        return
    if ctx.author.top_role.position <= role.position:
        await ctx.send("Você não tem permissão para atribuir esse cargo.")
        return
    if ctx.author.top_role.position <= member.top_role.position:
        await ctx.send("Você não pode atribuir um cargo a alguém com um cargo superior ou igual ao seu.")
        return

    await member.remove_roles(role)
    await ctx.send(f'O cargo {role.name} foi removido de {member.mention}.')


@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title='Informações do Bot',
        description='Informações sobre o bot:',
        color=discord.Color.red()
    )
    embed.add_field(name='Prefixo', value="??", inline=False)
    embed.add_field(name='Nome do Bot', value=bot.user.name, inline=False)
    embed.add_field(name='ID do Bot', value=bot.user.id, inline=False)
    embed.add_field(name='Criador do bot', value="Luís Gomes", inline=False)
    embed.add_field(name='Biblioteca Usada', value="discord.py", inline=False)
    embed.add_field(name='Quantidade do server em que estou', value=len(bot.guilds), inline=False)
    embed.add_field(name="Data em que foi criado", value=bot.user.created_at.strftime("%Y-%m-%d %H:%M"), inline=False)
    if ctx.guild:
        member = ctx.guild.get_member(bot.user.id)
        if member:
            embed.add_field(name="Data que entrei no servidor", value=member.joined_at.strftime("%Y-%m-%d %H:%M"),
                            inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.top_role >= ctx.author.top_role:
        await ctx.send("Você não tem permissão para banir este usuário.")
    elif member == ctx.guild.me:
        await ctx.send("Não posso banir me.")
    else:
        await member.ban(reason=reason)
        await ctx.send(f"O usuário {member.name} foi banido por {ctx.author.name}.")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member.top_role >= ctx.author.top_role:
        await ctx.send("Você não tem permissão para banir este usuário.")
    elif member == ctx.guild.me:
        await ctx.send("Não posso me expulsar.")
    else:
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} foi expulso do server!.")


@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, duration: int, *, reason=None):
    if member.top_role >= ctx.author.top_role:
        await ctx.send("Você não tem permissão para silenciar este usuário.")
    elif member == ctx.guild.me:
        await ctx.send("Não posso me silenciar.")
    else:
        end_time = datetime.now(timezone.utc) + timedelta(minutes=duration)

        muted_role = discord.utils.get(ctx.guild.roles, name="Mutado")
        if muted_role:
            await member.add_roles(muted_role)
            await ctx.send(f"{member.mention} foi silenciado por {duration} minutos com motivo {reason}.")

            await asyncio.sleep(duration * 60)
            await member.remove_roles(muted_role)
            await ctx.send(f"O silenciamento de {member.mention} acabou.")
        else:
            await ctx.send("O cargo 'Mutado' não foi encontrado. Por favor, crie o cargo com este nome e configure "
                           "as permissões.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'O usuário {user.mention} foi desbanido.')
            return

    await ctx.send(f'O usuário {member} não está banido.')


@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Mutado")
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f'O usuário {member.mention} foi desmutado.')
    else:
        await ctx.send(f'O usuário {member.mention} não está mutado.')


@bot.command()
async def cara_coroa(ctx, *, texto: str):
    texto.lower()
    if texto in ["cara", "coroa"]:
        opcao_bot = random.choice(["cara", "coroa"])
        valor_final = random.choice(["cara", "coroa"])
        if texto == valor_final and opcao_bot == valor_final:
            await ctx.send("Empate")
        elif texto == valor_final and opcao_bot != valor_final:
            await ctx.send("Vc ganhou")
        elif texto != valor_final and opcao_bot == valor_final:
            await ctx.send("Vc perdeu")
        elif texto != valor_final and opcao_bot != valor_final:
            await ctx.send("Empate")
    else:
        await ctx.send("Por favor, digite 'cara' ou 'coroa'")


@bot.command()
async def dado(ctx):
    await ctx.send(f'Valor do dado é: {random.randint(1, 6)}')


@bot.command()
async def rps(ctx, escolha: str):
    if escolha.lower() in ["pedra", "papel", "tesoura"]:
        opcao_bot = random.choice(["pedra", "papel", "tesoura"])
        if escolha == opcao_bot:
            await ctx.send("Empate")
        elif escolha == "pedra" and opcao_bot == "tesoura":
            await ctx.send("Vc ganhou")
        elif escolha == "papel" and opcao_bot == "pedra":
            await ctx.send("Vc ganhou")
        elif escolha == "tesoura" and opcao_bot == "papel":
            await ctx.send("Vc ganhou")
        else:
            await ctx.send("Vc perdeu")
    else:
        await ctx.send("Por favor, digite 'pedra', 'papel' ou 'tesoura'")


@bot.command()
async def traducao(ctx, *, texto: str):
    translator = Translator()
    detect_language = translator.detect(texto).lang
    translation = translator.translate(texto, src=detect_language, dest='pt')
    await ctx.send(f'A tradução do texto é: {translation.text}')


@bot.command()
async def tempo(ctx, *, cidade: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        translator = Translator()
        detect_language = translator.detect(weather_description).lang
        tempo_descricao = translator.translate(weather_description, src=detect_language, dest='pt')
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        cidade_mod = cidade.capitalize()
        embed = discord.Embed(
            title=f'Tempo para {cidade_mod}',
            description='Tempo do dia de Hoje',
            color=discord.Color.blue()
        )
        embed.add_field(name='Descricão', value=tempo_descricao.text, inline=False)
        embed.add_field(name='Temperatura', value=f'{temperature:.1f}°C', inline=False)
        embed.add_field(name='Humidade', value=f'{humidity}%', inline=False)
        embed.add_field(name='Velocidade do vento', value=f'{wind_speed} m/s', inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Cidade não encontrada!')


bot.run("TOKEN DO BOT")
