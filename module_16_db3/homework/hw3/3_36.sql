SELECT class
FROM ships
WHERE name IN (SELECT ship FROM outcomes WHERE result = 'sunk')
UNION
SELECT class
FROM classes
WHERE class IN (SELECT ship FROM outcomes WHERE result = 'sunk');