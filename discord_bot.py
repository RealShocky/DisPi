import discord
import os
import openai
from pi import PiAPI

client = discord.Client()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize PiCoin API with your API key
pi_api = PiAPI(os.getenv('PI_API_KEY'))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message) and '?' in message.content:
        question = message.content.replace(client.user.mention, '').strip()
        try:
            if "pi" in question.lower() or "pi coin" in question.lower():
                pi_info = pi_api.get_info()
                answer = f"PiCoin (PI):\nPrice: ${pi_info['price']}\nMarket Cap: ${pi_info['market_cap']}\n24h Volume: ${pi_info['volume']}"
            else:
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=question,
                    max_tokens=100
                )
                answer = response.choices[0].text.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            answer = "I'm sorry, I couldn't generate a response at the moment."

        await message.channel.send(answer)

client.run(os.getenv('DISCORD_BOT_TOKEN'))
