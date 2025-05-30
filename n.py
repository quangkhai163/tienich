import telebot
import requests

# ====== Cấu hình ======
bot = telebot.TeleBot("7752584378:AAGt2Ykue5Pj3XwgEoP62g0w9b6yLbr5pWo")  # 🔁 Thay bằng token thật
ALLOWED_GROUP_ID = -1002538985524        # ✅ ID nhóm chính
GROUP_LINK = "https://t.me/qkcheatmodvip"
API_BASE = "https://api-mobi.soundcloud.com/search"
CLIENT_ID = "KKzJxmw11tYpCs6T24P4uUYhqmjalG6M"

# ====== Tin nhắn nếu nhóm không hợp lệ ======
def reject_message(message):
    bot.reply_to(
        message,
        f"❌ Bot này chỉ hoạt động trong nhóm chính: [@qkcheatmodvip]({GROUP_LINK})",
        parse_mode='Markdown'
    )

# ====== /start và /help ======
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    if message.chat.type in ['group', 'supergroup'] and message.chat.id != ALLOWED_GROUP_ID:
        reject_message(message)
        return

    bot.reply_to(message, "Gõ /soun <từ khóa> để tìm nhạc trên SoundCloud!")

# ====== /soun <từ khóa> ======
@bot.message_handler(commands=['soun'])
def search(message):
    if message.chat.type in ['group', 'supergroup'] and message.chat.id != ALLOWED_GROUP_ID:
        reject_message(message)
        return

    query = message.text.replace('/soun', '').strip()
    if not query:
        bot.reply_to(message, "Vui lòng nhập từ khóa tìm kiếm sau lệnh /soun.")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        url = f"{API_BASE}?q={query}&client_id={CLIENT_ID}&stage="
        res = requests.get(url).json()

        if not res or not res.get("data"):
            bot.reply_to(message, "Không tìm thấy kết quả nào.")
            return

        for item in res["data"][:5]:  # Giới hạn 5 kết quả đầu
            title = item.get("title", "Không rõ tiêu đề")
            artist = item.get("user", {}).get("name", "Không rõ nghệ sĩ")
            link = item.get("permalink_url", "#")
            thumb = item.get("artwork_url")

            text = (
                f"🎵 <b>{title}</b>\n"
                f"👤 {artist}\n"
                f"🔗 <a href='{link}'>Nghe bài hát</a>"
            )

            if thumb:
                bot.send_photo(
                    message.chat.id,
                    photo=thumb,
                    caption=text,
                    parse_mode='HTML'
                )
            else:
                bot.send_message(message.chat.id, text, parse_mode='HTML')

    except Exception as e:
        print("Lỗi:", e)
        bot.reply_to(message, "Đã xảy ra lỗi khi tìm kiếm.")

# ====== Khởi động bot ======
bot.polling()