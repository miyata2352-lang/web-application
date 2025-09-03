# -*- coding: utf-8 -*-
#"""
#Created on Thu Aug 28 04:41:27 2025

#@author: miyat
#"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import openai
import base64
from io import BytesIO
from datetime import date

# Windows の場合
font_path = r"C:\Windows\Fonts\YuGothR.ttc"  # フォントファイルの絶対パス
font_path_name = r"C:\Windows\Fonts\YuGothB.ttc" 

# -------------------------------
# 0️⃣ APIキー
# -------------------------------
openai.api_key = "YOUR_API_KEY"  # ←自分のAPIキーを設定

# -------------------------------
# 1️⃣ 英語主体の単語リスト
# -------------------------------
# --- 1️⃣ 形容詞（EN主体） ---
adjectives_en = [
    "Jet-Black",
    "Abyssal",
    "Void",
    "Doom",
    "Dark",
    "Destructive",
    "Madness",
    "Merciless",
    "Mysterious",
    "Coldhearted",
    "Ominous",
    "Cursed",
    "Seductive",
    "Frozen",
    "Flaming",
    "Bloodstained",
    "Ethereal",
    "Demonic",
    "Weeping",
    "Thunderous",
    "Lone",
    "Undead",
    "Hopeless",
    "Sacred",
    "Sharp",
    "Majestic",
    "Icy",
    "Illusive",
    "Ruinous",
    "Absolute",
    "Eternal",
    "Evil",
    "Forbidden",
    "Nightbound",
    "Profound",
    "Infernal",
    "Storming",
    "Cosmic",
    "Elder",
    "Annihilating",
    "Blazing",
    "Shadowbound",
    "Savage",
    "Ashen",
    "Gloomy",
    "Soulbound",
    "Nether",
    "Blackflame"
]

# --- 2️⃣ 場所（EN主体） ---
places_en = [
    "Desert Wasteland",
    "Frozen Peaks",
    "Misty Forest",
    "Lake of Death",
    "Void Canyon",
    "Ruined Citadel",
    "Black Fortress",
    "Temple of Blood",
    "Cave of Despair",
    "Forest of Eternal Night",
    "Thunderous Plains",
    "Starry Void",
    "Rift to Hell",
    "Abyssal Valley",
    "Frostbitten Mountains",
    "Stormswept Plains",
    "Moonlit Lake",
    "Lonely Isle of Stars",
    "Sanctuary of Shadows",
    "Canyon of Doom",
    "Hidden Jungle",
    "Labyrinth of Mystery",
    "Volcanic Crater",
    "Abandoned Village",
    "Cliff of Darkness",
    "Sacred Summit",
    "Secret Hollow",
    "Shifting Sands",
    "Oracle’s Forest",
    "Glacial Rift",
    "Howling Wastes",
    "Sky of Radiance",
    "Lightning Peaks",
    "Darkwood",
    "Hidden Fairy Grove",
    "Abyssal Sea",
    "Cursed Lands",
    "Ancient Ruins",
    "Grave of Souls",
    "Crimson Falls",
    "Frozen Valley",
    "Plain of Stars",
    "Canyon of Thunder",
    "Shadowed Temple",
    "Flaming Pit",
    "Eternal Mountains",
    "Illusive Labyrinth"
]

# --- 3️⃣ 生物（EN主体） ---
creatures_en = [
    "Dragon",
    "Phoenix",
    "Golem",
    "Unicorn",
    "Beast",
    "Lizard",
    "Knight",
    "Demonlord",
    "Drake",
    "Swordsman",
    "Mage",
    "Vampire",
    "Giant",
    "Fairy",
    "Spirit",
    "Ninja",
    "Dragoon",
    "Paladin",
    "Archdemon",
    "Orb",
    "Wolf Demon",
    "Sage",
    "Ghost",
    "Bird Demon",
    "Cat Demon",
    "Beast Knight",
    "Undead",
    "Spirit Beast",
    "Wizard",
    "Beast King",
    "Dragon Cavalry",
    "Nether",
    "Black Flame",
    "Wolf Knight",
    "Cat Knight",
    "Demon King",
    "Beast Dragon",
    "Mage Dragon",
    "Dragon Spirit",
    "Magic Dragon",
    "Bird Knight",
    "Ghost Beast",
    "Wolf Dragon",
    "Demon Dragon",
    "Beast Knight Dragon",
    "Dragon Spirit",
    "Cat Dragon"
]

# -------------------------------
# 2️⃣ 英語→日本語辞書
# -------------------------------
adjectives_jp_map = {
    "Jet-Black":"漆黒なる",
    "Abyssal":"深淵を覗く",
    "Void":"虚無の",
    "Doom":"終焉の迎える",
    "Dark":"暗黒が宿る",
    "Destructive":"滅びの",
    "Madness":"狂気の",
    "Merciless":"無慈悲の",
    "Mysterious":"神秘めく",
    "Coldhearted":"冷酷な",
    "Ominous":"凶兆の",
    "Cursed":"怨嗟の宿りし",
    "Seductive":"妖艶なる",
    "Frozen":"凍てつく",
    "Flaming":"焔の",
    "Bloodstained":"血塗られた",
    "Ethereal":"幽玄なる",
    "Demonic":"魔性の",
    "Weeping":"哀哭の",
    "Thunderous":"雷光を帯びし",
    "Lone":"孤高の",
    "Undead":"亡者はこびる",
    "Hopeless":"絶望に染まりし",
    "Sacred":"聖なる",
    "Sharp":"鋭利な",
    "Majestic":"威厳ある",
    "Icy":"氷結の",
    "Illusive":"幻惑の",
    "Ruinous":"破滅のごとき",
    "Absolute":"絶対たる",
    "Eternal":"永劫なる",
    "Evil":"邪悪な",
    "Forbidden":"禁断の",
    "Nightbound":"夜闇に染まる",
    "Profound":"深淵の",
    "Infernal":"獄炎のごとき",
    "Storming":"轟雷響く",
    "Cosmic":"虚空の",
    "Elder":"邪神のごとき",
    "Annihilating":"滅殺の",
    "Blazing":"灼熱を纏う",
    "Shadowbound":"影縛の",
    "Savage":"獰猛なる",
    "Ashen":"灰燼の",
    "Gloomy":"暗澹の",
    "Soulbound":"霊魂の",
    "Nether":"魔界の",
    "Blackflame":"黒焔に染まりし"
}

places_jp_map = {
    "Desert Wasteland":"砂漠の荒野に潜む",
    "Frozen Peaks":"氷山の峰を統べる",
    "Misty Forest":"霧深き森より来たる",
    "Lake of Death":"死の湖に沈む",
    "Void Canyon":"虚空の渓谷を統べる",
    "Ruined Citadel":"滅びの廃墟に潜む",
    "Black Fortress":"漆黒の城塞に選ばれし",
    "Temple of Blood":"血の神殿に選ばれし",
    "Cave of Despair":"絶望の洞窟から来たる",
    "Forest of Eternal Night":"闇夜の森羅を喰らう",
    "Thunderous Plains":"雷鳴轟く荒野を統べる",
    "Starry Void":"星屑の空から生まれし",
    "Rift to Hell":"魔空の裂け目から来たる",
    "Abyssal Valley":"幽谷の深淵に潜む",
    "Frostbitten Mountains":"霜降る山脈に棲む",
    "Stormswept Plains":"嵐吹き荒ぶ平原の",
    "Moonlit Lake":"夜光の湖に選ばれし",
    "Lonely Isle of Stars":"銀河の孤島を統べる",
    "Sanctuary of Shadows":"月影の神域に潜む",
    "Canyon of Doom":"滅亡の峡谷を統べる",
    "Hidden Jungle":"秘められた樹海に潜む",
    "Labyrinth of Mystery":"神秘の迷宮にて待ち受ける",
    "Volcanic Crater":"荒れ狂う火山を喰らう",
    "Abandoned Village":"影潜む廃村から生まれし",
    "Cliff of Darkness":"暗黒の断崖から這い出づる",
    "Sacred Summit":"霊峰の頂を統べる",
    "Secret Hollow":"隠されし洞穴から来たる",
    "Shifting Sands":"流砂の砂漠から生まれし",
    "Oracle’s Forest":"神託の森に選ばれし",
    "Glacial Rift":"氷河の裂け目から来たる",
    "Howling Wastes":"風鳴る荒野を統べる",
    "Sky of Radiance":"光満つる天空を喰らう",
    "Lightning Peaks":"雷光走る峰から生まれし",
    "Darkwood":"闇潜む森に棲む",
    "Hidden Fairy Grove":"妖精の隠れ里に棲む",
    "Abyssal Sea":"深海の暗黒から生まれし",
    "Cursed Lands":"魔境の地より来たる",
    "Ancient Ruins":"古代の遺跡を守りし",
    "Grave of Souls":"幽冥の墓場の",
    "Crimson Falls":"紅蓮の滝に選ばれし",
    "Frozen Valley":"霧氷の谷に棲む",
    "Plain of Stars":"星屑の平原を統べる",
    "Canyon of Thunder":"雷撃の峡谷の",
    "Shadowed Temple":"光翳る神殿を守りし",
    "Flaming Pit":"焔舞う火口のから生まれし",
    "Eternal Mountains":"永劫の霊峰より来たる",
    "Illusive Labyrinth":"幻惑の迷宮に選ばれし"
}

creatures_jp_map = {
    "Dragon":"ドラゴン",
    "Phoenix":"フェニックス",
    "Golem":"ゴーレム",
    "Unicorn":"ユニコーン",
    "Beast":"魔獣",
    "Knight":"騎士",
    "Demonlord":"魔王",
    "Drake":"竜",
    "Mage":"魔導士",
    "Vampire":"吸血鬼",
    "Giant":"巨人",
    "Fairy":"妖精",
    "Spirit":"精霊",
    "Ninja":"忍者",
    "Dragoon":"竜騎士",
    "Paladin":"パラディン",
    "Archdemon":"魔神",
    "Orb":"オーブ",
    "Wolf Demon":"魔狼",
    "Sage":"賢者",
    "Ghost":"幽霊",
    "Bird Demon":"魔鳥",
    "Cat Demon":"魔猫",
    "Beast Knight":"魔獣騎士",
    "Undead":"亡者",
    "Magic Dragon":"魔竜",
    "Spirit Beast":"精獣",
    "Wizard":"ウィザード",
    "Beast King":"魔獣王",
    "Dragon Cavalry":"竜騎兵",
    "Nether":"幽冥",
    "Black Flame":"黒炎",
    "Wolf Knight":"魔狼士",
    "Cat Knight":"魔猫騎士",
    "Demon King":"魔神王",
    "Beast Dragon":"魔獣竜",
    "Mage Dragon":"魔導竜",
    "Dragon Spirit":"精霊竜",
    "Bird Knight":"魔鳥騎士",
    "Ghost Beast":"霊獣",
    "Wolf Dragon":"魔狼竜",
    "Demon Dragon":"魔神竜",
    "Beast Knight Dragon":"魔獣騎竜",
    "Dragon Spirit":"精霊竜",
    "Cat Dragon":"魔猫竜"
}

# -------------------------------
# 3️⃣ 枠色辞書（英語キーで管理）
# -------------------------------
place_colors = {
    "Desert Wasteland":"sienna",
    "Frozen Peaks":"lightblue",
    "Misty Forest":"green",
    "Lake of Death":"lightblue",
    "Void Canyon":"black",
    "Ruined Citadel":"red",
    "Black Fortress":"plum",
    "Temple of Blood":"red",
    "Cave of Despair":"black",
    "Forest of Eternal Night":"black",
    "Thunderous Plains":"red",
    "Starry Void":"plum",
    "Rift to Hell":"red",
    "Abyssal Valley":"lightblue",
    "Frostbitten Mountains":"lightblue",
    "Stormswept Plains":"black",
    "Moonlit Lake":"lightblue",
    "Lonely Isle of Stars":"plum",
    "Sanctuary of Shadows":"plum",
    "Canyon of Doom":"black",
    "Hidden Jungle":"green",
    "Labyrinth of Mystery":"plum",
    "Volcanic Crater":"red",
    "Abandoned Village":"black",
    "Cliff of Darkness":"black",
    "Sacred Summit":"lightblue",
    "Secret Hollow":"black",
    "Shifting Sands":"sienna",
    "Oracle’s Forest":"green",
    "Glacial Rift":"lightblue",
    "Howling Wastes":"sienna",
    "Sky of Radiance":"plum",
    "Lightning Peaks":"red",
    "Darkwood":"black",
    "Hidden Fairy Grove":"plum",
    "Abyssal Sea":"black",
    "Cursed Lands":"red",
    "Ancient Ruins":"sienna",
    "Grave of Souls":"black",
    "Crimson Falls":"red",
    "Frozen Valley":"lightblue",
    "Plain of Stars":"plum",
    "Canyon of Thunder":"red",
    "Shadowed Temple":"plum",
    "Flaming Pit":"red",
    "Eternal Mountains":"lightblue",
    "Illusive Labyrinth":"plum"
}

# 各レアリティの出現確率（重み）
rarities = ["Common", "Rare", "Super Rare"]
weights = [70, 25, 5]  # ％をそのまま重みにできる

rarlity_color = {
    "Common":"white",
    "Rare":"blue",
    "Super Rare":"yellow"
    }




def generate_nickname():
    adj_en = random.choice(adjectives_en)
    place_en = random.choice(places_en)
    creature_en = random.choice(creatures_en)

    rarity = random.choices(rarities, weights=weights, k=1)[0]
    frame_color = rarlity_color[rarity]

    # 日本語変換
    adj_jp = adjectives_jp_map.get(adj_en, adj_en)
    place_jp = places_jp_map.get(place_en, place_en)
    creature_jp = creatures_jp_map.get(creature_en, creature_en)

    nickname_jp = f"{adj_jp}{place_jp}{creature_jp}"

    # 場所テーマ色
    card_color = place_colors.get(place_en, "black")

    # AIプロンプト（英語基準）
    rarity_prompts = {
    "common": "simple background, minimal details",
    "rare": "richly detailed clothing and ornaments, intricate background, subtle lighting",
    "srare": "highly detailed clothing and armor, complex background, multiple layers of ornaments, subtle magical effects, cinematic composition"
}

    rarity_extra = rarity_prompts.get(rarity, "")

    ai_prompt = (
        f"Dark fantasy {creature_en}, {adj_en} style, in {place_en}, "
        f"highly detailed anime style, {rarity_extra}"
    )

    return nickname_jp, adj_en, place_en, creature_en, rarity, frame_color, card_color, ai_prompt


# === 2️⃣ AI画像生成（仮） ===
def generate_character_image(creature_en, adj_en, place_en, rarity, filename="character.png"):
    """
    レアリティに応じてプロンプトを調整し、AIで画像を生成して保存する

    Parameters
    ----------
    creature_en : str
        キャラクター種族・生物名
    adj_en : str
        形容詞（英語）
    place_en : str
        場所（英語）
    rarity : str
        "Common", "Rare", "Super Rare"
    filename : str
        保存するファイル名
    """
    # レアリティごとの装飾・ディテール量の調整
    rarity_prompts = {
        "Common": "simple background, minimal details",
        "Rare": "richly detailed clothing and ornaments, intricate background, subtle lighting",
        "Super Rare": "highly detailed clothing and armor, complex background, multiple layers of ornaments, subtle magical effects, cinematic composition"
    }

    # 基本プロンプト
    base_prompt = f"Dark fantasy {creature_en}, {adj_en} style, in {place_en}, highly detailed anime style"
    
    # レアリティプロンプトを追加
    prompt = f"{base_prompt}, {rarity_prompts.get(rarity,'')}"
    
    # 生成
    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="512x512"
    )
    
    image_base64 = response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    
    # 保存
    img = Image.open(BytesIO(image_data))
    img.save(filename)
    
    print(f"画像生成完了: {filename} (レアリティ: {rarity})")
    return filename


# === 3️⃣ カード合成 ===
def compose_card(nickname_jp, char_img_path, frame_color, card_color,name, boss_explanation):
    # --- 既存のカード背景画像を読み込む ---
    if card_color=="black":
        if frame_color=="white":
            background_path = r"C:\Users\miyat\Card_frame\black_common.png"
        elif frame_color=="blue":
            background_path = r"C:\Users\miyat\Card_frame\black_rare.png"
        elif frame_color=="yellow":
            background_path = r"C:\Users\miyat\Card_frame\black_srare.png"
            
            
    if card_color=="red":
        if frame_color=="white":
            background_path = r"C:\Users\miyat\Card_frame\red_common.png"
        elif frame_color=="blue":
            background_path = r"C:\Users\miyat\Card_frame\red_rare.png"
        elif frame_color=="yellow":
            background_path = r"C:\Users\miyat\Card_frame\red_srare.png"
            
            
    if card_color=="green":
        if frame_color=="white":
            background_path = r"C:\Users\miyat\Card_frame\green_common.png"
        elif frame_color=="blue":
            background_path = r"C:\Users\miyat\Card_frame\green_rare.png"
        elif frame_color=="yellow":
            background_path = r"C:\Users\miyat\Card_frame\green_srare.png"
    
    
    if card_color=="lightblue":
        if frame_color=="white":
            background_path = r"C:\Users\miyat\Card_frame\skyblue_common.png"
        elif frame_color=="blue":
            background_path = r"C:\Users\miyat\Card_frame\skyblue_rare.png"
        elif frame_color=="yellow":
            background_path = r"C:\Users\miyat\Card_frame\skyblue_srare.png"
            
            
    if card_color=="sienna":
        if frame_color=="white":
            background_path = r"C:\Users\miyat\Card_frame\sienna_common.png"
        elif frame_color=="blue":
            background_path = r"C:\Users\miyat\Card_frame\sienna_rare.png"
        elif frame_color=="yellow":
            background_path = r"C:\Users\miyat\Card_frame\sienna_srare.png"
            
            
    if card_color=="plum":
        if frame_color=="white":
            background_path = r"C:\Users\miyat\Card_frame\plum_common.png"
        elif frame_color=="blue":
            background_path = r"C:\Users\miyat\Card_frame\plum_rare.png"
        elif frame_color=="yellow":
            background_path = r"C:\Users\miyat\Card_frame\plum_srare.png"
    
    
    background = Image.open(background_path).convert("RGBA")
    draw = ImageDraw.Draw(background)
    stroke_width = 2 #ふちの太さ（
    stroke_width_name = 6   #（キャラ名、二つ名）
    stroke_width_explanation = 1
    
    # --- 枠線（必要なら色変更） ---
    #draw.rectangle([(0,0),(1050,1499)], outline=frame_color, width=10)

    # --- タイトル文字 ---
   

    #二つ名
    font_title = ImageFont.truetype(font_path_name,40,index=0)
    for dx in range(-stroke_width, stroke_width+1):
        for dy in range(-stroke_width, stroke_width+1):
            if dx != 0 or dy != 0:
                draw.text((70+dx, 70+dy), nickname_jp, font=font_title, fill="black")
    draw.text((70,70), nickname_jp, font=font_title, fill="white")
    
    #キャラ名
    font_title_name= ImageFont.truetype(font_path_name,100,index=0)
    bbox = draw.textbbox((0,0),name,font=font_title_name)
    text_width = bbox[2]-bbox[0]  
    image_width = background.width
    x = (image_width - text_width) / 2  
    for dx in range(-stroke_width_name, stroke_width_name+1):
        for dy in range(-stroke_width_name, stroke_width_name+1):
            if dx != 0 or dy != 0:
                draw.text((x+dx, 200+dy), name, font=font_title_name, fill="black")
    draw.text((x,200),name,font=font_title_name, fill="white")
    
    #説明文
    font_title_explanation = ImageFont.truetype(font_path_name,32,index=0)
    max_width = 925
    # 折り返した行リストを取得
    lines = wrap_text(boss_explanation, font_title_explanation, draw, max_width)
    y = 1270
    for line in lines:
        for dx in range(-stroke_width_explanation, stroke_width_explanation+1):
            for dy in range(-stroke_width_explanation, stroke_width_explanation+1):
                if dx != 0 or dy != 0:
                    draw.text((70+dx, y+dy), line, font=font_title_explanation, fill="black")
        draw.text((73,y), line, font=font_title_explanation, fill="white")
        y += font_title_explanation.size + 5  # 行間はフォントサイズ+10px
        
        
    #日付
    today = date.today()
    today_str = today.strftime("%Y/%m/%d") + "  StudioMIYA"
    font_title_date = ImageFont.truetype(font_path,30,index=0)
    for dx in range(-stroke_width, stroke_width+1):
        for dy in range(-stroke_width, stroke_width+1):
            if dx != 0 or dy != 0:
                draw.text((600+dx, 1410+dy), today_str, font=font_title_date, fill="black")
    draw.text((600,1410), today_str, font=font_title_date, fill="white")
    
    # --- キャラクター画像 ---
    char_img =  Image.open(char_img_path).resize((885,885))
    background.paste(char_img, (83,364), char_img)  # 透過情報も反映
    
    #エフェクト追加
    # --- 保存前にキラキラ追加 ---
    if frame_color == "yellow":  # Super Rare のとき
        background = add_glitter_effect(background, count=250)
    

    # --- 保存 ---
    output_path = "card_generated.png"
    background.save(output_path)
    print("カード生成完了:", output_path)
    return output_path

#4テキスト折り返し
def wrap_text(text, font, draw, max_width):
    """
    指定した幅(max_width)を超えないようにテキストを折り返す
    """
    lines = []
    current_line = ""

    for ch in text:
        test_line = current_line + ch
        width = draw.textlength(test_line, font=font)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = ch
    if current_line:
        lines.append(current_line)

    return lines

#5きらきらエフェクト
def add_glitter_effect(image, count=150):
    """大小のキラキラ粒を混ぜてリッチに見せる"""
    glitter = Image.new("RGBA", image.size, (0,0,0,0))
    draw = ImageDraw.Draw(glitter)

    for _ in range(count):
        x = random.randint(0, image.width)
        y = random.randint(0, image.height)

        # 大粒 or 小粒をランダムに選ぶ
        if random.random() < 0.25:  # 25% は大粒
            r = random.randint(8, 15)   # 大粒
            alpha = random.randint(120, 200)
        else:
            r = random.randint(2, 6)    # 小粒
            alpha = random.randint(80, 150)

        # 中心から外にフェードする円
        for i in range(r, 0, -1):
            a = int(alpha * (i / r))
            color = (255, 255, 220, a)
            draw.ellipse((x-i, y-i, x+i, y+i), fill=color)

        # 大粒の一部にはクロス光追加
        if r > 7 and random.random() < 0.5:
            cross_len = r * 2
            cross_alpha = int(alpha * 0.7)
            cross_color = (255, 255, 255, cross_alpha)
            draw.line((x-cross_len, y, x+cross_len, y), fill=cross_color, width=2)
            draw.line((x, y-cross_len, x, y+cross_len), fill=cross_color, width=2)

    # ほんの少しぼかして柔らかさを出す
    glitter = glitter.filter(ImageFilter.GaussianBlur(0.8))
    image.alpha_composite(glitter)
    return image


# === 実行例 ===
nickname_jp, adj_en, place_en, creature_en, rarity, frame_color, card_color, ai_prompt = generate_nickname()
print("生成:", nickname_jp, "| レアリティ:", rarity, "| 枠色:", frame_color, "| テーマ色:", card_color)
print("プロンプト:", ai_prompt)

char_img_path = generate_character_image(ai_prompt)
char_img_path = r"C:\Users\miyat\Card_frame\test.png"
#name = "あああああああああ"
#boss_explanation = "これはボスの説明文です。ああああああああああああああああああああああああああああああああああああああああああああああああ"
#compose_card(nickname_jp, char_img_path, frame_color, card_color,name, boss_explanation)