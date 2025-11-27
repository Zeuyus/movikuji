from dotenv import load_dotenv
import os
import discord
# 乱数を使うのでimport忘れずに！！
import random
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
# ここも追加分
OMIKUJI = [
    '大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶'
    ]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    # ここから追加分
    if message.content == '!おみくじ':
        await message.channel.send(f'あなたの運勢は"{OMIKUJI[random.randrange(len(OMIKUJI))]}"しゅこ～')
    # ここまで追加分
client.run(TOKEN)