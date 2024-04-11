from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from blackjack import Blackjack

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

# Store active Blackjack games
active_games = {}

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    is_private = user_message[0] == '?'
    user_message = user_message[1:] if is_private else user_message

    try:
        if 'play blackjack' in user_message.lower():
            game = Blackjack()
            response = "Starting a new Blackjack game!\n" + game.dealCards()
            active_games[message.author.id] = game
        elif 'hit' in user_message.lower() or 'stand' in user_message.lower():
            game = active_games.get(message.author.id)
            if game:
                move = user_message.lower().split()[0]
                response = game.hitOrStand(move)
            else:
                response = "You haven't started a Blackjack game yet. Type 'play blackjack' to start a new game."
        else:
            response = get_response(user_message)

        await (message.author.send(response) if is_private else message.channel.send(response))
    except Exception as e:
        print(e)

# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')

    await send_message(message, user_message)

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
