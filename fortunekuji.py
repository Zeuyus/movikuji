import discord
import random
import requests
import os
from dotenv import load_dotenv
# .envの読み込み
load_dotenv()

# Discord設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
LAMBDA_API_URL = os.getenv("LAMBDA_API_URL")

# ここも追加分
OMIKUJI = [
    '大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶'
    ]

MESSAGE = [
    '平凡な風景が、突然意味のある何かに変わる。陳腐でつまらない景色が美しく光り輝く真珠になる。音楽でね。'
    ]

MESSAGE_STAR_WARS_DAIKICHI_URL_FORCE = [
    'https://livedoor.blogimg.jp/swgm1138/imgs/f/7/f74bda19.png'
    ,'https://livedoor.blogimg.jp/swgm1138/imgs/d/1/d1b6f7f8.png'
    ,'https://livedoor.blogimg.jp/swgm1138/imgs/a/a/aabe64f6.png'
    ,'https://livedoor.blogimg.jp/swgm1138/imgs/4/f/4f09d098.png'
    ,'https://livedoor.blogimg.jp/swgm1138/imgs/5/b/5b576202.png'
    ]

MESSAGE_STAR_WARS_DAIKYO_URL_TRIP = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/7Admiral-Ackbar-Star-Wars-BTS-Everett-MCDSTWA_EC191-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_DAIKYO_URL_KAKURITU = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/15Star-Wars-C-3PO-Harrison-Ford-Everett-MSDEMST_EC061-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_DAIKYO_URL_UNUBORE = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/16Star-Wars-Carrie-Fisher-Harrison-Ford-Everett-MSDEMST_EC052.-H-2023jpg.jpg'
    ]

MESSAGE_STAR_WARS_DAIKICHI = [
    '「フォースと共にあらんことを」 (May the Force be with you.)'
    ,'「希望は太陽のようなもの。見える時だけ信じるなら、夜を越えることはできない」 (Hope is like the sun. If you only believe in it when you can see it, you will never make it through the night.)'
    ,'「助けて、オビ＝ワン・ケノービ。あなただけが頼りです」(Help me, Obi-Wan Kenobi. You’re my only hope.)'
    ]
MESSAGE_STAR_WARS_KICHI = [
    '「戦争は人を偉大にはしない」 (Wars not make one great.)'
    ,'「私にはフォースがついている。フォースは私と共にある」(I’m one with the Force. The Force is with me.)'
    ,'「恐れはダークサイドに通じる。恐れは怒りに、怒りは憎しみに、憎しみは苦痛へ」 (Fear is the path to the dark side. Fear leads to anger. Anger leads to hate. Hate leads to suffering.)'
    ]
MESSAGE_STAR_WARS_TYUKICHI = [
    '「反乱軍は希望を信じて戦う」 (Rebellions are built on hope.)'
    ,'「お前の信念の欠如が気掛かりだ」(I find your lack of faith disturbing.)'
    ,'「チューイ、帰ってきたぞ！」(Chewie, we’re home.)'
    ]
MESSAGE_STAR_WARS_SYOKICHI = [
    '「やるか、やらぬかだ。ためしなどいらん。」 (Do. Or do not. There is no try.)'
    ,'「愛してる 知ってるさ」(I love you. I know.)'
    ,'「私がお前の父親だ」 (I am your father.)'
    ]
MESSAGE_STAR_WARS_SUEKITCHI = [
    '「やあ、こんにちは！」(Hello there!)'
    ,'「あれは月じゃない」(That’s no moon.)'
    ,'「これで自由は死んだわ。万雷の拍手の中でね。」(This is how liberty dies … with thunderous applause.)'
    ]
MESSAGE_STAR_WARS_KYO = [
    '「嫌な予感がする」 (I have a bad feeling about this.)'
    ,'「お前たちが探しているドロイドではない」(These aren’t the droids you’re looking for.)'
    ,'「終わりだアナキン、私の方が有利だ」(It’s over, Anakin. I have the high ground.)'
    ]
MESSAGE_STAR_WARS_DAIKYO = [
    '「罠だ！」 (It’s a trap!)'
    ,'「確率なんてクソくらえだ！」(Never tell me the odds!)'
    ,'「自惚れ屋の、戯け者の、みすぼらしいナーフ飼いなんかに！」(Why, you stuck-up, half-witted, scruffy-looking …nerf-herder!)'
    ]

# 既に処理したメッセージIDを保持する集合
processed_messages = set()


# Lambda呼び出し関数
def call_lambda(action: str):
    try:
        response = requests.post(
            LAMBDA_API_URL,
            json={"action": action},
            timeout=30
        )
        return response.json() if response.status_code < 400 else {"error": f"Lambda API call failed with status code {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": str(e)}

# on_ready イベント
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# on_message イベント
@client.event
async def on_message(message):
    # 自分のメッセージや既に処理したメッセージはスキップ
    if message.author == client.user or message.id in processed_messages:
        return

    print(f"[LOG] message received: {message.content}")

    # メッセージIDを処理済みとしてフラグを立てる
    processed_messages.add(message.id)

    # !STARWARS コマンドに対する処理
    if message.content.strip() == '!STARWARS':
        result = random.choice(OMIKUJI)
        await message.channel.send(f'あなたの運勢は 「{result}」\n')

        # 運勢に応じてメッセージを変更
        if result == '大吉':
            extra_message = random.choice(MESSAGE_STAR_WARS_DAIKICHI)
            await message.channel.send(f'🎉 : {extra_message}')
        elif result == '吉':
            extra_message = random.choice(MESSAGE_STAR_WARS_KICHI)
            await message.channel.send(f'🍀 : {extra_message}')
        # 他の運勢に対するメッセージも同様に...

        # EC2 起動処理
        await message.channel.send("🚀 EC2 起動リクエスト中…")
        result_lambda = call_lambda("start")

        # Lambda 呼び出し結果を送信
        if "error" in result_lambda:
            await message.channel.send(f"❌ EC2 起動エラー\n```{result_lambda}```")
        else:
            await message.channel.send(f"✅ EC2 起動成功\n```{result_lambda}```")

client.run(TOKEN)
