import config
from pyrogram import Client, filters

# Ambil nilai konfigurasi dari file config.py
api_id = config.api_id
api_hash = config.api_hash
bot_token = config.bot_token
owner_id = config.owner_id

# Inisialisasi bot dengan konfigurasi dari config.py
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Dictionary untuk menyimpan ID pengguna yang mengirim pesan
user_message_dict = {}

# Fungsi untuk menerima pesan dari pengguna
@app.on_message(filters.private & ~filters.user(owner_id))
async def receive_message(client, message):
    user_id = message.from_user.id
    text = message.text
    
    # Simpan pesan yang diterima ke dalam dictionary dengan key = message.id
    user_message_dict[message.id] = user_id
    
    # Kirim pesan ke owner dan simpan ID pesan yang diterima owner
    await client.send_message(
        owner_id, 
        f"Pesan dari {message.from_user.first_name} (ID: {user_id}):\n{text}",
        reply_to_message_id=message.id
    )

    # Beri tahu pengguna bahwa pesan telah diteruskan ke owner
    await message.reply_text("Pesan kamu telah diteruskan ke owner. Mohon tunggu balasannya.")

# Fungsi untuk owner membalas pesan pengguna melalui reply
@app.on_message(filters.private & filters.user(owner_id) & filters.reply)
async def reply_to_user(client, message):
    # Cek apakah pesan yang dibalas ada di dalam dictionary
    if message.reply_to_message and message.reply_to_message.id in user_message_dict:
        user_id = user_message_dict[message.reply_to_message.id]
        
        # Kirim pesan balasan ke pengguna
        await client.send_message(user_id, message.text)
        
        # Konfirmasi ke owner bahwa pesan sudah terkirim
        await message.reply_text(f"Pesan terkirim ke user dengan ID {user_id}.")
    else:
        await message.reply_text("Tidak dapat menemukan pesan asli untuk dibalas.")

app.run()
