#!/usr/bin/env python3
"""
Main Program - Account Management System
Converted from COBOL MainProgram (main.cob)
"""

import sys
from operations import Operations


class MainProgram:
    """Main program class handling user interface and menu navigation"""

    def __init__(self):
        """Initialize the main program"""
        self.user_choice = 0
        self.continue_flag = True
        self.operations = Operations()

    def display_menu(self):
        """Display the main menu to the user"""
        print("--------------------------------")
        print("Account Management System")
        print("1. View Balance")
        print("2. Credit Account")
        print("3. Debit Account")
        print("4. Exit")
        print("--------------------------------")

    def get_user_choice(self):
        """Get and validate user input for menu choice"""
        try:
            choice = input("Enter your choice (1-4): ")
            return int(choice)
        except ValueError:
            return 0  # Invalid choice will be handled in main loop

    def process_choice(self, choice):
        """Process the user's menu choice"""
        if choice == 1:
            # View Balance - equivalent to CALL 'Operations' USING 'TOTAL '
            self.operations.execute_operation("TOTAL ")

        elif choice == 2:
            # Credit Account - equivalent to CALL 'Operations' USING 'CREDIT'
            self.operations.execute_operation("CREDIT")

        elif choice == 3:
            # Debit Account - equivalent to CALL 'Operations' USING 'DEBIT '
            self.operations.execute_operation("DEBIT ")

        elif choice == 4:
            # Exit - equivalent to MOVE 'NO' TO CONTINUE-FLAG
            self.continue_flag = False

        else:
            # Invalid choice - equivalent to WHEN OTHER
            print("Invalid choice, please select 1-4.")

    def run(self):
        """Main execution loop - equivalent to MAIN-LOGIC paragraph"""
        # PERFORM UNTIL CONTINUE-FLAG = 'NO'
        while self.continue_flag:
            self.display_menu()
            user_choice = self.get_user_choice()
            self.process_choice(user_choice)

        # Exit message - equivalent to DISPLAY "Exiting the program. Goodbye!"
        print("Exiting the program. Goodbye!")


def main():
    """Entry point - equivalent to COBOL program execution"""
    try:
        main_program = MainProgram()
        main_program.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Equivalent to COBOL program start
    main()
