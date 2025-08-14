from datetime import datetime

def define_models(db):
    """Define database models after db is initialized"""
    
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
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<Player {self.player_name}>'
        
        def to_dict(self):
            return {
                'id': self.id,
                'discord_id': self.discord_id,
                'player_name': self.player_name,
                'discord_name': self.discord_name,
                'wins': self.wins,
                'losses': self.losses,
                'draws': self.draws,
                'kills': self.kills,
                'deaths': self.deaths,
                'points': self.points,
                'created_at': self.created_at
            }

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
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<Duel {self.player1_id} vs {self.player2_id}>'

    class Match(db.Model):
        """Match history model"""
        __tablename__ = 'matches'
        
        id = db.Column(db.Integer, primary_key=True)
        player1_id = db.Column(db.String(20), nullable=False)
        player2_id = db.Column(db.String(20), nullable=False)
        winner_id = db.Column(db.String(20), nullable=True)  # None for draw
        player1_kills = db.Column(db.Integer, default=0)
        player1_deaths = db.Column(db.Integer, default=0)
        player2_kills = db.Column(db.Integer, default=0)
        player2_deaths = db.Column(db.Integer, default=0)
        match_date = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<Match {self.player1_id} vs {self.player2_id}>'
    
    return Player, Duel, Match