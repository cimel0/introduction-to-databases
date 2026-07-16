# ex2.py - Fully adapted for SQLite
# All queries are fixed to work with SQLite

import sqlite3
import calendar

print("Ex2 - SQLite Version")
print("-" * 70)
print()

# Connect to SQLite database
con = sqlite3.connect('chess.db')
cur = con.cursor()

# Print database version
cur.execute('SELECT sqlite_version()')  # <- FIXED: sqlite_version() instead of version()
print('SQLite Version:', cur.fetchone()[0])
print()

# 1. How many games were won by white? (1-0)/(0-1)
cur.execute("SELECT COUNT(*) FROM games WHERE result = '1-0'")
white_wins = cur.fetchone()[0]
print(f"Games won by white: {white_wins}")

# 2. Number of games per month (print month name, not number)  
print("\nGames per month:")
cur.execute("""
    SELECT CAST(strftime('%m', datetime(game_start, 'unixepoch')) AS INTEGER) as month, 
           COUNT(*) as count
    FROM games
    WHERE game_start IS NOT NULL
    GROUP BY strftime('%m', datetime(game_start, 'unixepoch'))
    ORDER BY month
""")  # <- FIXED: strftime() instead of EXTRACT() or timezone function, 
#game_start was stored as unix timestamps (not a date!) -> datetime() to convert it 
# strftime %m extract month, cast to get integer 

for row in cur.fetchall():
    month_number = row[0]
    if month_number is None:
        continue
    month_number = int(month_number)
    month_name = calendar.month_name[month_number]
    count = row[1]
    print(f"{month_name}: {count}")

# 3. Total number of games
cur.execute("SELECT COUNT(*) FROM games")
total_games = cur.fetchone()[0]
print(f"\nTotal number of games: {total_games}")

# Close connection
cur.close()
con.close()

print()