--- Names: Liza Salija, Melisa Cimendag 

/* Task 2 */
--- 1
SELECT opening_text 
FROM openings 
WHERE opening_id = 42; 

--- 2
SELECT COUNT(player_id) 
FROM players;

--- 3
SELECT player_id, MAX(diff)
FROM games_players
GROUP BY player_id;

--- 4
SELECT gp.player_id,
       gp.game_id,
       gp.diff
FROM games_players AS gp
WHERE gp.diff = (
    SELECT MAX(diff)
    FROM games_players AS gp2
    WHERE gp2.player_id = gp.player_id
);

--- 5
SELECT o.opening_text,
       COUNT(g.game_id) AS times_played
FROM openings AS o
INNER JOIN games AS g
  ON g.opening_id = o.opening_id
GROUP BY o.opening_text;



--- 6
SELECT p.player_id,
       p.player_name,
       COUNT(g.game_id) AS wins
FROM players AS p
INNER JOIN games_players AS gp
  ON p.player_id = gp.player_id
INNER JOIN games AS g
  ON g.game_id = gp.game_id
WHERE (gp.white = 1 AND g.result = '1-0')
   OR (gp.white = 0 AND g.result = '0-1')
GROUP BY p.player_id, p.player_name
ORDER BY wins DESC;


--- 7
SELECT p.player_name, COUNT(DISTINCT g.opening_id) AS 'distinct_openings'
FROM players AS p
LEFT JOIN games_players AS gp ON p.player_id = gp.player_id
LEFT JOIN games AS g ON gp.game_id = g.game_id
GROUP BY p.player_name
ORDER BY distinct_openings DESC, p.player_name
LIMIT 10;


--- 8
SELECT gp1.player_id AS player1, gp2.player_id AS player2, COUNT(*) AS games_played
FROM games_players gp1
JOIN games_players gp2 ON gp1.game_id = gp2.game_id AND gp1.player_id != gp2.player_id
GROUP BY gp1.player_id, gp2.player_id
HAVING COUNT(*) > 100
ORDER BY games_played DESC;


--- 9
SELECT g.game_id,
       e.event_name,
       t.tournament_url
FROM games AS g
         LEFT JOIN events AS e
                   ON e.event_id = g.event_id
         LEFT JOIN tournaments AS t
                   ON t.tournament_id = g.tournament_id;


--- 10
SELECT p.player_id,
       SUM(CASE WHEN gp.white = 1 AND g.result = '1-0' THEN 1 ELSE 0 END) AS white_wins
FROM players AS p
         INNER JOIN games_players AS gp
                    ON gp.player_id = p.player_id
         INNER JOIN games AS g
                    ON g.game_id = gp.game_id
GROUP BY p.player_id
HAVING SUM(CASE WHEN gp.white = 1 AND g.result = '1-0' THEN 1 ELSE 0 END)
           = SUM(CASE WHEN gp.white = 0 AND g.result = '0-1' THEN 1 ELSE 0 END);




--- 11
ALTER TABLE titles ADD COLUMN title_long TEXT;






--- 12
SELECT * FROM titles;

UPDATE titles
SET title_long = 'Grandmaster'
WHERE title_short = 'GM';

UPDATE titles
SET title_long = 'International Master'
WHERE title_short = 'IM';

UPDATE titles
SET title_long = 'FIDE Master'
WHERE title_short = 'FM';

UPDATE titles
SET title_long = 'Candidate Master'
WHERE title_short = 'CM';

UPDATE titles
SET title_long = 'Women’s Grandmaster'
WHERE title_short = 'WGM';

UPDATE titles
SET title_long = 'Women’s International Master'
WHERE title_short = 'WIM';

UPDATE titles
SET title_long = 'Women’s FIDE Master'
WHERE title_short = 'WFM';

UPDATE titles
SET title_long = 'Women’s Candidate Master'
WHERE title_short = 'WCM';

UPDATE titles
SET title_long = 'National Master'
WHERE title_short = 'NM';

UPDATE titles
SET title_long = 'Life Master'
WHERE title_short = 'LM';

SELECT * FROM titles;


/* Task 3 */
SELECT 
    orders.order_id, 
    orders.order_date, 
    customers.customer_name
FROM 
    customers, orders
WHERE
    customers.customer_id = orders.customer_id
    AND orders.order_date > '2025-07-01';
/*This query joins the customers and orders tables and selects each order together with the name of the customer who placed it.
It then filters the results to include only orders made after July 1st, 2025. */