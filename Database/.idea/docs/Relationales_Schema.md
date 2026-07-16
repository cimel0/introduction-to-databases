# CHESS DATABASE - RELATIONAL SCHEMA

## Task 1: Visualizing the Schema

## RELATIONAL SCHEMA (Compact Notation)

1. **Players** (`player_id`, `player_name`)

2. **Titles** (`title_id`, `title_short`)

3. **Ecos** (`eco_id`, `eco_code`)

4. **Openings** (`opening_id`, `opening_text`, `eco_id`)
   └─ FK: `eco_id` → `Ecos.eco_id`

5. **Endings** (`ending_id`, `ending_type`)

6. **Events** (`event_id`, `event_name`)

7. **Tournaments** (`tournament_id`, `tournament_url`)

8. **Games** (`game_id`, `event_id`, `tournament_id`, `site`, `result`,
   `game_start`, `opening_id`, `time_control`, `ending_id`, `game_data`)
   └─ FK: `event_id` → `Events.event_id`
   └─ FK: `tournament_id` → `Tournaments.tournament_id` *(nullable)*
   └─ FK: `opening_id` → `Openings.opening_id`
   └─ FK: `ending_id` → `Endings.ending_id`

9. **Games_Players** (`player_id`, `game_id`, `elo`, `diff`, `title_id`, `white`)
   └─ **PK:** (`player_id`, `game_id`) — Composite Key!
   └─ FK: `player_id` → `Players.player_id`
   └─ FK: `game_id` → `Games.game_id`
   └─ FK: `title_id` → `Titles.title_id` *(nullable)*

---

## KEY RELATIONSHIPS

* **Events** ──(1,*)──> **Games**
  One event has many games

* **Tournaments** ──(0,*)──> **Games**
  One tournament has many games (optional)

* **Ecos** ──(1,*)──> **Openings** ──(1,*)──> **Games**
  Classification hierarchy

* **Endings** ──(1,*)──> **Games**
  One ending type in many games

* **Players** ←──(2,*)──> **Games** *(via `Games_Players`)*
  MANY-TO-MANY: Each game has 2 players, each player plays many games

* **Titles** ──(0,*)──> **Games_Players**
  One title held by many players (optional)

## 4. KEY RELATIONSHIPS & CARDINALITIES

```
┌────────────────────────────────────────────────────────────┐
│ Relationship             │ From      │ To        │ Type   │
├──────────────────────────┼───────────┼───────────┼────────┤
│ Events → Games           │ (1,1)     │ (1,*)     │ 1:n    │
│ Tournaments → Games      │ (0,1)     │ (0,*)     │ 1:n    │
│ Ecos → Openings          │ (1,1)     │ (1,*)     │ 1:n    │
│ Openings → Games         │ (1,1)     │ (1,*)     │ 1:n    │
│ Endings → Games          │ (1,1)     │ (1,*)     │ 1:n    │
│ Players ↔ Games          │ (1,*)     │ (2,*)     │ m:n    │
│ Titles → Games_Players   │ (0,1)     │ (0,*)     │ 1:n    │
└──────────────────────────┴───────────┴───────────┴────────┘
```

---

## IMPORTANT NOTES

1. **`GAMES_PLAYERS` is a many-to-many relationship table**

* Connects Players and Games
* Contains game-specific player data (elo, title, color)
* `white` boolean: `TRUE` = played white, `FALSE` = played black

2. **Composite Primary Key in `Games_Players`:**

* (`player_id`, `game_id`) together form the PK

3. **Nullable Foreign Keys:**

* `tournament_id` in `Games` (not all games in tournaments)
* `title_id` in `Games_Players` (not all players have titles)

4. **Each game has exactly 2 rows in `Games_Players`:**

* One where `white = TRUE` (white player)
* One where `white = FALSE` (black player)

---

# Chess Database - ER Diagram (Visual)

## Complete Entity-Relationship Diagram

```
┌──────────────┐
│    Events    │
│──────────────│
│ event_id PK  │
│ event_name   │
└──────┬───────┘
│
│ has
(1,1) │ (1,*)
↓
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│     Ecos     │         │    Games     │         │ Tournaments  │
│──────────────│         │──────────────│         │──────────────│
│ eco_id PK    │    ┌───►│ game_id PK   │◄───┐    │tournament_id │
│ eco_code     │    │    │ event_id FK  │    │    │     PK       │
└──────┬───────┘    │    │tournament_id │    │    │tournament_url│
│            │    │     FK       │    │    └──────────────┘
│ classifies │    │ site         │    │
│ (1,*)      │    │ result       │    │ held_in
↓            │    │ game_start   │    │ (0,1) (0,*)
┌──────────────┐    │    │ opening_id FK│    │
│   Openings   │    │    │ time_control │    │
│──────────────│    │    │ ending_id FK │    │
│ opening_id PK│────┘    │ game_data    │    │
│ opening_text │         └──────┬───────┘    │
│ eco_id FK    │                │            │
└──────────────┘                │            │
│ ends_with  │
(1,1) │ (1,*)      │
↓            │
┌──────────────┐    │
│   Endings    │    │
│──────────────│    │
│ ending_id PK │    │
│ ending_type  │    │
└──────────────┘    │
│
┌────────────────────────────────────┘
│
│ participates_in (MANY-TO-MANY via Games_Players)
│
↓
┌─────────────────────────────────────────────┐
│           Games_Players                      │
│      (Relationship Table)                    │
│─────────────────────────────────────────────│
│ player_id PK, FK → Players                  │
│ game_id PK, FK → Games                      │
│ elo                                          │
│ diff                                         │
│ title_id FK → Titles                        │
│ white (boolean: TRUE=white, FALSE=black)    │
└────────┬─────────────────────┬──────────────┘
│                     │
(1,*) │                     │ (0,1)
↓                     ↓
┌──────────────┐       ┌──────────────┐
│   Players    │       │    Titles    │
│──────────────│       │──────────────│
│ player_id PK │       │ title_id PK  │
│ player_name  │       │ title_short  │
└──────────────┘       └──────────────┘
```

## Cardinality Explanation

**(min, max) notation:**

1. **Events → Games: (1,1) to (1,*)**

* Every game belongs to exactly ONE event
* Every event has AT LEAST one game (can have many)

2. **Tournaments → Games: (0,1) to (0,*)**

* A game MAY belong to a tournament (optional)
* A tournament can have zero or many games

3. **Ecos → Openings: (1,*)**

* One ECO code has many opening variations

4. **Openings → Games: (1,*)**

* One opening is used in many games
* Every game has exactly one opening

5. **Endings → Games: (1,*)**

* One ending type occurs in many games
* Every game has exactly one ending

6. **Players ↔ Games: (2,*) via `Games_Players`**

* MANY-TO-MANY relationship
* Each game has EXACTLY 2 players (one white, one black)
* Each player plays MANY games
* Represented via the `Games_Players` junction table

7. **Titles → Games_Players: (0,1) to (0,*)**

* A player in a game MAY have a title (optional)
* One title can be held by many players

## Reading the Diagram

**Example: How to find all players in a game?**

```
Games → Games_Players → Players
(game_id)       (player_id)
```

**Example: What opening was used in a game?**

```
Games → Openings → Ecos
(opening_id) (eco_id)
```

## Special Notes

### Games_Players Table

This is a **many-to-many relationship table** with additional attributes:

* **Primary Key:** (`player_id`, `game_id`) — Composite key!

* **Special attribute `white`:**

* `TRUE` = player played as white
* `FALSE` = player played as black
* This allows us to distinguish the two players in each game

* **Time-specific data:**

* `elo`: Player’s rating **at the time** of this specific game
* `diff`: Rating change **after** this game
* This is why we can’t just put this in the Players table!

### Why `Games_Players` is needed

**WITHOUT `Games_Players` (wrong!):**

```
Games (game_id, white_player_id, black_player_id, ...)
```

* ❌ Problem: Can’t store player-specific data like `elo`/`diff`
* ❌ Problem: Not flexible (what about 3+ player variants?)

**WITH `Games_Players` (correct!):**

```
Games (game_id, ...)
Games_Players (player_id, game_id, white, elo, diff, ...)
```

* ✓ Flexible: Easy to add more players if needed
* ✓ Normalized: Player data stored with the specific game
* ✓ Queryable: Easy to find “all games where player X played white”
