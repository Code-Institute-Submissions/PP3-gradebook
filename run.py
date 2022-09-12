import statistics

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('gradebook')

wks_raw_data = SHEET.worksheet("grades_raw")
wks_adjusted = SHEET.worksheet("grades_adjusted_and_final")
wks_advising = SHEET.worksheet("final_result_needed")

df = pd.DataFrame(wks_raw_data.get_all_records())

def get_student_records():
    print(df.iloc[0, 3:-1
    ])
    name  = input("Enter student's name:")
    student = df[["Assignment", name]]
    print(student)
    options()


def find_percent(num1, num2):
    """
    Calculates student score as a percent
    """
    result = (num1/num2)*100
    return round(result)


def end_program():
    """
    Ends to program if teacher does
    not want to enter more results.
    """
    answer = ""
    while answer == "":
        answer = input("Do you really want to exit?\n")
        check_answer(answer)
        if answer in ("yes", "y"):
            print(f"""Thank you for using grade center.\n""")
        if answer in ("no", "n"):
            options()


def check_int(points):
    """
    Checks user input is an integer.
    If it isn't, it prompts the user
    for a valid number.
    """
    while True:
        try:
            points = float(input(points))
            return points
        except ValueError:
            print("Please enter a valid number.")


def check_answer(answer):
    """
    Checks the user has entered a valid
    yes/no response.
    """
    answer = answer.lower()
    while answer not in ("yes", "y", "no", "n"):
        answer = input("Please answer yes/y or no/n.\n")
    return answer


def get_num1():
    """
    Gets the total number of points for a test
    or assignment, checks if it's an integer and
    allows the user to re-enter a number if they
    entered the wrong one.
    """
    confirm_points = ""
    while confirm_points == "":
        points_possible = "Please enter the highest possible score?\n"
        num1 = check_int(points_possible)
        print(f"You entered {num1}. Is this correct?")
        points_validation = input("Enter yes/y to continue or no/n to re-enter.\n")
        confirm_points = check_answer(points_validation)
        if confirm_points in ("no", "n"):
            confirm_points = ""
        elif confirm_points in ("yes", "y"):
            confirm_points = points_validation
        else:
            confirm_points = ""
    return num1


def get_grades():
    """
    Requests total score value of test or assignment, the
    student scores, then inserts the calculated percent
    into a Google Sheet with the class average.
    """
    # Get the first assignment for which grades need to be entered
    start_col = [item for item in wks_raw_data.col_values(1) if item]
    index = start_col.index("due")
    assignment = wks_raw_data.cell(index + 1, 2).value
    wks_raw_data.update_cell(index+1, 1, "=TODAY()")

    # Get grades from user. User enters total points and
    # a percentage is calculated.
    grades = []
    student_list = wks_raw_data.row_values(1)
    # row_length = len(student_list)
    row_number = index + 1
    row_values = wks_raw_data.row_values(row_number)
    grades = row_values
    print(f"Accepting grades for {assignment}\n")
    num1 = get_num1()
    for student in student_list[2:-1]:
        confirm = ""
        while confirm == "":
            student_points = "Enter score achieved for " + student + "\n"
            num2 = check_int(student_points)
            while num2 > num1:
                student_points = """The student score must not exceed total possible score.
                Please re-enter student score:\n"""
                num2 = check_int(student_points)
            print(f"You entered {num2}. ")
            sscore_validation = input("Is this correct?\n")
            confirm = check_answer(sscore_validation)
            if confirm in ("no", "n"):
                confirm = ""
            elif confirm in ("yes", "y"):
                confirm = sscore_validation
            else:
                confirm = ""
        result = find_percent(num2, num1)
        print(f"{num2}/{num1} is {result}%")
        grades.append(result)
    grades_only = grades[2:]
    for index in range(len(grades)):
        grade = grades[index]
        wks_raw_data.update_cell(row_number, index + 1, grade)
    print("Calculating class average, please wait...")
    class_ave = int(statistics.mean(grades_only))
    print(f"The class average for {assignment} was {class_ave}%\n")
    wks_raw_data.update_cell(row_number, 13, class_ave)
    options()


def check_if_due():
    """
    Finds the first row where grades are due and
    calls the get_grades function so the user can
    enter the grades.
    """
    start_col = [item for item in wks_raw_data.col_values(1) if item]
    while True:
        try:
            index = start_col.index("due")
            get_grades()
            break
        except ValueError:
            print("All grades have already been entered.")
            break


def options():
    option1 = "1. Enter grades"
    option2 = "2. View individual student results"
    option3 = "3. View individual assignment results"
    option4 = "4. View class averages"
    option5 = "5. Quit"

    print(f"""You have the following options:\n
    {option1}\n 
    {option2}\n
    {option3}\n
    {option4}\n
    {option5}\n""")
    selection = "Choose by entering the number."
    option = check_int(selection)
    print(f"You chose option {option}")
    if option == 1:
        check_if_due()
    elif option == 2:
        get_student_records()
    elif option == 5:
        end_program()
    else:
        print("The options 2-4 aren't ready yet")
        end_program()

def main():
    """
    Run's the programs main functions
    """
    summary = df[["Date Entered", "Assignment", "Class Average"]]
    print(f"Previously entered grades and class averages:\n {summary}\n")
    options()



instructions = ("""Welcome to Grade Center\n
Below is a table with results you have already entered.\n""")
print(instructions)
main()