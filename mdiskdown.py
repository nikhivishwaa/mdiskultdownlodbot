from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.raw.functions.bots import SetBotCommands
from pyrogram.raw.types import BotCommand, BotCommandScopeDefault
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
import os
import asyncio
import time
import threading
import mdisk
import split

BOT_USERNAME = os.environ.get("BOT_USERNAME", "MdiskDownloaderultronBot")
BOT_NAME = os.environ.get("BOT_NAME", "Mdisk link Downloader")
bot_token = os.environ.get("TOKEN", "5260749200:AAGAn7-UDsaUsf1P6a5m9FSflkZBJ9GTOBE") 
api_hash = os.environ.get("HASH", "168c8159234070c260a85df74feae727") 
api_id = os.environ.get("ID", "19977122") 

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)

TG_SPLIT_SIZE = 2097151000

@app.on_message(filters.command(["start", "help"]))
def echo(client, message):
       app.send_message(message.chat.id, f'Hi 👋\n\nI Am {BOT_NAME}\n\nUse Me To Download Mdisk Link To 📁File\n\nSend Me The Mdisk Link Like ➡️\n /mdisk https://mdisk.me/link',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🙏 Support Group", url=f"https://t.me/+WyQN-XIUKUU1Mzk1"),
                    InlineKeyboardButton("📢 Updates Channel", url=f"https://t.me/Tech_Ai_Bots"),
                ],
            ]
        ),
        disable_web_page_preview=False,
    ) 


def down(v,a,message,link):
    app.send_message(message.chat.id, '📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ.... Yᴏᴜʀ Lɪɴᴋ\n\n I Nᴏᴛɪғʏ Yᴏᴜ Wʜᴇɴ Dᴏᴡɴʟᴏᴀᴅ 📁 Is Cᴏᴍᴘʟᴇᴛᴇ.')
    file = mdisk.mdow(link,v,a,message)
    size = split.get_path_size(file)
    #get_path_size = os.path.splitext(get_path_size)[0] + "." + "mkv"
    #size = os.stat(get_path_size).st_size
    if(size > 2097151000):
        app.send_message(message.chat.id, '📥 ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ ✅\n\n  Now ✂ Sᴘʟɪᴛɪɴɢ Your 📁File to below 2GB\n\n\n.')
        flist = split.split_file(file,size,file,".", TG_SPLIT_SIZE)
        flist = split.split_file(file,size,file,".", TG_SPLIT_SIZE)
        os.remove(file)
        app.send_message(message.chat.id, '⚜️Your File📁 Sᴘʟɪᴛᴇᴅ 📖 \n\n 🔸 Now Uploading Your 📁File\n\n⚜️ ᴜsᴇ @File_Thumbnail_bot')
        i = 1
        for ele in flist:
            app.send_document(message.chat.id,document=ele,caption=f"part {i}")
            i = i + 1
            os.remove(ele)
    else: 
        app.send_message(message.chat.id, ' 📥 ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ ✅ \n\n 🔸 Now 📤 Uploading Your 📁File\n\n⚜️ ᴜsᴇ @File_Thumbnail_bot')
        app.send_document(message.chat.id,document=file)
        os.remove(file)


@app.on_message(filters.command(["mdisk"]))
def echo(client, message):
    try:
        link = message.text.split("mdisk ")[1]
        if "mdisk" in link:
            out = mdisk.req(link)
            app.send_message(message.chat.id, out)
            app.send_message(message.chat.id, 'Send VideoID,AudioID Like >> 2,1')
            with open(f"{message.chat.id}.txt","w") as ci:
                ci.write(link)
    except:
        app.send_message(message.chat.id, '❎ Wrong Method 🔄 Send me\n /mdisk https://mdisk.me/link \n\n ↔️ Iɴ Bᴇᴛᴡᴇᴇɴ Tʜᴇ Cᴏᴍᴍᴀɴᴅ Aɴᴅ Mᴅɪsᴋ Lɪɴᴋ Gɪᴠᴇ ᴀ Sᴘᴀᴄᴇ.')

              
@app.on_message(filters.text)
def echo(client, message):
        if os.path.exists(f"{message.chat.id}.txt"):
            with open(f"{message.chat.id}.txt","r") as li:
                link = li.read()
            link = link.split("\n")[0] 
            os.remove(f"{message.chat.id}.txt")
            ids = message.text.split(",")
            d = threading.Thread(target=lambda:down(ids[0],ids[1],message,link),daemon=True)
            d.start()
            #await down(ids[0],ids[1],message,link)
        else:
            app.send_message(message.chat.id, "🥇First Send Me The Mdisk Link🔗 With Command /mdisk")



app.run()
app.start()
print("\n\nMdisk To File Bot Started")
