import discord  # discord.py module
from discord.ext import commands

client = commands.Bot(command_prefix='!')


class FeedbackBot(discord.Client):
    async def on_ready(self):
        print('Logged on as {self.user}!')

    async def on_message(self, message):  # When a message is sent
        if (message.author.bot == False):  # If the message is not from a bot
            await message.reply('Hello World!')
            channel = message.channel.name
            restricted_channels = ["staff"] # List of restricted channels
            allowed_channels = ["feedback"] # List of allowed channels

            prefix = "!"  # Replace with your prefix
            # If the message starts with the prefix
            if message.content.startswith(prefix):
                if channel in restricted_channels: # If the message was sent in a restricted channel
                    command = message.content[len(prefix):]  # Get the command
                    # Check if the user is an admin
                    isAdmin = [role.name ==
                            "staff" for role in message.author.roles][0]
                    # Check for commands
                    if command == "newfeedback" and isAdmin:
                        # Send a message
                        await message.channel.send("New feedback has been created")

                    if command == "help":
                        await message.channel.send("```\n"
                                                "Commands:\n"
                                                "help - This is the help §erver stats\n"
                                                "```")

                    else:
                        # If the command is not found
                        await message.channel.send("This command doesn't exist")
                else:
                    await message.delete()
                    await message.author.send(f"You can't use commands in #{channel}")
                    # await message.channel.send("You can't use commands in this channel")\

              elif channel in allowed_channels:
                command = message.content[len(prefix):]

                if command == "feedback":
                    # looks into the json database and finds the assignment number, if no assignment feedback for that number,return a message.

                
                    


client = FeedbackBot()
# Replace with your token
client.run('5601e85812b6f8ab7639bd1fd3ecf748cdf8bb57d8856983ea3d86a68caaf4a7')