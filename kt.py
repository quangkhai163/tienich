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

# Check admin access
async def is_admin(update: Update):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(json.dumps({
            "error": "You are not authorized to use this bot."
        }, indent=2))
        return False
    return True

# /status command
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
    await update.message.reply_text(json.dumps(data, indent=2))

# /uptime
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    await update.message.reply_text(json.dumps({
        "uptime": str(uptime).split(".")[0]
    }, indent=2))

# /cpu
async def cpu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    cpu_percent = psutil.cpu_percent(interval=1)
    await update.message.reply_text(json.dumps({
        "cpu_percent": cpu_percent
    }, indent=2))

# /ram
async def ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    ram = psutil.virtual_memory()
    await update.message.reply_text(json.dumps({
        "ram": {
            "used_mb": ram.used // (1024 ** 2),
            "total_mb": ram.total // (1024 ** 2),
            "percent": ram.percent
        }
    }, indent=2))

# /disk
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
    await update.message.reply_text(json.dumps({
        "disk": disks
    }, indent=2))

# /alert
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global alerts_enabled
    if not await is_admin(update): return
    alerts_enabled = not alerts_enabled
    await update.message.reply_text(json.dumps({
        "alerts": "enabled" if alerts_enabled else "disabled"
    }, indent=2))

# /shutdown
async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    await update.message.reply_text(json.dumps({
        "message": "Shutting down the server..."
    }, indent=2))
    os.system("shutdown -h now")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    await update.message.reply_text(json.dumps({
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
    }, indent=2))

# Start bot
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

    print("✅ JSON-based VPS Monitor Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()