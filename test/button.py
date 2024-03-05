import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='??', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def menu(ctx):
    # Envia a mensagem com as opções
    message = await ctx.send("Escolha uma opção:\n"
                              "1️⃣ Botão 1\n"
                              "2️⃣ Botão 2\n"
                              "3️⃣ Botão 3")

    # Adiciona as reações à mensagem
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")

    # Função para verificar se a reação é válida
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣']

    try:
        # Espera a reação do usuário
        reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)

        # Responde com base na reação
        if str(reaction.emoji) == '1️⃣':
            await ctx.send("Você clicou no Botão 1!")
        elif str(reaction.emoji) == '2️⃣':
            await ctx.send("Você clicou no Botão 2!")
        elif str(reaction.emoji) == '3️⃣':
            await ctx.send("Você clicou no Botão 3!")

        # Remove as reações após o usuário clicar
        await message.clear_reactions()
    except TimeoutError:
        await ctx.send("Tempo esgotado! Por favor, tente novamente.")


bot.run("Token")  # Run the bot
