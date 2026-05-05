SELECT t.full_name, AVG(ag.grade) AS avg_grade
FROM assignments_grades ag
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
JOIN teachers t ON a.teacher_id = t.teacher_id
GROUP BY t.teacher_id
ORDER BY avg_grade ASC
LIMIT 1;

SELECT s.full_name, AVG(ag.grade) AS avg_grade
FROM assignments_grades ag
JOIN students s ON ag.student_id = s.student_id
GROUP BY s.student_id
ORDER BY avg_grade DESC
LIMIT 10;

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

SELECT sg.group_id,
       COUNT(DISTINCT s.student_id) AS total_students,
       AVG(ag.grade) AS avg_grade,
       COUNT(DISTINCT CASE WHEN ag.grade IS NULL OR ag.grade = 0 THEN s.student_id END) AS not_submitted,
       COUNT(DISTINCT CASE WHEN ag.date > a.due_date THEN s.student_id END) AS late_submissions,
       COUNT(DISTINCT CASE WHEN ag.grade IS NOT NULL AND ag.grade > 0 THEN ag.grade_id END) -
       COUNT(DISTINCT s.student_id) AS retakes
FROM students_groups sg
JOIN students s ON sg.group_id = s.group_id
LEFT JOIN assignments_grades ag ON s.student_id = ag.student_id
LEFT JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
GROUP BY sg.group_id;

SELECT AVG(ag.grade) AS avg_grade
FROM assignments_grades ag
WHERE ag.assisgnment_id IN (
    SELECT a.assisgnment_id
    FROM assignments a
    WHERE a.assignment_text LIKE '%прочитать%'
       OR a.assignment_text LIKE '%выучить%'
);