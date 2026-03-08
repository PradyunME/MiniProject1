import sys

from db import get_connection
from auth import login, register
from instructor import menu as instructor_menu
from student import menu as student_menu
from admin import menu as admin_menu


def login_screen(conn):
    while True:
        print("\n----------------------------------------------")
        print("      Welcome to the Learning Platform  ")
        print("----------------------------------------------")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        print("========================================")

        choice = input("Choose an option (1-3): ").strip()

        if choice == '1':
            result = login(conn)
            if result is not None:
                return result
        elif choice == '2':
            result = register(conn)
            if result is not None:
                return result
        elif choice == '3':
            conn.close()
            sys.exit(0)
        else:
            print("\nInvalid option. Please enter 1, 2, or 3.")


def main():
    conn = get_connection()

    while True:
        uid, role = login_screen(conn)

        if role == 'Student':
            student_menu(uid, conn)
        elif role == 'Instructor':
            instructor_menu(uid, conn)
        elif role == 'Admin':
            admin_menu(uid, conn)
        else:
            print(f"Unknown role '{role}'. Contact an administrator.")


if __name__ == "__main__":
    main()
