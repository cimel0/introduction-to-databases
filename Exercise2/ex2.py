# /// script
# requires-python = ">=3.10"
# dependencies = [
#  "psycopg[binary]"
# ]
# ///

import psycopg
import getpass
import calendar

# Securely prompt for password
password = getpass.getpass("Password: ")

# Connect to the database
con = psycopg.connect(
    host='dmi-dbis-introdb1.dmi.unibas.ch',
    port=5432,
    dbname='introdb',
    user='introdb107',
    password=password,
)

cur = con.cursor()

# Print database version
cur.execute('SELECT version()')
print('Version:', cur.fetchone()[0])
print()

# 1. How many games were won by white? (1-0)/(0-1)
cur.execute("SELECT COUNT(*) FROM games WHERE result = '1-0'")
white_wins = cur.fetchone()[0]
print(f"Games won by white: {white_wins}")

# 2. Number of games per month (print month name, not number)
print("\nGames per month:")
cur.execute("""
    SELECT EXTRACT(MONTH FROM game_start AT TIME ZONE 'UTC') as month, 
           COUNT(*) as count
    FROM games
    GROUP BY EXTRACT(MONTH FROM game_start AT TIME ZONE 'UTC')
    ORDER BY month
""")

for row in cur.fetchall():
    month_number = int(row[0])
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