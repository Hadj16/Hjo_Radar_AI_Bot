
import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BINANCE_API = "https://api.binance.com/api/v3"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🚀 مرحباً بك في Hjo Radar AI\n\n"
        "📊 نظام مراقبة سوق العملات الرقمية\n\n"
        "الأوامر المتاحة:\n"
        "/price BTCUSDT - سعر العملة\n"
        "/market - حالة السوق\n"
        "/help - المساعدة\n\n"
        "⚡ Hjo Radar AI Bot"
    )
    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 طريقة الاستخدام:\n\n"
        "اكتب:\n"
        "/price BTCUSDT\n\n"
        "لمعرفة سعر البيتكوين.\n\n"
        "اكتب /market لمعلومات السوق."
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "اكتب اسم العملة، مثال:\n/price BTCUSDT"
        )
        return

    symbol = context.args[0].upper()

    try:
        response = requests.get(
            f"{BINANCE_API}/ticker/price",
            params={"symbol": symbol},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        await update.message.reply_text(
            f"📊 العملة: {symbol}\n"
            f"💰 السعر: {data['price']}\n\n"
            "Hjo Radar AI"
        )

    except Exception:
        await update.message.reply_text(
            "⚠️ تعذر جلب السعر. تحقق من رمز العملة."
        )


async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(
            f"{BINANCE_API}/ticker/24hr",
            params={"symbol": "BTCUSDT"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        change = float(data["priceChangePercent"])
        direction = "🟢 ارتفاع" if change >= 0 else "🔴 انخفاض"

        await update.message.reply_text(
            "📈 تقرير السوق - BTCUSDT\n\n"
            f"💰 السعر: {data['lastPrice']}\n"
            f"📊 التغيير 24 ساعة: {change:.2f}%\n"
            f"📍 الحالة: {direction}\n\n"
            "⚠️ بيانات للمراقبة والتعليم وليست توصية تداول."
        )

    except Exception:
        await update.message.reply_text(
            "⚠️ تعذر الاتصال ببيانات السوق."
        )


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("market", market))

    print("Hjo Radar AI Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
