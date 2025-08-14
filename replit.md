# Overview

Duel Lords is a comprehensive Discord bot and web application for managing BombSquad tournaments. The system provides player registration, match scheduling, statistics tracking, and a professional web interface for tournament management. It features a Discord bot with slash commands for player interaction and a Flask web application for displaying leaderboards and match history.

## Recent Updates (August 2025)
- ✅ Complete Discord bot implementation with slash commands
- ✅ Player registration system with admin-only access
- ✅ Statistics tracking (wins/losses/draws/kills/deaths)
- ✅ Match scheduling with 5-minute reminder system
- ✅ Professional web interface with Bootstrap dark theme
- ✅ Multi-language support (English/Portuguese)
- ✅ Dual-process architecture (Bot + Web server)
- ✅ Environment secret configuration for Discord token
- ✅ Comprehensive README with Render.com deployment guide

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Architecture
- **Discord Bot Framework**: Uses discord.py with slash commands for modern Discord integration
- **Command System**: Implements admin-only commands for player management and public commands for server information
- **Background Tasks**: Automated reminder system using discord.ext.tasks for match notifications
- **Multi-language Support**: Translation system supporting English and Portuguese languages

## Web Application Architecture
- **Flask Framework**: Lightweight web framework serving the tournament dashboard
- **Template Engine**: Jinja2 templating with Bootstrap for responsive UI
- **Route Structure**: RESTful endpoints for home, leaderboard, and player pages
- **Static Assets**: CSS styling with dark theme and responsive design

## Data Layer Architecture
- **Dual Database Implementation**: 
  - SQLite with raw SQL queries (database.py) for Discord bot operations
  - SQLAlchemy ORM models (models.py) for web application data access
- **Database Schema**: Players, Duels, and Matches tables for comprehensive tournament tracking
- **Connection Management**: Context managers and connection pooling for reliability

## Authentication & Authorization
- **Discord-based Admin System**: Admin permissions based on Discord user IDs and server permissions
- **Command Restrictions**: Admin-only commands for sensitive operations like player registration
- **No Web Authentication**: Web interface is read-only and publicly accessible

## Application Lifecycle
- **Dual Process Architecture**: Separate Discord bot and web server running concurrently
- **Keepalive System**: Threading-based approach to run both Flask app and Discord bot
- **Main Entry Point**: Unified startup in main.py coordinating both services

# External Dependencies

## Discord Integration
- **Discord API**: Full Discord bot functionality via discord.py library
- **Slash Commands**: Modern Discord command interface
- **Rich Embeds**: Professional Discord message formatting
- **Direct Messaging**: Automated player notifications

## Web Technologies
- **Bootstrap CSS**: Frontend framework for responsive design
- **Font Awesome**: Icon library for enhanced UI
- **Flask Extensions**: SQLAlchemy for ORM, template rendering

## Game Server Integration
- **BombSquad Server**: Hardcoded server IP (18.228.228.44:3827) for tournament matches
- **No Direct API**: Manual result entry system rather than automated game integration

## Development & Deployment
- **Environment Variables**: Discord bot token and session secrets via environment configuration
- **SQLite Database**: File-based database for simple deployment
- **Static File Serving**: Flask serving CSS and other static assets
- **Logging System**: Python logging throughout the application for debugging and monitoring