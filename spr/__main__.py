import asyncio
import re
from importlib import import_module as import_

from pyrogram import filters, idle
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from spr import BOT_USERNAME, conn, session, spr
from spr.core import ikb
from spr.modules import MODULES
from spr.utils.misc import once_a_day, paginate_modules

HELPABLE = {}


async def main():
    await spr.start()
    # Load all the modules.
    for module in MODULES:
        imported_module = import_(module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.lower()
                ] = imported_module
    print("STARTED !")
    loop = asyncio.get_running_loop()
    loop.create_task(once_a_day())
    await idle()
    conn.commit()
    conn.close()
    await session.close()
    await spr.stop()


@spr.on_message(filters.command(["sphelp", "spstart"]), group=2)
async def help_command(_, message: Message):
    if message.chat.type != "private":
        kb = ikb({"Help": f"https://t.me/{BOT_USERNAME}?start=help"})
        return await message.reply("Pm Me For Help", reply_markup=kb)
    kb = ikb(
        {
            "Help": "bot_commands",
        }
    )
    mention = message.from_user.mention
    await message.reply_photo(
        "https://hamker.me/logo_3.png",
        caption=f"Hi {mention}, I'm Stacy SPB, I can protect "
        + "your group from Spam and NSFW media using "
        + "machine learning. Choose an option from below."
        + " Here is the help for Stacy's Spam Protection:"
        + "/anti_nsfw [ENABLE|DISABLE] - Enable or disable NSFW Detection."
        + "/anti_spam [ENABLE|DISABLE] - Enable or disable Spam Detection."
        + "/nsfw_scan - Classify a media."
        + "/spam_scan - Get Spam predictions of replied message.",
        reply_markup=kb,
    )


@spr.on_message(filters.command("runs"), group=3)
async def runs_func(_, message: Message):
    await message.reply("What am i? Rose?")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
