from Utils.jsonManipulation import read_or_init_json, update_assignment_json
from Utils.requestExcelFile import requestExcelFile

import discord
from discord.ext import commands
from discord import Embed



# Define your intents
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

# Create a bot instance with a '!' prefix for commands
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

##### STAFF INTERFACE #####
@client.command()
async def newfeedback(ctx, assignment_number: int, feedback_file: str):
    allowed_channels = ['staff']
    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return


    # Update the JSON file with the new feedback URL
    update_assignment_json(assignment_number, feedback_file)
    await ctx.send(f"Assignment {assignment_number} feedback link updated.")


##### STUDENT INTERFACE #####

# @commands.cooldown(rate=2, per=60, type=commands.BucketType.user)
@client.command()
async def feedback(ctx, assignment_number: int = None):
    allowed_channels = ['feedback']
    if ctx.channel.name not in allowed_channels:
        await ctx.send("This command can't be used in this channel.")
        return


    data = read_or_init_json()

    if not assignment_number:
        if data:
            latest_assignment = max(data.keys(), key=int)
            assignment_number = int(latest_assignment)
        else:
            await ctx.send("No feedback available yet.")
            return

    feedback_file = data.get(str(assignment_number))

    if not feedback_file:
        await ctx.send("Feedback for this assignment is not available yet.")
        return

    try:
        user_feedback = requestExcelFile(feedback_file, ctx)

        if user_feedback.size > 0:
            embed = Embed(title=f"Feedback for Assignment {assignment_number}", color=0x00ff00)  # You can change the title and color
            embed.set_image(url="TESTING_URL")  # Replace TESTING_URL with your actual image URL
            embed.add_field(name="Your Feedback", value=user_feedback[0], inline=False)

            await ctx.author.send(embed=embed)
        else:
            await ctx.author.send("No feedback found for you.")

    except Exception as e:
        await ctx.send("There was a problem retrieving the feedback.")
        print(e)


# Run the bot with your token
client.run('TOKEN_GOES_HERE2')


