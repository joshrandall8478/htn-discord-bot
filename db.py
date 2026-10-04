import sqlite3


class Database:
    def __init__(self, db_path="app_data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.init_db()

    def init_db(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    guildId INTEGER NOT NULL,
                    guildName TEXT NOT NULL,
                    ticketCategoryId INTEGER NOT NULL,
                    ticketCategoryName TEXT NOT NULL,
                    ticketRoleId INTEGER NOT NULL,
                    ticketRoleName TEXT NOT NULL
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    guildId INTEGER NOT NULL,
                    channelId INTEGER NOT NULL,
                    subject TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('resolved', 'open'))
                );
                """
            )
            self.conn.commit()
            print("Tables created/checked successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()


    def save_config(self, guildId, guildName, categoryId, categoryName, roldeId, roleName):
                # Example:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                       INSERT INTO config (
                guildId,
                guildName,
                ticketCategoryId,
                ticketCategoryName,
                ticketRoleId,
                ticketRoleName
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                guildId, guildName, categoryId, categoryName, roldeId, roleName
            ))
            self.conn.commit()
            print("Config for " + guildName + " created")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
#
        # cursor.execute(
        #     """
        #     INSERT INTO config (
        #         guildId,
        #         ticketCategory,
        #         ticketRoleId,
        #         ticketChannelId,
        #         ticketMessage
        #     )
        #     VALUES (?, ?, ?, ?, ?)
        #     """,
        #     (
        #         interaction.guild.id,
        #         category.id,
        #         role.id,
        #         ticket_channel.id,
        #         ticket_message
        #     )
        # )
        #
        # db.commit()

    def get_cursor(self):
        return self.conn.cursor()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print("\nDatabase connection closed.")

    def __del__(self):
        if getattr(self, "conn", None) is not None:
            self.close()


if __name__ == "__main__":
    db = Database()
    db.close()