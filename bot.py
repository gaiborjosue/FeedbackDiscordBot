from Utils.jsonManipulation import read_or_init_json, update_assignment_json, delete_feedback, assignment_number_not_provided
from Utils.requestExcelFile import fetchExcelFile, requestExcelFile, getGraphData, buildRubric
from Utils.generateBarGraph import generateBarGraph, generatePointGraph

import discord
from discord.ext import commands
from discord import Embed
from discord.file import File
import json
from discord import app_commands

def get_banner_for_server(server_name):
    """Get the appropriate banner for a server based on known servers JSON"""
    try:
        with open('known_servers.json', 'r') as f:
            known_servers = json.load(f)
        
        # Check for exact match first
        if server_name in known_servers:
            return known_servers[server_name]
        
        # Check for partial matches (case-insensitive)
        server_lower = server_name.lower()
        for known_server, banner_path in known_servers.items():
            if known_server.lower() in server_lower or server_lower in known_server.lower():
                return banner_path
        
        # Default banner if no match found
        return "Images/Banner_Default_horiz.png"
        
    except FileNotFoundError:
        # Fallback to hardcoded logic if JSON file doesn't exist
        if "cs617" in server_name.lower():
            return "Images/Banner_617_horiz.png"
        elif "cs666" in server_name.lower():
            return "Images/Banner_666_horiz.png"
        else:
            return "Images/Banner_Default_horiz.png"
    except Exception as e:
        print(f"Error reading known_servers.json: {e}")
        return "Images/Banner_Default_horiz.png"


# Define the intents
# Define the intents
intents = discord.Intents.all()

activity = discord.Game(name="/helpstudent")

client = commands.Bot(command_prefix='!', activity=activity, intents=intents)

# Use the existing command tree
tree = client.tree

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    
    # Sync slash commands
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")
    
    wizard_ascii_legendary_level_feedback_giver_9000 = r"""

   ___             _ _                _      __    __ _                  _ 
  / __\__  ___  __| | |__   __ _  ___| | __ / / /\ \ (_)______ _ _ __ __| |
 / _\/ _ \/ _ \/ _` | '_ \ / _` |/ __| |/ / \ \/  \/ / |_  / _` | '__/ _` |
/ / |  __/  __/ (_| | |_) | (_| | (__|   <   \  /\  /| |/ / (_| | | | (_| |
\/   \___|\___|\__,_|_.__/ \__,_|\___|_|\_\   \/  \/ |_/___\__,_|_|  \__,_|
                                                                           
                                      ....
                                .'' .'''
.                             .'   :
\\                          .:    :
 \\                        _:    :       ..----.._
  \\                    .:::.....:::.. .'         ''.
   \\                 .'  #-. .-######'     #        '.
    \\                 '.##'/ ' ################       :
     \\                  #####################         :
      \\               ..##.-.#### .''''###'.._        :
       \\             :--:########:            '.    .' :
        \\..__...--.. :--:#######.'   '.         '.     :
        :     :  : : '':'-:'':'::        .         '.  .'
        '---'''..: :    ':    '..'''.      '.        :'
           \\  :: : :     '      ''''''.     '.      .:
            \\ ::  : :     '            '.      '      :
             \\::   : :           ....' ..:       '     '.
              \\::  : :    .....####\\ .~~.:.             :
               \\':.:.:.:'#########.===. ~ |.'-.   . '''.. :
                \\    .'  ########## \ \ _.' '. '-.       '''.
                :\\  :     ########   \ \      '.  '-.        :
               :  \\'    '   #### :    \ \      :.    '-.      :
              :  .'\\   :'  :     :     \ \       :      '-.    :
             : .'  .\\  '  :      :     :\ \       :        '.   :
             ::   :  \\'  :.      :     : \ \      :          '. :
             ::. :    \\  : :      :    ;  \ \     :           '.:
              : ':    '\\ :  :     :     :  \:\     :        ..'
                 :    ' \\ :        :     ;  \|      :   .'''
                 '.   '  \\:                         :.''
                  .:..... \\:       :            ..''
                 '._____|'.\\......'''''''.:..'''
    """
    print(wizard_ascii_legendary_level_feedback_giver_9000)

@client.event
async def on_guild_join(guild):
    """Send welcome messages when the bot joins a new server"""
    try:
        # Send welcome message to general channel (for students)
        general_channel = discord.utils.get(guild.channels, name='general')
        
        if general_channel:
            # Create a welcome embed for students
            student_embed = discord.Embed(
                title="🎓 Welcome to Feedback Wizard Bot!",
                description=f"Hello everyone! I'm here to help manage your assignment feedback in **{guild.name}**!",
                color=0x00ff00
            )
            
            # Add student commands section
            student_embed.add_field(
                name="📚 Student Commands (Use in #feedback channel only)",
                value=(
                    "• `/feedback [assignment_number]` - Get your feedback directly via DM\n"
                    "• `/checkassignments` - See all assignments with feedback available\n"
                    "• `/track` - View your grade progression across all assignments\n"
                    "• `/helpstudent` - Show all available student commands"
                ),
                inline=False
            )
            
            # Add important notes
            student_embed.add_field(
                name="⚠️ Important Notes",
                value=(
                    "• **Only use commands in the #feedback channel**\n"
                    "• Use `/feedback` to get your assignment feedback directly in your DMs\n"
                    "• If no assignment number is provided, I'll give you the latest assignment\n"
                    "• Feedback is sent directly to your DMs for privacy\n"
                    "• Staff members have additional commands in the #_staff channel"
                ),
                inline=False
            )
            
            # Add footer
            student_embed.set_footer(text="Need help? Use /helpstudent in the #feedback channel!")
            
            await general_channel.send(embed=student_embed)
            
        else:
            # If no 'general' channel found, try to send to the first text channel
            text_channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages]
            if text_channels:
                await text_channels[0].send(
                    f"🎓 **Feedback Wizard Bot** has joined **{guild.name}**!\n\n"
                    f"Please create a #general channel for welcome messages, and a #feedback channel for student interactions.\n"
                    f"Use `/feedback` to get your assignment feedback!\n"
                    f"Use `/helpstudent` in the #feedback channel to see all available commands!"
                )

        # Send welcome message to staff channel
        staff_channel = discord.utils.get(guild.channels, name='_staff')
        
        if staff_channel:
            # Create a welcome embed for staff
            staff_embed = discord.Embed(
                title="👨‍🏫 Staff Setup Complete!",
                description=f"Feedback Wizard Bot is now ready to manage assignments in **{guild.name}**!",
                color=0xff6b35
            )
            
            # Add staff commands section
            staff_embed.add_field(
                name="🛠️ Staff Commands (Use in #_staff channel only)",
                value=(
                    "• `/newfeedback <assignment_number> <feedback_url>` - Add new assignment feedback\n"
                    "• `/summary <assignment_number> [colors]` - Generate grade distribution graph\n"
                    "• `/feedbacklink <assignment_number>` - Get feedback link for assignment\n"
                    "• `/feedbacklist` - List all available feedback links\n"
                    "• `/deletefeedback <assignment_number>` - Remove assignment feedback\n"
                    "• `/announcefeedback [assignment_number]` - Announce feedback to students\n"
                    "• `/studentfeedback <username> [assignment_number]` - Get student's feedback\n"
                    "• `/trackstudent <username>` - Track student's grade progression\n"
                    "• `/helpstaff` - Show detailed staff help"
                ),
                inline=False
            )
            
            # Add setup instructions
            staff_embed.add_field(
                name="📋 Quick Setup Guide",
                value=(
                    "1. **Upload your Excel file** to oneDrive and grade it :)\n"
                    "2. **Share the link** (make sure it's publicly accessible)\n"
                    "3. **Use `/newfeedback 1 <your_link>`** to add your first assignment\n"
                    "4. **Use `/announcefeedback`** to notify students\n"
                    "5. **Students can then use `/feedback`** in the #feedback channel"
                ),
                inline=False
            )
            
            # Add Excel file requirements
            staff_embed.add_field(
                name="📊 Excel File Requirements",
                value=(
                    "Your Excel file must have these columns:\n"
                    "• **Discord Username** (case-insensitive)\n"
                    "• **Feedback** (the actual feedback text)\n"
                    "• **Grade** or **Points** (for scoring)"
                ),
                inline=False
            )
            
            # Add footer
            staff_embed.set_footer(text="Need help? Use /helpstaff for detailed command information!")
            
            await staff_channel.send(embed=staff_embed)
            
        else:
            # If no staff channel found, mention it in the general message
            if general_channel:
                await general_channel.send(
                    "⚠️ **Staff Notice**: Please create a `#_staff` channel for staff-only commands!"
                )
                
    except Exception as e:
        print(f"Error sending welcome messages to {guild.name}: {e}")

##### Owner Red Button Shutdown ######











##### Owner Red Button Shutdown ######
@client.command(aliases=["DO_NOT_PRESS", "kill", "fireball"])
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("I have been attacked! I'm going down! *screams*, *explosion*, *silence*, *crickets*, *tumbleweed*, *more silence*, *even more silence*, *the end*, *credits*, *post-credits scene*")
    exit()

##### SLASH COMMANDS #####

@tree.command(name="feedback", description="Get feedback for an assignment")
@app_commands.describe(assignment_number="The assignment number (optional - will use latest if not provided)")
async def slash_feedback(interaction: discord.Interaction, assignment_number: int = None):
    """Slash command for getting feedback directly via DM"""
    allowed_channels = ['feedback', "_staff"]
    server_name = interaction.guild.name

    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #feedback channel.", ephemeral=True)
        return

    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
        return

    try:
        # Get user feedback directly
        result = requestExcelFile(feedback_file, interaction, grade=True)
        
        # Check if result is an exception (error case)
        if isinstance(result, Exception):
            await interaction.response.send_message("❌ There was a problem retrieving the feedback.", ephemeral=True)
            return
        
        # Unpack the result safely
        user_feedback, user_grade = result
        
        if user_feedback.size > 0:
            feedback_text = user_feedback[0]
            
            if len(feedback_text) <= 1024:
                embed = Embed(title=f"Feedback for Assignment {assignment_number} - Score={user_grade[0] if len(user_grade) > 0 else 'N/A'}", color=0xFF914D)
                
                # Set banner based on server using the helper function
                banner_path = get_banner_for_server(server_name)
                banner_url = f"https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/{banner_path}"
                embed.set_image(url=banner_url)
                
                embed.add_field(name=f"Feedback for Assignment #{assignment_number}", value=feedback_text, inline=False)
                
                await interaction.user.send(embed=embed)
                await interaction.response.send_message("✅ Feedback sent to your DMs!", ephemeral=True)
            else:
                # Long feedback - send as text
                banner_path = get_banner_for_server(server_name)
                banner_url = f"https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/{banner_path}"
                
                grade_text = user_grade[0] if len(user_grade) > 0 else 'N/A'
                await interaction.user.send(banner_url + "\n\n" + f"Score={grade_text}" + "\n\n" + feedback_text)
                await interaction.response.send_message("✅ Feedback sent to your DMs!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No feedback found for this user :(", ephemeral=True)
            
    except Exception as e:
        print(f"Error in feedback command: {e}")
        await interaction.response.send_message("❌ There was a problem retrieving the feedback.", ephemeral=True)

@tree.command(name="checkassignments", description="List all assignments with feedback available")
async def slash_checkassignments(interaction: discord.Interaction):
    """Slash command for checking available assignments"""
    allowed_channels = ['feedback', "_staff"]
    server_name = interaction.guild.name

    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #feedback channel.", ephemeral=True)
        return

    data = read_or_init_json()
    assignments = data.get(server_name, {})

    embed = discord.Embed(title="📚 Assignments Ready for Feedback", color=0x00ff00)
    embed.add_field(name="Info", value="These are the assignments already posted and ready with your feedback.", inline=False)

    if assignments:
        for num in assignments.keys():
            embed.add_field(name=f"Assignment {num}", value=":white_check_mark:", inline=False)
        embed.set_footer(text="Use /feedback <assignment_number> to get the feedback!")
    else:
        embed.description = "No assignments with feedback available yet."

    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="track", description="View your grade progression across all assignments")
async def slash_track(interaction: discord.Interaction):
    """Slash command for tracking grades"""
    allowed_channels = ['feedback', "_staff", "general"]
    server_name = interaction.guild.name

    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #feedback, #_staff, or #general channels.", ephemeral=True)
        return

    data = read_or_init_json()
    assignments = data.get(server_name, {})

    try:
        grades = []
        for assignment_number, feedback_file in assignments.items():
            user_feedback, user_grade = requestExcelFile(feedback_file, interaction, grade=True)
            grades.append(user_grade[0])

        if grades:
            title = "Grades Summary"
            xlabel = "Assignments"
            ylabel = "Grades"
            graph = generatePointGraph(list(range(1, len(grades)+1)), grades, title, xlabel, ylabel, "black", "#5192EA", "white")

            await interaction.response.send_message(file=File(graph, filename="grades_summary.png"), ephemeral=True)
        else:
            await interaction.response.send_message("❌ No grades available yet.", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message("❌ There was a problem retrieving the grades.", ephemeral=True)

@tree.command(name="helpstudent", description="Show all available student commands")
async def slash_helpstudent(interaction: discord.Interaction):
    """Slash command for student help"""
    allowed_channels = ['feedback', "_staff"]

    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #feedback channel.", ephemeral=True)
        return

    embed = Embed(title="📚 Student Commands", description="Here are the commands available for students:", color=0x00ff00)
    embed.add_field(name="/feedback [assignment_number]", value="Get the feedback for a specific assignment directly via DM.", inline=False)
    embed.add_field(name="/checkassignments", value="List all the assignments that have feedback available.", inline=False)
    embed.add_field(name="/track", value="View your grade progression across all assignments.", inline=False)
    embed.add_field(name="/helpstudent", value="Show this help message.", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

##### STAFF SLASH COMMANDS #####

def has_staff_role(interaction: discord.Interaction) -> bool:
    """Check if user has staff role"""
    staff_role = discord.utils.get(interaction.guild.roles, name='staff')
    if not staff_role:
        return False
    return staff_role in interaction.user.roles

@tree.command(name="newfeedback", description="Add new assignment feedback (Staff only)")
@app_commands.describe(
    assignment_number="The assignment number",
    feedback_file="URL to the Excel file with feedback",
    announce="Whether to announce the feedback to students (default: true)"
)
async def slash_newfeedback(interaction: discord.Interaction, assignment_number: int, feedback_file: str, announce: bool = True):
    """Slash command for adding new feedback"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    server_name = interaction.guild.name

    try:
        x, y = getGraphData(feedback_file)

        if x and y:
            update_assignment_json(server_name, assignment_number, feedback_file)
            await interaction.response.send_message(f"✅ Assignment {assignment_number} feedback link updated.", ephemeral=True)

            if announce:
                channel = discord.utils.get(interaction.guild.channels, name="feedback")
                if channel:
                    await channel.send(f"Hello @everyone feedback for assignment {assignment_number} is ready :tada:! Use `/feedback {assignment_number}` to get it.", file=File("Images/spongebob.gif"))
        else:
            await interaction.response.send_message(f"❌ Assignment {assignment_number} feedback link not valid.", ephemeral=True)
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Assignment {assignment_number} feedback link not valid.", ephemeral=True)

@tree.command(name="summary", description="Generate grade distribution graph (Staff only)")
@app_commands.describe(
    assignment_number="The assignment number (optional - will use latest if not provided)",
    background_color="Background color for the graph (default: black)",
    bar_color="Bar color for the graph (default: #5192EA)",
    label_color="Label color for the graph (default: white)"
)
async def slash_summary(interaction: discord.Interaction, assignment_number: int = None, background_color: str = "black", bar_color: str = "#5192EA", label_color: str = "white"):
    """Slash command for generating grade distribution graphs"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    server_name = interaction.guild.name
    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
        return

    try:
        x, y = getGraphData(feedback_file)

        if x and y:
            title = f"Assignment #{assignment_number}"
            xlabel = "Points"
            ylabel = "Number of Students"
            graph = generateBarGraph(x, y, title, xlabel, ylabel, background_color, bar_color, label_color)

            await interaction.response.send_message(file=File(graph, filename="grade_distribution.png"))
        else:
            await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
            
    except Exception as e:
        await interaction.response.send_message("❌ There was a problem retrieving the grading distribution graph.", ephemeral=True)

@tree.command(name="feedbacklink", description="Get feedback link for assignment (Staff only)")
@app_commands.describe(assignment_number="The assignment number (optional - will use latest if not provided)")
async def slash_feedbacklink(interaction: discord.Interaction, assignment_number: int = None):
    """Slash command for getting feedback links"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    server_name = interaction.guild.name
    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
        return

    await interaction.response.send_message(f"📋 Feedback for assignment {assignment_number}: {feedback_file}", ephemeral=True)

@tree.command(name="feedbacklist", description="List all available feedback links (Staff only)")
async def slash_feedbacklist(interaction: discord.Interaction):
    """Slash command for listing all feedback"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    server_name = interaction.guild.name
    data = read_or_init_json()

    if data and server_name in data and data[server_name]:
        feedback_list = "\n".join([f"Assignment {assignment_number}: {url}" for assignment_number, url in data[server_name].items()])
        await interaction.response.send_message(f"📋 Available feedback:\n{feedback_list}", ephemeral=True)
    else:
        await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)

@tree.command(name="deletefeedback", description="Delete feedback link for assignment (Staff only)")
@app_commands.describe(assignment_number="The assignment number to delete")
async def slash_deletefeedback(interaction: discord.Interaction, assignment_number: int):
    """Slash command for deleting feedback"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    server_name = interaction.guild.name

    if delete_feedback(assignment_number, server_name):
        await interaction.response.send_message(f"✅ Assignment {assignment_number} feedback link deleted.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Assignment {assignment_number} feedback link not found.", ephemeral=True)

@tree.command(name="announcefeedback", description="Announce feedback to students (Staff only)")
@app_commands.describe(assignment_number="The assignment number (optional - will use latest if not provided)")
async def slash_announcefeedback(interaction: discord.Interaction, assignment_number: int = None):
    """Slash command for announcing feedback"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    server_name = interaction.guild.name
    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
        return

    try:
        channel = discord.utils.get(interaction.guild.channels, name="feedback")
        if channel:
            await channel.send(f"Hello @everyone feedback for assignment {assignment_number} is ready :tada:! Use `/feedback {assignment_number}` to get it.", file=File("Images/spongebob.gif"))
            await interaction.response.send_message(f"✅ Announced feedback for assignment {assignment_number} to students.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Could not find #feedback channel.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("❌ There was a problem announcing the feedback.", ephemeral=True)

@tree.command(name="studentfeedback", description="Get feedback for a specific student (Staff only)")
@app_commands.describe(
    username="The student's Discord username",
    assignment_number="The assignment number (optional - will use latest if not provided)"
)
async def slash_studentfeedback(interaction: discord.Interaction, username: str, assignment_number: int = None):
    """Slash command for getting student feedback"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    server_name = interaction.guild.name
    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await interaction.response.send_message("❌ No feedback available yet.", ephemeral=True)
        return

    try:
        user_feedback, user_grade = requestExcelFile(feedback_file, interaction, username, grade=True)

        if user_feedback.size > 0:
            feedback_text = user_feedback[0]
            if len(feedback_text) <= 1024:
                embed = Embed(title=f"Feedback for Assignment {assignment_number} - Score={user_grade}", color=0xFF914D)

                banner_path = get_banner_for_server(interaction.guild.name)
                embed.set_image(url=f"https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/{banner_path}")

                embed.add_field(name=f"Feedback for Assignment #{assignment_number}", value=user_feedback[0], inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                banner_path = get_banner_for_server(interaction.guild.name)
                banner_url = f"https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/{banner_path}"
                
                await interaction.response.send_message(banner_url + "\n\n" + f"Score={user_grade}" + "\n\n" + feedback_text, ephemeral=True)
        else:
            await interaction.response.send_message("❌ No feedback found for this user :(", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message("❌ There was a problem retrieving the feedback.", ephemeral=True)

@tree.command(name="trackstudent", description="Track a student's grade progression (Staff only)")
@app_commands.describe(username="The student's Discord username")
async def slash_trackstudent(interaction: discord.Interaction, username: str):
    """Slash command for tracking student grades"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    server_name = interaction.guild.name
    data = read_or_init_json()
    assignments = data.get(server_name, {})

    try:
        grades = []
        for assignment_number, feedback_file in assignments.items():
            user_feedback, user_grade = requestExcelFile(feedback_file, interaction, username, grade=True)
            grades.append(user_grade[0])

        if grades:
            title = "Grades Summary"
            xlabel = "Assignments"
            ylabel = "Grades"
            graph = generatePointGraph(list(range(1, len(grades)+1)), grades, title, xlabel, ylabel, "black", "#5192EA", "white")

            await interaction.response.send_message(file=File(graph, filename="grades_summary.png"), ephemeral=True)
        else:
            await interaction.response.send_message("❌ No grades available yet.", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message("❌ There was a problem retrieving the grades.", ephemeral=True)

@tree.command(name="helpstaff", description="Show all available staff commands (Staff only)")
async def slash_helpstaff(interaction: discord.Interaction):
    """Slash command for staff help"""
    if not has_staff_role(interaction):
        await interaction.response.send_message("❌ This command requires the 'staff' role.", ephemeral=True)
        return
    
    allowed_channels = ['_staff']
    if interaction.channel.name not in allowed_channels:
        await interaction.response.send_message("❌ This command can only be used in the #_staff channel.", ephemeral=True)
        return

    embed = Embed(title="🛠️ Staff Commands", description="Here are the commands available for staff:", color=0x00ff00)
    embed.add_field(name="/newfeedback <assignment_number> <feedback_url>", value="Add new assignment feedback.", inline=False)
    embed.add_field(name="/summary <assignment_number> [colors]", value="Generate grade distribution graph.", inline=False)
    embed.add_field(name="/feedbacklink <assignment_number>", value="Get feedback link for assignment.", inline=False)
    embed.add_field(name="/feedbacklist", value="List all available feedback links.", inline=False)
    embed.add_field(name="/deletefeedback <assignment_number>", value="Delete feedback link for assignment.", inline=False)
    embed.add_field(name="/announcefeedback [assignment_number]", value="Announce feedback to students.", inline=False)
    embed.add_field(name="/studentfeedback <username> [assignment_number]", value="Get student's feedback.", inline=False)
    embed.add_field(name="/trackstudent <username>", value="Track student's grade progression.", inline=False)
    embed.add_field(name="/helpstaff", value="Show this help message.", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)