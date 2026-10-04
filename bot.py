import os
import nextcord
import argparse
from nextcord.ext import commands
from nextcord import SlashOption
import db


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

db = db.Database()




@bot.slash_command(name="help", description="See bot commands")
async def help_command(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="Hack The Nest",
        description="",
        color=nextcord.Color.green(),
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command(name="ticket", description="Creates a new ticket")
async def ticket_create(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
            title="Hack The Nest",
            description="",
            color=nextcord.Color.green(),
        )
    await interaction.response.send_message(embed=embed, ephemeral=True)

class SetupModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Server Setup")
        self.name = nextcord.ui.TextInput(label="Ticket Category Name", required=True, max_length=100)
        self.add_item(self.name)

    async def callback(self, interaction: nextcord.Interaction):
        # validate + save to db here
        view = ChannelPickView(self.name.value)
        await interaction.response.send_message("Pick a channel:", view=view, ephemeral=True)

class CategoryPickView(nextcord.ui.View):
    def __init__(self, name: str):
        super().__init__(timeout=120)
        self.name = name

    @nextcord.ui.channel_select(
        placeholder="Choose a category",
        channel_types=[nextcord.ChannelType.category],
        min_values=1,
        max_values=1,
    )
    async def pick(self, select: nextcord.ui.ChannelSelect, interaction: nextcord.Interaction):
        category = select.values.channels[0]   # a partial channel object; has .id and .name
        # save self.name + category.id to your db
        await interaction.response.edit_message(
            content=f"Using category **{category.name}**", view=None
        )

class ChannelPickView(nextcord.ui.View):
    def __init__(self, name):
        super().__init__(timeout=120)
        self.name = name

    @nextcord.ui.channel_select(placeholder="Announcement channel")
    async def pick(self, select, interaction: nextcord.Interaction):
        channel = select.values.channels[0]
        # save self.name + channel.id to db
        await interaction.response.edit_message(content="Setup complete!", view=None)

@bot.slash_command(description="Configure the bot")
async def setup(interaction: nextcord.Interaction):
    await interaction.response.send_modal(SetupModal())



def main():
    db.init_db()
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
