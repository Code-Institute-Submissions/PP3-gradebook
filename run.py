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
wks_class_ave = SHEET.worksheet("target_averages")
wks_adjusted = SHEET.worksheet("grades_adjusted_and_final")
wks_advising = SHEET.worksheet("final_result_needed")

def find_percent(num1, num2):

    result = (num1/num2)*100
    return round(result)


def end_program():
    print("end")
def get_grades():
    """
    Tells the user for which assignment they are entering grades,
    and requests the grades by user.
    """
    #Get the first assignment for which grades need to be entered
    start_col = [item for item in wks_raw_data.col_values(1) if item]
    index = start_col.index("due")
    assignment = wks_raw_data.cell(index + 1, 2).value
    wks_raw_data.update_cell(index+1, 1, "=TODAY()")

    #Get grades from user. User enters total points and 
    #a percentage is calculated.
    grades = []
    student_list = wks_raw_data.row_values(1)
    print(f"Accepting grades for {assignment}")
    while True:
        try:
            points_possible = float(input("What were the total possible points?\n"))
            break
        except ValueError:
            print("Please enter a valid number.")
    for student in student_list[2:]:
        while True:
            try:
                student_points = float(input(f"Enter points achieved for {student}\n"))
                break
            except ValueError:
                print("Please enter a valid number.")
        while student_points > points_possible:
            student_points = float(input("The student score is greater than " +
                            "possible points, please re-enter"))
        result = find_percent(student_points, points_possible)
        print(f"This is a {result}% for {student}")
        grades.append(result)
    return grades

def check_if_due():
    start_col = [item for item in wks_raw_data.col_values(1) if item]
    while True: 
        try:
            index = start_col.index("due")
            get_grades()
            break
        except ValueError:
            print("All grades have already been entered.")
            break
    

def main():
    check_if_due()
    end_program()

# instructions = ("""You will be prompted to enter grades for each student for
# the next homework or exam due.\n
# After each grade, please confirm if the grade you entered is correct.
# If you enter an incorrect grade, you will have the chance to enter it again.
# After all the grades are entered, you will be given the class average, and 
# and you will be asked if you would like to add a curve to the results.\n
# The orinal scores and adjusted grades will be added to the spreadsheet on 
# separate sheets. Students scores will be averaged, with and calculations will be
# made for what the student needs to gain a pass, reach the class average
# or acheive an A.""")
# print(instructions)
main()