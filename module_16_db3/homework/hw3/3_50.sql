SELECT DISTINCT battle
FROM outcomes
WHERE ship IN (SELECT name FROM ships WHERE class = 'Kongo');