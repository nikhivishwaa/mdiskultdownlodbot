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

BOT_USERNAME = os.environ.get("BOT_USERNAME", "MdiskDownloadersBot")
BOT_NAME = os.environ.get("BOT_NAME", "Mdisk Downloader Bot")
bot_token = os.environ.get("TOKEN", "5336784270:AAHLLAdyoCKLt5_XdV_Aj1UAqHLB5b_Li1g") 
api_hash = os.environ.get("HASH", "db62aa57ef8162bb4c95d0cf81e1c09b") 
api_id = os.environ.get("ID", "7651392") 

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)

TG_SPLIT_SIZE = 2097151000

@app.on_message(filters.command(["start", "help"]))
def echo(client, message):
       app.send_message(message.chat.id, f'**Hi 👋\n\nI Am {BOT_NAME}\n\nUse Me To Download Mdisk Link To Video\n\nSend Me The Mdisk Link Like ➡️\n /mdisk https://mdisk.me/convertr/250×380/asd12**',
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
    app.send_message(message.chat.id, '📥 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠....\n\n**Its Take Some Time Depend On Your File Size. Wait for Downloading ⬇️ do not 🗑 Delete bot before Download is Complete ✅**')
    file = mdisk.mdow(link,v,a,message)
    size = split.get_path_size(file)
    #get_path_size = os.path.splitext(get_path_size)[0] + "." + "mkv"
    #size = os.stat(get_path_size).st_size
    if(size > 2097151000):
        app.send_message(message.chat.id, 'Congratulations🎉\n\n Your Mdisk Link🔗 Video 📁File is ⬇️ Downloaded Successfully ✅.\n\n Now ✂ 𝗦𝗽𝗹𝗶𝘁𝗶𝗻𝗴 ↔️ Your 📁File \n So you Got ✌ Two 📁Files Or More Than 2 Files.\n\n\n ⚜️ Rᴇᴀsᴏɴ : ғɪʟᴇ sɪᴢᴇ ɪs ʙɪɢɢᴇʀ ᴛʜᴇɴ 𝟸ɢʙ.')
        flist = split.split_file(file,size,file,".", TG_SPLIT_SIZE)
        flist = split.split_file(file,size,file,".", TG_SPLIT_SIZE)
        os.remove(file)
        app.send_message(message.chat.id, 'Congratulations🎉\n\n Your Mdisk Link🔗 Video 📁File is ⬇️ Downloaded Successfully ✅.\n\n 🔸 And After Process Your Mdisk Link 🔗 Video 📁File is Started to Uploading ⬆️\n\n\n ⚜️ Nᴏᴛɪᴄᴇ : ᴅᴏ ɴᴏᴛ ᴅᴇʟᴇᴛᴇ ᴄʜᴀᴛ ʙᴇғᴏʀᴇ ᴜᴘʟᴏᴀᴅɪɴɢ ɪs ᴅᴏɴᴇ.')
        i = 1
        for ele in flist:
            app.send_document(message.chat.id,document=ele,caption=f"part {i}")
            i = i + 1
            os.remove(ele)
    else: 
        app.send_message(message.chat.id, '𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠')
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
        app.send_message(message.chat.id, '**Wrong Method Send /mdisk Link**')

              
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
            app.send_message(message.chat.id, "**First Send Me Link With /mdisk**")



app.run()
app.start()
print("\n\nMdisk Link Downloader Bot Started")
