#!./env/bin/python

from dotenv import load_dotenv
import os
from bot import client

# Load environment variables from .env file
load_dotenv()

client.run(os.environ.get('DISCORD_TOKEN'))
