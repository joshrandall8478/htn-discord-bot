import db
import nextcord

from nextcord.ext import commands
from nextcord import SlashOption

db = db.Database()

# Bot class
class Bot(commands.Bot):
    def __init__(self):
        db.init_db()
        intents = nextcord.Intents.default()
        intents.members = True
        intents.guilds = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"Bot is ready! Logged in as {self.user}")
        print(f"Connected to {len(self.guilds)} guild(s)")


bot = Bot()



# Help command
@bot.slash_command(name="help", description="See bot commands")
async def help_command(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="Hack The Nest",
        description="",
        color=nextcord.Color.green(),
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)

# Ticket
@bot.slash_command(name="ticket", description="Creates a new ticket")
async def ticket_create(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
            title="Hack The Nest",
            description="",
            color=nextcord.Color.green(),
        )
    await interaction.response.send_message(embed=embed, ephemeral=True)


# Setup commands
# TODO: Make sure only admins can run setup


# =========================================================
# SETUP VIEW
# =========================================================


class SetupView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

        self.step = 1

        # Store wizard values here
        self.category = None
        self.role = None
        self.ticket_message = None
        self.ticket_channel = None

        self.load_step()

    def load_step(self):
        # Remove controls from previous step
        self.clear_items()

        match self.step:
            case 1:
                self.add_item(CategorySelect(self))

            case 2:
                self.add_item(RoleSelect(self))

            case 3:
                self.add_item(TicketMessageButton(self))
                self.add_item(SkipStepButton(self, next_step=5))


            case 4:
                self.add_item(TicketChannelSelect(self))
                self.add_item(SkipStepButton(self, next_step=5))

            case 5:
                self.add_item(SaveSetupButton(self))
                self.add_item(RestartSetupButton(self))

    def get_embed(self):
        embed = nextcord.Embed(
            title="Ticket System Setup",
            color=nextcord.Color.blurple()
        )

        match self.step:

            # =================================================
            # STEP 1
            # =================================================

            case 1:
                embed.description = "### Step 1 of 5"

                embed.add_field(
                    name="📁 Ticket Category",
                    value=(
                        f"Selected: **{self.category.name}**"
                        if self.category
                        else "Choose the category where ticket channels will be created."
                    ),
                    inline=False
                )

            # =================================================
            # STEP 2
            # =================================================

            case 2:
                embed.description = "### Step 2 of 5"

                embed.add_field(
                    name="📁 Ticket Category",
                    value=f"✅ **{self.category.name}**",
                    inline=False
                )

                embed.add_field(
                    name="🛡️ Support Role",
                    value=(
                        f"Selected: {self.role.mention}"
                        if self.role
                        else "Choose the role that can view and respond to tickets."
                    ),
                    inline=False
                )

            # =================================================
            # STEP 3
            # =================================================

            case 3:
                embed.description = "### Step 3 of 5"

                embed.add_field(
                    name="📁 Ticket Category",
                    value=f"✅ **{self.category.name}**",
                    inline=False
                )

                embed.add_field(
                    name="🛡️ Support Role",
                    value=f"✅ {self.role.mention}",
                    inline=False
                )

                embed.add_field(
                    name="📝 Ticket Message",
                    value=(
                        f"✅ {self.ticket_message}"
                        if self.ticket_message
                        else "Click the button below to configure the ticket message."
                    ),
                    inline=False
                )

            # =================================================
            # STEP 4
            # =================================================

            case 4:
                embed.description = "### Step 4 of 5"

                embed.add_field(
                    name="📁 Ticket Category",
                    value=f"✅ **{self.category.name}**",
                    inline=False
                )

                embed.add_field(
                    name="🛡️ Support Role",
                    value=f"✅ {self.role.mention}",
                    inline=False
                )

                embed.add_field(
                    name="📝 Ticket Message",
                    value=f"✅ {self.ticket_message}",
                    inline=False
                )

                embed.add_field(
                    name="💬 Ticket Channel",
                    value=(
                        f"Selected: {self.ticket_channel.mention}"
                        if self.ticket_channel
                        else "Choose the channel where the ticket message will be placed."
                    ),
                    inline=False
                )

            # =================================================
            # STEP 5
            # =================================================

            case 5:
                embed.description = (
                    "### Step 5 of 5\n"
                    "Review your configuration before saving."
                )

                embed.add_field(
                    name="📁 Ticket Category",
                    value=f"**{self.category.name}**",
                    inline=False
                )

                embed.add_field(
                    name="🛡️ Support Role",
                    value=self.role.mention,
                    inline=False
                )

                embed.add_field(
                    name="📝 Ticket Message",
                    value=self.ticket_message if self.ticket_message else "",
                    inline=False
                )

                embed.add_field(
                    name="💬 Ticket Channel",
                    value=self.ticket_channel.mention if self.ticket_channel else "",
                    inline=False
                )

        embed.set_footer(text="Ticket setup wizard")

        return embed


# =========================================================
# Skip button
# =========================================================

class SkipStepButton(nextcord.ui.Button):
    def __init__(self, setup_view, next_step):
        self.setup_view = setup_view
        self.next_step = next_step

        super().__init__(
            label="Skip",
            style=nextcord.ButtonStyle.secondary,
            emoji="⏭️"
        )

    async def callback(self, interaction: nextcord.Interaction):
        self.setup_view.step = self.next_step
        self.setup_view.load_step()

        await interaction.response.edit_message(
            embed=self.setup_view.get_embed(),
            view=self.setup_view
        )

# =========================================================
# STEP 1: CATEGORY
# =========================================================

class CategorySelect(nextcord.ui.ChannelSelect):
    def __init__(self, setup_view):
        self.setup_view = setup_view

        super().__init__(
            placeholder="Choose a ticket category...",
            channel_types=[
                nextcord.ChannelType.category
            ],
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: nextcord.Interaction):
        self.setup_view.category = self.values[0]

        self.setup_view.step = 2
        self.setup_view.load_step()

        await interaction.response.edit_message(
            embed=self.setup_view.get_embed(),
            view=self.setup_view
        )


# =========================================================
# STEP 2: SUPPORT ROLE
# =========================================================

class RoleSelect(nextcord.ui.RoleSelect):
    def __init__(self, setup_view):
        self.setup_view = setup_view

        super().__init__(
            placeholder="Choose a support role...",
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: nextcord.Interaction):
        self.setup_view.role = self.values[0]

        self.setup_view.step = 3
        self.setup_view.load_step()

        await interaction.response.edit_message(
            embed=self.setup_view.get_embed(),
            view=self.setup_view
        )


# =========================================================
# STEP 3: TICKET MESSAGE MODAL
# =========================================================

class TicketMessageModal(nextcord.ui.Modal):
    def __init__(self, setup_view):
        super().__init__(
            title="Configure Ticket Message"
        )

        self.setup_view = setup_view

        self.ticket_message_input = nextcord.ui.TextInput(
            label="Ticket Message",
            placeholder="Need help? Open a ticket below!",
            style=nextcord.TextInputStyle.paragraph,
            required=True,
            max_length=1000
        )

        self.add_item(self.ticket_message_input)

    async def callback(self, interaction: nextcord.Interaction):
        self.setup_view.ticket_message = self.ticket_message_input.value

        self.setup_view.step = 4
        self.setup_view.load_step()

        await interaction.response.edit_message(
            embed=self.setup_view.get_embed(),
            view=self.setup_view
        )


class TicketMessageButton(nextcord.ui.Button):
    def __init__(self, setup_view):
        self.setup_view = setup_view

        super().__init__(
            label="Configure Ticket Message",
            style=nextcord.ButtonStyle.primary,
            emoji="📝"
        )

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(
            TicketMessageModal(self.setup_view)
        )


# =========================================================
# STEP 4: TICKET CHANNEL
# =========================================================

class TicketChannelSelect(nextcord.ui.ChannelSelect):
    def __init__(self, setup_view):
        self.setup_view = setup_view

        super().__init__(
            placeholder="Choose the ticket message channel...",
            channel_types=[
                nextcord.ChannelType.text
            ],
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: nextcord.Interaction):
        self.setup_view.ticket_channel = self.values[0]

        self.setup_view.step = 5
        self.setup_view.load_step()

        await interaction.response.edit_message(
            embed=self.setup_view.get_embed(),
            view=self.setup_view
        )


# =========================================================
# STEP 5: SAVE
# =========================================================

class SaveSetupButton(nextcord.ui.Button):
    def __init__(self, setup_view):
        self.setup_view = setup_view

        super().__init__(
            label="Save Configuration",
            style=nextcord.ButtonStyle.success,
            emoji="✅"
        )

    async def callback(self, interaction: nextcord.Interaction):
        category = self.setup_view.category
        role = self.setup_view.role
        ticket_message = self.setup_view.ticket_message
        ticket_channel = self.setup_view.ticket_channel

        

        # =====================================================
        # SAVE TO DATABASE HERE
        # =====================================================
        guild_name = interaction.guild.name
        guild_id = interaction.guild.id
        category_name = category.name
        category_id = category.id
        role_name = role.name
        role_id = role.id
        ticket_channel_id = ticket_channel.id if ticket_channel else None

        print("Guild:", guild_name)
        print("Guild ID:", guild_id)
        print("Category:", category_name)
        print("Category ID:", category_id)
        print("Role:", role_name)
        print("Role ID:", role_id)
        print("Ticket Message:", ticket_message)
        print("Ticket Channel ID:", ticket_channel_id)

        db.save_config(
            guild_id,
            guild_name,
            category_id,
            category_name,
            role_id,
            role_name,
        )



        embed = nextcord.Embed(
            title="✅ Setup Complete",
            description="The ticket system has been configured successfully.",
            color=nextcord.Color.green()
        )

        embed.add_field(
            name="📁 Ticket Category",
            value=f"**{category.name}**",
            inline=False
        )

        embed.add_field(
            name="🛡️ Support Role",
            value=role.mention,
            inline=False
        )

        embed.add_field(
            name="💬 Ticket Channel",
            value= ticket_channel.mention if ticket_channel else "",
            inline=False
        )

        embed.add_field(
            name="📝 Ticket Message",
            value=ticket_message if ticket_message else "",
            inline=False
        )

        await interaction.response.edit_message(
            embed=embed,
            view=None
        )


# =========================================================
# RESTART BUTTON
# =========================================================

class RestartSetupButton(nextcord.ui.Button):
    def __init__(self, setup_view):
        self.setup_view = setup_view

        super().__init__(
            label="Start Over",
            style=nextcord.ButtonStyle.secondary,
            emoji="🔄"
        )

    async def callback(self, interaction: nextcord.Interaction):
        self.setup_view.step = 1

        self.setup_view.category = None
        self.setup_view.role = None
        self.setup_view.ticket_message = None
        self.setup_view.ticket_channel = None

        self.setup_view.load_step()

        await interaction.response.edit_message(
            embed=self.setup_view.get_embed(),
            view=self.setup_view
        )


# =========================================================
# SLASH COMMAND
# =========================================================

@bot.slash_command(description="Configure the bot")
async def setup(interaction: nextcord.Interaction):
    view = SetupView()

    await interaction.response.send_message(
        embed=view.get_embed(),
        view=view,
        ephemeral=True
    )



