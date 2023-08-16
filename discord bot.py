# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:34:03 2023

@author: herre
"""
import discord
from discord import app_commands
from discord.ext import commands
from time import sleep
import datetime
import asyncio

error = True
intents = discord.Intents.default()
description = '''Bot Python'''
guild_id = 956596151359000576
bot = commands.Bot(
  command_prefix="§",
  intents = intents
)

intents.message_content = True
intents.guilds = True
intents.members = True

bot.remove_command('help')
bot.remove_command('mute')

###############################################################################################

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

###############################################################################################

@bot.command()
async def help(ctx):
    command = help
    name = ctx.author.name
    date = ctx.message.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{name}] §{command}")
    embed=discord.Embed(title="commandes :", color=0x00ffcc)
    embed.set_author(name="BuddyByte", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon_url="https://cdn.discordapp.com/avatars/985964074972090378/d654bfebebcae133ecedfb0017e7f061.webp")
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/115px-Python-logo-notext.svg.png?20220821155029")
    embed.add_field(name="echo", value="répète le texte suivit mais avec un seul espace entre chaque mot", inline=False)
    embed.add_field(name="ping", value="répond part un pong", inline=False)
    embed.add_field(name="name", value="Donne le nom est la date de la personne qui à envoyé le message", inline=False)
    embed.add_field(name="clear", value="supprime un nombre de message définit tapez 0 pour supprimer tout", inline=False)
    embed.set_footer(text="le préfixe est \"§\"")
    await ctx.send(embed=embed)


@bot.command()
async def echo(ctx, *, args: str):
    command = echo
    name = ctx.author.name
    date = ctx.message.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{name}] §{command} {args}")
    await ctx.send(f"{args}")


@bot.command()
async def ping(ctx):
    command = ping
    name = ctx.author.name
    date = ctx.message.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{name}] §{command}")
    await ctx.send("pong")


@bot.command()
async def name(ctx):
    command = name
    nom = ctx.author.name
    date = ctx.message.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{nom}] §{command}")
    await ctx.send(f"Votre nom est : {nom}\nLa Date du message est : {date}")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
    command = clear
    name = ctx.author.name
    date = ctx.message.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{name}] §{command} {amount}")
    if amount == 0:
        await ctx.channel.purge()
        await ctx.send("tout les message ont été supprimés.")
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)
    else:
        amount += 1
        await ctx.channel.purge(limit=amount)
        amount -= 1
        await ctx.send(f"{amount} message ont été supprimés.")
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} a été banni du serveur.\nRaison = {reason}.")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} a été expulsé du serveur.\nRaison = {reason}.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, *args):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    if not mute_role:
        await ctx.send("Le rôle de mute n'existe pas.")
        return
    
    if len(args) % 2 != 0:
        await ctx.send("Veuillez fournir un délai pour chaque utilisateur.")
        return
    
    for i in range(0, len(args), 2):
        member = discord.utils.get(ctx.guild.members, mention=args[i])
        duration = int(args[i+1])
        
        await member.add_roles(mute_role)
        await ctx.send(f"{member.mention} a été rendu muet pour {duration} secondes.")
        
        await asyncio.sleep(duration)
        await member.remove_roles(mute_role)
        await ctx.send(f"{member.mention} n'est plus muet.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"{member.name} n'est plus muet.")


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Informations sur le serveur",
                          description=f"Nom: {guild.name}\nID: {guild.id}\nRégion: Europe\nPropriétaire: {guild.owner.mention}",
                          color=0x00ffcc)
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Nombre de membres", value=guild.member_count)
    embed.add_field(name="Nombre de rôles", value=len(guild.roles))
    embed.add_field(name="Nombre de salons", value=len(guild.channels))
    await ctx.send(embed=embed)



@bot.event
async def on_ready():
    current_datetime = datetime.datetime.now()
    formated_datetime = current_datetime.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{formated_datetime} [INFO    ] {bot.user.name} ({bot.user.id}) is ready !")
    # argument = bot.tree.clear_commands(guild=None, type=discord.AppCommandType.chat_input)
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=guild_id))
        print(f"{formated_datetime} [INFO    ] Synced {len(synced)} commands")
        synced = await bot.tree.sync()
        print(f"{formated_datetime} [INFO    ] Synced {len(synced)} global commands")

    except Exception as e:
            print(e)
@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = client.get_channel(1130147789431652483)
    await channel.send(f"bonjour {member.mention} et bienvenue à {guild.name}!")
###########################################################################################

# @bot.tree.command(guild=discord.Object(id=guild_id), name="bonjour", description="écrit ton nom et la date de ton message")
# async def name_slash(interaction: discord.Interaction):
#     command = "bonjour"
#     mention = interaction.user.mention
#     nom = interaction.user.name
#     date = interaction.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
#     print(f"{date} [{nom}] /{command}")
#     await interaction.response.send_message(f"Votre nom est : {mention}\nLa Date du message est : {date}", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=guild_id), name="echo", description="répète le message demandé")
@app_commands.describe(message = "Message à répeter")
async def echo_slash(interaction: discord.Interaction, message: str):
    command = "echo"
    nom = interaction.user.name
    date = interaction.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{nom}] /{command} {message}")
    await interaction.response.send_message(f"{message}")

@bot.tree.command(guild=discord.Object(id=guild_id), name="dev-only", description="this command is for the developpers")
async def dev_slash(interaction: discord.Interaction):
    command = "dev-only"
    nom = interaction.user.name
    date = interaction.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{nom}] /{command}")
    argument = None
    await print(f"{argument}")
    await interaction.response.send_message(f"{argument}")

@bot.tree.command(guild=discord.Object(id=guild_id), name="kick", description="kick la personne désigné(e)")
@app_commands.describe(membre = "Personne à kick")
@app_commands.describe(raison = "raison du kick")
async def kick_slash(interaction: discord.Interaction, membre: discord.Member, raison: str):
    command = "kick"
    nom = interaction.user.name
    date = interaction.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{nom}] /{command} {membre} {raison}")
    if interaction.permissions.kick_members:
        await membre.kick(reason=raison)
        await interaction.response.send_message(f"{membre.mention} a été expulsé du serveur.\nRaison = {raison}.", ephemeral=True)
    else:
        print(f"{date} [{nom}] N'a pas la permission \"kick_members\"")
        await interaction.response.send_message("Vous n'avez pas la permission de kicker des utilisateurs !")

@bot.tree.command(guild=discord.Object(id=guild_id), name="ban", description="ban la personne désigné(e)")
@app_commands.describe(membre="personne à Bannir")
@app_commands.describe(raison="raison du Bannissement")
async def ban_slash(interaction: discord.Interaction, membre: discord.Member, raison: str):
    command = "ban"
    nom = interaction.user.name
    date = interaction.created_at.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [{nom}] /{command} {membre} {raison}")
    if interaction.permissions.ban_members == True:
        await membre.ban(reason=raison)
        await interaction.response.send_message(f"{membre.mention} a été banni du serveur.\nRaison = {raison}.")
    else:
        print(f"{date} [{nom}] N'a pas la permission \"ban_members\"")
        await interaction.response.send_message("Vous n'avez pas les permissions pour bannir des utilisateurs")

# @bot.tree.command(guild=discord.Object(id=guild_id), name="mute", description="mute la personne avec un certain temps")
# @app_commands.describe(personne = "Qui voulez vous mute ?")
# @app_commands.describe(time = "combien de temps voulez vous mute la personne ?")
# async def mute_slash(interaction: discord.Interaction, personne: discord.Member, time: int):
#     mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
#     if not mute_role:
#         await interaction.send("Le rôle de mute n'existe pas.")
#         return
    
#     member = discord.utils.get(interaction.guild.members, mention=personne)
#     duration = time*60
    
#     await interaction.member.add_roles(mute_role)
#     await interaction.send(f"{member.mention} a été rendu muet pour {duration} secondes.")
#     await asyncio.sleep(duration)
#     await member.remove_roles(mute_role)
#     await interaction.send(f"{member.mention} n'est plus muet.")

    
###########################################################################################
@bot.event
async def on_command_error(ctx, error):
    current_datetime = datetime.datetime.now()
    date = current_datetime.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{date} [Error] {error}")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande non trouvée. Veuillez vérifier la syntaxe et réessayer.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Argument manquant. Veuillez spécifier tous les arguments nécessaires.")
    else:
        # Gestionnaire d'erreur par défaut
        await ctx.send(f"Une erreur s'est produite : {str(error)}")

"""
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await client.change_presence(status=discord.Status.online, activity=discord.Game("Un jeu bien bizarre ..."))

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if message.content == 'ping':
            print("sending : pong")
            await message.channel.send('pong')
        else:
            print("dont find ping !")
        
        if message.content.startswith('!hello'):
            print("!hello detected")
            await message.reply('Hello!', mention_author=True)
        else:
            print("dont find !hello !")
client = MyClient(intents = intents)
"""
intents.message_content = True


bot.run('A TOKEN')
