import statistics
# import fuzzy_pandas
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process 
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
wks_class_list = SHEET.worksheet("class_list")

df = pd.DataFrame(wks_raw_data.get_all_records())
df2 = pd.DataFrame(wks_class_list.get_all_records())

def plot_points(row_number, grades_weighted):
    """
    After grades are converted to points this
    function places them in the 
    'grades_adjusted_and_final' worksheet.
    """
    for index in range(len(grades_weighted)):
        grade = grades_weighted[index]
        wks_adjusted.update_cell(row_number, index + 3, grade)   


def weighted_points(assignment, result):
    """
    Convert the list of percentages into weighted points 
    which will contribute to the final grade
    """
    weights = {
        "Homework": 0.05,
        "Quiz": 0.1,
        "Midterm": 0.20,
        "Final": 0.40,
    }
    assignment_points = result * weights[assignment]
    return assignment_points


def get_averages():
    """
    Gets and displays class averages for each
    assignment or exam
    """
    summary = df[["Date Entered", "Assignment", "Class Average"]].to_string(index = False)
    print(f"Class averages for previously entered grades:\n {summary}\n")
    options()

def get_student_records():
    """
    Allows the user to see results for 
    individual students
    """
    print("Here is your classlist:\n\n")
    student_num = (df2[["Number", "Students"]].to_string(index=False))
    print(student_num)
    user_choice = int(input("Choose a number: \n"))
    while user_choice > (len(df2["Students"])):
        user_choice = int(input("Choose a number: \n"))
    student = (df2["Students"][user_choice-1])
    print("Results:\n")
    result = df[["Assignment", student]].to_string(index=False)
    print(result)
    answer = input("Do you wish to view another student's records?")
    check_answer(answer)
    if answer in ("yes", "y"):
            get_student_records()
    elif answer in ("no", "n"):
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
        answer = input("Would you like to exit?\n")
        check_answer(answer)
        if answer in ("yes", "y"):
            print(f"""Thank you for using Grade Center.\n""")
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
    grades_weighted = []
    student_list = wks_raw_data.row_values(1)
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
                student_points = """The student score must not exceed total possible score.Please re-enter student score:\n"""
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
        grade_to_points = weighted_points(assignment, result)
        print(f"{num2}/{num1} is {result}%")
        print(f"This assignment contributes {grade_to_points} towards the final grade.")
        grades.append(result)
        grades_weighted.append(grade_to_points)
    print("Updating spreadsheet and calculating class average, please wait...")
    grades_only = grades[2:]
    for index in range(len(grades)):
        grade = grades[index]
        wks_raw_data.update_cell(row_number, index + 1, grade)
    class_ave = int(statistics.mean(grades_only))
    print(f"The class average for {assignment} was {class_ave}%\n")
    wks_raw_data.update_cell(row_number, 13, class_ave)
    plot_points(row_number, grades_weighted)
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
    option3 = "3. View class averages"
    option4 = "4. Quit"

    print(f"""Please select from the following options:\n
    {option1}\n 
    {option2}\n
    {option3}\n
    {option4}\n""")
    selection = "Choose by entering the number.\n"
    option = check_int(selection)
    if option == 1:
        check_if_due()
    elif option == 2:
        get_student_records()
    elif option == 3:
        get_averages()
    elif option == 4:
        end_program()
    else:
        print(f"{option} is not a valid response")
        end_program()

def main():
    """
    Run's the programs main functions
    """
    options()

instructions = ("""Welcome to Grade Center.\n""")
print(instructions)
main()
