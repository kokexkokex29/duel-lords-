import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Create database instance
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure database
database_url = os.environ.get("DATABASE_URL", "sqlite:///tournament.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database with app
db.init_app(app)

# Define models inline to avoid circular imports
class Player(db.Model):
    """Player model for tournament participants"""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(20), unique=True, nullable=False)
    player_name = db.Column(db.String(100), nullable=False)
    discord_name = db.Column(db.String(100), nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Player {self.player_name}>'

class Duel(db.Model):
    """Duel model for scheduled matches"""
    __tablename__ = 'duels'
    
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.String(20), nullable=False)
    player2_id = db.Column(db.String(20), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    reminder_sent = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    winner_id = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Duel {self.player1_id} vs {self.player2_id}>'

class Match(db.Model):
    """Match history model"""
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.String(20), nullable=False)
    player2_id = db.Column(db.String(20), nullable=False)
    winner_id = db.Column(db.String(20), nullable=True)
    player1_kills = db.Column(db.Integer, default=0)
    player1_deaths = db.Column(db.Integer, default=0)
    player2_kills = db.Column(db.Integer, default=0)
    player2_deaths = db.Column(db.Integer, default=0)
    match_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Match {self.player1_id} vs {self.player2_id}>'

# Import routes after models are defined
from web_routes import *

# Create tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)