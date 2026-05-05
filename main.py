import asyncio
import logging
from aiogram import Bot
from aiogram.utils import exceptions

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
    print("Bot yenidən başladılır...")
    while True:
        for font_text in FONTS:
            # Axıcılıq üçün hər 4 simvoldan bir yeniləyirik
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
                    # Saniyədə 1 edit limitini aşmamaq üçün 1.2-1.5 saniyə gözləmə
                    await asyncio.sleep(1) 
                    
                except exceptions.RetryAfter as e:
                    print(f"Limit: {e.timeout} saniyə gözlənilir...")
                    await asyncio.sleep(e.timeout)
                except exceptions.MessageNotModified:
                    continue
                except Exception as e:
                    print(f"Xəta: {e}")
                    await asyncio.sleep(1)

            await asyncio.sleep(1) # Cümlə bitəndə qısa fasilə

if __name__ == "__main__":
    asyncio.run(start_typing())
