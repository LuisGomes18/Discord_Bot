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
    """
    Event handler for the on_ready event.
    
    Prints a message indicating that the bot has successfully logged in.
    The message includes the bot's username.
    """
    print(f"\n\nLogged in as {bot.user.name}\n\n")


bot.run(token)
