# This example requires the 'message_content' intent.
import os
import discord
import markov 

filename = './texts/twain.txt'
chains = markov.make_chains(markov.open_and_read_file([filename]))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = markov.make_text(chains)

    if message.content.startswith('$hello'):
        await message.channel.send(text)

client.run(os.environ['DISCORD_TOKEN'])