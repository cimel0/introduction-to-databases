========================================
CHESS DATABASE - RELATIONAL SCHEMA
Task 1: Visualizing the Schema
========================================

## RELATIONAL SCHEMA (Compact Notation)

1. Players (player_id, player_name)

2. Titles (title_id, title_short)

3. Ecos (eco_id, eco_code)

4. Openings (opening_id, opening_text, eco_id)
   └─ FK: eco_id → Ecos.eco_id

5. Endings (ending_id, ending_type)

6. Events (event_id, event_name)

7. Tournaments (tournament_id, tournament_url)

8. Games (game_id, event_id, tournament_id, site, result, 
          game_start, opening_id, time_control, ending_id, game_data)
   └─ FK: event_id → Events.event_id
   └─ FK: tournament_id → Tournaments.tournament_id (nullable)
   └─ FK: opening_id → Openings.opening_id
   └─ FK: ending_id → Endings.ending_id

9. Games_Players (player_id, game_id, elo, diff, title_id, white)
   └─ PK: (player_id, game_id) - Composite Key!
   └─ FK: player_id → Players.player_id
   └─ FK: game_id → Games.game_id
   └─ FK: title_id → Titles.title_id (nullable)

========================================
KEY RELATIONSHIPS
========================================

• Events ──(1,*)──> Games
  One event has many games

• Tournaments ──(0,*)──> Games
  One tournament has many games (optional)

• Ecos ──(1,*)──> Openings ──(1,*)──> Games
  Classification hierarchy

• Endings ──(1,*)──> Games
  One ending type in many games

• Players ←──(2,*)──> Games (via Games_Players)
  MANY-TO-MANY: Each game has 2 players, each player plays many games

• Titles ──(0,*)──> Games_Players
  One title held by many players (optional)

========================================
IMPORTANT NOTES
========================================

1. GAMES_PLAYERS is a many-to-many relationship table
   - Connects Players and Games
   - Contains game-specific player data (elo, title, color)
   - 'white' boolean: TRUE = played white, FALSE = played black

2. COMPOSITE PRIMARY KEY in Games_Players:
   - (player_id, game_id) together form the PK

3. NULLABLE FOREIGN KEYS:
   - tournament_id in Games (not all games in tournaments)
   - title_id in Games_Players (not all players have titles)

4. EACH GAME HAS EXACTLY 2 ROWS in Games_Players:
   - One where white=TRUE (white player)
   - One where white=FALSE (black player)