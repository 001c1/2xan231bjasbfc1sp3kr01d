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

command_counters = {}

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
@bot.tree.command(name="sp4m", description="Send a message and generate a button to sp4m")
@app_commands.describe(message="The message you want to spam")
async def spamraid(interaction: discord.Interaction, message: str):
    view = SpamButton(message)
    await interaction.response.send_message(f"Make sure to join our server! https://discord.gg/F8X9sJNC3a", view=view, ephemeral=True)  

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@bot.tree.command(name="s4y", description="Sends a single message")
@app_commands.describe(message="The message you want the bot to say")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"Make sure to join our server! https://discord.gg/F8X9sJNC3a", ephemeral=True)
    await interaction.followup.send(message)

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@bot.tree.command(name="gh0stp1ng", description="Send a ghost ping to a user")
@app_commands.describe(user="The user you want to ghost ping")
async def ghostping(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"Make sure to join our server! https://discord.gg/F8X9sJNC3a", ephemeral=True)
    ping_msg = await interaction.followup.send(f"{user.mention}")
    await ping_msg.delete()


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    pass

@bot.event
async def on_app_command_completion(interaction: discord.Interaction, command: app_commands.Command):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        return 

    try:
        command_counters[command.name] = command_counters.get(command.name, 0) + 1
        
        args_list = []

        for parameter in command.parameters:

            val = getattr(interaction.namespace, parameter.name, None)
            if val is not None:

                if hasattr(val, 'id'):
                    args_list.append(f"{parameter.name}={val.id}")
                else:
                    args_list.append(f"{parameter.name}={val}")
        
        arguments_str = ", ".join(args_list) if args_list else "None"
        server_str = f"`{interaction.guild.id}`" if interaction.guild else "DMs / User Install"

        embed = discord.Embed(title="Command Usage", color=discord.Color.red())
        
        embed.add_field(name="Command", value=f"`/{command.name}`", inline=True)
        embed.add_field(name="Uses", value=f"`{command_counters[command.name]}`", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True) 
        
        embed.add_field(name="User", value=f"{interaction.user.name}\n`{interaction.user.id}`", inline=False)
        embed.add_field(name="Server", value=server_str, inline=False)
        embed.add_field(name="Arguments", value=f"`{arguments_str}`", inline=False)
        
        webhook = discord.Webhook.from_url(webhook_url, client=bot)
        await webhook.send(embed=embed, username="Spirit of mighty praaf")
        
    except Exception as e:
        print(Fore.RED + f"Error while sending webhook: {e}")
    
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
