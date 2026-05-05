import asyncio
import logging
from aiogram import Bot

# Məlumatlar
API_TOKEN = '8712453996:AAHfzva1GZ9WDIxjhMK_rZoLtvy2j2L99vY'
CHAT_ID = '@rveanx'  # Kanalın istifadəçi adı
MESSAGE_ID = 267     # Mesajın ID-si

# 10 fərqli font (Unicode əsaslı)
FONTS = [
    "Hello, my name is @Ryhavean This is my channel. Try to stay away from every scumbag who does dirty/shady things",
    "Ｈｅｌｌｏ, ｍｙ ｎａｍｅ ｉｓ @Ｒｙｈａｖｅａｎ Ｔｈｉｓ ｉｓ ｍｙ ｃｈａｎｎｅｌ. Ｔｒｙ ｔｏ ｓｔａｙ ａｗａｙ ｆｒｏｍ ｅｖｅｒｙ ｓｃｕｍｂａｇ ｗｈｏ ｄｏｅｓ ｄｉｒｔｙ/ｓｈａｄｙ ｔｈｉｎｇｓ",
    "Ħ𝕖𝕝𝕝𝕠, 𝕞𝕪 𝕟𝕒𝕞𝕖 𝕚𝕤 @ℝ𝕪𝕙𝕒𝕧𝕖𝕒𝕟 𝕋𝕙𝕚𝕤 𝕚𝕤 𝕞𝕪 𝕔𝕙𝕒𝕟𝕟𝕖𝕝. 𝕋𝕣𝕪 𝕥𝕠 𝕤𝕥𝕒𝕪 𝕒𝕨𝕒𝕪 𝕗𝕣𝕠𝕞 𝕖𝕧𝕖𝕣𝕪 𝕤𝕔𝕦𝕞𝕓𝕒𝕘 𝕨𝕙𝕠 𝕕𝕠𝕖𝕤 𝕕𝕚𝕣𝕥𝕪/𝕤𝕙𝕒𝕕𝕪 𝕥𝕙𝕚𝕟𝕘𝕤",
    "Hᴇʟʟᴏ, ᴍʏ ɴᴀᴍᴇ ɪs @Rʏʜᴀᴠᴇᴀɴ Tʜɪs ɪs ᴍʏ ᴄʜᴀɴɴᴇʟ. Tʀʏ ᴛᴏ sᴛᴀʏ ᴀᴡᴀʏ ғʀᴏᴍ ᴇᴠᴇʀʏ sᴄᴜᴍʙᴀɢ ᴡʜᴏ ᴅᴏᴇs ᴅɪʀᴛʏ/sʜᴀᴅʏ ᴛʜɪɴɢs",
    "Hᴇʟʟᴏ, ᴍʏ ɴᴀᴍᴇ ɪs @Ryʜᴀᴠᴇᴀɴ Tʜɪs ɪs ᴍʏ ᴄʜᴀɴɴᴇʟ. Tʀʏ ᴛᴏ sᴛᴀʏ ᴀᴡᴀʏ ғʀᴏᴍ ᴇᴠᴇʀʏ sᴄᴜᴍʙᴀɢ ᴡʜᴏ ᴅᴏᴇs ᴅɪʀᴛʏ/sʜᴀᴅʏ ᴛʜɪɴɢs",
    "ℌ𝔢𝔩𝔩𝔬, 𝔪𝔶 𝔫𝔞𝔪𝔢 𝔦𝔰 @ℜ𝔶𝔥𝔞𝔳𝔢𝔞𝔫 𝔗𝔥𝔦𝔰 𝔦𝔰 𝔪𝔶 𝔠𝔥𝔞𝔫𝔫𝔢𝔩. 𝔗𝔯𝔶 𝔱𝔬 𝔰𝔱𝔞𝔶 𝔞𝔴𝔞𝔶 𝔣𝔯𝔬𝔪 𝔢𝔳𝔢𝔯𝔶 𝔰𝔠𝔲𝔪𝔟𝔞𝔤 𝔴𝔥𝔬 𝔡𝔬𝔢𝔰 𝔡𝔦𝔯𝔱𝔶/𝔰𝔥𝔞𝔡𝔶 𝔱𝔥𝔦𝔫𝔫𝔤𝔰",
    "ℋℯ𝓁𝓁ℴ, 𝓂𝓎 𝓃𝒶𝓂ℯ 𝒾𝓈 @ℛ𝓎𝒽𝒶𝓋ℯ𝒶𝓃 𝒯𝒽𝒾𝓈 𝒾𝓈 𝓂𝓎 𝒸𝒽𝒶𝓃𝓃ℯ𝓁. 𝒯𝓇𝓎 𝓉ℴ 𝓈𝓉𝒶𝓎 𝒶𝓌𝒶𝓎 𝒻𝓇ℴ𝓂 ℯ𝓋ℯ𝓇𝓎 𝓈𝒸𝓊𝓂𝒷𝒶ℊ 𝓌𝒽ℴ 𝒹ℴℯ𝓈 𝒹𝒾𝓇𝓉𝓎/𝓈𝒽𝒶𝒹𝓎 𝓉𝒽𝒾𝓃ℊ𝓈",
    "Hҽllσ, mч nαmҽ íѕ @Rчhαvєαn Thíѕ íѕ mч chαnnєl. Trч tσ ѕtαч αwαч frσm єvєrч ѕcumвαg whσ dσєѕ dírtч/ѕhαdч thíngѕ",
    "Hêllð, m¥ ñåmê ï§ @R¥håvêåñ Thï§ ï§ m¥ çhåññêl. Tr¥ þð §þå¥ åwå¥ £rðm êvêr¥ §çumbåg whð ððê§ ðïrþ¥/§håð¥ þhïñg§",
    "Hǝllo, ɯʎ uɐɯǝ ıs @Ryɥɐʌǝɐu Tɥıs ıs ɯʎ cɥɐuuǝl. Try ʇo sʇɐʎ ɐʍɐʎ ɟroɯ ǝʌǝry scuɯqɐƃ ʍɥo poǝs pırʇy/sɥɐpy ʇɥıuƃs"
]

bot = Bot(token=API_TOKEN)
logging.basicConfig(level=logging.INFO)

async def start_typing():
    print("Bot işə düşdü...")
    while True:
        for font_text in FONTS:
            current_display = ""
            # Hərf-hərf yazma hissəsi
            for char in font_text:
                current_display += char
                try:
                    await bot.edit_message_text(
                        chat_id=CHAT_ID,
                        message_id=MESSAGE_ID,
                        text=current_display
                    )
                    await asyncio.sleep(0.8) # Sənin istədiyin sürət
                except Exception as e:
                    # Flood limitə düşəndə və ya eyni mətni göndərəndə xətanı keç
                    if "message is not modified" in str(e):
                        continue
                    elif "retry after" in str(e).lower():
                        wait_time = int(''.join(filter(str.isdigit, str(e))))
                        print(f"Limitə düşdük. {wait_time} saniyə gözlənilir...")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"Xəta: {e}")
                        await asyncio.sleep(5)

            await asyncio.sleep(2) # Fontlar arası fasilə

if __name__ == "__main__":
    asyncio.run(start_typing())
