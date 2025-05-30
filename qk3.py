import os
import asyncio
import random
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_CONFIG = {
    'TOKEN': '8069437407:AAFqVxUgLemYg7_mr-OhSnmY89oThGCOc5k',
    'USER_ID': 5976243149
}

# --- Các lệnh bot gái ---
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🔥 MENU TIỆN ÍCH 🔥

👩‍🦰
- /videogai : Random video gái 
- /anhgai : Random ảnh gái xinh
- /ban (reply) : Ban thành viên
- /unban (reply) : Gỡ ban thành viên
- /mute (reply) : Mute thành viên
- /unmute (reply) : Gỡ mute thành viên
- /kickrandom : Kick random thành viên
- /spam [sdt] : Spam SMS cực mạnh
- /tiktok [link] : Tải video TikTok không logo
- /addfr [UID] : Gửi kết bạn UID Free Fire
- /tkinfo [username] : Xem thông tin tài khoản TikTok
- /weather [tên thành phố] : Xem thời tiết hiện tại

💬 ĐỪNG QUÊN BOT NÀY LÀ CỦA ADM @qkdzvcl206
""")

async def videogai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return
    try:
        res = requests.get("https://api.ffcommunity.site/randomvideo.php", timeout=10).json()
        video_url = res['url']
        captions = [
            "Vitamin gái đẹp mỗi ngày!",
            "Gái đẹp tiếp thêm năng lượng!",
            "Cùng ngắm gái xinh nào bro!",
            "Gái đẹp giúp giảm stress cực mạnh!"
        ]
        caption = random.choice(captions)
        await update.message.reply_video(video=video_url, caption=caption)
    except Exception as e:
        print(f'Lỗi: {e}')
        await update.message.reply_text("❌ Không lấy được video gái!")

async def anhgai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return
    try:
        res = requests.get("https://api-kiendev.up.railway.app/random_girl_image", timeout=10).json()
        img_url = res['data']['url']
        await update.message.reply_photo(photo=img_url, caption="📸 Gái xinh đây bro!")
    except Exception as e:
        print(f'Lỗi: {e}')
        await update.message.reply_text("❌ Không lấy được ảnh gái!")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("✅ Đã ban thành viên!")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await update.effective_chat.unban_member(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("✅ Đã gỡ ban thành viên!")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        permissions = ChatPermissions(can_send_messages=False)
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, permissions)
        await update.message.reply_text("✅ Đã mute thành viên!")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        permissions = ChatPermissions(can_send_messages=True)
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, permissions)
        await update.message.reply_text("✅ Đã gỡ mute thành viên!")

async def kickrandom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get_members() không khả dụng cho bot Telegram
    members = []  # cần thay bằng cách lấy danh sách thành viên thủ công nếu có
    user = random.choice(members)
    await update.effective_chat.kick_member(user.user.id)
    await update.message.reply_text(f"✅ Đã kick random: {user.user.first_name}")

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return
    if len(context.args) != 1:
        await update.message.reply_text("📥 Dùng: /spam [số điện thoại]")
        return
    phone = context.args[0]
    try:
        requests.post("https://vietteltelecom.vn/api/Account/SendOTP", json={"phoneNumber": phone}, timeout=10)
        requests.post("https://fptplay.net/api/user/sendOTP", json={"phone": phone}, timeout=10)
        await update.message.reply_text(f"✅ Đã gửi spam tới {phone}!")
    except Exception as e:
        print(f'Lỗi: {e}')
        await update.message.reply_text("❌ Lỗi spam!")

async def tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("📥 Dùng: /tiktok [link]")
        return
    link = context.args[0]
    try:
        res = requests.get(f"https://tikwm.com/api/?url={link}", timeout=10).json()
        video_url = res['data']['play']
        await update.message.reply_video(video=video_url, caption="✅ Tải thành công TikTok!")
    except Exception as e:
        print(f'Lỗi: {e}')
        await update.message.reply_text("❌ Lỗi tải TikTok!")

async def addfr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return
    if len(context.args) != 1:
        await update.message.reply_text("📥 Dùng: /addfr [UID]")
        return
    uid = context.args[0]
    await update.message.reply_text(f"✅ Đã gửi kết bạn tới UID: {uid}")

# --- Hàm gửi gái khi có thành viên mới ---
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        api_video_list = [
            "https://api.ffcommunity.site/randomvideo.php",
            "https://api.leanhtruong.net/api/v2/video/gai.php",
            "https://api-ttk3.hoanghao.click/api/video/gai.php"
        ]
        api_image = "https://api.leanhtruong.net/api/v2/image/gai.php"

        captions = [
            "Chào mừng bro mới bằng gái đẹp nè!",
            "Gia nhập group nhận ngay gái xinh!",
            "Món quà chào mừng: vitamin gái cực mạnh!",
            "Mở màn bằng gái đẹp, vào group cực phê!",
            "Anh em welcome thành viên mới với gái đẹp!",
            "Gái đẹp - Thành viên mới, combo hoàn hảo!",
            "Gái xinh chào đón bạn bro!"
        ]

        video_url = None

        # Thử lần lượt các API video
        for api_url in random.sample(api_video_list, len(api_video_list)):
            try:
                res = requests.get(api_url, timeout=10).json()
                if 'url' in res:
                    video_url = res['url']
                elif 'data' in res and 'url' in res['data']:
                    video_url = res['data']['url']
                if video_url:
                    break
            except Exception as e:
                print(f"⚠️ API lỗi {api_url}: {e}")

        # Nếu không lấy được video -> lấy ảnh gái
        if not video_url:
            try:
                res_img = requests.get(api_image, timeout=10).json()
                if 'data' in res_img and 'url' in res_img['data']:
                    image_url = res_img['data']['url']
                    caption = random.choice(captions)
                    for member in update.message.new_chat_members:
                        await update.message.reply_photo(photo=image_url, caption=f"{caption}\n(Ảnh gái xinh thay thế)")
                    return
            except Exception as e:
                print(f"❌ Lỗi lấy ảnh gái: {e}")
            # Nếu cả ảnh cũng fail
            await update.message.reply_text("❌ Không lấy được gái đẹp để chào mừng!")
            return

        # Nếu lấy được video
        caption = random.choice(captions)
        for member in update.message.new_chat_members:
            await update.message.reply_video(video=video_url, caption=caption)

    except Exception as e:
        print(f"❌ Lỗi tổng quát welcome_new_member: {e}")

# --- Alive ping ---
async def ping_alive(application: Application):
    while True:
        try:
            await application.bot.send_message(chat_id=BOT_CONFIG['USER_ID'], text="#bot_alive_qk")
        except Exception as e:
            print(f"⚠️ Lỗi alive: {e}")
        await asyncio.sleep(30)

# --- MAIN ---
async def tkinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return
    if len(context.args) < 1:
        await update.message.reply_text("please send username With command like this /inftiktok ss_dd_f")
        return
    username = context.args[0]
    url = f"http://145.223.80.56:5009/info_tiktok?username={username}"
    res = requests.get(url, timeout=10)
    data = res.json()
    msg = f"""
<b>📊 TikTok Account Info 📊</b>

<b>✨ Statistics:</b>
<code>👍 Digg Count:</code> <b>{data.get('digg_count', 'N/A')}</b>
<code>👥 Followers:</code> <b>{data.get('followers', 'N/A')}</b>
<code>👤 Following:</code> <b>{data.get('following', 'N/A')}</b>
<code>❤️ Hearts:</code> <b>{data.get('hearts', 'N/A')}</b>
<code>🎬 Videos:</code> <b>{data.get('videos', 'N/A')}</b>

<b>🔒 Account Details:</b>
<code>📛 Name:</code> <b>{data.get('name', 'N/A')}</b>
<code>👤 Username:</code> <b>@{data.get('username', 'N/A')}</b>
<code>🆔 User ID:</code> <b>{data.get('user_id', 'N/A')}</b>
<code>🔒 Private Account:</code> <b>{'Yes 🔐' if data.get('is_private') else 'No 🔓'}</b>
<code>⭐ Open Favorite:</code> <b>{'Yes ✅' if data.get('open_favorite') else 'No ❌'}</b>

<b>📝 Bio:</b>
<code>{data.get('signature', 'No bio available')}</code>

<b>🔐 Technical Info:</b>
<code>🔒 Sec UID:</code> <code>{data.get('sec_uid', 'N/A')}</code>
<code>🖼️ Profile Picture:</code> <a href="{data.get('profile_picture', '#')}">View Image</a>
"""
    await update.message.reply_text(msg, parse_mode="HTML")


# --- Weather Handler ---


# --- TikTok Info Handler ---
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE:
        return
    args = context.args
    if not args:
        await update.message.reply_text('Nhập đúng định dạng:\n/weather Hà Nội')
        return
    city = ' '.join(args)
    API_KEY = '1dcdf9b01ee855ab4b7760d43a10f854'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(base_url, timeout=10)
    weather_data = response.json()

    if weather_data['cod'] == 200:
        weather_info = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['main']
        temp_info = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        city = weather_data['name']
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        country = weather_data['sys']['country']
        cloudiness = weather_data['clouds']['all']
        humidity_info = weather_data['main']['humidity']
        wind_speed_info = weather_data['wind']['speed']
        gg = f"(https://www.google.com/maps/place/{lat},{lon})"
        msg = f"""╭─────⭓Thời Tiết
│🌍 City: {city}
│🔗 Link map: [{city}] {gg}
│☁️ Thời tiết: {weather_info}
│🌡 Nhiệt độ: {temp_info}°C
│🌡️ Nhiệt độ cảm nhận: {feels_like}°C
│🌡️ Nhiệt độ tối đa: {temp_max}°C
│🌡️ Nhiệt độ tối thiểu: {temp_min}°C
│📡 Tình trạng thời tiết: {icon}
│🫧 Độ ẩm: {humidity_info}%
│☁️ Mức độ mây: {cloudiness}%
│🌬️ Tốc độ gió: {wind_speed_info} m/s
│🌐 Quốc gia: {country}
╰─────────────⭓"""
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text('Không tìm thấy thông tin thời tiết cho địa điểm này.')



# --- Bot ON/OFF Commands ---
BOT_ACTIVE = True

async def bot_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    BOT_ACTIVE = True
    await update.message.reply_text("✅ Bot đã được bật.")

async def bot_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    BOT_ACTIVE = False
    await update.message.reply_text("⛔ Bot đã tắt tạm thời.")

async def main():
    app = Application.builder().token(BOT_CONFIG['TOKEN']).build()

    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("videogai", videogai))
    app.add_handler(CommandHandler("anhgai", anhgai))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("kickrandom", kickrandom))
    app.add_handler(CommandHandler("spam", spam))
    app.add_handler(CommandHandler("tiktok", tiktok))
    app.add_handler(CommandHandler("addfr", addfr))
    app.add_handler(CommandHandler("tkinfo", tkinfo))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("boton", bot_on))
    app.add_handler(CommandHandler("botoff", bot_off))

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    print("🤖 BOT chạy rồi...")
    await app.initialize()
    await app.start()
    await app.bot.send_message(chat_id=BOT_CONFIG['USER_ID'], text="✅ BOT đã hoạt động!")

    asyncio.create_task(ping_alive(app))

    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())


