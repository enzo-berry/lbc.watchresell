from config.config import bot_token  

print("Importing modules.")
import lbc
import discord_bot

filters_manager = lbc.Lbc()

discord_bot.run(filters_manager)