import os
import nextcord
import argparse
from nextcord.ext import commands
from nextcord import SlashOption


class Bot(commands.Bot):
    def __init__(self):
        intents = nextcord.Intents.default()
        intents.members = True
        intents.guilds = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"Bot is ready! Logged in as {self.user}")
        print(f"Connected to {len(self.guilds)} guild(s)")

bot = Bot()




@bot.slash_command(name="help", description="See bot commands")
async def help_command(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="Hack The Nest",
        description="",
        color=nextcord.Color.green(),
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)



def main():
    parser =  argparse.ArgumentParser()
    parser.add_argument(
        "--token",
        type=str,
        help="Discord bot token (can also be set via DISCORD_TOKEN environment variable)",
    )
    args = parser.parse_args()
    if not os.getenv("DISCORD_TOKEN"):
        token = args.token
    else:
        token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN environment variable is not set, or --token argument not provided!")
        print("Please set it in your .env file or environment.")
        exit(1)

    bot.run(token)


if __name__ == "__main__":
    main()
