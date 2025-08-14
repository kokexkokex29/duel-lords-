from flask import Flask
import threading
import time
import logging

logger = logging.getLogger(__name__)

def create_keepalive_app():
    """Create a simple Flask app for keepalive"""
    from app import app
    return app

def keep_alive():
    """Start the keepalive web server"""
    def run():
        try:
            app = create_keepalive_app()
            app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        except Exception as e:
            logger.error(f"Error in keepalive server: {e}")
    
    # Start the web server in a separate thread
    server_thread = threading.Thread(target=run, daemon=True)
    server_thread.start()
    logger.info("Keepalive web server started on port 5000")
