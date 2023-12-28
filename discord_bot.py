from config.config import bot_token, module_error_message

import disnake
import lbc
from disnake.ext import commands

bot = commands.InteractionBot()

filters_manager:filter = None

@bot.event
async def on_ready():
    print("The discord bot is ready.")


@bot.slash_command(description="Adds a filter to monitor a leboncoin url")
async def add_filter(
    interaction: disnake.ApplicationCommandInteraction,
    url: str = commands.Param(name="url", description="The url to monitor"),
):
    global filters_manager
    await interaction.response.defer()

    filter = {"url": url, "discord_channel_id": interaction.channel.id}
    filters_manager.add_filter(filter, True)

    await interaction.edit_original_message(content=f"Filtre ajouté {url}")

@bot.slash_command(description="Removes a filter to monitor a leboncoin url")
async def remove_filter(
    interaction: disnake.ApplicationCommandInteraction,
):
    global filters_manager
    await interaction.response.defer()

    filters_manager.remove_filter(interaction.channel)

    await interaction.edit_original_message(content=f"Filtre supprimé")

@bot.slash_command(description="Lists all filters")
async def list_filters(
    interaction: disnake.ApplicationCommandInteraction,
):
    global filters_manager
    await interaction.response.defer()

    filters = filters_manager.filters["filters"]
    msg = ""
    for filter in filters:
        msg += f"{filter['url']}\n"
    await interaction.edit_original_message(content=msg)

@bot.slash_command(description="Clears all messages")
async def clear(
    interaction: disnake.ApplicationCommandInteraction,
):
    await interaction.response.defer()
    await interaction.channel.purge()

def run(fm:lbc):
    global filters_manager
    filters_manager = fm
    bot.run(bot_token)


if __name__ == "__main__":
    print(__file__.split('\\')[-1],":",module_error_message)
    exit(1)



