import argparse
import os
import bot


bot = bot.Bot()

# Main process
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