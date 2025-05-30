import requests
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Hàm lấy dữ liệu JSON từ API
def get_raw_ff_info(uid):
    url = f"https://dichvukey.site/ff.php?uid={uid}"
    try:
        res = requests.get(url)
        data = res.json()
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Lỗi khi lấy dữ liệu: {e}"

# Gửi tin nhắn dạng chia nhỏ nếu quá dài
async def send_long_json(chat_id, bot, text):
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for chunk in chunks:
        await bot.send_message(chat_id=chat_id, text=f"<pre>{chunk}</pre>", parse_mode="HTML")

# Hàm xử lý lệnh /ffraw
async def ffraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗ Dùng đúng cú pháp: /ffraw <uid>")
        return

    uid = context.args[0]
    json_text = get_raw_ff_info(uid)

    await send_long_json(update.effective_chat.id, context.bot, json_text)

# Khởi động bot
app = ApplicationBuilder().token("7999858853:AAETciR2r9y7o0NMMdEz26OwX6oL8l8g02c").build()
app.add_handler(CommandHandler("ffraw", ffraw_command))

print("Bot đang chạy...")
app.run_polling()