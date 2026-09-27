import discord
from discord.ext import commands
from discord import app_commands
import os
from colorama import init, Fore

init(autoreset=True)

def display_logo():
    logo = '''
█▄░█ █▄░█ █▀█ █▄▄ █▀█ █▀▄ █▄█ █▄█ █▄▀ ▄█ █░░ █░░ █▀▀ █▀█
█░▀█ █░▀█ █▄█ █▄█ █▄█ █▄▀ ░█░ ░█░ █░█ ░█ █▄▄ █▄▄ ██▄ █▀▄
'''
    os.system('cls' if os.name == 'nt' else 'clear')  
    print(Fore.RED + logo)

def display_status(connected):
    if connected:
        print(Fore.GREEN + "Status: Connected")
    else:
        print(Fore.RED + "Status: Disconnected")

intents = discord.Intents.default()
intents.messages = True  
intents.message_content = True  
intents.typing = False  
intents.presences = False  

bot = commands.Bot(
    command_prefix="!", 
    intents=intents, 
    allowed_mentions=discord.AllowedMentions(everyone=True)
)

class SpamButton(discord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Spam", style=discord.ButtonStyle.red)
    async def spam_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()  
        for _ in range(5):  
            await interaction.followup.send(self.message)  

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@bot.tree.command(name="spam", description="Send a message and generate a button to spam")
@app_commands.describe(message="The message you want to spam")
async def spamraid(interaction: discord.Interaction, message: str):
    view = SpamButton(message)
    await interaction.response.send_message(f"Make sure to join our server! https://discord.gg/F8X9sJNC3a", view=view, ephemeral=True)  

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@bot.tree.command(name="say", description="Sends a single message")
@app_commands.describe(message="The message you want the bot to say")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"Make sure to join our server! https://discord.gg/F8X9sJNC3a", ephemeral=True)
    await interaction.followup.send(message)

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@bot.tree.command(name="ghostping", description="Send a ghost ping to a user")
@app_commands.describe(user="The user you want to ghost ping")
async def ghostping(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"Make sure to join our server! https://discord.gg/F8X9sJNC3a", ephemeral=True)
    ping_msg = await interaction.followup.send(f"{user.mention}")
    await ping_msg.delete()
    
@bot.event
async def on_ready():
    display_logo()
    display_status(True)
    print("Connected as " + Fore.YELLOW + f"{bot.user}")

    try:
        await bot.tree.sync()  
        print(Fore.GREEN + "Commands successfully synchronized.")
    except Exception as e:
        display_status(False)
        print(Fore.RED + f"Error during synchronization: {e}")

if __name__ == "__main__":
    # Получаем заранее заданный токен из переменных окружения
    TOKEN = os.getenv("BOT_TOKEN")
    
    if TOKEN:
        try:
            bot.run(TOKEN)
        except discord.errors.LoginFailure:
            print(Fore.RED + "Can't connect to token. Please check your BOT_TOKEN variable.")
        except Exception as e:
            print(Fore.RED + f"An unexpected error occurred: {e}")
    else:
        print(Fore.RED + "❌ Error: BOT_TOKEN environment variable is not set.")
