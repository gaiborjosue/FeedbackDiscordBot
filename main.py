#!./env/bin/python

from dotenv import load_dotenv
import os
from bot import client


client.run(os.environ.get('DISCORD_TOKEN'))
