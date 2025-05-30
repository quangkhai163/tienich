import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 👉 NHỚ THAY TOKEN BẰNG CỦA BẠN
bot_token = "7238295879:AAHuJtmPWWUeiLiCLT8Mqx6-vujQy983Yn0"

API_URL = "https://scromnyi.vercel.app/region/ban-info?uid="

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Gửi UID Free Fire hoặc dùng /check <uid> để kiểm tra ban status.")

# /check <uid>
async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Bạn cần nhập UID. Ví dụ: /check 12345678")
        return

    uid = context.args[0].strip()
    if not uid.isdigit():
        await update.message.reply_text("❌ UID không hợp lệ. Vui lòng nhập số UID.")
        return

    await check_ban(update, uid)

# Gửi UID trực tiếp
async def check_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    if uid.isdigit():
        await check_ban(update, uid)
    else:
        await update.message.reply_text("❌ UID không hợp lệ. Vui lòng nhập số UID.")

# Hàm gọi API check ban
async def check_ban(update: Update, uid: str):
    try:
        response = requests.get(f"{API_URL}{uid}")
        data = response.json()

        msg = f"""✅ Kết quả kiểm tra UID {uid}:
👤 Nickname: {data.get("nickname")}
📍 Khu vực: {data.get("region")}
🚫 Trạng thái ban: {data.get("ban_status")}
⏳ Thời gian ban: {data.get("ban_period") or "Không có"}
🔗 API bởi: bố m đây @qkdzvcl206
"""
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi khi kiểm tra UID: {e}")

# Chạy bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_uid))

    print("🚀 Bot đang chạy...")
    app.run_polling()