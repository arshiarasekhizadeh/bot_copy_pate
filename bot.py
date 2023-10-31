import re
import os
import json
import random
import asyncio
import logging
from telegram import Update
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


Send_message = True
msg_id_data = [0]
target_data = [0]
send_message_data = []
edit_origin_data = []
edit_destination_data = []
origin_data = []
destination_data = []



ID , PATTERN , TIMEON , AMOUNT_CHANGE , MESSAGE_TO_ADD_A_AMOUNT , AMOUNT_TO_ADD = range(6)
ID_DESTINATION , PATTERN_DESTINATION = range(2)
TEST_PATERN_ORIGIN = range(1)
TEST_PATERN_DESTINATION = range(1)
ID_EDIT_ORIGIN , PATTERN_EDIT_ORIGIN , TIMEON_EDIT_ORIGIN = range(3)
ID_EDIT_DESTINATION , PATTERN_EDIT_DESTINATION , TIMEON_EDIT_DESTINATION = range(3)
ID_DEL_ORIGIN = range(1)
ID_DEL_DESTINATION = range(1)
ID_START , PATTERN_START = range(2)


you_username = 'YOUR TELEGRAM USERNAME'
api_id = 'YOUR TELEGRAM API ID'
api_hash = 'YOUR TELEGRAM API HASH'
your_phone = 'YOUR TELEGRAM PHONE NUMBER'

client = TelegramClient(you_username, api_id, api_hash)
client.start()

if not client.is_user_authorized():
    client.send_code_request(your_phone)
    try:
        client.sign_in(your_phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))


async def send_message(origin_channel_id , destination_channel_id) :
    Send_message = True
    with open("origin.json" , 'r') as originf :
        origin = json.load(originf) 
    with open("destination.json" , "r") as destinationf :
        destination = json.load(destinationf)
    n = random.randrange(messgae_to_add_amount)
    counter = 0
    counter_m = 0
    while (origin_channel_id in origin) and (destination_channel_id in destination) and Send_message == True :
        await asyncio.sleep(5)
        with open("origin.json" , 'r') as originf :
            origin = json.load(originf) 
        with open("destination.json" , "r") as destinationf :
            destination = json.load(destinationf)
        messgae_to_add_amount = int(origin[origin_channel_id][3])
        start_time = origin[origin_channel_id][1].split("-")
        time1 = start_time[0]
        time2 = start_time[1]
        amount_change = int(origin[origin_channel_id][2])
        amount_to_add = int(origin[origin_channel_id][4])
        origin_message_pattern =  origin[origin_channel_id][0]
        destination_message_pattern = destination[destination_channel_id][0]
        regex_patern_origin = origin_message_pattern.replace("_any_" , "(\d+(?:,\d{3})*(?:\.\d+)?)")
        regex_patern_origin = regex_patern_origin.replace("_target_" , "(?P<target>\d+(?:,\d{3})*(?:\.\d+)?)")    
        pattern = re.compile(regex_patern_origin)
        messages = await client.get_messages(origin_channel_id, limit=5)
        messages = list(messages)
        for m in messages :
            message = m.message            
            time = int(str(m.date).split(" ")[-1].split(":")[0]) + 3
            if re.match(pattern , message) and (time >= int(time1)) and (time <= int(time2)):
                mach = re.search(pattern , message)
                target = mach.group("target")
                target = target.replace(',' , "")
                target = int(target)
                if counter == n :
                    target += amount_to_add
                    n = random.randrange(messgae_to_add_amount)
                    counter = 0
                if len(target_data) == 100 :
                    ld = target_data[-1]
                    target_data.clear()
                    target_data.append(ld)
                if len(msg_id_data) == 300 :
                    lmi = msg_id_data[-1]
                    msg_id_data.clear()
                    msg_id_data.append(lmi)
                if abs(target - target_data[-1]) < amount_change and counter_m == 5:
                    counter_m = 0
                    continue
                if m.id in msg_id_data:
                    continue 
                final_message = destination_message_pattern.replace("_target_" , str(target))
                await client.send_message(destination_channel_id, final_message, parse_mode='html')
                msg_id_data.append(m.id)
                target_data.append(target)
        counter_m += 1
        counter += 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    keyboard = [[InlineKeyboardButton("اضافه کردن کانال مبدا", callback_data='add_origin_channel'),
                 InlineKeyboardButton("اضافه کردن کانال مقصد", callback_data='add_destination_channel')],
                 [InlineKeyboardButton("دیدن کانال های مبدا", callback_data="see_origin_channels"),
                 InlineKeyboardButton("دیدن کانال های مقصد", callback_data="see_destination_channels")],
                 [InlineKeyboardButton("تغیر کانال مبدا", callback_data="edit_origin_channel"),
                 InlineKeyboardButton("تغیر کانال مقصد", callback_data="edit_destination_channels")],
                 [InlineKeyboardButton("پاک کردن کانال مبدا", callback_data='delete_origin'),
                 InlineKeyboardButton("پاک کردن کانال مقصد", callback_data='delete_destination')],
                 [InlineKeyboardButton("شروع کپی کردن", callback_data="start_sending_messages")]
                ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('چه کاری می خواید انجام بدید : ', reply_markup=reply_markup)

async def add_origin_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفا ایدی چنل رو برام بفرست" , reply_markup=reply_markup)
    return ID

async def get_id_origin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    channel_id = update.message.text
    await update.message.reply_text("لطفا فرمت پیام رو برام بفرست", reply_markup=reply_markup)
    origin_data.append(channel_id)
    return PATTERN

async def get_time_on_origin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    pattern = update.message.text
    await update.message.reply_text("لطفا تایم شروع کار ربات رو برام بفرست\nبه این فرمت باشه 19-14", reply_markup=reply_markup)
    origin_data.append(pattern)
    return  TIMEON

async def get_amount_change(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    time_on = update.message.text
    await update.message.reply_text("مقداری که نرخ تغیر کرده باشد تا مسیج کپی شود رو برام بفرست" ,reply_markup=reply_markup)
    origin_data.append(time_on)
    return AMOUNT_CHANGE

async def get_message_to_add_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    amount_change = update.message.text
    await update.message.reply_text("هر چند پیام نرخ رو تغیر بدم",reply_markup=reply_markup)
    origin_data.append(amount_change)
    return MESSAGE_TO_ADD_A_AMOUNT

async def amount_to_chenge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_to_add_amount = update.message.text
    await update.message.reply_text("چقدر اضافه کنم",reply_markup=reply_markup)
    origin_data.append(message_to_add_amount)
    return AMOUNT_TO_ADD

async def finish_add_orogin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    amout_to_add = update.message.text
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home"),
                 InlineKeyboardButton("تست چنل مبدا" ,callback_data="test_origin")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("چنل مبدا با موفقیت اضافه شد" , reply_markup=reply_markup)
    origin_data.append(amout_to_add)
    with open('origin.json' , 'r') as f1 :
        channel_origin = json.load(f1)
    channel_origin[origin_data[0]] = origin_data[1:]
    with open('origin.json' , 'w') as f :
        json.dump(channel_origin , f)
    origin_data.clear()
    return ConversationHandler.END

async def add_destination_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفا ایدی چنل رو برام بفرست",reply_markup=reply_markup)
    return ID_DESTINATION

async def get_id_destination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    channel_id = update.message.text
    await update.message.reply_text("لطفا فرمت پیام رو برام بفرست",reply_markup=reply_markup)
    destination_data.append(channel_id)
    return PATTERN_DESTINATION

async def finish_add_destination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    pattern = update.message.text
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home") ,
                 InlineKeyboardButton("تست چنل مقصد" ,callback_data="test_destination")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("چنل مقصد با موفقیت اضافه شد" , reply_markup=reply_markup)
    destination_data.append(pattern)
    with open('destination.json' , 'r') as f1 :
        channel_destination = json.load(f1)
    channel_destination[destination_data[0]] = destination_data[1:]
    with open('destination.json' , 'w') as f :
        json.dump(channel_destination , f)
    destination_data.clear()
    return ConversationHandler.END

async def test_origin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفا فرمتی که می خوای تست شه رو برام بفرست", reply_markup=reply_markup)
    return TEST_PATERN_ORIGIN

async def get_test_origin_pattern(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    pattern = update.message.text
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home"),
                 InlineKeyboardButton("تست چنل مبدا" ,callback_data="test_origin")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    with open("origin.json" , 'r') as f :
        origin = json.load(f)
    last_key = list (origin.keys())[-1]
    for i in origin :
        data = origin[i]
        regex_patern_origin_test = data[0]
        if "_any_" in data[0] :
            regex_patern_origin_test = data[0].replace("_any_" , "(\d+(?:,\d{3})*(?:\.\d+)?)")
        if "_target_" in data[0] :
            regex_patern_origin_test = data[0].replace("_target_" , "(\d+(?:,\d{3})*(?:\.\d+)?)")
        pattern_test = re.compile(regex_patern_origin_test)
        if re.match(pattern_test , pattern):
            await update.message.reply_text("فرمت مسیج درست است" , reply_markup=reply_markup)
            break
        elif (pattern not in data) and (i == last_key):
            await update.message.reply_text("فرمت غلط است" , reply_markup=reply_markup)
            break

    return ConversationHandler.END

async def test_destination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفا فرمتی که می خوای تست شه رو برام بفرست", reply_markup=reply_markup)
    return TEST_PATERN_DESTINATION

async def get_test_destination_pattern(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    pattern = update.message.text
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home") ,
                 InlineKeyboardButton("تست چنل مقصد" ,callback_data="test_destination")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    with open("destination.json" , 'r') as f :
        destination = json.load(f)
    last_key = list (destination.keys())[-1]
    for i in destination :
        data = destination[i]
        regex_patern_destination_test = data[0]
        if "_any_" in data[0] :
            regex_patern_destination_test = data[0].replace("_any_" , "(\d+(?:,\d{3})*(?:\.\d+)?)")
        if "_target_" in data[0] :
            regex_patern_destination_test = data[0].replace("_target_" , "(\d+(?:,\d{3})*(?:\.\d+)?)")
        pattern_test = re.compile(regex_patern_destination_test)
        if re.match(pattern_test , pattern):
            await update.message.reply_text("فرمت مسیج درست است" , reply_markup=reply_markup)
            break
        elif (pattern not in data) and (i == last_key):
            await update.message.reply_text("فرمت غلط است" , reply_markup=reply_markup)
            break
    return ConversationHandler.END

async def edit_origin_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("چه چیزی را می خواید تغیر بدید\n[ایدی - فرمت - ساعات کار ربات - نرخ تغیر کرده - تعداد پیام - نرخ اضافه شده]", reply_markup=reply_markup)
    return ID_EDIT_ORIGIN

async def get_edit_origin_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    topic = update.message.text
    if topic == "ایدی" :
        await update.message.reply_text("ایدی قدیمی چنل مبدا ای رو که می خواید تغیر بدید بفرستید", reply_markup=reply_markup)
    else :
        await update.message.reply_text(f"ایدی چنل مبدایی را که می خواهید {topic} اون رو تغیر بدید بفرستید", reply_markup=reply_markup)
    edit_origin_data.append(topic)
    return PATTERN_EDIT_ORIGIN

async def get_edit_origin_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    id = update.message.text
    if edit_origin_data[0] == "ایدی" :
        await update.message.reply_text("ایدی جدید رو بفریست", reply_markup=reply_markup)
    else :
        await update.message.reply_text(f"{edit_origin_data[0]} جدید رو برام بفرست", reply_markup=reply_markup)
    edit_origin_data.append(id)
    return TIMEON_EDIT_ORIGIN

async def finish_edit_origin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    topic_to_change = update.message.text
    with open("origin.json" , 'r') as of1 :
        origin = json.load(of1)
    if edit_origin_data[0] == "ایدی" :
        data = origin[edit_origin_data[1]]
        origin[topic_to_change] = data
        origin.pop(edit_origin_data[1])
        with open("origin.json" , 'w') as of2 :
            json.dump(origin , of2)
        await update.message.reply_text("ایدی چنل مبدا با موفقیت تغیر کرد." , reply_markup=reply_markup)
    elif edit_origin_data[0] == "فرمت" :
        data = origin[edit_origin_data[1]]
        data[0] = topic_to_change
        origin[edit_origin_data[1]] = data
        with open("origin.json" , 'w') as of2 :
            json.dump(origin , of2)
        await update.message.reply_text("فرمت کار ربات چنل مبدا با موفقیت تغیر کرد.", reply_markup=reply_markup)
    elif edit_origin_data[0] == "ساعت کار ربات" :
        data = origin[edit_origin_data[1]]
        data[1] = topic_to_change
        origin[edit_origin_data[1]] = data
        with open("origin.json" , 'w') as of2 :
            json.dump(origin , of2)
        await update.message.reply_text("ساعات کار ربات چنل مبدا با موفقیت تغیر کرد.", reply_markup=reply_markup)
    elif edit_origin_data[0] == "نرخ تغیر کرده" :
        data = origin[edit_origin_data[1]]
        data[2] = topic_to_change
        origin[edit_origin_data[1]] = data
        with open("origin.json" , 'w') as of2 :
            json.dump(origin , of2)
        await update.message.reply_text("نرخ تغیر کرده چنل مبدا با موفقیت تغیر کرد.", reply_markup=reply_markup)
    elif edit_origin_data[0] == "تعداد پیام" :
        data = origin[edit_origin_data[1]]
        data[3] = topic_to_change
        origin[edit_origin_data[1]] = data
        with open("origin.json" , 'w') as of2 :
            json.dump(origin , of2)
        await update.message.reply_text("تعداد پیام چنل مبدا با موفقیت تغیر کرد.", reply_markup=reply_markup)
    elif edit_origin_data[0] == "نرخ اضافه شده" :
        data = origin[edit_origin_data[1]]
        data[4] = topic_to_change
        origin[edit_origin_data[1]] = data
        with open("origin.json" , 'w') as of2 :
            json.dump(origin , of2)
        await update.message.reply_text("نرخ اضافه شده چنل مبدا با موفقیت تغیر کرد.", reply_markup=reply_markup)
    else : 
        await update.message.reply_text("در تغیر دادن چنل مبدا مشکلی پیش اومده برای تلاش دباره می توانید دستور /edit_origin_channels را وارد کنید", reply_markup=reply_markup)
    edit_origin_data.clear()
    return ConversationHandler.END

async def edit_destination_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("چه چیزی را می خواید تغیر بدید\n[ایدی - فرمت]", reply_markup=reply_markup)
    return ID_EDIT_DESTINATION

async def get_edit_destination_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    topic = update.message.text
    if topic == "ایدی" :
        await update.message.reply_text("ایدی قدیمی چنل مقصد ای رو که می خواید تغیر بدید بفرستید", reply_markup=reply_markup)
    else :
        await update.message.reply_text(f"ایدی چنل مقصدی را که می خواهید {topic} اون رو تغیر بدید بفرستید", reply_markup=reply_markup)
    edit_destination_data.append(topic)
    return PATTERN_EDIT_DESTINATION

async def get_edit_destination_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    id = update.message.text
    if edit_origin_data[0] == "ایدی" :
        await update.message.reply_text("ایدی جدید رو بفریست", reply_markup=reply_markup)
    else :
        await update.message.reply_text(f"{edit_origin_data[0]} جدید رو برام بفرست", reply_markup=reply_markup)
    edit_destination_data.append(id)
    return TIMEON_EDIT_DESTINATION

async def finish_edit_destination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    topic_to_change = update.message.text
    with open("destination.json" , 'r') as od1 :
        destination = json.load(od1)
    if edit_destination_data[0] == "ایدی" :
        data = destination[edit_destination_data[1]]
        destination[topic_to_change] = data
        destination.pop(edit_destination_data[1])
        with open("destination.json" , 'w') as od2 :
            json.dump(destination , od2)
        await update.message.reply_text("ایدی چنل مقصد با موفقیت تغیر کرد." , reply_markup=reply_markup)
    elif edit_destination_data[0] == "فرمت" :
        data = destination[edit_destination_data[1]]
        data[0] = topic_to_change
        destination[edit_destination_data[1]] = data
        with open("destination.json" , 'w') as od2 :
            json.dump(destination , od2)
        await update.message.reply_text("فرمت چنل مقصد با موفقیت تغیر کرد.", reply_markup=reply_markup)
    else : 
        await update.message.reply_text("در تغیر دادن چنل مقصد مشکلی پیش اومده برای تلاش دباره می توانید دستور /edit_destination_channels را وارد کنید", reply_markup=reply_markup)
    edit_destination_data.clear()
    return ConversationHandler.END

async def delete_origin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("ایدی چنل مبدایی رو که می خواید پاک کنی رو بفرست.", reply_markup=reply_markup)
    return ID_DEL_ORIGIN

async def get_delet_origin_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    id = update.message.text
    with open("origin.json" , 'r') as of1 :
        origin = json.load(of1)
    origin.pop(id)
    with open("origin.json" , 'w') as of2 :
        json.dump(origin , of2)
    await update.message.reply_text("چنل مبدا با موفقیت پاک شد." , reply_markup=reply_markup)
    return ConversationHandler.END

async def delete_destination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("ایدی چنل مقصدی رو که می خواید پاک کنی رو بفرست.", reply_markup=reply_markup)
    return ID_DEL_DESTINATION

async def get_delete_destination_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    id = update.message.text
    with open("destination.json" , 'r') as df1 :
        destination = json.load(df1)
    destination.pop(id)
    with open("destination.json" , 'w') as df2 :
        json.dump(destination , df2)
    await update.message.reply_text("چنل مقصد با موفقیت پاک شد." , reply_markup=reply_markup)
    return ConversationHandler.END

async def start_send_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("ایدی چنل مبدا رو برام بفرست", reply_markup=reply_markup)
    return ID_START

async def send_message_get_origin_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("کنسل کردن" , callback_data="cancel_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    origin_id = update.message.text
    send_message_data.append(origin_id)
    await update.message.reply_text("ایدی چنل مقضد رو برام بفرست", reply_markup=reply_markup)
    return PATTERN_START

async def send_message_get_destination_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home") ,
                 InlineKeyboardButton("کنسل کردن فرستادن پیام" , callback_data="cancel_send_message")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    destination_id = update.message.text
    send_message_data.append(destination_id)
    loop = asyncio.get_event_loop()
    task = loop.create_task(send_message(send_message_data[0] , send_message_data[1]))
    await update.message.reply_text("شروع به فرستادن پیام از چنل مبدا به مقصد" , reply_markup=reply_markup)
    send_message_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("فرایند کنسل شد", reply_markup=reply_markup)
    send_message_data.clear()
    edit_origin_data.clear()
    edit_destination_data.clear()
    origin_data.clear()
    destination_data.clear()
    return ConversationHandler.END



async def main_menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data="back_home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    start_keyboard = [[InlineKeyboardButton("اضافه کردن کانال مبدا", callback_data='add_origin_channel'),
                 InlineKeyboardButton("اضافه کردن کانال مقصد", callback_data='add_destination_channel')],
                 [InlineKeyboardButton("دیدن کانال های مبدا", callback_data="see_origin_channels"),
                 InlineKeyboardButton("دیدن کانال های مقصد", callback_data="see_destination_channels")],
                 [InlineKeyboardButton("تغیر کانال مبدا", callback_data="edit_origin_channel"),
                 InlineKeyboardButton("تغیر کانال مقصد", callback_data="edit_destination_channels")],
                 [InlineKeyboardButton("پاک کردن کانال مبدا", callback_data='delete_origin'),
                 InlineKeyboardButton("پاک کردن کانال مقصد", callback_data='delete_destination')],
                 [InlineKeyboardButton("شروع کپی کردن", callback_data="start_sending_messages")]
                ]
    
    start_reply_markup = InlineKeyboardMarkup(start_keyboard)
    if data == 'add_origin_channel':
        await query.edit_message_text("برای شروع دستور /add_origin_channel وارد کنید")
    elif data == 'add_destination_channel':
        await query.edit_message_text("برای شروع دستور /add_destination_channel وارد کنید")
    elif data == "back_home" :
        await query.message.reply_text('چه کاری می خواید انجام بدید : ', reply_markup=start_reply_markup)
    elif data == "test_destination" :
        await query.edit_message_text("برای تست چنل مقصد دستور /test_destination را وارد کنید")
    elif data == "test_origin" :
        await query.edit_message_text("برای تست چنل مبدا دستور /test_origin را وارد کنید")
    elif data == "see_origin_channels" :
        if os.path.getsize("origin.json") <= 3 :
            await query.edit_message_text("شما هیچ کانال مبدایی ثپت نکردید" , reply_markup=reply_markup)
        else :
            with open("origin.json" , 'r') as originf :
                origin = json.load(originf)
            for i in origin :
                data = origin[i]
                await query.message.reply_text(f"ایدی: {i}\nفرمت ست شده: {data[0]}\nساعت کار ربات: {data[1]}\nمقداری که نرخ باید تغیر کرده باشد: {data[2]}\nتعداد پیامی که رندوم نرخ اضافه می شود: {data[3]}\nمقدار نرخی که اضافه می شود: {data[4]}" , reply_markup=reply_markup)
    elif data == "see_destination_channels" :
        if os.path.getsize("destination.json") <= 3 :
            await query.edit_message_text("شما هیچ کانال مقصدی ثپت نکردید" , reply_markup=reply_markup)
        else :
            with open("destination.json" , 'r') as destinationf :
                destination = json.load(destinationf)
            for i in destination :
                data = destination[i]
                await query.message.reply_text(f"ایدی: {i}\nفرمت ست شده: {data[0]}" , reply_markup=reply_markup)
    elif data == "edit_origin_channel" :
        await query.edit_message_text("برای تغیر چنل مبدا دستور /edit_origin_channels را وارد کنید")
    elif data == "edit_destination_channels" :
        await query.edit_message_text("برای تغیر چنل مقصد دستور /edit_destination_channels را وارد کنید")
    elif data == "delete_origin" :
        await query.edit_message_text("برای پاک کردن چنل میدا دستور /delete_origin را وارد کنید")
    elif data == "delete_destination" :
        await query.edit_message_text("برای پاک کردن چنل مقصد دصتور /delete_destination را وارد کنید")
    elif data == "start_sending_messages" :
        if os.path.getsize("origin.json") <= 3 or os.path.getsize("destination.json") <= 3 :
            await query.edit_message_text("شما هیج چنل مبدا و مقصدی ندارید لطفا ابتدا چنل مبدا و مقضد رو اضافه کنید." , reply_markup=reply_markup)
        else :
            await query.edit_message_text("برای شروع فرستادن پیام دستور /send_message را وارد کنید")
    elif data == "cancel_task" :
        await query.message.reply_text('برای کنسل کردن فرایند مجود دستور /cancel را وارد کنید')
    elif data == "cancel_send_message" :
        Send_message = False
        await query.message.reply_text("فرستادن پیام از کنسل شد", reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token("YOUR BOT TOKEN").build()

    start_handler = CommandHandler('start' , start)
    origin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_origin_channel", add_origin_channel)],
        states={
            ID: [MessageHandler(filters.Regex("^(?!/).*$") , get_id_origin)] ,
            PATTERN: [MessageHandler(filters.Regex("^(?!/).*$") , get_time_on_origin)] ,
            TIMEON: [MessageHandler(filters.Regex("^(?!/).*$") , get_amount_change)] ,
            AMOUNT_CHANGE: [MessageHandler(filters.Regex("^(?!/).*$") , get_message_to_add_amount)] ,
            MESSAGE_TO_ADD_A_AMOUNT: [MessageHandler(filters.Regex("^(?!/).*$") , amount_to_chenge)],
            AMOUNT_TO_ADD: [MessageHandler(filters.Regex("^(?!/).*$") , finish_add_orogin)]
        },
        fallbacks=[CommandHandler('cancel' , cancel)] , allow_reentry = True
    )
    destination_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_destination_channel" , add_destination_channel)],
        states={
            ID_DESTINATION: [MessageHandler(filters.Regex("^(?!/).*$") , get_id_destination)] ,
            PATTERN_DESTINATION: [MessageHandler(filters.Regex("^(?!/).*$") , finish_add_destination)]
        },
        fallbacks=[CommandHandler('cancel' , cancel)], allow_reentry = True
    )
    tes_origin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("test_origin" , test_origin)],
        states={
            TEST_PATERN_ORIGIN: [MessageHandler(filters.Regex("^(?!/).*$") , get_test_origin_pattern)]
        },
        fallbacks=[CommandHandler('cancel' , cancel)], allow_reentry = True

    )
    test_destination_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("test_destination" , test_destination)],
        states={
            TEST_PATERN_DESTINATION: [MessageHandler(filters.Regex("^(?!/).*$") , get_test_destination_pattern)]
        },
        fallbacks=[CommandHandler('cancel' , cancel)] , allow_reentry = True
    )
    edit_origin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("edit_origin_channels" , edit_origin_channels)] ,
        states={
            ID_EDIT_ORIGIN: [MessageHandler(filters.Regex("^(?!/).*$") , get_edit_origin_topic)],
            PATTERN_EDIT_ORIGIN: [MessageHandler(filters.Regex("^(?!/).*$") , get_edit_origin_id)] ,
            TIMEON_EDIT_ORIGIN : [MessageHandler(filters.Regex("^(?!/).*$") , finish_edit_origin)]
        },
        fallbacks=[CommandHandler("cancel" , cancel)], allow_reentry = True
    )
    edit_destination_con_handler = ConversationHandler(
        entry_points=[
            CommandHandler('edit_destination_channels' , edit_destination_channels)
        ],
        states={
            ID_EDIT_DESTINATION: [MessageHandler(filters.Regex("^(?!/).*$") ,get_edit_destination_topic)] ,
            PATTERN_EDIT_DESTINATION : [MessageHandler(filters.Regex("^(?!/).*$") ,get_edit_destination_id )] ,
            TIMEON_EDIT_DESTINATION: [MessageHandler(filters.Regex("^(?!/).*$") , finish_edit_destination)]
        },
        fallbacks=[CommandHandler('cancel' , cancel)], allow_reentry = True
    )
    delete_origin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("delete_origin" , delete_origin)] ,
        states={
            ID_DEL_ORIGIN: [MessageHandler(filters.Regex("^(?!/).*$") , get_delet_origin_id)]
        },
        fallbacks=[CommandHandler('cancel' , cancel)], allow_reentry = True
    )
    delete_destination_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("delete_destination" , delete_destination)] ,
        states={
            ID_DEL_DESTINATION: [MessageHandler(filters.Regex("^(?!/).*$") , get_delete_destination_id)]
        },
        fallbacks=[CommandHandler('cancel' , cancel)], allow_reentry = True
    )
    send_message_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("send_message" , start_send_message)] ,
        states={
            ID_START: [MessageHandler(filters.Regex("^(?!/).*$") , send_message_get_origin_id)],
            PATTERN_START: [MessageHandler(filters.Regex("^(?!/).*$") ,send_message_get_destination_id )]
        },
        fallbacks=[CommandHandler('cancel' , cancel)], allow_reentry = True
    )

    application.add_handler(start_handler)
    application.add_handler(origin_conv_handler)
    application.add_handler(destination_conv_handler)
    application.add_handler(tes_origin_conv_handler)
    application.add_handler(test_destination_conv_handler)
    application.add_handler(edit_origin_conv_handler)
    application.add_handler(edit_destination_con_handler)
    application.add_handler(delete_origin_conv_handler)
    application.add_handler(delete_destination_conv_handler)
    application.add_handler(send_message_conv_handler)
    application.add_handler(CallbackQueryHandler(main_menu_button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()