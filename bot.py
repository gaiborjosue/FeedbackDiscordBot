from Utils.jsonManipulation import read_or_init_json, update_assignment_json, delete_feedback, assignment_number_not_provided
from Utils.requestExcelFile import requestExcelFile, getGraphData
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


client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    wizard_ascii_legendary_level_feedback_giver_9000 = """
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

@client.command()
async def newfeedback(ctx, assignment_number: int, feedback_file: str):
    allowed_channels = ['_staff']
    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return


    # Update the JSON file with the new feedback URL
    update_assignment_json(assignment_number, feedback_file)
    await ctx.send(f"Assignment {assignment_number} feedback link updated.")

@client.command()
async def summary(ctx, assignment_number: int = None):
    allowed_channels = ['_staff']

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    assignment_number = assignment_number_not_provided(data)

    if assignment_number is None:
        await ctx.send("No feedback available yet.")
        return

    feedback_file = data.get(str(assignment_number))

    if not feedback_file:
        await ctx.send("No feedback available yet.")
        return

    try:
        x, y = getGraphData(feedback_file)

        if x and y:
            title = f"Assignment #{assignment_number}"
            xlabel = "Grade"
            ylabel = "Number of Students"
            graph = generateBarGraph(x, y, title, xlabel, ylabel)

            await ctx.send(file=File(graph, filename="grade_distribution.png"))
        else:
            await ctx.send("No feedback available yet.")
    except Exception as e:
        await ctx.send("There was a problem retrieving the grading distribution graph.")
        print(e)

@client.command()
async def feedbacklink(ctx, assignment_number: int = None):
    allowed_channels = ['_staff']

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    assignment_number = assignment_number_not_provided(data)

    if assignment_number is None:
        await ctx.send("No feedback available yet.")
        return

    feedback_file = data.get(str(assignment_number))

    if not feedback_file:
        await ctx.send("No feedback available yet.")
        return

    await ctx.send(f"Feedback for assignment {assignment_number}: {feedback_file}")

@client.command()
async def feedbacklist(ctx):
    allowed_channels = ['_staff']

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    if data:
        feedback_list = "\n".join([f"Assignment {k}: {v}" for k, v in data.items()])
        await ctx.send(feedback_list)
    else:
        await ctx.send("No feedback available yet.")

@client.command()
async def deletefeedback(ctx, assignment_number: int):
    allowed_channels = ['_staff']

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    if delete_feedback(assignment_number):
        await ctx.send(f"Assignment {assignment_number} feedback link deleted.")
    else:
        await ctx.send(f"Assignment {assignment_number} feedback link not found.")

@client.command()
async def helpstaff(ctx):
    allowed_channels = ['_staff']

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    embed = Embed(title="Staff Commands", description="Here are the commands available for staff:", color=0x00ff00)
    embed.add_field(name="!newfeedback *assignment_number* *feedback_file*", value="Update the feedback link for a specific assignment.", inline=False)
    embed.add_field(name="!summary *assignment_number*", value="Generate a bar graph with the grading distribution for a specific assignment.", inline=False)
    embed.add_field(name="!feedbacklink *assignment_number*", value="Get the feedback link for a specific assignment.", inline=False)
    embed.add_field(name="!feedbacklist", value="List all the feedback links available.", inline=False)
    embed.add_field(name="!deletefeedback *assignment_number*", value="Delete the feedback link for a specific assignment.", inline=False)
    embed.add_field(name="!helpstaff", value="Show this help message.", inline=False)

    await ctx.send(embed=embed)

##### STUDENT INTERFACE #####

# @commands.cooldown(rate=2, per=60, type=commands.BucketType.user)
@client.command()
async def feedback(ctx, assignment_number: int = None):
    allowed_channels = ['feedback', "_staff"]
    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    data = read_or_init_json()

    assignment_number = assignment_number_not_provided(data)

    if assignment_number is None:
        await ctx.send("No feedback available yet.")
        return


    feedback_file = data.get(str(assignment_number))

    if not feedback_file:
        await ctx.send("No feedback available yet.")
        return

    try:
        user_feedback = requestExcelFile(feedback_file, ctx)

        if user_feedback.size > 0:
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
            await ctx.author.send("No feedback found for you :(.")

    except Exception as e:
        await ctx.send("There was a problem retrieving the feedback.")
        print(e)
        
@client.command()
async def help(ctx):
    allowed_channels = ['feedback', "_staff"]

    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return

    embed = Embed(title="Student Commands", description="Here are the commands available for students:", color=0x00ff00)
    embed.add_field(name="!feedback *assignment_number*", value="Get the feedback for a specific assignment.", inline=False)
    embed.add_field(name="!help", value="Show this help message.", inline=False)

    await ctx.send(embed=embed)
    