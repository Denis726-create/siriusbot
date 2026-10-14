import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os
import time

TOKEN = os.environ.get("VK_TOKEN")
GROUP_ID = int(os.environ.get("GROUP_ID"))

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk, GROUP_ID)

def get_chat_members(chat_id):
    try:
        response = vk.method("messages.getConversationMembers", {
            "peer_id": 2000000000 + chat_id
        })
        profiles = response.get("profiles", [])
        members = []
        for p in profiles:
            username = p.get("domain", "")
            first = p.get("first_name", "")
            last = p.get("last_name", "")
            if username:
                members.append(f"@{username} {first} {last}")
            else:
                members.append(f"{first} {last}")
        return members
    except Exception as e:
        return [f"Ошибка: {e}"]

print("✅ Бот SiriusBot запущен!")
print("👂 Слушаю беседы...")

last_heartbeat = time.time()

for event in longpoll.listen():
    if time.time() - last_heartbeat > 30:
        print("💓 Бот жив...")
        last_heartbeat = time.time()
    
    if event.type == VkBotEventType.MESSAGE_NEW:
        msg = event.object.message
        text = msg.get("text", "").strip().lower()
        peer_id = msg.get("peer_id", 0)
        
        if peer_id > 2000000000 and text == "/ники":
            chat_id = peer_id - 2000000000
            members = get_chat_members(chat_id)
            
            answer = "📋 Ники участников чата:\n\n"
            for i, name in enumerate(members, 1):
                answer += f"{i}. {name}\n"
            
            vk.method("messages.send", {
                "peer_id": peer_id,
                "message": answer,
                "random_id": 0
            })
            print(f"📤 Отправлен список ников в беседу {chat_id}")
