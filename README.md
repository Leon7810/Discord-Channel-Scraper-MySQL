# Discord Message Scraper with MySQL Integration

This Python script creates a Discord bot to scrape messages from a specific channel and store them in a MySQL database. It uses environment variables to configure the bot token, Discord server, channel, and MySQL database connection details.

## Prerequisites
- **Python**: Ensure Python 3.6 or higher is installed on your system. You can check your Python version with `python --version`.
- **MySQL Database**: A MySQL server must be set up and running. The script uses environment variables for database configuration.
- **Discord Bot**: Create a Discord bot with the necessary permissions to read messages. You need the bot's token and IDs for the server and channel you want to scrape.

## Setup Instructions
1. **Install Python and Virtual Environment**:
   - If Python isn't installed, download and install it from the [official website](https://www.python.org/).
   - Create a virtual environment for your project.

```bash
# Create a virtual environment
python -m venv my_venv

# Activate the virtual environment
source my_venv/bin/activate  # Linux/macOS
my_venv\Scripts\activate  # Windows
```

2. **Install Required Packages**:
   - Use `pip` to install `discord.py`, `mysql-connector-python`, and `python-dotenv`.

```bash
pip install discord.py mysql-connector-python python-dotenv
```

3. **Set Up the MySQL Database**:
   - Ensure you have a running MySQL server. Create a database for the Discord messages.
   - Create a table to store the Discord messages.

```sql
CREATE TABLE discord_messages (
    id BIGINT PRIMARY KEY,
    timestamp DATETIME,
    author VARCHAR(255),
    content TEXT,
    channel_id BIGINT,
    server_id BIGINT
);
```

4. **Configure Environment Variables**:
   - Create a `.env` file in the same directory as your Python script.
   - Add the following environment variables to the `.env` file, replacing the placeholders with your specific values:

```env
DISCORD_TOKEN=YourDiscordBotToken
DISCORD_SERVER_ID=YourServerID
DISCORD_CHANNEL_ID=YourChannelID
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=  # Leave empty if there's no password
DB_NAME=test
```

## Running the Script
1. **Activate the Virtual Environment**:
   - Before running the script, ensure the virtual environment is activated.

```bash
source my_venv/bin/activate  # Linux/macOS
my_venv\Scripts\activate  # Windows
```

2. **Run the Script**:
   - Use `python` to run your script.

```bash
python app.py
```

3. **Verify Output**:
   - The script should log messages to the console and insert them into the MySQL database.
   - Check your MySQL database to ensure the messages are being inserted correctly.

## Troubleshooting and Common Errors
- **No Module Named 'mysql'**: If you encounter this error, ensure you've installed `mysql-connector-python`.
- **Environment Variable Errors**: If you get a `NoneType` error, ensure the `.env` file is correctly configured and loaded. Check for typos in environment variable names.
- **Discord Bot Permissions**: Ensure your Discord bot has the necessary permissions to read messages and access the specified channel.
- **Connection Errors**: Check your MySQL server status and ensure it's running and accessible. If using a local server, ensure it's listening on `localhost`.

## Additional Tips and Best Practices
- **Rate Limits**: To avoid rate limits, the script introduces a delay during scraping. Be mindful of Discord's rate limits.
- **Permissions and Privacy**: Ensure you have permission to scrape messages and comply with Discord's Terms of Service and Privacy Policy.
- **Resource Cleanup**: The script uses `finally` to ensure proper cleanup. If you encounter unclosed connection issues, review the code to ensure all resources are properly closed.
- **Security**: Avoid exposing sensitive information like database passwords. Keep these details in the `.env` file, not in the codebase.

## Further Information
For more information on creating and managing Discord bots, refer to the [Discord Developer Portal](https://discord.com/developers/docs/intro). For MySQL setup and management, check the [official MySQL documentation](https://dev.mysql.com/doc/).