import config

from NandhaBot import bot
from pyrogram import filters
from pyrogram.types import *

BANNED_TEXT = "Another one dust Cleared {}!"

@bot.on_message(filters.command("ban",config.COMMANDS))
def bans(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    if not reply:
       try:
          
       except Exception as error:
            message.reply_text(str(error))
    else:
         try:
           user_id = message.reply_to_message.from_user.id
           bot.ban_chat_member(chat_id, user_id)
           user_info = bot.get_chat(user_id)
           name = user_info.first_name
           message.reply_text(BANNED_TEXT.format(name)
         except Exception as e:
            message.reply_text(str(e))
