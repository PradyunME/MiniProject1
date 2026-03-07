-- Help with Gemini --
/*
Prompt: 
imagine i have a sqlite database with the tables:
users(uid, name, email, role, pwd), where role ∈ {Student, Instructor, Admin} (i.e., role can be Student, Instructor, or Admin).
courses(cid, title, description, category, price, pass_grade, max_students)
enrollments(cid, uid, start_ts, end_ts, role), where role ∈ {Student, Instructor} (i.e., role can be Student or Instructor).
modules(cid, mid, name, summary, weight)
lessons(cid, mid, lid, title, duration, content)
completion(uid, cid, mid, lid, ts)
grades(uid, cid, mid, received_ts, grade)
certificates(cid, uid, received_ts, final_grade)
payments(uid, cid, ts, credit_card_no, expiry_date)

how would you write an sql query that finds course stats:

cid, title, number of active enrollments, percentage of actively enrolled students who have completed all lessons in the course, and average grade 

*/

-- This is meant to serve as the command passed to the c.execute() code and only needing 1 value, the instructor uid.--

WITH allCourseLessons AS (
    SELECT 
        lsn.cid,
        COUNT(lsn.lid) AS total_lessons
    FROM
        lessons lsn
    GROUP BY
        lsn.cid
),

activeStudents AS (
    SELECT
        enr.cid,
        enr.uid
    FROM
        enrollments enr
    WHERE
        role = 'Student'
        AND (end_ts IS NULL OR end_ts >= CURRENT_TIMESTAMP)
),

studentProgress AS (
    SELECT
        ast.cid,
        ast.uid,
        COUNT(cmp.lid) AS completed_lessons
    FROM activeStudents ast
    LEFT JOIN completion cmp ON ast.cid = cmp.cid AND ast.uid = cmp.uid
    GROUP BY
        ast.cid, ast.uid
),

courseAverage AS (
    SELECT
        ctf.cid,
        AVG(ctf.final_grade) AS average_final_grade
    FROM 
        certificates ctf
    GROUP BY 
        ctf.cid
)

SELECT
    crs.cid,
    crs.title,
    COUNT(sp.uid) AS active_enrollment,
    ROUND(
        IFNULL(
            SUM(
                CASE 
                    WHEN sp.completed_lessons >= acl.total_lessons AND acl.total_lessons > 0 THEN 1.0 
                    ELSE 0.0 
                END
            ) * 100.0 / NULLIF(COUNT(sp.uid), 0), 
        0), 
    2) AS completion_rate,
    ROUND(avg.average_final_grade, 2) AS average_final_grade
FROM 
    users usr,
    enrollments enr,
    courses crs
    LEFT JOIN allCourseLessons acl ON crs.cid = acl.cid
    LEFT JOIN studentProgress sp ON crs.cid = sp.cid
    LEFT JOIN courseAverage avg ON crs.cid = avg.cid
--condition that courses taught by the instructor only here
WHERE
    crs.cid = enr.cid
    AND usr.uid = enr.uid
    AND usr.role = 'Instructor' -- I dont think this is necessary but just in case
    AND enr.uid = 5 --CHANGE THE VARIABLE HERE ON PYTHON CODE!!!!!
GROUP BY
    crs.cid, crs.title, acl.total_lessons, avg.average_final_grade;
