import sqlite3



"""
============================= HELPER FUNCTIONS START =============================

"""
def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
  
def isCourseTaught(instrUID, cid, conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            enr.cid, 
            enr.uid
        FROM    
            enrollments enr
        WHERE 
            enr.uid = ?
            AND enr.cid = ?
            AND enr.end_ts > CURRENT_TIMESTAMP; 
    """, (instrUID, cid))

    result = cursor.fetchone()
    cursor.close()

    if result is None:
        return False
    return True

def courseExists(cid, conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            crs.cid
        FROM
            courses crs
        WHERE
            crs.cid = ?;
    """, (cid,))

    result = cursor.fetchone()
    cursor.close()

    if result is None:
        return False
    return True

def studentExists(uid, conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            usr.uid
        FROM
            users usr
        WHERE
            usr.role = 'Student'
            AND usr.uid = ?;
    """, (uid,))

    result = cursor.fetchone()
    cursor.close()

    if result is None:
        return False
    return True

def studentEnrolled(uid, cid, conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            enr.uid,
            enr.cid
        FROM
            enrollments enr
        WHERE
            enr.uid = ?
            AND enr.cid = ?
            AND enr.end_ts > CURRENT_TIMESTAMP;
    """, (uid, cid))

    result = cursor.fetchone()
    cursor.close()

    if result is None:
        return False
    return True

"""
============================= HELPER FUNCTIONS END =============================

"""



# initial loop (the whole instructor functions setup)
def menu(instrUID, conn):
    while True:
        print("\n-----------Instructor Menu-----------")
        print("\nEnter the number to choose an option\n")
        print("1. Update Course\n2. Override Enrollment\n3. Course Stats\n4. Log Out")
        print("\n-----------Instructor Menu-----------")
        
        usrInput = input("Number: ")
        # check if input is an integer or not
        if not usrInput.isdigit():
            print("\nInvalid option, try again!\n")
            continue # next loop

        else:
            option = int(usrInput)
            match option:
                case 1:
                    updateCourse(instrUID, conn)
                case 2:  
                    overrideEnrollment(instrUID, conn)
                case 3:    
                    courseStats(instrUID, conn)
                case 4: # MAKE THIS INTO LOG OUT??
                    break
                case _:
                    print("\nInvalid option, try again!")

def updateCourse(instrUID, conn):
    print("---------Update Course Info---------\n")
    print("Enter the key 'e' anytime we ask for input to exit\n")
    print("---------Update Course Info---------\n")

    cursor = conn.cursor()

    EXIT = False
    while True:
        # important variables
        cid = 0
        price = 0
        passGrade = 0
        maxStudents = 0
        removedCount = 0
        addedCount = 0

        # Get course id (NEEDED)
        # TODO make sure value is > 0???
        while True:
            print("Enter the course ID (cid) to update")
            cidInput = input("cid: ")
            # check if exit key has been inputted
            if cidInput == "e":
                EXIT = True
                break 
            elif not cidInput.isdigit():
                print("\nInvalid input, try again!\n")
                continue 
            # input is valid and convert it to appropriate type
            else:
                cid = int(cidInput)
                break
        
        # check exit
        if EXIT:
            break

        # Check if course exists
        if not courseExists(cid, conn):
            print("Entered course does not exist, try again!\n")
            continue

        # Check if course exist but is not taught by the Instructor
        if not isCourseTaught(instrUID, cid, conn):
            print("Entered course is not taught by you, try again!\n")
            continue


        # Get value for price (allowed to skip)
        while True:
            print("Enter the new price")
            print("Enter the key 'c' to skip this option")
            priceInput = input("price: ")
            # check exit again
            if priceInput == "e":
                EXIT = True
                break
            elif priceInput == "c":
                price = priceInput
                break
            elif not isFloat(priceInput):
                print("\nInvalid input, try again!\n")
                continue 
            # input is valid and convert to float
            else:
                price = float(priceInput)
                if price < 0:
                    print("\nPrice cannot be negative, try again!\n")
                    continue
                break
        
        # check exit
        if EXIT:
            break

        # Get value for pass_grade(allowed to skip)
        #TODO make sure the entered value is > 0
        while True:
            print("Enter the new pass_grade")
            print("Enter the key 'c' to skip this option")
            passGradeInput = input("pass_grade: ")
            # check exit again
            if passGradeInput == "e":
                EXIT = True
                break
            elif passGradeInput == "c":
                passGrade = passGradeInput
                break
            elif not isFloat(passGradeInput):
                print("\nInvalid input, try again!\n")
                continue # go back to start
            # convert to float
            else:
                passGrade = float(passGradeInput)
                break
        
        # check exit
        if EXIT:
            break

        # Get value for max_students (allowed to skip)
        while True:
            print("Enter the new max_students")
            print("Enter the key 'c' to skip this option")
            maxStudentsInput = input("max_students: ")
            # check exit again
            if maxStudentsInput == "e":
                EXIT = True
                break 
            elif maxStudentsInput == "c":
                maxStudents = maxStudentsInput
                break
            elif not maxStudentsInput.isdigit():
                print("\nInvalid option, try again!\n")
                continue # go back to start
            # convert to int
            else:
                maxStudents = int(maxStudentsInput)
                break
        # check exit
        if EXIT:
            break

        """

        At this point, gather all the valid parameters (if input value is 'c' skip it)
        and do the database task. display ('cid', 'title', 'category', 'price', etc...)
        
        Then, update the tables if pass_grade has been modified. use python count to count
        how many students were removed and how many were added!
        """
        # UPDATE COURSE VALUES HERE
        if price != 'c':
            cursor.execute("""
                UPDATE
                    courses 
                SET 
                    price = ?
                WHERE
                    cid = ?; 
            """, (price, cid))

            conn.commit()

        if passGrade != 'c':
            cursor.execute("""
                UPDATE
                    courses 
                SET 
                    pass_grade = ?
                WHERE
                    cid = ?; 
            """, (passGrade, cid))

            conn.commit()

        if maxStudents != 'c':
            cursor.execute("""
                UPDATE
                    courses 
                SET 
                    max_students = ?
                WHERE
                    cid = ?; 
            """, (maxStudents, cid))

            conn.commit()
    

        # UPDATE CERTIFICATES TABLE FOR INELIGIBLE STUDENTS HERE (only if there a valid passGrade value)
        if passGrade != 'c':
            cursor.execute("""
                DELETE FROM 
                    certificates
                WHERE
                    cid = ?
                    AND final_grade < (SELECT crs.pass_grade FROM courses crs WHERE crs.cid = ?);
            """, (cid, cid))

            removedCount = cursor.rowcount

        # GET ELIGIBLE STUDENTS HERE
        cursor.execute("""
            WITH courseModules AS (
                SELECT 
                    mdl.cid,
                    count(DISTINCT mdl.mid) AS total_modules
                FROM
                    modules mdl
                GROUP BY
                    mdl.cid
            ),

            studentFinalGrade AS (
                SELECT 
                    grd.uid,
                    ROUND((SUM(grd.grade * mdl.weight) / SUM(mdl.weight)), 2) AS final_grade
                FROM
                    modules mdl,
                    grades grd
                WHERE
                    mdl.cid = grd.cid
                    AND mdl.mid = grd.mid
                GROUP BY
                    grd.uid
            ),

            courseCompletionDeadline AS (
                SELECT
                    enr.cid AS cid,
                    enr.uid AS uid,
                    enr.end_ts AS end_ts
                FROM
                    enrollments enr
                WHERE
                    enr.role = 'Student'

            ),

            eligibleStudents AS ( 
                SELECT -- These are the list of students that need to be added to certificates
                    grd.cid,
                    grd.uid,
                    COUNT(DISTINCT grd.mid) AS completed_modules,
                    cm.total_modules,
                    sfg.final_grade AS final_grade
                FROM
                    grades grd,
                    courseCompletionDeadline ccd,
                    courseModules cm,
                    studentFinalGrade sfg,
                    courses crs
                -- WHERE makes sure to consider only students who completed all modules within the allocated time (end_ts
                WHERE
                    grd.cid = ccd.cid
                    AND grd.cid = crs.cid
                    AND cm.cid = grd.cid
                    AND grd.uid = ccd.uid 
                    AND grd.uid = sfg.uid
                    AND grd.received_ts < ccd.end_ts
                GROUP BY
                    grd.uid
                HAVING
                    completed_modules >= cm.total_modules
                    AND final_grade >= crs.pass_grade
            )

            SELECT --Main Source
                es.cid,
                es.uid,
                es.final_grade
            FROM
                eligibleStudents es
            WHERE
                es.cid = ?
                AND (es.cid, es.uid) NOT IN (SELECT cid, uid FROM certificates); -- Makes sure it only returns student not having a certificate
                                
        """, (cid,))

        eligibleStudents = cursor.fetchall()
        addedCount = len(eligibleStudents)

        # UPDATE CERTIFICATES TABLE FOR ELIGIBLE STUDENTS HERE
        for student in eligibleStudents:
            cursor.execute("""
                INSERT INTO certificates VALUES
                    (?, ?, CURRENT_TIMESTAMP, ?);
            """, (student[0], student[1], student[2]))
            conn.commit()
        
        # PRINT RESULT
        cursor.execute("""
            SELECT
                cid,
                price,
                pass_grade,
                max_students
            FROM
                courses
            WHERE
                cid = ?
        """, (cid,))

        course = cursor.fetchone()
        result = (course[0], course[1], course[2], course[3], addedCount, removedCount)

        print("\n--------------------- RESULT ---------------------\n")
        print(result)
        print("\n--------------------- RESULT ---------------------\n")

        while True:
            print("Enter the key 'c' to update another course")
            print("Enter the key 'e' to exit")
            key = input("key: ")
            if key == "e":
                EXIT = True
                break
            elif key == "c":
                break
            #input invalid
            else:
                print("\nInvalid input, try again!\n")
                continue
        
        # check exit
        if EXIT:
            break

    cursor.close()

def overrideEnrollment(instrUID, conn):
    print("---------Override Enrollment Info---------\n")
    print("Enter the key 'e' anytime we ask for input to exit\n")
    print("---------Override Enrollment Info---------\n")

    cursor = conn.cursor()

    EXIT = False
    while True:
        cid = 0
        uid = 0
        # get cid
        while True:
            print("Enter the course cid you want the student to add to")
            cidInput = input("cid: ")
            # check if exit key has been inputted
            if cidInput == "e":
                EXIT = True
                break 
            elif not cidInput.isdigit():
                print("\nInvalid input, try again!\n")
                continue 
            # input is valid and convert it to appropriate type
            else:
                cid = int(cidInput)
                break

        if EXIT:
            break

        
        # Check if course exists
        if not courseExists(cid, conn):
            print("Entered course does not exist, try again!\n")
            continue

        # Check if course exist but is not taught by the Instructor
        if not isCourseTaught(instrUID, cid, conn):
            print("Entered course is not taught by you, try again!\n")
            continue

        """
        If both conditions weren't activated, that means the cid is valid
        and it is taught by the logged in instructor
        """

        # get student uid
        while True:
            print("Enter the student uid you want to add")
            uidInput = input("uid: ")
            if uidInput == "e":
                EXIT = True
                break
            elif not uidInput.isdigit():
                print("\nInvalid input, try again!\n")
                continue
            # input is a valid integer
            else:
                """
                Here is where we check if the entered uid
                exists in users and is a student. 

                Then check if uid is already in enrollment at the given course
                """
                uid = int(uidInput)

                if not studentExists(uid, conn):
                    print("Entered Student does not exist, try again!\n")
                    continue
                elif studentEnrolled(uid, cid, conn):
                    print("Student is already enrolled, try again\n")
                    continue
                else:
                    break
        
        if EXIT:
            break

        """
        If we got at this point, we have a valid student uid
        and they are not added to the enrollment table yet.

        we do the update table beyond this point
        we also update the payment table aswell
        """
        # Inserting the student into Enrollments
        cursor.execute("""
            INSERT INTO enrollments VALUES
                (?, ?, CURRENT_TIMESTAMP, datetime('now', '+1 year'), 'Student');
            """, (cid, uid))

        conn.commit()

        # Inserting Payment Row
        cursor.execute("""
            INSERT INTO payments VALUES
                (?, ?, CURRENT_TIMESTAMP, '0000000000000000', '12/2026');
        """, (uid, cid))

        conn.commit()

        # Print result
        cursor.execute("""
            SELECT
                enr.cid,
                crs.title AS course_title,
                enr.uid,
                usr.name AS student_name,
                enr.start_ts
            FROM
                enrollments enr, courses crs, users usr
            WHERE
                usr.role = 'Student'
                AND usr.uid = enr.uid
                AND enr.cid = crs.cid
                AND enr.uid = ?
                AND enr.cid = ?;
        """, (uid, cid))

        result = cursor.fetchone()
        print("\n--------------------- RESULT ---------------------\n")
        print(result)
        print("\n--------------------- RESULT ---------------------\n")

        # end of the function (ask whether to continue or exit)
        while True:
            print("Enter the key 'c' to add another student to a specified course")
            print("Enter the key 'e' to exit")
            key = input("key: ")
            if key == "e":
                EXIT = True
                break
            elif key == "c":
                break
            #input invalid
            else:
                print("\nInvalid input, try again!\n")
                continue
        
        # check exit
        if EXIT:
            break

    cursor.close()

"""
This function displays the course stats:

('cid', 'title', 'active_enrollment', 'completion_rate', 'average_final_grade') 

From the provided instructor uid teaches

Parameters
----------
    instrUID : int
        Instructor uid 
    cursor : sqlite3.Cursor
        sqlite3 cursor for query execution use

Returns
-------
    None
"""       
def courseStats(instrUID, conn):

    cursor = conn.cursor()

    EXIT = False
    while True:
        
        cursor.execute("""
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
                AND enr.uid = ? -- POSITIONAL VAL HERE
            GROUP BY
                crs.cid, crs.title, acl.total_lessons, avg.average_final_grade;
        """, (instrUID,))

        results = cursor.fetchall()

        print("\n--------------- Course Stats ---------------\n")
        for row in results:
            print(row)
        print("\n--------------- Course Stats ---------------\n")

        # End of the function (ask whether to continue or exit)
        while True:
            print("Enter the key 'e' to exit")
            key = input("key: ")
            if key == "e":
                EXIT = True
                break
            #input invalid
            else:
                print("\nInvalid input, try again!\n")
                continue
        
        # check exit
        if EXIT:
            break

    cursor.close()

if __name__ == "__main__":
    menu()
 
