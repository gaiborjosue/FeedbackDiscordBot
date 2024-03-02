from Utils.jsonManipulation import read_or_init_json, update_assignment_json, delete_feedback, assignment_number_not_provided
from Utils.requestExcelFile import requestExcelFile, getGraphData, buildRubric
from Utils.generateBarGraph import generateBarGraph

import discord
from discord.ext import commands
from discord import Embed
from discord.file import File
import json


# Define the intents
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

activity = discord.Game(name="!helpstudent")

client = commands.Bot(command_prefix='!', activity=activity, intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    wizard_ascii_legendary_level_feedback_giver_9000 = """

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

##### STAFF INTERFACE #####

@client.command(aliases=["new_feedback"])
async def newfeedback(ctx, assignment_number: str = None, feedback_file: str = None):
    server_name = ctx.guild.name
    allowed_channels = ['_staff']
    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    if assignment_number is not None:
        assignment_number = int(assignment_number)

    # Update the JSON file with the new feedback URL
    update_assignment_json(server_name, assignment_number, feedback_file)
    await ctx.send(f"Assignment {assignment_number} feedback link updated.")

@client.command(aliases=["summarygraph", "graphsummary", "graph_summary", "summary_graph"])
async def summary(ctx, assignment_number: str = None, background_color: str = "black", bar_color: str = "#5192EA", label_color: str = "white"):
    server_name = ctx.guild.name
    allowed_channels = ['_staff']

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
        
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await ctx.send("No feedback available yet.")
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await ctx.send("No feedback available yet.")
        return

    try:
        x, y = getGraphData(feedback_file)

        if x and y:
            title = f"Assignment #{assignment_number}"
            xlabel = "Points"
            ylabel = "Number of Students"
            graph = generateBarGraph(x, y, title, xlabel, ylabel, background_color, bar_color, label_color)

            await ctx.send(file=File(graph, filename="grade_distribution.png"))
        else:
            await ctx.send("No feedback available yet.")
    except Exception as e:
        await ctx.send("There was a problem retrieving the grading distribution graph.")
        print(e)

@client.command(aliases=["linkfeedback", "link_feedback", "feedback_link"])
async def feedbacklink(ctx, assignment_number: str = None):
    allowed_channels = ['_staff']
    server_name = ctx.guild.name

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
        
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await ctx.send("No feedback available yet.")
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await ctx.send("No feedback available yet.")
        return

    await ctx.send(f"Feedback for assignment {assignment_number}: {feedback_file}")

@client.command(aliases=["listfeedback", "list_feedback"])
async def feedbacklist(ctx):
    allowed_channels = ['_staff']
    server_name = ctx.guild.name

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    if data:
        feedback_list = "\n".join([f"Assignment {assignment_number}: {url}" for assignment_number, url in data[server_name].items()])
        await ctx.send(feedback_list)
    else:
        await ctx.send("No feedback available yet.")

@client.command(aliases=["delete_feedback"])
async def deletefeedback(ctx, assignment_number: str = None):
    allowed_channels = ['_staff']
    server_name = ctx.guild.name

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    if assignment_number is not None:
        assignment_number = int(assignment_number)

    if delete_feedback(assignment_number, server_name):
        await ctx.send(f"Assignment {assignment_number} feedback link deleted.")
    else:
        await ctx.send(f"Assignment {assignment_number} feedback link not found.")

@client.command(aliases=["feedbackstudent", "student_feedback", "feedback_student"])
async def studentfeedback(ctx, username: str, assignment_number: str = None):
    allowed_channels = ['_staff']
    server_name = ctx.guild.name

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
        
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await ctx.send("No feedback available yet.")
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await ctx.send("No feedback available yet.")
        return

    try:
        user_feedback = requestExcelFile(feedback_file, ctx, username)

        if user_feedback.size > 0:
            feedback_text = user_feedback[0]
            if len(feedback_text) <= 1024:
                embed = Embed(title=f"Feedback for Assignment {assignment_number}", color=0xFF914D)

                if "cs617" in ctx.guild.name.lower():
                    embed.set_image(url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_617_horiz.png")
                elif "cs666" in ctx.guild.name.lower():
                    embed.set_image(url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_666_horiz.png")
                else:
                    embed.set_image(url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_Default_horiz.png")

                embed.add_field(name=f"Feedback for Assignment #{assignment_number}", value=user_feedback[0], inline=False)

                await ctx.send(embed=embed)
            else:
                banner_url = ""
                if "cs617" in ctx.guild.name.lower():
                    banner_url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_617_horiz.png"
                elif "cs666" in ctx.guild.name.lower():
                    banner_url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_666_horiz.png"
                else:
                    banner_url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_Default_horiz.png"
                
                await ctx.send(banner_url + "\n\n" + feedback_text)
        else:
            await ctx.send("No feedback found for this user :(.")

    except Exception as e:
        await ctx.send("There was a problem retrieving the feedback.")
        print(e)

@client.command(aliases=["staffhelp"])
async def helpstaff(ctx):
    allowed_channels = ['_staff']

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    embed = Embed(title="Staff Commands", description="Here are the commands available for staff:", color=0x00ff00)
    embed.add_field(name="!newfeedback *assignment_number* *feedback_file*", value="Update the feedback link for a specific assignment.", inline=False)
    embed.add_field(name="!summary *assignment_number* *background_color* *bar_color* *label_color*", value="Generate a bar graph with the grading distribution for a specific assignment. Defaults to black background, blue bars and white labels/ticks.", inline=False)
    embed.add_field(name="!feedbacklink *assignment_number*", value="Get the feedback link for a specific assignment.", inline=False)
    embed.add_field(name="!feedbacklist", value="List all the feedback links available.", inline=False)
    embed.add_field(name="!deletefeedback *assignment_number*", value="Delete the feedback link for a specific assignment.", inline=False)
    embed.add_field(name="!studentfeedback *student_discord_username* *assignment_number*", value="Get the feedback for a certain assignment for a specific user in the server.")
    embed.add_field(name="!helpstaff", value="Show this help message.", inline=False)

    await ctx.send(embed=embed)

##### STUDENT INTERFACE #####

@commands.cooldown(rate=3, per=60, type=commands.BucketType.user)
@client.command()
async def feedback(ctx, assignment_number: str = None):
    allowed_channels = ['feedback', "_staff"]
    server_name = ctx.guild.name

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
        
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await ctx.send("No feedback available yet.")
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await ctx.send("No feedback available yet.")
        return

    try:
        user_feedback = requestExcelFile(feedback_file, ctx)

        if user_feedback.size > 0:
            feedback_text = user_feedback[0]
            if len(feedback_text) <= 1024:
                embed = Embed(title=f"Feedback for Assignment {assignment_number}", color=0xFF914D)

                if "cs617" in ctx.guild.name.lower():
                    embed.set_image(url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_617_horiz.png")
                elif "cs666" in ctx.guild.name.lower():
                    embed.set_image(url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_666_horiz.png")
                else:
                    embed.set_image(url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_Default_horiz.png")

                embed.add_field(name=f"Feedback for Assignment #{assignment_number}", value=user_feedback[0], inline=False)

                await ctx.author.send(embed=embed)
            else:
                banner_url = ""
                if "cs617" in ctx.guild.name.lower():
                    banner_url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_617_horiz.png"
                elif "cs666" in ctx.guild.name.lower():
                    banner_url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_666_horiz.png"
                else:
                    banner_url="https://raw.githubusercontent.com/gaiborjosue/FeedbackDiscordBot/main/Images/Banner_Default_horiz.png"
                
                await ctx.author.send(banner_url + "\n\n" + feedback_text)
        else:
            await ctx.send("No feedback found for this user :(.")

    except Exception as e:
        await ctx.send("There was a problem retrieving the feedback.")
        print(e)

@commands.cooldown(rate=3, per=60, type=commands.BucketType.user)        
@client.command(aliases=["assignments", "feedbackassignments"])
async def checkassignments(ctx):
    allowed_channels = ['feedback', "_staff"]
    server_name = ctx.guild.name

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    assignments = data.get(server_name, {})

    embed = discord.Embed(title="Assignments Ready for Feedback", color=0x00ff00)
    embed.add_field(name="Info", value="These are the assignments already posted and ready with your feedback.", inline=False)

    if assignments:
        for num in assignments.keys():
            embed.add_field(name=f"Assignment {num}", value=":white_check_mark:", inline=False)
        embed.set_footer(text="Use `!feedback <assignment_number>` to get the feedback!")
    else:
        embed.description = "No assignments with feedback available yet."

    await ctx.send(embed=embed)

@commands.cooldown(rate=3, per=60, type=commands.BucketType.user)
@client.command()
async def rubric(ctx, assignment_number: str = None):
    allowed_channels = ['feedback', "_staff"]
    server_name = ctx.guild.name

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    elif "cs617" not in server_name.lower():
        await ctx.send("Rubric functionality is only available for CS617.")
        return

    data = read_or_init_json()

    if assignment_number is not None:
        assignment_number = int(assignment_number)
        
    else:
        assignment_number = assignment_number_not_provided(data, server_name)
        if assignment_number is None:
            await ctx.send("Assignment not available yet.")
            return

    feedback_file = data.get(server_name, {}).get(str(assignment_number))

    if not feedback_file:
        await ctx.send("No rubric available yet.")
        with open("Images/goblin.png", "rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
        return

    try:
    
        table = buildRubric(feedback_file)

        await ctx.send(f"## Rubric for assignment {assignment_number}", file=File(table, filename="rubric.png"))

    except Exception as e:
        await ctx.send("There was a problem retrieving the rubric.")
        print(e)


@client.command(aliases=["studenthelp"])
async def helpstudent(ctx):
    allowed_channels = ['feedback', "_staff"]

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    embed = Embed(title="Student Commands", description="Here are the commands available for students:", color=0x00ff00)
    embed.add_field(name="!feedback *assignment_number*", value="Get the feedback for a specific assignment.", inline=False)
    embed.add_field(name="!checkassignments", value="List all the assignments that have feedback available.", inline=False)
    embed.add_field(name="!rubric *assignment_number*", value="Get the rubric for a specific assignment.", inline=False)
    embed.add_field(name="!helpstudent", value="Show this help message.", inline=False)

    await ctx.send(embed=embed)

##### Owner Red Button Shutdown ######
@client.command(aliases=["DO_NOT_PRESS", "kill", "fireball"])
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("I have been attacked! I'm going down! *screams*, *explosion*, *silence*, *crickets*, *tumbleweed*, *more silence*, *even more silence*, *the end*, *credits*, *post-credits scene*")
    exit()