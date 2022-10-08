import config


from pyrogram import filters
from NandhaBot import bot
from NandhaBot.helpers.scansdb import (
get_scan_users, add_scan_user, get_scan_user,
 is_scan_user, remove_scan_user, update_scan_reason, update_scan_proof
)

from NandhaBot.rank import RANK_USERS


SCAN_TEXT = """
which date this 
scan process: {}

scanned user: {}
reason: {}
"""

CHECK_TEXT = """
SCANNED USER:

scanned id: {}
the reason for scan: 
{}

some proofs:
{}

scanned date: {}
"""
@bot.on_message(filters.command("scan",config.COMMANDS))
async def scan(_, message):
      reply = message.reply_to_message
      date = message.date
      msg = await message.reply_text("`scanning....`")
      if not message.from_user.id in (await RANK_USERS()):
          return await msg.edit("`you don't have enough rights to use me.`")
      elif len(message.command) <2:
          return await msg.edit("`you need to use correct `/formatting` for scanning someone else.`")
      elif reply:
         try:
            user_id = int(reply.from_user.id)
            reason = message.text.split("-r")[1]
            mention = f"[{user_id}](tg://user?id={user_id})"
            if (await is_scan_user(user_id)) == True:
                  await update_scan_reason(user_id,reason,date)
                  await bot.send_message(config.LOG_CHANNEL_ID, text=SCAN_TEXT.format(date,mention,reason))
                  await msg.edit("`the user already scanned.\nI have updated the details!`")
            else:
                  await add_scan_user(user_id,reason,date)
                  await bot.send_message(config.LOG_CHANNEL_ID, text=SCAN_TEXT.format(date,mention,reason))
                  await msg.edit("`the user successfully scanned!`")
         except Exception as e:
             await msg.edit(str(e))
      elif not reply:
            try:
               user_id = int(message.text.split("-u")[1].split("-r")[0])
               reason = message.text.split("-r")[1]
               mention = f"[{user_id}](tg://user?id={user_id})"
               if (await is_scan_user(user_id)) == True:
                  await update_scan_reason(user_id,reason,date)
                  await bot.send_message(config.LOG_CHANNEL_ID, text=SCAN_TEXT.format(date,mention,reason))
                  await msg.edit("`the user already scanned.\nI have updated the details!`")
               else:
                  await add_scan_user(user_id,reason,date)
                  await bot.send_message(config.LOG_CHANNEL_ID, text=SCAN_TEXT.format(date,mention,reason))  
                  await msg.edit("`the user successfully scanned!`")            
            except Exception as e:
               await msg.edit(str(e))
      
      
@bot.on_message(filters.command("addproof",config.COMMANDS))
async def addproof(_, message):
      reply = message.reply_to_message
      date = message.date
      msg = await message.reply_text("`adding proof...`")
      if not message.from_user.id in (await RANK_USERS()):
           return await msg.edit("`you don't have enough rights to use me.`")
      elif len(message.command) <2:
           return await msg.edit("`use a correct format for add proof.`")
      else:  
          try:           
             user_id = int(message.text.split("-u")[1].split("-p")[0])
             proof = message.text.split("-p")[1]
             if not user_id in (await get_scan_users()):
                 return await msg.edit("`this user not a scanned user to add proof.`")

             await update_scan_proof(user_id,proof,date)
             await msg.edit("`Successfully proof added!`")   
          except Exception as e:
              await msg.edit(str(e))

@bot.on_message(filters.command("check",config.COMMANDS))
async def check(_, message):
       reply = message.reply_to_message
       msg = await message.reply_text("`checking...`")
       if not message.from_user.id in (await RANK_USERS()):
            return await msg.edit_text("`your don't have enough rights to use me.`")
       elif len(message.command) <2:
            return await msg.edit_text("`use a correct format for check user.`")
       else:
         try:
             user_id = int(message.text.split("-u")[1])
             if (await is_scan_user(user_id)) == False:
                  return await msg.edit_text("`This user not scanned.`")
             else:
                 details = await get_scan_user(user_id)
                 user_id = details["user_id"]
                 reason = details["reason"]
                 date = details["date"]
                 proof = details["proof"]
                 await bot.send_message(message.chat.id, 
                 text=CHECK_TEXT.format(user_id,reason,proof,date),disable_web_page_preview=True)
              
         except Exception as e:
             await msg.edit_text(str(e))
