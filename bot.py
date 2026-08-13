import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN set in environment")

# NOTE: The Mini App is not yet set up with a valid HTTPS web server.
# Telegram keyboard buttons require a real "https://" URL - a "t.me/..." link
# is not valid for a `url` or `web_app` button and causes Button_url_invalid
# errors. Once you have a real web server for the Mini App, set its HTTPS
# URL here and register it with BotFather, then restore the web_app buttons.
WEBSITE_URL = "https://storesm.net"
SUPPORT_CHANNEL = "https://t.me/ForexMarketBrief"  # or your support contact

# ---------- Keyboards ----------
def get_main_keyboard():
    """Inline keyboard with Visit Website (only valid HTTPS URL available)."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🌐 Visit Website",
                url=WEBSITE_URL
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_app_only_keyboard():
    """Mini App is not configured yet, so just link to the website."""
    keyboard = [
        [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_URL)]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_categories_keyboard():
    """
    Category browsing normally deep-links into the Mini App, but no valid
    Mini App URL is configured yet. Show categories as plain text and only
    offer the website link button.
    """
    keyboard = [
        [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_URL)]
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- Command Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = (
        f"👋 Welcome to STORESM, {user.first_name}!\n\n"
        "Your place to explore digital resources, marketing tools, "
        "social media solutions and online services.\n\n"
        "🔎 Browse available resources\n"
        "📂 Explore different categories\n"
        "🚀 Discover useful services\n"
        "🌐 Access the STORESM marketplace\n\n"
        "🚧 Our Mini App is being set up. In the meantime, visit our "
        "website below to explore STORESM."
    )
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🚧 The STORESM Mini App isn't available yet. "
        "In the meantime, check out our website below.",
        reply_markup=get_app_only_keyboard()
    )

async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📂 Explore our main categories:\n\n"
        "• Social Media\n"
        "• Marketing Tools\n"
        "• Digital Resources\n"
        "• Online Services\n\n"
        "Our Mini App is coming soon. For now, visit our website below to learn more."
    )
    await update.message.reply_text(
        text,
        reply_markup=get_categories_keyboard()
    )

async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"🌐 Visit our official website: {WEBSITE_URL}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🤖 *STORESM Bot Commands*\n\n"
        "/start – Welcome message & website link\n"
        "/app – Mini App status (coming soon)\n"
        "/categories – Browse product categories\n"
        "/website – Visit storesm.net\n"
        "/help – Show this help message\n"
        "/support – Get support contact\n\n"
        "Need more? Just ask!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    support_text = (
        "📞 For support, please reach out through:\n\n"
        f"• Telegram Channel: {SUPPORT_CHANNEL}\n"
        "• Or visit our website for contact options."
    )
    await update.message.reply_text(support_text)

# ---------- Error Handler ----------
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Oops, something went wrong. Please try again later."
        )

# ---------- Main ----------
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Register commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("app", app_command))
    application.add_handler(CommandHandler("categories", categories_command))
    application.add_handler(CommandHandler("website", website_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("support", support_command))

    application.add_error_handler(error_handler)

    # Start polling (or use webhook if preferred)
    logger.info("Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
