import datetime
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetDialogsRequest

# Create the client and connect
you_username = 'Arshiarasekhi'
api_id = '15149922'
api_hash = '645874defad2a0a502e67f3301b6db52'
your_phone = '+989034151503'
client = TelegramClient(you_username, api_id, api_hash)
client.start()
print("Client Created")
# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(your_phone)
    try:
        client.sign_in(your_phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))
def get_entity_data(entity_id, limit):
    entity = client.get_entity(entity_id)
    today = datetime.datetime.today()
    # y = today - datetime.timedelta(days=1)
    posts = client(GetHistoryRequest(
                   peer=entity,
                   limit=limit,
                   offset_date=None,
                   offset_id=0,
                   max_id=0,
                   min_id=0,
                   add_offset=0,
                   hash=0))

    messages = []
    for message in posts.messages:
        messages.append(message.message)
    return messages
result = client(GetDialogsRequest(
             offset_date=None,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=100,
             hash=0)) 
entities = ["RegaPlus" , "RealMadridNewsir"]
for entity in entities:
    messages = get_entity_data(entity, 15)
    print(messages)
    print('#######')