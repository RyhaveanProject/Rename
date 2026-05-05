import asyncio
import logging
from aiogram import Bot
from aiogram.utils import exceptions

# Məlumatlar
API_TOKEN = '8712453996:AAHfzva1GZ9WDIxjhMK_rZoLtvy2j2L99vY'
CHAT_ID = '@rveanx'
MESSAGE_ID = 267 # Şəkilli mesajın ID-si

FONTS = [
    "Hello, my name is @Ryhavean  ненависть к прошлому  это застывшая боль которая маскируется под силу Настоящая сила перестать воевать с тем, чего уже нет и начать строить то что будет завтрa"
]

bot = Bot(token=API_TOKEN)
logging.basicConfig(level=logging.INFO)

async def start_typing():
    print("Şəkilli mesaj redaktə rejimi aktivdir...")
    while True:
        for font_text in FONTS:
            # Axıcılıq üçün hər 4 simvoldan bir (step=4)
            step = 4
            for i in range(0, len(font_text) + step, step):
                current_display = font_text[:i]
                if not current_display:
                    continue
                
                try:
                    # Şəkilli mesajlar üçün xüsusi funksiya:
                    await bot.edit_message_caption(
                        chat_id=CHAT_ID,
                        message_id=MESSAGE_ID,
                        caption=current_display
                    )
                    # Saniyədə 1 edit limitini aşmamaq üçün 1.2 saniyə gözləmə
                    await asyncio.sleep(1.5) 
                    
                except exceptions.RetryAfter as e:
                    print(f"Limit: {e.timeout} saniyə gözlənilir...")
                    await asyncio.sleep(e.timeout)
                except exceptions.MessageNotModified:
                    continue
                except exceptions.MessageToEditNotFound:
                    print("Xəta: Mesaj ID-si tapılmadı.")
                    return
                except Exception as e:
                    print(f"Gözlənilməz xəta: {e}")
                    await asyncio.sleep(1.5)

            await asyncio.sleep(1.5) # Cümlə bitəndə fasilə

if __name__ == "__main__":
    asyncio.run(start_typing())
