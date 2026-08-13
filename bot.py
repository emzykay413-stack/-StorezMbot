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

# Your Mini App URL (use the one you set via BotFather)
MINI_APP_URL = "https://t.me/StorezMbot/StorezMminiapp"   # or your direct webapp URL
WEBSITE_URL = "https://storesm.net"
SUPPORT_CHANNEL = "https://t.me/ForexMarketBrief"  # or your support contact

# ---------- Keyboards ----------
def get_main_keyboard():
    """Inline keyboard with Open App, Visit Website, and Join Channel."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🛍 Open STORESM",
                url=MINI_APP_URL
            ),
            InlineKeyboardButton(
                text="🌐 Visit Website",
                url=WEBSITE_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 Join Channel",
                url=SUPPORT_CHANNEL
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_app_only_keyboard():
    """Keyboard with only the Open App button."""
    keyboard = [
        [InlineKeyboardButton("🛍 Open STORESM", url=MINI_APP_URL)]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_categories_keyboard():
    """Category buttons that open the app with a start_param for deep-linking."""
    categories = [
        ("Social Media", "social_media"),
        ("Marketing Tools", "marketing_tools"),
        ("Digital Resources", "digital_resources"),
        ("Online Services", "online_services"),
    ]
    keyboard = []
    for label, param in categories:
        # Deep link: ?startapp=category_param
        deep_link = f"{MINI_APP_URL}?startapp=category_{param}"
        keyboard.append([InlineKeyboardButton(label, url=deep_link)])
    # Add a general "Open App" button at the bottom
    keyboard.append([InlineKeyboardButton("🛍 Open STORESM", url=MINI_APP_URL)])
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
        "Ready to explore? 👇 Tap the button below to open STORESM."
    )
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🛍 Tap the button below to open the STORESM Mini App.",
        reply_markup=get_app_only_keyboard()
    )

async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📂 Explore our main categories:\n\n"
        "• Social Media\n"
        "• Marketing Tools\n"
        "• Digital Resources\n"
        "• Online Services\n\n"
        "Tap a category below to open the app and see relevant resources."
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
        "/start – Welcome & open the Mini App\n"
        "/app – Open the Mini App directly\n"
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
