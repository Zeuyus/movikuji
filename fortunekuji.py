from dotenv import load_dotenv
import discord
import requests
import os
import random
import boto3

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
LAMBDA_API_URL = os.getenv("LAMBDA_API_URL")
INSTANCE_ID = os.getenv("EC2_INSTANCE_ID")

OMIKUJI = [
    '大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶'
    ]

MESSAGE_STAR_WARS_DAIKICHI = [
    '「フォースと共にあらんことを」 (May the Force be with you.)'
    ,'「戦争は人を偉大にはしない」 (Wars not make one great.)'
    ,'「助けて、オビ＝ワン・ケノービ。あなただけが頼りです」(Help me, Obi-Wan Kenobi. You’re my only hope.)'
    ]

MESSAGE_STAR_WARS_DAIKICHI_URL_FORCE = [
    'https://livedoor.blogimg.jp/swgm1138/imgs/f/7/f74bda19.png'
    ,'https://livedoor.blogimg.jp/swgm1138/imgs/d/1/d1b6f7f8.png'
    ,'https://livedoor.blogimg.jp/swgm1138/imgs/a/a/aabe64f6.png'
    ,'https://livedoor.blogimg.jp/swgm1138/imgs/4/f/4f09d098.png'
    ,'https://livedoor.blogimg.jp/swgm1138/imgs/5/b/5b576202.png'
    ]
MESSAGE_STAR_WARS_DAIKICHI_URL_SENSOU = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/13Star-Wars-Yoda-Everett-MSDEMST_EC017-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_DAIKICHI_URL_TASUKETE = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/12Star-Wars-Carrie-Fisher-R2D2-Everett-MSDSTWA_EC102-H-2023.jpg'
    ]

MESSAGE_STAR_WARS_KICHI = [
    '「私にはフォースがついている。フォースは私と共にある」(I’m one with the Force. The Force is with me.)'
    ,'「あんたが憎い！」「弟と思ってた。愛してた！」 (I hate you! You were my brother, Anakin. I loved you.)'
    ,'「違う！やるか、やらぬかだ。ためしなどいらん。(No! Try not. Do. Or do not. There is no try.)」'
    ]

MESSAGE_STAR_WARS_KICHI_URL_WATASHINIHA = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/8rogueone57ff8b775caac-embed_0.jpg'
    ]
MESSAGE_STAR_WARS_KICHI_URL_OSOREHA = [
    'https://castel.jp/item/34496/'
    ]
MESSAGE_STAR_WARS_KICHI_URL_TIGAU = [
    'https://pbs.twimg.com/media/DsAi8I1VsAAkGhN.jpg'
    ]

MESSAGE_STAR_WARS_TYUKICHI = [
    '「反乱軍は希望を信じて戦う」 (Rebellions are built on hope.)'
    ,'「お前の信念の欠如が気掛かりだ」(I find your lack of faith disturbing.)'
    ,'「チューイ、帰ってきたぞ！」(Chewie, we’re home.)'
    ]

MESSAGE_STAR_WARS_TYUKICHI_URL_HANRAN = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/9MCDROON_EC037-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_TYUKICHI_URL_OMAENO = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/10Star-Wars-Darth-Vader-Everett-MMDSTWA_FE009-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_TYUKICHI_URL_TYUI = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/20Star-Wars-Chewbacca-Harrison-Ford-Everett-MCDSTWA_EC145-H-2023.jpg'
    ]

MESSAGE_STAR_WARS_SYOKICHI = [
    '「やるか、やらぬかだ。ためしなどいらん。」 (Do. Or do not. There is no try.)'
    ,'「愛してる 知ってるさ」(I love you. I know.)'
    ,'「私がお前の父親だ」 (I am your father.)'
    ]

MESSAGE_STAR_WARS_SYOKICHI_URL_YARUKA = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/6Star-Wars-Yoda-R2D2-Everett-MSDEMST_EC030-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_SYOKICHI_URL_AISITERU = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/4Star-Wars-Carrie-Fisher-Harrison-Ford-2-Everett-MBDSTWA_FE006-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_SYOKICHI_URL_WATASIGA = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/5star_wars_the_empire_strikes_back.jpg'
    ]

MESSAGE_STAR_WARS_SUEKITCHI = [
    '「やあ、こんにちは！」(Hello there!)'
    ,'「あれは月じゃない」(That’s no moon.)'
    ,'「これで自由は死んだわ。万雷の拍手の中でね。」(This is how liberty dies … with thunderous applause.)'
    ]

MESSAGE_STAR_WARS_SUEKITCHI_URL_YA = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/3Star-Wars-Alec-Guinness-Everett-MSDSTWA_EC007-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_SUEKITCHI_URL_AREWATUKI = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/19MSDSTWA_FE099-H-2022.jpg'
    ]
MESSAGE_STAR_WARS_SUEKITCHI_URL_KOREDEJIYUU = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/18Star-Wars-Natalie-Portman-Everett-MCDSTWA_FE027-H-2023.jpg'
    ]

MESSAGE_STAR_WARS_KYO = [
    '「嫌な予感がする」 (I have a bad feeling about this.)'
    ,'「お前たちが探しているドロイドではない」(These aren’t the droids you’re looking for.)'
    ,'「終わりだアナキン、私の方が有利だ」(It’s over, Anakin. I have the high ground.)'
    ]

MESSAGE_STAR_WARS_KYO_URL_IYANA = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/2Star-Wars-Millennium-Falcon-Scene-Everett-MBDSTWA_FE035-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_KYO_URL_OMAE = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/11Star-Wars-Stormtroopers-Alec-Guinness-Everett-MSDSTWA_EC095-H-2023.jpg'
    ]
MESSAGE_STAR_WARS_KYO_URL_OWARI = [
    'https://hollywoodreporter.jp/wp-content/uploads/2025/03/14Star-Wars-Ewan-McGregor-Hayden-Christensen-Everett-MCDSTWA_FE058-H-2023.jpg'
    ]

MESSAGE_STAR_WARS_DAIKYO = [
    '「罠だ！」 (It’s a trap!)'
    ,'「確率なんてクソくらえだ！」(Never tell me the odds!)'
    ,'「自惚れ屋の、戯け者の、みすぼらしいナーフ飼いなんかに！」(Why, you stuck-up, half-witted, scruffy-looking …nerf-herder!)'
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

# ========================================================
# EC2の状態を確認する関数
# ========================================================
def check_ec2_state(instance_id):
    # EC2クライアントの作成
    ec2 = boto3.client('ec2')

    try:
        # インスタンスのステータスを取得
        response = ec2.describe_instances(InstanceIds=[instance_id])

        # インスタンスの状態を取得
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        
        print(f"EC2インスタンスの状態: {state}")

        return state

    except Exception as e:
        print(f"EC2ステータス取得中にエラーが発生しました: {e}")
        return None

# ========================================================
#  ★ Lambda を呼び出す関数（ここが今回の追加ポイント）
# ========================================================
def call_lambda(action: str):
    try:
        print(f"📡 Lambda へ送信: action={action}")

        response = requests.post(
            LAMBDA_API_URL,
            json={"action": action},
            timeout=30
        )

        # debuq
        # print(f"📡 Lambda 応答ステータス: {response.status_code}")
        # print(f"📡 Lambda 応答内容: {response.text}")

        # ステータスコードが 400 以上の場合、エラーとして処理
        if response.status_code >= 400:
            return {"error": f"Lambda API call failed with status code {response.status_code}", "details": response.text}

        # JSON 化できない場合はそのまま返す
        try:
            return response.json()
        except Exception:
            return {"error": "Invalid JSON response", "raw": response.text}

    except Exception as e:
        print(f"❌ Lambda 呼び出しエラー: {e}")
        return {"error": str(e)}

# ========================================================
#  Discord Bot メイン処理
# ========================================================
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"[LOG] message received: {message.content}")

    # --------------------------
    #  おみくじ
    # --------------------------
    if message.content.strip() == '!おみくじ':
        result = random.choice(OMIKUJI)
        await message.channel.send(f'あなたの運勢は 「{result}」\n')

        if result == '大吉':
            await message.channel.send('🎉 ラッキー！いいことあるはず〜♪')
        elif result == '大凶':
            await message.channel.send('😱 大凶…でも諦めずに〜')
        else:
            await message.channel.send('✨ 普通の日かも〜')

    # --------------------------
    #  STARWARS おみくじ
    # --------------------------
    if message.content.strip() == '!STARWARS':
        # EC2インスタンスの状態を確認
        # ec2_state = check_ec2_state(INSTANCE_ID)

        # # EC2インスタンスが停止していた場合、Lambdaで起動処理を実行
        # if ec2_state == 'stopped':
        #     await message.channel.send("🚀 サーバーが停止しています。起動中…")
        #     result_lambda = call_lambda("start")
            
        #     if "error" in result_lambda:
        #         await message.channel.send(f"❌ サーバー起動エラー\n```{result_lambda}```")
        #     else:
        #         await message.channel.send("✅ サーバーが正常に起動しました。")

        result = random.choice(OMIKUJI)
        await message.channel.send(f'あなたの運勢は 「{result}」\n')

        if result == '大吉':
            extra_message = random.choice(MESSAGE_STAR_WARS_DAIKICHI)

            if extra_message == '「フォースと共にあらんことを」 (May the Force be with you.)':
                embed = discord.Embed(title=f'🎉 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_DAIKICHI_URL_FORCE))
                await message.channel.send(embed=embed)
            elif extra_message == '「戦争は人を偉大にはしない」 (Wars not make one great.)':
                embed = discord.Embed(title=f'🎉 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_DAIKICHI_URL_SENSOU))
                await message.channel.send(embed=embed)
            elif extra_message == '「助けて、オビ＝ワン・ケノービ。あなただけが頼りです」(Help me, Obi-Wan Kenobi. You’re my only hope.)':
                embed = discord.Embed(title=f'🎉 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_DAIKICHI_URL_TASUKETE))
                await message.channel.send(embed=embed)

        elif result == '吉':
            extra_message = random.choice(MESSAGE_STAR_WARS_KICHI)

            if extra_message == '「私にはフォースがついている。フォースは私と共にある」(I’m one with the Force. The Force is with me.)':
                embed = discord.Embed(title=f'🍀 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_KICHI_URL_WATASHINIHA))
                await message.channel.send(embed=embed)
            elif extra_message == '「あんたが憎い！」「弟と思ってた。愛してた！」 (I hate you! You were my brother, Anakin. I loved you.)':
                embed = discord.Embed(title=f'🍀 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_KICHI_URL_OSOREHA))
                await message.channel.send(embed=embed)
            elif extra_message == '「違う！やるか、やらぬかだ。ためしなどいらん。(No! Try not. Do. Or do not. There is no try.)':
                embed = discord.Embed(title=f'🍀 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_KICHI_URL_TIGAU))
                await message.channel.send(embed=embed)

        elif result == '中吉':
            extra_message = random.choice(MESSAGE_STAR_WARS_TYUKICHI)

            if extra_message == '「反乱軍は希望を信じて戦う」 (Rebellions are built on hope.)':
                embed = discord.Embed(title=f'✨ : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_TYUKICHI_URL_HANRAN))
                await message.channel.send(embed=embed)
            elif extra_message == '「お前の信念の欠如が気掛かりだ」(I find your lack of faith disturbing.)':
                embed = discord.Embed(title=f'✨ : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_TYUKICHI_URL_OMAENO))
                await message.channel.send(embed=embed)
            elif extra_message == '「チューイ、帰ってきたぞ！」(Chewie, we’re home.)':
                embed = discord.Embed(title=f'✨ : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_TYUKICHI_URL_TYUI))
                await message.channel.send(embed=embed)

        elif result == '小吉':
            extra_message = random.choice(MESSAGE_STAR_WARS_SYOKICHI)

            if extra_message == '「やるか、やらぬかだ。ためしなどいらん。」 (Do. Or do not. There is no try.)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_SYOKICHI_URL_YARUKA))
                await message.channel.send(embed=embed)
            elif extra_message == '「愛してる 知ってるさ」(I love you. I know.)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_SYOKICHI_URL_AISITERU))
                await message.channel.send(embed=embed)
            elif extra_message == '「私がお前の父親だ」 (I am your father.)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_SYOKICHI_URL_WATASIGA))
                await message.channel.send(embed=embed)

        elif result == '末吉':
            extra_message = random.choice(MESSAGE_STAR_WARS_SUEKITCHI)

            if extra_message == '「やあ、こんにちは！」(Hello there!)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_SUEKITCHI_URL_YA))
                await message.channel.send(embed=embed)
            elif extra_message == '「あれは月じゃない」(That’s no moon.)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_SUEKITCHI_URL_AREWATUKI))
                await message.channel.send(embed=embed)
            elif extra_message == '「これで自由は死んだわ。万雷の拍手の中でね。」(This is how liberty dies … with thunderous applause.)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_SUEKITCHI_URL_KOREDEJIYUU))
                await message.channel.send(embed=embed)

        elif result == '凶':
            extra_message = random.choice(MESSAGE_STAR_WARS_KYO)

            if extra_message == '「嫌な予感がする」 (I have a bad feeling about this.)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_KYO_URL_IYANA))
                await message.channel.send(embed=embed)
            elif extra_message == '「お前たちが探しているドロイドではない」(These aren’t the droids you’re looking for.)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_KYO_URL_OMAE))
                await message.channel.send(embed=embed)
            elif extra_message == '「終わりだアナキン、私の方が有利だ」(It’s over, Anakin. I have the high ground.)':
                embed = discord.Embed(title=f'{extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_KYO_URL_OWARI))
                await message.channel.send(embed=embed)

        elif result == '大凶':
            extra_message = random.choice(MESSAGE_STAR_WARS_DAIKYO)

            if extra_message == '「罠だ！」 (It’s a trap!)':
                embed = discord.Embed(title=f'💀 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_DAIKYO_URL_TRIP))
                await message.channel.send(embed=embed)
            elif extra_message == '「確率なんてクソくらえだ！」(Never tell me the odds!)':
                embed = discord.Embed(title=f'💀 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_DAIKYO_URL_KAKURITU))
                await message.channel.send(embed=embed)
            elif extra_message == '「自惚れ屋の、戯け者の、みすぼらしいナーフ飼いなんかに！」(Why, you stuck-up, half-witted, scruffy-looking …nerf-herder!)':
                embed = discord.Embed(title=f'💀 : {extra_message}')
                embed.set_image(url=random.choice(MESSAGE_STAR_WARS_DAIKYO_URL_UNUBORE))
                await message.channel.send(embed=embed)

        # ========================================
        #  EC2 起動処理を必ず実行
        # ========================================
        # await message.channel.send("🚀 Server起動中…")
        result_lambda = call_lambda("start")

        # Lambda のエラーとステータスコードをチェック
        if "error" in result_lambda:
            await message.channel.send(f"❌ Server起動エラー\n```{result_lambda}```")
        # else:
        #     await message.channel.send(f"✅ Server起動成功\n```{result_lambda}```")

        # ========================================
        #  EC2 停止処理を必ず実行
        # ========================================
        # await message.channel.send("🛑 Server停止中…")
        result_lambda = call_lambda("stop")

        # Lambda のエラーとステータスコードをチェック
        if "error" in result_lambda:
            await message.channel.send(f"❌ Server停止エラー\n```{result_lambda}```")
        # else:
        #     await message.channel.send(f"✅ Server停止成功\n```{result_lambda}```")

    # #===========================================================
    # #  EC2 起動
    # #===========================================================
    # if message.content == '!ec2_start':
    #     await message.channel.send("🚀 EC2 起動リクエスト中…")

    #     result = call_lambda("start")

    #     if "error" in result:
    #         await message.channel.send(f"❌ エラー発生\n```{result}```")
    #     else:
    #         await message.channel.send(f"✅ 成功\n```{result}```")


    # #===========================================================
    # #  EC2 停止
    # #===========================================================
    # if message.content == '!ec2_stop':
    #     await message.channel.send("🛑 EC2 停止リクエスト中…")

    #     result = call_lambda("stop")

    #     if "error" in result:
    #         await message.channel.send(f"❌ エラー発生\n```{result}```")
    #     else:
    #         await message.channel.send(f"🟢 成功\n```{result}```")

client.run(TOKEN)