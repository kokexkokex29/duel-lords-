import sqlite3
import logging
from datetime import datetime, timedelta
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path="tournament.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Players table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id TEXT UNIQUE NOT NULL,
                    player_name TEXT NOT NULL,
                    discord_name TEXT NOT NULL,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    draws INTEGER DEFAULT 0,
                    kills INTEGER DEFAULT 0,
                    deaths INTEGER DEFAULT 0,
                    points INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Duels table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS duels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player1_id TEXT NOT NULL,
                    player2_id TEXT NOT NULL,
                    scheduled_time TIMESTAMP NOT NULL,
                    reminder_sent BOOLEAN DEFAULT FALSE,
                    completed BOOLEAN DEFAULT FALSE,
                    winner_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Matches table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player1_id TEXT NOT NULL,
                    player2_id TEXT NOT NULL,
                    winner_id TEXT,
                    player1_kills INTEGER DEFAULT 0,
                    player1_deaths INTEGER DEFAULT 0,
                    player2_kills INTEGER DEFAULT 0,
                    player2_deaths INTEGER DEFAULT 0,
                    match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def add_player(self, discord_id, player_name, discord_name):
        """Add a new player to the tournament"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO players (discord_id, player_name, discord_name)
                    VALUES (?, ?, ?)
                ''', (str(discord_id), player_name, discord_name))
                conn.commit()
                logger.info(f"Added player: {player_name} ({discord_id})")
                return True
        except sqlite3.IntegrityError:
            logger.warning(f"Player already exists: {discord_id}")
            return False
        except Exception as e:
            logger.error(f"Error adding player: {e}")
            return False
    
    def remove_player(self, discord_id):
        """Remove a player from the tournament"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM players WHERE discord_id = ?', (str(discord_id),))
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Removed player: {discord_id}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error removing player: {e}")
            return False
    
    def get_player_stats(self, discord_id):
        """Get player statistics"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM players WHERE discord_id = ?', (str(discord_id),))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Error getting player stats: {e}")
            return None
    
    def get_all_players(self):
        """Get all registered players"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM players ORDER BY created_at')
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all players: {e}")
            return []
    
    def get_leaderboard(self, limit=20):
        """Get tournament leaderboard"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM players 
                    ORDER BY points DESC, wins DESC, kills DESC
                    LIMIT ?
                ''', (limit,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    def update_match_result(self, player1_id, player2_id, result, p1_kills=0, p1_deaths=0, p2_kills=0, p2_deaths=0):
        """Update player statistics after a match"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Check if both players exist
                cursor.execute('SELECT discord_id FROM players WHERE discord_id IN (?, ?)', 
                             (str(player1_id), str(player2_id)))
                if len(cursor.fetchall()) != 2:
                    return False
                
                # Determine winner and points
                winner_id = None
                p1_points = 0
                p2_points = 0
                
                if result == "player1_win":
                    winner_id = str(player1_id)
                    p1_points = 3
                    p2_points = 0
                    # Update player1 wins, player2 losses
                    cursor.execute('UPDATE players SET wins = wins + 1, points = points + ? WHERE discord_id = ?', 
                                 (p1_points, str(player1_id)))
                    cursor.execute('UPDATE players SET losses = losses + 1, points = points + ? WHERE discord_id = ?', 
                                 (p2_points, str(player2_id)))
                elif result == "player2_win":
                    winner_id = str(player2_id)
                    p1_points = 0
                    p2_points = 3
                    # Update player2 wins, player1 losses
                    cursor.execute('UPDATE players SET wins = wins + 1, points = points + ? WHERE discord_id = ?', 
                                 (p2_points, str(player2_id)))
                    cursor.execute('UPDATE players SET losses = losses + 1, points = points + ? WHERE discord_id = ?', 
                                 (p1_points, str(player1_id)))
                elif result == "draw":
                    p1_points = 1
                    p2_points = 1
                    # Update both players draws
                    cursor.execute('UPDATE players SET draws = draws + 1, points = points + ? WHERE discord_id = ?', 
                                 (p1_points, str(player1_id)))
                    cursor.execute('UPDATE players SET draws = draws + 1, points = points + ? WHERE discord_id = ?', 
                                 (p2_points, str(player2_id)))
                
                # Update kills and deaths
                cursor.execute('UPDATE players SET kills = kills + ?, deaths = deaths + ? WHERE discord_id = ?', 
                             (p1_kills, p1_deaths, str(player1_id)))
                cursor.execute('UPDATE players SET kills = kills + ?, deaths = deaths + ? WHERE discord_id = ?', 
                             (p2_kills, p2_deaths, str(player2_id)))
                
                # Record the match
                cursor.execute('''
                    INSERT INTO matches (player1_id, player2_id, winner_id, player1_kills, player1_deaths, player2_kills, player2_deaths)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (str(player1_id), str(player2_id), winner_id, p1_kills, p1_deaths, p2_kills, p2_deaths))
                
                conn.commit()
                logger.info(f"Updated match result: {player1_id} vs {player2_id} - {result}")
                return True
                
        except Exception as e:
            logger.error(f"Error updating match result: {e}")
            return False
    
    def schedule_duel(self, player1_id, player2_id, scheduled_time):
        """Schedule a duel between two players"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Check if both players exist
                cursor.execute('SELECT discord_id FROM players WHERE discord_id IN (?, ?)', 
                             (str(player1_id), str(player2_id)))
                if len(cursor.fetchall()) != 2:
                    return None
                
                cursor.execute('''
                    INSERT INTO duels (player1_id, player2_id, scheduled_time)
                    VALUES (?, ?, ?)
                ''', (str(player1_id), str(player2_id), scheduled_time))
                
                duel_id = cursor.lastrowid
                conn.commit()
                logger.info(f"Scheduled duel: {player1_id} vs {player2_id} at {scheduled_time}")
                return duel_id
                
        except Exception as e:
            logger.error(f"Error scheduling duel: {e}")
            return None
    
    def get_upcoming_duels(self):
        """Get duels that need reminders (5 minutes before start)"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                reminder_time = datetime.utcnow() + timedelta(minutes=5)
                
                cursor.execute('''
                    SELECT * FROM duels 
                    WHERE reminder_sent = FALSE 
                    AND completed = FALSE 
                    AND scheduled_time <= ?
                    AND scheduled_time > ?
                ''', (reminder_time, datetime.utcnow()))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting upcoming duels: {e}")
            return []
    
    def mark_reminder_sent(self, duel_id):
        """Mark reminder as sent for a duel"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE duels SET reminder_sent = TRUE WHERE id = ?', (duel_id,))
                conn.commit()
        except Exception as e:
            logger.error(f"Error marking reminder sent: {e}")
    
    def get_recent_matches(self, limit=10):
        """Get recent match history"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT m.*, p1.player_name as player1_name, p2.player_name as player2_name,
                           pw.player_name as winner_name
                    FROM matches m
                    JOIN players p1 ON m.player1_id = p1.discord_id
                    JOIN players p2 ON m.player2_id = p2.discord_id
                    LEFT JOIN players pw ON m.winner_id = pw.discord_id
                    ORDER BY m.match_date DESC
                    LIMIT ?
                ''', (limit,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting recent matches: {e}")
            return []
