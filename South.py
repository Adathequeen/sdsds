import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import os
import asyncio  # Import asyncio for sleep

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.guild_messages = True
intents.guild_reactions = True
intents.typing = True  # Enable typing intent

bot = commands.Bot(command_prefix="?", intents=intents)

user_ticket_mapping = {}  # Dictionary to map users to their ticket channels
custom_commands = {}  # Dictionary to store custom commands



# File paths
TICKET_SAVE_FILE = "ticket_mappings.json"
COMMAND_SAVE_FILE = "custom_commands.json"
CONNECT_MESSAGE_FILE = "connect_message.json"
CLOSE_EMBED_FILE = "close_embed.json"
# Replace these with your actual server's details
GUILD_ID = 1278754132991152210  # Your server's ID
TICKET_CATEGORY_ID = 1279033352095137862  # ID of the category where tickets should be created

# Custom user and icon for automated messages
CUSTOM_USER_NAME = "South African Airways Helpdesk"
CUSTOM_AVATAR_URL = "https://media.discordapp.net/attachments/1278684214337994914/1278820990746492951/Screenshot_2024-08-29_231113.png?ex=66d2325b&is=66d0e0db&hm=4b93e2e5f9dc13a1eb15d7adae90334162ee975432fcaa82ef545437f56b1272&=&format=webp&quality=lossless&width=685&height=453"



connect_message = "# <:saalogo2:1278761927522123921>  South African Helpdesk.\n\u2570 ***Unjani***, thank you for contacting South African support. Please select the appropriate support category for your inquiry.\n\n<:AFarrow:1278689990200524892>  1. Staffing Enquiry\n<:AFarrow:1278689990200524892> 2. General Enquiry\n<:AFarrow:1278689990200524892> 3. Rank Request Enquiry\n<:AFarrow:1278689990200524892> 4. Application Enquiry\n<:AFarrow:1278689990200524892> 5. Affiliate Request"

def load_ticket_mappings():
    if os.path.exists(TICKET_SAVE_FILE):
        with open(TICKET_SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_ticket_mappings():
    with open(TICKET_SAVE_FILE, "w") as f:
        json.dump(user_ticket_mapping, f)

def load_custom_commands():
    if os.path.exists(COMMAND_SAVE_FILE):
        with open(COMMAND_SAVE_FILE, "r") as f:
            try:
                commands = json.load(f)
                print(f"Loaded commands: {commands}")  # Debug print
                return commands
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file: {e}")
                return {}
    return {}

def save_custom_commands():
    try:
        with open(COMMAND_SAVE_FILE, "w") as f:
            json.dump(custom_commands, f)
    except IOError as e:
        print(f"Failed to save custom commands: {e}")

def load_connect_message():
    global connect_message
    if os.path.exists(CONNECT_MESSAGE_FILE):
        try:
            with open(CONNECT_MESSAGE_FILE, "r") as f:
                data = json.load(f)
                connect_message = data.get("message", connect_message)
                print(f"Loaded connect message: {connect_message}")  # Debugging line
        except (IOError, json.JSONDecodeError) as e:
            print(f"Failed to load connect message: {e}")
    else:
        print(f"Connect message file not found. Using default message.")

def save_connect_message():
    with open(CONNECT_MESSAGE_FILE, "w") as f:
        json.dump({"message": connect_message}, f)

def load_close_embed_customization():
    global close_embed_customization
    if os.path.exists(CLOSE_EMBED_FILE):
        with open(CLOSE_EMBED_FILE, "r") as f:
            close_embed_customization.update(json.load(f))

def save_close_embed_customization():
    with open(CLOSE_EMBED_FILE, "w") as f:
        json.dump(close_embed_customization, f)

# Default close embed customization
close_embed_customization = {
    "title": "Thread Closed",
    "description": "Resolved.",
    "footer_text": "Replying will create a new thread",
    "footer_image": "https://media.discordapp.net/attachments/1227746298258784346/1279013696210993172/discord_fake_avatar_decorations_1725011012974.gif?ex=66d2e5d4&is=66d19454&hm=e9543e2c4d4a03f80ffc44ffee0693b2e325a6909aad7424b18d3322dbd6d741&=&width=360&height=360"
}

# Load customization on bot start
load_close_embed_customization()

@bot.event
async def on_ready():
    global user_ticket_mapping, custom_commands
    user_ticket_mapping = load_ticket_mappings()
    custom_commands = load_custom_commands()
    load_connect_message()
    print(f"Logged in as {bot.user}")

class TicketButtons(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="⛥", style=discord.ButtonStyle.primary, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = bot.get_guild(GUILD_ID)
        category = guild.get_channel(TICKET_CATEGORY_ID)

        if self.user_id in user_ticket_mapping:
            ticket_channel = bot.get_channel(user_ticket_mapping[self.user_id])
            await interaction.response.send_message("You already have an open ticket.", ephemeral=True)
        else:
            ticket_channel = await guild.create_text_channel(
                name=f'ticket-{interaction.user.name}',
                category=category,
                topic=f'Ticket for {interaction.user.mention} ({interaction.user.id})'
            )
            user_ticket_mapping[self.user_id] = ticket_channel.id
            save_ticket_mappings()

            embed = discord.Embed(
                title="<:saslogo3:1278762299154235493> DRAAD GESKEP | THREAD CREATED",
                description="Unjani, thanks for getting in touch. We've received your support ticket and a support agent will be with you shortly to address your inquiry. Your patience is greatly appreciated, and we look forward to assisting you. While you wait, please check our Frequently Asked Questions to check to see if your question has already been answered.‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  <:AFarrow:1278689990200524892> https://bit.ly/afrfrequently",
                color=discord.Color(int('313338', 16))  # Dark Red hex color
            )
            await interaction.user.send(embed=embed)

            embed = discord.Embed(
                title="New Ticket",
                description=f"A new ticket has been opened by {interaction.user.mention}",
                color=discord.Color(int('313338', 16))  # Blue hex color
            )
            await ticket_channel.send(embed=embed)

            # Send the connect message to the user's DM
            connect_embed = discord.Embed(
                description=connect_message.replace("?reply ", ""),
                color=discord.Color(int('313338', 16)),  # Blue hex color
                timestamp=interaction.message.created_at
            )
            connect_embed.set_author(name=CUSTOM_USER_NAME, icon_url=CUSTOM_AVATAR_URL)
            connect_embed.set_footer(text=f"Response • {interaction.message.created_at.strftime('%m/%d/%Y %I:%M %p')}")
            try:
                await interaction.user.send(embed=connect_embed)
            except discord.Forbidden:
                print(f"Failed to send connect message to {interaction.user.id}")

            # Also send the connect message to the ticket channel
            await ticket_channel.send(embed=connect_embed)

            # Add the Close button to the ticket channel
            close_button = CloseTicketButton()
            await ticket_channel.send("Click the button below to close the ticket.", view=close_button)

            # Disable the buttons after use
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view=self)

            await interaction.response.send_message("Ticket has been opened.", ephemeral=True)

    @discord.ui.button(label="⛥", style=discord.ButtonStyle.danger, custom_id="cancel_ticket")
    async def cancel_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Disable the buttons after use
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await interaction.response.send_message("Ticket creation has been canceled.", ephemeral=True)


    @discord.ui.button(label="⛥", style=discord.ButtonStyle.danger, custom_id="cancel_ticket")
    async def cancel_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ticket creation has been canceled.", ephemeral=True)

class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Setting timeout to None makes the view persistent

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if the interaction channel is a ticket channel
        if interaction.channel and interaction.channel.id in user_ticket_mapping.values():
            # Find the user ID associated with the ticket channel
            user_id = next((user_id for user_id, channel_id in user_ticket_mapping.items() if channel_id == interaction.channel.id), None)
            
            if user_id:
                # Check if the user closing the ticket is the ticket owner or has admin permissions
                if interaction.user.id == user_id or interaction.user.guild_permissions.administrator:
                    # Create and send the customized embed
                    close_embed = discord.Embed(
                        title=close_embed_customization["title"],
                        description=close_embed_customization["description"],
                        color=discord.Color.red(),
                        timestamp=interaction.message.created_at
                    )
                    close_embed.set_footer(
                        text=close_embed_customization["footer_text"],
                        icon_url=close_embed_customization["footer_image"]
                    )

                    try:
                        user = bot.get_user(user_id)
                        if user:
                            await user.send(embed=close_embed)
                    except discord.Forbidden:
                        print(f"Failed to send close message to {user_id}")

                    await interaction.response.send_message("Closing the ticket. Goodbye!", ephemeral=True)

                    # Remove the ticket mapping and save the updated mappings
                    del user_ticket_mapping[user_id]
                    save_ticket_mappings()

                    # Delete the ticket channel
                    await interaction.channel.delete()
                else:
                    error_embed = discord.Embed(
                        title="Error",
                        description="You do not have permission to close this ticket.",
                        color=discord.Color.red()
                    )
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)
            else:
                error_embed = discord.Embed(
                    title="Error",
                    description="This ticket is not correctly associated with any user.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
        else:
            error_embed = discord.Embed(
                title="Error",
                description="This ticket is not associated with a valid channel.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


@bot.event
async def on_message(message):
    # Check if the message is from a DM and is not from the bot itself
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        try:
            # Add a custom reaction to the user's message
            await message.add_reaction('<:AFYes:1278699122446307349>')
        except discord.Forbidden:
            print(f"Could not add reaction to message from {message.author}")

        if message.author.id in user_ticket_mapping:
            ticket_channel = bot.get_channel(user_ticket_mapping[message.author.id])
            if ticket_channel:
                # Create an embed for the message using a color hex code
                embed = discord.Embed(
                    title=f"Message from {message.author}",
                    description=message.content,
                    color=discord.Color(int('313338', 16))  # Replace '#3498db' with any hex code
                )
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                embed.set_footer(text=f"User ID: {message.author.id}")
                await ticket_channel.send(embed=embed)
        else:
            # If no open ticket, prompt user to create one
            view = TicketButtons(user_id=message.author.id)
            embed = discord.Embed(
                title="<:saalogo:1278823379129991300> Are you sure you'd like to be connected to the Helpline?",
                description="*Please confirm whether you'd like to be connected to a Helpline agent who can assist you with your inquiries*.",
                color=discord.Color(int('313338', 16))  # Use hex color code for red
            )
            await message.channel.send(embed=embed, view=view)

    # Ensure commands are still processed
    await bot.process_commands(message)

@bot.command()
async def reply(ctx, *, response):
    if ctx.channel.id in user_ticket_mapping.values():
        user_id = next((user_id for user_id, channel_id in user_ticket_mapping.items() if channel_id == ctx.channel.id), None)
        
        if user_id:
            user = bot.get_user(user_id)
            if user:
                try:
                    embed = discord.Embed(
                        description=response,
                        color=discord.Color.orange(),
                        timestamp=ctx.message.created_at
                    )
                    embed.set_author(
                        name=f"{ctx.author}",
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url,
                        url=f"https://discord.com/users/{ctx.author.id}"
                    )
                    embed.set_footer(text=f"Customer • {ctx.message.created_at.strftime('%m/%d/%Y %I:%M %p')}")
                    await user.send(embed=embed)
                    
                    confirmation_embed = discord.Embed(
                        title="Reply Sent",
                        description=f"Replied to {user.mention}",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=confirmation_embed)
                except discord.Forbidden:
                    error_embed = discord.Embed(
                        title="Error",
                        description="Failed to send the message. The user might have DMs disabled.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=error_embed)
            else:
                error_embed = discord.Embed(
                    title="Error",
                    description="User not found. The user may have left the server.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
        else:
            error_embed = discord.Embed(
                title="Error",
                description="User not found. This ticket is not correctly associated with any user.",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
    else:
        error_embed = discord.Embed(
            title="Error",
            description="This command can only be used in a ticket channel.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)

@bot.command()
async def connect(ctx):
    if ctx.channel.id in user_ticket_mapping.values():
        user_id = next((user_id for user_id, channel_id in user_ticket_mapping.items() if channel_id == ctx.channel.id), None)
        
        if user_id:
            user = bot.get_user(user_id)
            if user:
                try:
                    embed = discord.Embed(
                        description=connect_message.replace("?reply ", ""),
                        color=discord.Color.blue(),
                        timestamp=ctx.message.created_at
                    )
                    embed.set_author(name=CUSTOM_USER_NAME, icon_url=CUSTOM_AVATAR_URL)
                    embed.set_footer(text=f"Response • {ctx.message.created_at.strftime('%m/%d/%Y %I:%M %p')}")
                    await user.send(embed=embed)
                    
                    confirmation_embed = discord.Embed(
                        title="Automated Message Sent",
                        description=f"Sent to {user.mention}",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=confirmation_embed)
                except discord.Forbidden:
                    error_embed = discord.Embed(
                        title="Error",
                        description="Failed to send the message. The user might have DMs disabled.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=error_embed)
            else:
                error_embed = discord.Embed(
                    title="Error",
                    description="User not found. The user may have left the server.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
        else:
            error_embed = discord.Embed(
                title="Error",
                description="User not found. This ticket is not correctly associated with any user.",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
    else:
        error_embed = discord.Embed(
            title="Error",
            description="This command can only be used in a ticket channel.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def edit_connect_message(ctx, *, new_message):
    global connect_message
    connect_message = new_message
    save_connect_message()
    confirmation_embed = discord.Embed(
        title="Connect Message Updated",
        description=f"The new connect message is:\n\n{new_message}",
        color=discord.Color.green()
    )
    await ctx.send(embed=confirmation_embed)
    print(f"Updated connect message to: {new_message}")  # Debugging line

@bot.command()
@commands.has_permissions(administrator=True)
async def create_command(ctx, name: str, *, message: str):
    custom_commands[name] = {
        "message": message,
        "color": "#00FF00"
    }
    save_custom_commands()
    await ctx.send(f"Custom command '{name}' created.")
    print(f"Created command: {name} with message: {message}")

@bot.command()
@commands.has_permissions(administrator=True)
async def edit_command(ctx, name: str, *, message: str):
    if name in custom_commands:
        custom_commands[name]["message"] = message
        save_custom_commands()
        await ctx.send(f"Custom command '{name}' updated.")
        print(f"Updated command: {name} with new message: {message}")
    else:
        await ctx.send(f"Custom command '{name}' does not exist.")
        print(f"Attempted to update non-existent command: {name}")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_command_color(ctx, name: str, color: str):
    if name in custom_commands:
        custom_commands[name]["color"] = color
        save_custom_commands()
        await ctx.send(f"Custom command '{name}' color updated.")
    else:
        await ctx.send(f"Custom command '{name}' does not exist.")

@bot.command()
async def ex(ctx, name: str):
    if ctx.channel.id in user_ticket_mapping.values():
        user_id = next((user_id for user_id, channel_id in user_ticket_mapping.items() if channel_id == ctx.channel.id), None)
        
        if user_id and name in custom_commands:
            user = bot.get_user(user_id)
            cmd = custom_commands[name]

            embed = discord.Embed(
                description=cmd["message"],
                color=int(cmd["color"].strip('#'), 16)
            )
            embed.set_author(name=CUSTOM_USER_NAME, icon_url=CUSTOM_AVATAR_URL)
            embed.set_footer(text=f"Response • {discord.utils.format_dt(ctx.message.created_at, 'F')}")

            if user:
                try:
                    await user.send(embed=embed)
                    # Also send the command message to the ticket channel
                    ticket_channel = ctx.channel
                    await ticket_channel.send(embed=embed)
                    await ctx.send("The command has been executed and sent to the user.")
                except discord.Forbidden:
                    await ctx.send("I can't send a DM to the user. Please make sure their DMs are open.")
            else:
                await ctx.send("User not found.")
        else:
            await ctx.send("Custom command not found or this is not a ticket channel.")
    else:
        await ctx.send("This command can only be used in a ticket channel.")

@bot.command(name='commands')
async def list_custom_commands(ctx):
    if custom_commands:
        embed = discord.Embed(
            title="Custom Commands",
            description="Here are all the available custom commands:",
            color=discord.Color.blue()
        )

        for command_name in custom_commands.keys():
            embed.add_field(name=command_name, value=f"Use ?ex {command_name} to execute", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("There are no custom commands available.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # Set the bot's status to "Watching YouTube"
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="South Africa Airways"))


user_ticket_mapping = load_ticket_mappings()
custom_commands = load_custom_commands()

# Load the bot token from an environment variable or a file for security reasons
bot.run("MTI3ODgwMDM1OTQyNjM1OTMzMA.GTXUIh._1UmzjwW4visk68GC8lCRMYioaq9xzeoZKFQU4")