from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import spam3_1 as spam  # Đảm bảo file spam3_1.py nằm cùng thư mục

import json
import os

# ====== Cấu hình ======
APPROVED_FILE = "approved_groups.json"
OWNER_ID = 5976243149  # 🔁 Thay bằng Telegram user ID của bạn

# ====== Load/Lưu nhóm đã duyệt ======
def load_approved_groups():
    if os.path.exists(APPROVED_FILE):
        with open(APPROVED_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_approved_groups(groups):
    with open(APPROVED_FILE, "w") as f:
        json.dump(list(groups), f)

approved_groups = load_approved_groups()

# ====== Kiểm tra nhóm đã duyệt chưa ======
async def is_group_approved(update: Update):
    chat = update.effective_chat
    if chat.type in ['group', 'supergroup']:
        return chat.id in approved_groups
    return True  # Luôn cho phép trong private

# ====== /addgr để duyệt nhóm ======
async def addgr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat = update.effective_chat

    if user_id != OWNER_ID:
        await update.message.reply_text("❌ Bạn không có quyền duyệt nhóm này.")
        return

    approved_groups.add(chat.id)
    save_approved_groups(approved_groups)
    await update.message.reply_text(
        f"✅ Đã duyệt nhóm `{chat.title}` (`{chat.id}`)",
        parse_mode="Markdown"
    )

# ====== Spam OTP ======
async def spam_otp(update: Update, phone: str):
    await update.message.reply_text(f"📲 Đang spam OTP tới số: {phone}")
    try:
        spam.XWXWWWXWWWXXXXXXWW(phone)
        spam.lIlIlllllllIllIlI(phone)
        spam.S2S22SS22SSSSSSSSS2SS(phone)
        spam.OODOOooDoOOoOoOooDD(phone)
        spam.JIILIILJJILJJILJIILLJILI(phone)
        spam.NMMNNNMMNMMMMNNNM(phone)
        spam.XWWWWXWXWXXXXXXWXXW(phone)
        spam.MNMNNNMNMNMNNNMMNNMN(phone)
        spam.OO00OoO0o0Oo0ooOOo0OOO0o(phone)
        spam.Oo0oO0ooooo0O000O0ooO(phone)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi: {e}")
        return
    await update.message.reply_text("✅ Đã hoàn thành spam OTP.")

# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gửi số điện thoại hoặc dùng lệnh /spam <sdt> để spam OTP.")

# ====== /spam <sdt> ======
async def spam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ['group', 'supergroup']:
        if not await is_group_approved(update):
            await update.message.reply_text(
                "❌ Bot chưa được duyệt. Liên hệ admin [@qkdzvcl206](https://t.me/qkdzvcl206)",
                parse_mode="Markdown"
            )
            return

    if len(context.args) != 1:
        await update.message.reply_text("❌ Sai cú pháp. Dùng: /spam <sdt>")
        return

    phone = context.args[0]
    await spam_otp(update, phone)

# ====== Xử lý tin nhắn văn bản (số điện thoại) ======
async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ['group', 'supergroup']:
        if not await is_group_approved(update):
            await update.message.reply_text(
                "❌ Bot chưa được duyệt. Liên hệ admin [@qkdzvcl206](https://t.me/qkdzvcl206)",
                parse_mode="Markdown"
            )
            return

    phone = update.message.text.strip()
    await spam_otp(update, phone)

# ====== Khởi tạo bot ======
app = ApplicationBuilder().token("7600722167:AAHwi0iGZ97R9rwDKsoyskW1sp8dbUeFY1c").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("spam", spam_command))
app.add_handler(CommandHandler("addgr", addgr))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone))

app.run_polling()