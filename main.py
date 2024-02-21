from dotenv import load_dotenv
import os
from bot import client

load_dotenv()

client.run(os.getenv('DISCORD_TOKEN'))
