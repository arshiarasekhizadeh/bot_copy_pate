import re
import os
import json
import asyncio
import logging
from telegram import Update
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

channel_origin = {}
channel_destination = {}

you_username = 'Arshiarasekhi'
api_id = '15149922'
api_hash = '645874defad2a0a502e67f3301b6db52'
your_phone = '+989034151503'

client = TelegramClient(you_username, api_id, api_hash)
client.start()

if not client.is_user_authorized():
    client.send_code_request(your_phone)
    try:
        client.sign_in(your_phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))


async def send_message(origin_channel_id , destination_channel_id , time_1 , time_2) :
    msg_id = 0
    with open("origin.json" , 'r') as originf :
        origin = json.load(originf) 
    with open("destination.json" , "r") as destinationf :
        destination = json.load(destinationf)
    origin_message_pattern =  origin[origin_channel_id]
    regex_patern_origin = origin_message_pattern.replace("_any_" , "(\d+(?:,\d{3})*(?:\.\d+)?)")
    regex_patern_origin = regex_patern_origin.replace("_target_" , "(?P<target>\d+(?:,\d{3})*(?:\.\d+)?)")
    pattern = re.compile(regex_patern_origin)
    destination_message_pattern = destination[destination_channel_id]
    while (origin_channel_id in origin) and (destination_channel_id in destination):
        await asyncio.sleep(5)
        messages = await client.get_messages(origin_channel_id, limit=1)
        if msg_id == messages[0].id :
            continue
        message = messages[0].message
        time = int(str(messages[0].date).split(" ")[-1].split(":")[0]) + 3
        msg_id = messages[0].id
        if (time == time_1) or (time == time_2) :
            continue
        if re.match(pattern , message) :
            mach = re.search(pattern , message)
            target = mach.group("target")
            final_message = destination_message_pattern.replace("_target_" , target)
            await client.send_message(destination_channel_id, final_message, parse_mode='html')

async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    await update.message.reply_text("welcome to copy paste bot!\nto see all comands use /comannds")

async def comannds(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    await update.message.reply_text("use :  /setchannel_origin\nchannel_id(ex : some_channel_id)\nmessage_patern")
    await update.message.reply_text("use : /setchannel_destination\nchannel_id(ex : @some_channel_id)\nmessage_patern")
    await update.message.reply_text("use : /start\norigin_channel_id(ex : some_channel_id)\ndestination_channel_id(ex : some_channel_id)\ntime for bot to stop(ex : 10-14)")
    await update.message.reply_text("use : /delete_origin_channel\norigin_channel_id(ex : some_channel_id)")
    await update.message.reply_text("use : /delete_destination_channel\ndestination_channel_id(ex : some_channel_id)")
    await update.message.reply_text("use : /edit_origin_channel\norigin_channel_id(ex : some_channel_id\nnew message pattern")
    await update.message.reply_text("use : /edit_destination_channel\ndestination_channel_id(ex : some_channel_id\nnew message pattern")
    await update.message.reply_text("use : /my_origin_channels\nto see all of your origin channels")
    await update.message.reply_text("use : /my_destination_channels\nto see all of your destination channels")

async def setchannel_origin(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    origin_channel = update.message.text.split('\n')
    del origin_channel[0]
    message_pattern = "".join(origin_channel[1:])
    channel_origin[origin_channel[0]] = message_pattern
    if os.path.getsize("origin.json") == 0 :
        with open("origin.json" , 'w') as file :
            json.dump(channel_origin , file)
    elif os.path.getsize("origin.json") != 0 :
        with open("origin.json" , 'r') as f :
            data = json.load(f)
        with open("origin.json" , 'w') as file :
            message_pattern = "".join(origin_channel[1:])
            data[origin_channel[0]] = message_pattern
            json.dump(data , file)
    await update.message.reply_text("origin channel set sucssefuly.\nto edit origin channel use /edit_origin_channel")

async def setchannel_destination(update: Update, context: ContextTypes.DEFAULT_TYPE) : 
    destination_channel = update.message.text.split('\n')
    del destination_channel[0]
    message_pattern = "".join(destination_channel[1:])
    channel_destination[destination_channel[0]] = message_pattern
    if os.path.getsize("destination.json") == 0 :
        with open("destination.json" , 'w') as file :
            json.dump(channel_destination , file)
    elif os.path.getsize("destination.json") != 0 :
        with open("destination.json" , 'r') as f :
            data = json.load(f)
        with open("destination.json" , 'w') as file :
            message_pattern = "".join(destination_channel[1:])
            data[destination_channel[0]] = message_pattern
            json.dump(data , file)
    await update.message.reply_text("destination channel set sucssefuly.\nto edit destination channel use /edit_destination_channel")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if os.path.getsize("destination.json") == 0 or os.path.getsize("origin.json") == 0 :
        await update.message.reply_text("there is no origin channel or destination channel please set origin channel or destination channel first.")
    start_data = update.message.text.split('\n')
    del start_data[0]
    time1 = start_data[-1].split("-")[0]
    time2 = start_data[-1].split("-")[-1]
    loop = asyncio.get_event_loop()
    task = loop.create_task(send_message(start_data[0] , start_data[1] , time1 , time2))

async def delete_origin_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) : 
    with open("origin.json" , 'r') as originf :
        origin = json.load(originf)
    delete_data = update.message.text.split('\n')
    channel_id = delete_data[-1]
    origin.pop(channel_id)
    with open("origin.json" , 'w') as originf1 :
        json.dump(origin , originf1)
    await update.message.reply_text(f"'{channel_id}' channel sucsessfuly deleted from origin channels.")

async def delete_destination_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) : 
    with open("destination.json" , "r") as destinationf :
        destination = json.load(destinationf)
    delete_data = update.message.text.split('\n')
    channel_id = delete_data[-1]
    destination.pop(channel_id)
    with open("destination.json" , "w") as destinationf1 :
        json.dump(destination , destinationf1)
    await update.message.reply_text(f"'{channel_id}' channel sucsessfuly deleted from destinations channels.")

async def edit_destination_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) : 
    with open("destination.json" , 'r') as destinationf :
        destination = json.load(destinationf)
    edit_data = update.message.text.split("\n")
    del edit_data[0]
    message_pattern = "".join(edit_data[1:])
    destination[edit_data[0]] = message_pattern
    with open("destination.json" , "w") as destinationf1 :
        json.dump(destination , destinationf1)
    await update.message.reply_text("destination channel updated sucsessfuly")

async def edit_origin_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) : 
    with open("origin.json" , 'r') as originf :
        origin = json.load(originf)
    edit_data = update.message.text.split("\n")
    del edit_data[0]
    message_pattern = "".join(edit_data[1:])
    origin[edit_data[0]] = message_pattern
    with open("origin.json" , "w") as originf1 :
        json.dump(origin , originf1)
    await update.message.reply_text("origin channel updated sucsessfuly")

async def my_origin_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if os.path.getsize("origin.json") == 0 :
        await update.message.reply_text("you have no origin channels set")
    with open("origin.json" , 'r') as originf :
        origin = json.load(originf)
    for k,v in origin.items() :
        await update.message.reply_text(f"your origin channels are :\n@{k}\nwith this message pattern :\n{v}")

async def my_destination_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if os.path.getsize("destination.json") == 0 :
        await update.message.reply_text("you have no destination channels set")
    with open("destination.json" , 'r') as destinationf :
        destination = json.load(destinationf)
    for k,v in destination.items() :
        await update.message.reply_text(f"your destination channels are :\n@{k}\nwith this message pattern :\n{v}")

def main() -> None:
    application = Application.builder().token("6077844571:AAFqK0ZNCYTEdlG2k6w3jbfRCm_yl8R0AuI").build()

    start_handler = CommandHandler('start' , start)
    home_handler = CommandHandler('home' , home)
    command_handler = CommandHandler('comannds' , comannds)
    setchannel_origin_handler = CommandHandler('setchannel_origin' , setchannel_origin)
    setchannel_destination_handler = CommandHandler("setchannel_destination" , setchannel_destination)
    delete_origin_channel_handeler = CommandHandler('delete_origin_channel' , delete_origin_channel)
    delete_destination_channel_handler = CommandHandler('delete_destination_channel', delete_destination_channel)
    edit_destination_channel_handler = CommandHandler("edit_destination_channel" , edit_destination_channel)
    edit_origin_channel_handler = CommandHandler("edit_origin_channel" , edit_origin_channel)
    my_origin_channels_handler = CommandHandler("my_origin_channels" , my_origin_channels)
    my_destination_channels_handler = CommandHandler("my_destination_channels" , my_destination_channels)

    application.add_handler(start_handler)
    application.add_handler(home_handler)
    application.add_handler(command_handler)
    application.add_handler(setchannel_origin_handler)
    application.add_handler(setchannel_destination_handler)
    application.add_handler(delete_origin_channel_handeler)
    application.add_handler(delete_destination_channel_handler)
    application.add_handler(edit_destination_channel_handler)
    application.add_handler(edit_origin_channel_handler)
    application.add_handler(my_origin_channels_handler)
    application.add_handler(my_destination_channels_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()