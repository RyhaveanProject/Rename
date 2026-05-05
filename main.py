import asyncio
import logging
from aiogram import Bot
from aiogram.utils.exceptions import FloodControlRetryAfter, MessageNotModified

# Məlumatlar
API_TOKEN = '8712453996:AAHfzva1GZ9WDIxjhMK_rZoLtvy2j2L99vY'
CHAT_ID = '@rveanx'
MESSAGE_ID = 267

FONTS = [
    "Hello, my name is @Ryhavean  ненависть к прошлому  это застывшая боль которая маскируется под силу Настоящая сила перестать воевать с тем, чего уже нет и начать строить то что будет завтрa"
]

bot = Bot(token=API_TOKEN)
logging.basicConfig(level=logging.INFO)

async def start_typing():
    print("Bot optimallaşdırılmış rejimdə işə düşdü...")
    while True:
        for font_text in FONTS:
            # Hər hərfdə yox, hər 4 simvoldan bir yeniləyirik (Axıcılıq üçün)
            step = 4
            for i in range(0, len(font_text) + step, step):
                current_display = font_text[:i]
                if not current_display:
                    continue
                
                try:
                    await bot.edit_message_text(
                        chat_id=CHAT_ID,
                        message_id=MESSAGE_ID,
                        text=current_display
                    )
                    # 1.0 və ya 1.2 saniyə Telegram limitləri üçün ən stabil vaxtdır
                    await asyncio.sleep(0.5) 
                    
                except FloodControlRetryAfter as e:
                    print(f"Limit: {e.retry_after} saniyə gözlənilir...")
                    await asyncio.sleep(e.retry_after)
                except MessageNotModified:
                    continue
                except Exception as e:
                    print(f"Gözlənilməz xəta: {e}")
                    await asyncio.sleep(0.5)

            await asyncio.sleep(3) # Mətn bitəndə fasilə

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_typing())
    except KeyboardInterrupt:
        pass
