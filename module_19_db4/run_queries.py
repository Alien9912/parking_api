import sqlite3

conn = sqlite3.connect('homework.db')
cursor = conn.cursor()

print("===== Задание 1. Преподаватель с самыми сложными заданиями =====")
query1 = """
SELECT t.full_name, AVG(ag.grade) AS avg_grade
FROM assignments_grades ag
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
JOIN teachers t ON a.teacher_id = t.teacher_id
GROUP BY t.teacher_id
ORDER BY avg_grade ASC
LIMIT 1;
"""
cursor.execute(query1)
print(cursor.fetchall())

print("\n===== Задание 2. 10 лучших учеников =====")
query2 = """
SELECT s.full_name, AVG(ag.grade) AS avg_grade
FROM assignments_grades ag
JOIN students s ON ag.student_id = s.student_id
GROUP BY s.student_id
ORDER BY avg_grade DESC
LIMIT 10;
"""
cursor.execute(query2)
print(cursor.fetchall())

print("\n===== Задание 3. Ученики самого лёгкого преподавателя (вложенный) =====")
query3 = """
SELECT DISTINCT s.full_name
FROM students s
JOIN assignments_grades ag ON s.student_id = ag.student_id
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
WHERE a.teacher_id = (
    SELECT a.teacher_id
    FROM assignments_grades ag
    JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
    GROUP BY a.teacher_id
    ORDER BY AVG(ag.grade) DESC
    LIMIT 1
);
"""
cursor.execute(query3)
for row in cursor.fetchall():
    print(row[0])

print("\n===== Задание 3. Ученики самого лёгкого преподавателя (JOIN) =====")
query4 = """
SELECT DISTINCT s.full_name
FROM students s
JOIN assignments_grades ag ON s.student_id = ag.student_id
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
JOIN (
    SELECT a.teacher_id
    FROM assignments_grades ag
    JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
    GROUP BY a.teacher_id
    ORDER BY AVG(ag.grade) DESC
    LIMIT 1
) easiest ON a.teacher_id = easiest.teacher_id;
"""
cursor.execute(query4)
for row in cursor.fetchall():
    print(row[0])

print("\n===== Задание 4. Просроченные задания по классам (вложенный) =====")
query5 = """
SELECT sg.group_id,
       AVG(late_count) AS avg_late,
       MAX(late_count) AS max_late,
       MIN(late_count) AS min_late
FROM students_groups sg
JOIN (
    SELECT s.group_id, s.student_id, COUNT(*) AS late_count
    FROM students s
    JOIN assignments_grades ag ON s.student_id = ag.student_id
    JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
    WHERE ag.date > a.due_date
    GROUP BY s.student_id
) late_students ON sg.group_id = late_students.group_id
GROUP BY sg.group_id;
"""
cursor.execute(query5)
print("group_id | avg_late | max_late | min_late")
for row in cursor.fetchall():
    print(row)

print("\n===== Задание 4. Просроченные задания по классам (JOIN) =====")
query6 = """
SELECT sg.group_id,
       AVG(late_count) AS avg_late,
       MAX(late_count) AS max_late,
       MIN(late_count) AS min_late
FROM students_groups sg
JOIN students s ON sg.group_id = s.group_id
JOIN (
    SELECT ag.student_id, COUNT(*) AS late_count
    FROM assignments_grades ag
    JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
    WHERE ag.date > a.due_date
    GROUP BY ag.student_id
) late_students ON s.student_id = late_students.student_id
GROUP BY sg.group_id;
"""
cursor.execute(query6)
print("group_id | avg_late | max_late | min_late")
for row in cursor.fetchall():
    print(row)

print("\n===== Задание 5. Статистика по группам =====")
query7 = """
SELECT sg.group_id,
       COUNT(DISTINCT s.student_id) AS total_students,
       AVG(ag.grade) AS avg_grade,
       COUNT(DISTINCT CASE WHEN ag.grade IS NULL OR ag.grade = 0 THEN s.student_id END) AS not_submitted,
       COUNT(DISTINCT CASE WHEN ag.date > a.due_date THEN s.student_id END) AS late_submissions,
       COUNT(ag.grade_id) - COUNT(DISTINCT s.student_id) AS retakes
FROM students_groups sg
JOIN students s ON sg.group_id = s.group_id
LEFT JOIN assignments_grades ag ON s.student_id = ag.student_id
LEFT JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
GROUP BY sg.group_id;
"""
cursor.execute(query7)
print("group_id | total_students | avg_grade | not_submitted | late | retakes")
for row in cursor.fetchall():
    print(row)

print("\n===== Задание 6. Средняя оценка за 'прочитать' и 'выучить' =====")
query8 = """
SELECT AVG(ag.grade) AS avg_grade
FROM assignments_grades ag
WHERE ag.assisgnment_id IN (
    SELECT a.assisgnment_id
    FROM assignments a
    WHERE a.assignment_text LIKE '%прочитать%'
       OR a.assignment_text LIKE '%выучить%'
);
"""
cursor.execute(query8)
print(cursor.fetchall())

conn.close()
print("\nГотово!")