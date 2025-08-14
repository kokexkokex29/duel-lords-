import os
import threading
import logging
import time
from app import app

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_discord_bot():
    """Run Discord bot in separate thread"""
    try:
        logger.info("🚀 Starting Discord bot thread...")
        from bot import run_bot
        run_bot()
    except Exception as e:
        logger.error(f"❌ Error in Discord bot: {e}")

# Start Discord bot in background thread when module is imported
bot_thread = threading.Thread(target=run_discord_bot, daemon=True)
bot_thread.start()
logger.info("🤖 Discord bot thread started")

# Give bot some time to initialize
time.sleep(1)

# This is for gunicorn compatibility
if __name__ == "__main__":
    logger.info("🌐 Starting Flask app directly...")
    app.run(host='0.0.0.0', port=5000, debug=False)
