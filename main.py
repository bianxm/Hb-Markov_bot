# This example requires the 'message_content' intent.
import os
import discord
import markov 

filename = './texts/twain.txt'
chains = markov.make_chains(markov.open_and_read_file([filename]))
#def new_chains(filename):
    #global
    #chains = markov.make_chains(markov.open_and_read_file([filename]))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global chains
    if message.author == client.user:
        return

    if message.content.startswith('$mb'):
        tokens = message.content.split()
        messageToSend = ''
        if tokens[1] == 'hello':
            messageToSend = markov.make_text(chains)
        elif tokens[1] == 'help':
            messageToSend = f"'$mb hello' to generate some text from a certain source\n'$mb get' to see available sources\n'$mb set <filename>' to set a source file"
        elif tokens[1] == 'get':
            for filename in os.listdir('./texts'):
                messageToSend += f'{filename}     '
        elif tokens[1] == 'set':
            try:
                if os.path.isfile('./texts/' + tokens[2]):
                    chains = markov.make_chains(markov.open_and_read_file([f'./texts/{tokens[2]}']))
                    #new_chains(f'./texts/{tokens[2]}')
                    messageToSend = f"Thanks! Source text is now {tokens[2]}"
                else:
                    messageToSend = f"Sorry, {tokens[2]} not found. Please call '$mb get' to see available texts."
            except:
                messageToSend = f"Proper syntax: '$mb set <filename here>' \n'$mb get' to see available texts"
        else:
           messageToSend = "Sorry, I don't understand that" 
        
        await message.channel.send(messageToSend)

client.run(os.environ['DISCORD_TOKEN'])