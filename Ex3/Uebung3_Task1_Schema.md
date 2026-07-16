erDiagram
  Players ||--o{ Games_Players : plays
  Games   ||--o{ Games_Players : has
  Titles  ||--o{ Games_Players : has_title
  Events  ||--o{ Games : hosts
  Tournaments ||--o{ Games : includes
  Openings ||--o{ Games : used_in
  Endings  ||--o{ Games : ends_as
  Ecos ||--o{ Openings : defines

  Players { int player_id PK
            text player_name UNIQUE }

  Events { int event_id PK
           text event_name UNIQUE }

  Tournaments { int tournament_id PK
                text tournament_url UNIQUE }

  Ecos { int eco_id PK
         text eco_code UNIQUE }

  Openings { int opening_id PK
             text opening_text UNIQUE
             int eco_id FK }

  Endings { int ending_id PK
            text ending_type UNIQUE }

  Titles { int title_id PK
           text title_short UNIQUE }

  Games { int game_id PK
          text site UNIQUE
          text result
          timestamptz game_start
          text time_control
          text game_data
          int event_id FK
          int tournament_id FK
          int opening_id FK
          int ending_id FK }

  Games_Players {
    int player_id FK
    int game_id   FK
    bool white    -- mit (player_id, game_id) UNIQUE
    int elo
    int diff
    int title_id FK
  }
