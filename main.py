import asyncio
import logging
from aiogram import Bot

# Məlumatlar
API_TOKEN = '8712453996:AAHfzva1GZ9WDIxjhMK_rZoLtvy2j2L99vY'
CHAT_ID = '@rveanx'  # Kanalın istifadəçi adı
MESSAGE_ID = 267     # Mesajın ID-si

# 10 fərqli font (Unicode əsaslı)
FONTS = [
    "Hello, my name is @Ryhavean  ненависть к прошлому  это застывшая боль которая маскируется под силу Настоящая сила перестать воевать с тем, чего уже нет и начать строить то что будет завтра",
  
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
                    await asyncio.sleep(0.4) # Sənin istədiyin sürət
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
