import discord
import discord_slash
import pymongo
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash import SlashCommand, SlashContext
from discord.ext import commands, tasks
from discord_slash import SlashContext, ComponentContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType as OptionType
from discord_slash.utils.manage_components import create_actionrow
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandOptionType
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash import ComponentContext
from discord_slash import SlashCommand, SlashContext, SlashCommandOptionType, utils
from discord_slash.utils import manage_components
from discord_slash import SlashContext, SlashCommand, ComponentContext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils import manage_components
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import ButtonStyle

intents = discord.Intents.default()
intents.guilds = True 
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix =";", description = "Fusely", intents=intents)
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

mongo_client = pymongo.MongoClient("") #Lien de votre mongoDB
db = mongo_client["autorole"]
collection = db["autorole"]

@slash.slash(name="autorole",
             description="Activer ou désactiver l'autorole pour les nouveaux membres.",
             options=[
                 {
                     "name": "status",
                     "description": "ON ou OFF",
                     "required": True,
                     "type": SlashCommandOptionType.STRING,
                     "choices": [
                         {
                             "name": "ON",
                             "value": "on"
                         },
                         {
                             "name": "OFF",
                             "value": "off"
                         }
                     ]
                 },
                 {
                     "name": "role",
                     "description": "Le rôle à ajouter automatiquement.",
                     "required": False,
                     "type": SlashCommandOptionType.ROLE
                 }
             ])
@commands.has_permissions(administrator=True)             
async def autorole(ctx: SlashContext, status: str, role: discord.Role = None):
    if not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send("Je n'ai pas les permissions nécessaires pour gérer les rôles.")
        return

    guild_id = str(ctx.guild.id)

    if status.lower() == "on" and role is None:
        await ctx.send("Veuillez spécifier le rôle à ajouter automatiquement.")
        return

    if role and role not in ctx.guild.roles:
        await ctx.send("Le rôle spécifié n'est pas valide.")
        return

    if status.lower() == "on":
        collection.update_one(
            {"guild_id": guild_id},
            {"$set": {"status": status.lower(), "role_id": str(role.id)}},
            upsert=True
        )
        await ctx.send(f"Autorole activé. Les nouveaux membres recevront automatiquement le rôle {role.mention}.")
    elif status.lower() == "off":
        collection.delete_one({"guild_id": guild_id})
        await ctx.send("Autorole désactivé. Les nouveaux membres n'auront plus de rôle ajouté automatiquement.")
    else:
        await ctx.send("Option invalide. Utilisez 'ON' ou 'OFF'.")

@autorole.error
async def autorole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "", description = "", color = ) #Embed d'erreur, couleur & contenu 
        embed.set_footer(text = "") #Footer de l'embed d'erreur
        await ctx.send(embed = embed)  

bot.run('') #Votre token        