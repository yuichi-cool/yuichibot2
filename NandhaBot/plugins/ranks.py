import os
import io
import traceback
import sys
import config

from contextlib import redirect_stdout
from NandhaBot import bot
from pyrogram.types import *
from pyrogram import filters
from NandhaBot import rank

      
@bot.on_message(filters.user(rank.RANK_A_USER) & filters.command("eval",config.COMMANDS))
async def eval(client, message):
    status_message = await message.reply_text("Processing ...")
    if len(message.command) <2:
        return await status_message.edit("`GIVE CODE TO RUN..`")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "<b>EVAL</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)



@bot.on_message(
    filters.command("logs", prefixes=[".", "/", ";", "," "*"]) & filters.user(dev_user)
)
def sendlogs(_, m: Message):
    logs = run("tail logs.txt")
    x = paste(logs)
    keyb = [
        [
            InlineKeyboardButton("Link", url=x),
            InlineKeyboardButton("File", callback_data="sendfile"),
        ],
    ]
    m.reply(x, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(keyb))



@bot.on_callback_query(filters.regex("sendfile"))
def sendfilecallback(_, query: CallbackQuery):
    sender = query.from_user.id
    query.message.chat.id

    if sender in dev_user:
        query.message.edit("`Sending...`")
        query.message.reply_document("logs.txt")
      
