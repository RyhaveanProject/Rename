"""
Telegram Channel Caption Animator
=================================
Optimized "typing animation" bot that edits the caption of a single
channel post character-by-character to simulate live typing.

Key performance fixes vs. original:
  • Latency-aware pacing: subtract network round-trip from sleep
  • Step size tuned (8) — smooth visual + fewer API calls
  • Effective pace ~2.5s (Telegram's real limit for channel post
    caption edits) → no flood waits, no freezes
  • Adaptive backoff: auto-increases interval when throttled,
    relaxes back on success
  • Proper RetryAfter handling without double-sleeping
  • Reads config from environment variables (Railway-ready)
"""

import asyncio
import logging
import os
import time

from aiogram import Bot
from aiogram.utils import exceptions

# ──────────────────────────────  CONFIG  ──────────────────────────────
API_TOKEN = os.getenv("API_TOKEN", "8712453996:AAHfzva1GZ9WDIxjhMK_rZoLtvy2j2L99vY")
CHAT_ID = os.getenv("CHAT_ID", "@rveanx")
MESSAGE_ID = int(os.getenv("MESSAGE_ID", "267"))

# Performance knobs ────────────────────────────────────────────────────
# How many characters to add per edit. Higher = visually faster animation
# (more text appears per second), fewer total API calls. Sweet spot: 8.
STEP = int(os.getenv("STEP", "8"))

# Target seconds *between the start of consecutive edits*.
# Telegram's real limit for editing the same channel post is roughly
# ~30 edits/minute (~1 edit / 2.5s). Going faster triggers RetryAfter
# (10-60s) which is exactly what was making the bot freeze.
EDIT_INTERVAL = float(os.getenv("EDIT_INTERVAL", "2.5"))

# Pause between full-text cycles
CYCLE_PAUSE = float(os.getenv("CYCLE_PAUSE", "2.0"))

# Adaptive: if we hit flood waits, gently increase the interval.
ADAPTIVE_BACKOFF = True
_current_interval = EDIT_INTERVAL

FONTS = [
    "Hello, my name is @Ryhavean  ненависть к прошлому  это застывшая боль "
    "которая маскируется под силу Настоящая сила перестать воевать с тем, "
    "чего уже нет и начать строить то что будет завтрa"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("animator")

bot = Bot(token=API_TOKEN, parse_mode=None)


async def edit_caption(text: str) -> bool:
    """Edit the caption once. Returns True on success, False if skipped."""
    global _current_interval
    try:
        await bot.edit_message_caption(
            chat_id=CHAT_ID,
            message_id=MESSAGE_ID,
            caption=text,
        )
        # Successful edit → gradually relax interval back toward configured value
        if ADAPTIVE_BACKOFF and _current_interval > EDIT_INTERVAL:
            _current_interval = max(EDIT_INTERVAL, _current_interval * 0.97)
        return True
    except exceptions.RetryAfter as e:
        wait = float(e.timeout) + 0.05
        log.warning("Flood limit, waiting %.2fs", wait)
        await asyncio.sleep(wait)
        if ADAPTIVE_BACKOFF:
            _current_interval = min(_current_interval + 0.25, 5.0)
            log.info("Adaptive interval bumped to %.2fs", _current_interval)
        return False
    except exceptions.MessageNotModified:
        return False
    except exceptions.MessageToEditNotFound:
        log.error("Message id %s not found in %s — stopping.", MESSAGE_ID, CHAT_ID)
        raise
    except exceptions.TelegramAPIError as e:
        log.error("API error: %s", e)
        await asyncio.sleep(0.5)
        return False


async def animate() -> None:
    log.info(
        "Animation started: chat=%s msg_id=%s step=%d interval=%.2fs",
        CHAT_ID, MESSAGE_ID, STEP, EDIT_INTERVAL,
    )

    last_caption = None
    next_deadline = time.monotonic()

    while True:
        for font_text in FONTS:
            length = len(font_text)
            frames = [font_text[: min(i, length)] for i in range(STEP, length + STEP, STEP)]

            for frame in frames:
                if frame == last_caption:
                    continue

                # Latency-aware pacing — sleep only as much as needed
                now = time.monotonic()
                if now < next_deadline:
                    await asyncio.sleep(next_deadline - now)

                start = time.monotonic()
                ok = await edit_caption(frame)
                if ok:
                    last_caption = frame

                # Schedule the next edit relative to when this one started
                next_deadline = start + (_current_interval if ADAPTIVE_BACKOFF else EDIT_INTERVAL)

            await asyncio.sleep(CYCLE_PAUSE)


async def main() -> None:
    try:
        await animate()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Stopped by user")
