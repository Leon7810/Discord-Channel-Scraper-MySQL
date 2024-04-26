import discord
import asyncio
import logging
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv
import os

# Set up logging to capture errors
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Define your bot token, server ID, and channel ID
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Define the MySQL connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Create the Discord bot class with specified intents
class DiscordScraperBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, intents=intents, **kwargs)

        # Set up the MySQL connection
        self.db_conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.db_cursor = self.db_conn.cursor()

    async def on_ready(self):
        try:
            print(f'Logged in as {self.user}')

            # Get the target guild (server)
            guild = self.get_guild(SERVER_ID)
            if not guild:
                print("Guild not found!")
                return

            # Get the specific text channel to scrape
            channel = guild.get_channel(CHANNEL_ID)
            if not channel or not isinstance(channel, discord.TextChannel):
                print("Text channel not found!")
                return

            # Fetch messages from the channel with a delay to slow down the scraping
            async for message in channel.history(limit=100):  # Adjust the limit as needed
                timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                author = str(message.author)
                content = message.content.replace('\n', ' ')  # Avoid newlines in the text file

                # Log the message to the console
                print(f"{timestamp} - {author}: {content}")

                # Insert the message into the MySQL database
                insert_query = "INSERT INTO discord_messages (id, timestamp, author, content, channel_id, server_id) VALUES (%s, %s, %s, %s, %s, %s)"
                self.db_cursor.execute(insert_query, (message.id, timestamp, author, content, CHANNEL_ID, SERVER_ID))
                self.db_conn.commit()  # Commit the changes to the database

                # Introduce a delay to slow down the scraping
                await asyncio.sleep(1)

            print("Messages scraped and inserted into the MySQL database.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            # Properly close the bot and the MySQL connection to avoid unclosed connections and other issues
            self.db_cursor.close()
            self.db_conn.close()
            await self.close()

# Create and run the bot with the specified token
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = DiscordScraperBot()
bot.run(TOKEN)
