import psutil
import platform
import datetime
import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7441292874:AAEZBck1OTom82vHwx_0dCweW9mDRqcUUnY"
ADMIN_ID = 5976243149
alerts_enabled = False

def as_json(data):
    return f"```json\n{json.dumps(data, indent=2)}\n```"

async def is_admin(update: Update):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(as_json({
            "error": "m nghĩ m đủ tuổi để sờ vào bot của t à😏."
        }), parse_mode="Markdown")
        return False
    return True

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    data = {
        "os": f"{platform.system()} {platform.release()}",
        "uptime": str(uptime).split(".")[0],
        "cpu_percent": cpu,
        "ram": {
            "used_mb": ram.used // (1024 ** 2),
            "total_mb": ram.total // (1024 ** 2),
            "percent": ram.percent
        },
        "disk": {
            "used_gb": disk.used // (1024 ** 3),
            "total_gb": disk.total // (1024 ** 3),
            "percent": disk.percent
        }
    }
    await update.message.reply_text(as_json(data), parse_mode="Markdown")

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    await update.message.reply_text(as_json({
        "uptime": str(uptime).split(".")[0]
    }), parse_mode="Markdown")

async def cpu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    cpu_percent = psutil.cpu_percent(interval=1)
    await update.message.reply_text(as_json({
        "cpu_percent": cpu_percent
    }), parse_mode="Markdown")

async def ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    ram = psutil.virtual_memory()
    await update.message.reply_text(as_json({
        "ram": {
            "used_mb": ram.used // (1024 ** 2),
            "total_mb": ram.total // (1024 ** 2),
            "percent": ram.percent
        }
    }), parse_mode="Markdown")

async def disk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    disks = {}
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks[part.mountpoint] = {
                "used_gb": usage.used // (1024 ** 3),
                "total_gb": usage.total // (1024 ** 3),
                "percent": usage.percent
            }
        except: continue
    await update.message.reply_text(as_json({
        "disk": disks
    }), parse_mode="Markdown")

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global alerts_enabled
    if not await is_admin(update): return
    alerts_enabled = not alerts_enabled
    await update.message.reply_text(as_json({
        "alerts": "enabled" if alerts_enabled else "disabled"
    }), parse_mode="Markdown")

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    await update.message.reply_text(as_json({
        "message": "Shutting down the server..."
    }), parse_mode="Markdown")
    os.system("shutdown -h now")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    await update.message.reply_text(as_json({
        "commands": {
            "/status": "Show full system info (CPU, RAM, disk, uptime)",
            "/uptime": "Show system uptime",
            "/cpu": "Check CPU usage",
            "/ram": "Check RAM usage",
            "/disk": "Check disk usage",
            "/alert": "Toggle CPU alert (over 80%)",
            "/shutdown": "Shutdown the VPS (dangerous)",
            "/help": "Show command list"
        }
    }), parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("uptime", uptime))
    app.add_handler(CommandHandler("cpu", cpu))
    app.add_handler(CommandHandler("ram", ram))
    app.add_handler(CommandHandler("disk", disk))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("shutdown", shutdown))
    app.add_handler(CommandHandler("help", help_command))

    print("✅ Bot started with JSON replies.")
    app.run_polling()

if __name__ == "__main__":
    main()
