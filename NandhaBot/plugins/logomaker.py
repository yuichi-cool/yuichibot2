import requests


from NandhaBot import telebot

@telebot.message_handler(commands=['logo'])
def logo(message):
    logo_name = message.text.split(None, 1)[1]
    
    try:
       API = f"https://api.sdbots.tk/anime-logo?name={logo_name}"
       req = requests.get(API).url
       telebot.send_photo(
            message.chat.id,
            photo=req,
            caption="Successfully Generated by Trunks",
            reply_to_message_id=message.id)
    except Exception as e:
        telebot.reply_to(message, e)
  
telebot.infinity_polling()     
