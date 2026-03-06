"""
Helper functions start

"""
def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
"""
Helper functions end

"""
# initial loop (the whole instructor functions setup)
def menu():
    while True:
        print("-----------Instructor Menu-----------")
        print("\nEnter the number to choose an option\n")
        print("1. Update Course\n2. Override Enrollment\n3. Course Stats\n4. Exit")
        print("-----------Instructor Menu-----------")
        
        usrInput = input("Number: ")
        # check if input is an integer or not
        if not usrInput.isdigit():
            print("\nInvalid option, try again!\n")
            continue # next loop

        else:
            option = int(usrInput)
            match option:
                case 1:
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    updateCourse()
                case 2:
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    overrideEnrollment()
                case 3:
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    courseStats()
                case 4:
                    break
                case _:
                    print("\nInvalid option, try again!\n")

def updateCourse():
    print("---------Update Course Info---------\n")
    print("Enter the key 'e' anytime we ask for input to exit\n")
    print("---------Update Course Info---------\n")

    EXIT = False
    while True:
        # important variables
        cid = 0
        price = 0
        passGrade = 0
        maxStudents = 0

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

        """
        At this point, check if the entered course id is indeed valid
        and course is taught by the logged in instructor. Doing a simple
        print statement to fill this part.

        PSEUDO:
        if cid not in courses table:
            cid entered does not exist, try again
            continue
            
        if (cid in courses table) and not (cid is taught by prof):
            course is valid but not taught by you!, try again
            continue
            
        if (cid in courses table) and (cid is taught by prof):
            course is valid!
        """
        # filler
        print("Entered cid has been validated and is taught by you!")

        # Get value for price (allowed to skip)
        # TODO make sure that the entered value is > 0
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
                price = float(passGradeInput)
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
        # filler code (update when ready to implement)
        print("gathered values: ", cid, price, passGrade, maxStudents)
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

def overrideEnrollment():
    print("---------Override Enrollment Info---------\n")
    print("Enter the key 'e' anytime we ask for input to exit\n")
    print("---------Override Enrollment Info---------\n")
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
        """
        At this point, check if the entered course id is indeed valid
        and course is taught by the logged in instructor. Doing a simple
        print statement to fill this part.

        PSEUDO:
        if cid not in courses table:
            cid entered does not exist, try again
            continue
            
        if (cid in courses table) and not (cid is taught by prof):
            course is valid but not taught by you!, try again
            continue
            
        if (cid in courses table) and (cid is taught by prof):
            course is valid!
        """
        # filler
        print("Entered cid has been validated and is taught by you!")

        if EXIT:
            break

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

                If in enrollment, print a message and break loop.
                Then restart the main while loop (via continue) 
                and provide an option to try again.

                eg.

                if uid not in users table:
                    given student uid does not exist, try again

                if uid in enrollment table:
                    student uid already enrolled in course, try again
                
                """
                #filler
                print("Student is valid and not in Enrollment yet!")
                uid = int(uidInput)
                break
        
        if EXIT:
            break

        """
        If we got at this point, we have a valid student uid
        and they are not added to the enrollment table yet.

        we do the update table beyond this point
        we also update the payment table aswell
        """
        #filler
        print("Updates were successful. Here are the given values: ", cid, uid)

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
        
def courseStats():
    print("---------Course Stats Info---------\n")
    print("Enter the key 'e' anytime we ask for input to exit\n")
    print("---------Course Stats Info---------\n")
    #filler
    EXIT = False
    while True:
        """
        This function mostly uses the queries so theres little python code here
        """
        print("Stats displayed!")

        # end of the function (ask whether to continue or exit)
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


if __name__ == "__main__":
    menu()
 
