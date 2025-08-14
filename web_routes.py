from flask import render_template, jsonify, request
from app import app, db, Player, Match
from database import DatabaseManager
import logging

logger = logging.getLogger(__name__)
db_manager = DatabaseManager()

@app.route('/')
def index():
    """Home page"""
    try:
        total_players = len(db_manager.get_all_players())
        recent_matches = db_manager.get_recent_matches(5)
        top_players = db_manager.get_leaderboard(3)
        
        return render_template('index.html', 
                             total_players=total_players,
                             recent_matches=recent_matches,
                             top_players=top_players)
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        return render_template('index.html', 
                             total_players=0,
                             recent_matches=[],
                             top_players=[])

@app.route('/leaderboard')
def leaderboard():
    """Leaderboard page"""
    try:
        players = db_manager.get_leaderboard(50)
        return render_template('leaderboard.html', players=players)
    except Exception as e:
        logger.error(f"Error loading leaderboard: {e}")
        return render_template('leaderboard.html', players=[])

@app.route('/players')
def players():
    """All players page"""
    try:
        all_players = db_manager.get_all_players()
        recent_matches = db_manager.get_recent_matches(20)
        return render_template('players.html', 
                             players=all_players,
                             recent_matches=recent_matches)
    except Exception as e:
        logger.error(f"Error loading players page: {e}")
        return render_template('players.html', 
                             players=[],
                             recent_matches=[])

@app.route('/api/stats')
def api_stats():
    """API endpoint for tournament statistics"""
    try:
        total_players = len(db_manager.get_all_players())
        recent_matches = db_manager.get_recent_matches(10)
        top_players = db_manager.get_leaderboard(10)
        
        return jsonify({
            'total_players': total_players,
            'recent_matches': recent_matches,
            'top_players': top_players,
            'server_ip': '18.228.228.44',
            'server_port': '3827'
        })
    except Exception as e:
        logger.error(f"Error in API stats: {e}")
        return jsonify({'error': 'Failed to load statistics'}), 500

@app.route('/api/leaderboard')
def api_leaderboard():
    """API endpoint for leaderboard data"""
    try:
        limit = request.args.get('limit', 20, type=int)
        players = db_manager.get_leaderboard(limit)
        return jsonify({'players': players})
    except Exception as e:
        logger.error(f"Error in API leaderboard: {e}")
        return jsonify({'error': 'Failed to load leaderboard'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'bot': 'Duel Lords',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {error}")
    return render_template('index.html'), 500
