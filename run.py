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
wks_class_list = SHEET.worksheet("class_list")

df = pd.DataFrame(wks_raw_data.get_all_records())
df2 = pd.DataFrame(wks_class_list.get_all_records())
df3 = pd.DataFrame(wks_adjusted.get_all_records())
df4 = pd.DataFrame(wks_advising.get_all_records())


def check_int(num):
    """
    Checks user input is an integer.
    If it isn't, it prompts the user
    for a valid number.
    """
    while True:
        try:
            num = int(input(num))
            return num
        except ValueError:
            print("Please enter a valid integer.\n")


def check_answer(answer):
    """
    Checks the user has entered a valid
    yes/no response.
    """
    answer = answer.lower()
    while answer not in ("yes", "y", "no", "n"):
        answer = input("Please answer yes/y or no/n.\n")
    return answer


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
    assignment_points = round(result * weights[assignment], 2)
    return assignment_points


def get_averages():
    """
    Gets and displays class averages for each
    assignment or exam
    """
    df = pd.DataFrame(wks_raw_data.get_all_records())
    summary = df[["Date Entered",
                  "Assignment",
                  "Class Average"]].to_string(index=False)
    print(f"Class averages for previously entered grades:\n {summary}\n")
    main()


def records_input():
    num = check_int("\nSelect student by roster number: \n")
    while num > (len(df2["Students"])):
        num = int(input("Choose a number: \n"))
    return num


def get_student_records():
    """
    Allows the user to see results for
    individual students
    """
    df = pd.DataFrame(wks_raw_data.get_all_records())
    df2 = pd.DataFrame(wks_class_list.get_all_records())
    df4 = pd.DataFrame(wks_advising.get_all_records())
    print("Here is your classlist:\n")
    student_num = (df2[["Number", "Students"]].to_string(index=False))
    print(student_num)
    user_choice = records_input()
    student = (df2["Students"][user_choice-1])
    print("Results:\n")
    result = df[["Assignment", student]].to_string(index=False)
    print(result)
    print("\nAdvising results")
    print("Future averages needed for end of term grade.\n")
    advising_result = df4[["Grade", student]].to_string(index=False)
    print(advising_result)
    answer = input("\nDo you wish to view another student's records?\n")
    answer = check_answer(answer)
    if answer in ("yes", "y"):
        get_student_records()
    elif answer in ("no", "n"):
        main()


def find_percent(num1, num2):
    """
    Calculates student score as a percent
    """
    result = int((num1/num2)*100)
    result = round(result, 2)
    return round(result, 2)


def end_program():
    """
    Ends to program if teacher does
    not want to enter more results.
    """
    answer = input("Would you like to exit?\n")
    answer = check_answer(answer)
    if answer in ("yes", "y"):
        print("Thank you for using Grade Center.\n")
    if answer in ("no", "n"):
        main()


def get_num1():
    """
    Gets the total number of points for a test
    or assignment, checks if it's an integer and
    allows the user to re-enter a number if they
    entered the wrong one.
    """
    confirm_points = ""
    while confirm_points == "":
        points_possible = "What as the total possible score?\n"
        num1 = check_int(points_possible)
        print(f"You entered {num1}. Is this correct?")
        points_validation = input("Respond with yes/y or no/n.\n")
        confirm_points = check_answer(points_validation)
        if confirm_points in ("no", "n"):
            confirm_points = ""
        elif confirm_points in ("yes", "y"):
            confirm_points = points_validation
        else:
            confirm_points = ""
    return num1


def calc_points_needed():
    """
    While grades are incomplete, it tells the user
    what the student needs to achive an A, B, C or D.
    When grades are complete, it gives a final term
    grade and converts the result.
    """
    # Create dictionary for grade values
    letter_grades = {
        "A": 94,
        "B": 83,
        "C": 77,
        "D": 67,
        "Pass": 60,
    }

    # names = Get the list of student names to iterate through
    students = wks_advising.row_values(1)
    student_list = students[1:]
    num_students = len(student_list)
    # Get the points for the student - need to create values variable
    num = 3
    for student in student_list:
        s_sco_earn = [item for item in wks_adjusted.col_values(num)if item][1:]
        # Convert list to floats
        s_sco_earn = [float(item) for item in s_sco_earn]
        # Get the list of weights and convert into floats
        wts_list = [item for item in wks_adjusted.col_values(2) if item][1:]
        wts_list = [float(item) for item in wts_list]
        # Get the sum of all the weights
        # total_points_possible = sum(wts_list)
        # Slice using the length of the student scores earned
        length = len(s_sco_earn)
        weights_used = wts_list[0:length]
        weights_to_be_used = wts_list[length:]
        # Add calcuations
        sum1_scores = sum(s_sco_earn)
        sum2_weights = sum(weights_used)
        sum3_weights = sum(weights_to_be_used)
        current_average = int((sum1_scores/sum2_weights)*100)
        list_averages = []
        row = 2
        for key in letter_grades:
            col = num-1
            ave_nd = int(((letter_grades[key] - sum1_scores)/sum3_weights)*100)
            if ave_nd > 100:
                message = "Not possible"
            else:
                message = ave_nd
            list_averages.append(message)
            wks_advising.update_cell(row, col, message)
            row += 1
        num += 1


def check_final_grade(assignment):
    columns = [3, 4, 5, 6, 7]
    letter_grade = ""
    if assignment == "Final":
        for col in columns:
            sc_lt = [item for item in wks_adjusted.col_values(col) if item][1:]
            scores = round(sum([float(item) for item in sc_lt]))
            wks_adjusted.update_cell(10, col, scores)
            if scores > 93:
                letter_grade = "A"
            elif scores > 82:
                letter_grade = "B"
            elif scores > 76:
                letter_grade = "C"
            elif scores > 66:
                letter_grade = "D"
            elif scores > 59:
                letter_grade = "Pass"
            else:
                letter_grade = "Fail"
            wks_adjusted.update_cell(11, col, letter_grade)
            wks_raw_data.update_cell(10, col, letter_grade)
        main()
    else:
        calc_points_needed()
        main()


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
                student_points = f"Enter a score up to {num1}:\n"
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
        print(f"This adds {grade_to_points} points to the term grade.\n")
        grades.append(result)
        grades_weighted.append(grade_to_points)
    print("Updating sheets and calculating class average")
    print("Please wait...")
    grades_only = grades[2:]
    for index in range(len(grades)):
        grade = grades[index]
        wks_raw_data.update_cell(row_number, index + 1, grade)
    class_ave = int(statistics.mean(grades_only))
    print(f"The class average for {assignment} was {class_ave}%\n")
    print("Calcuating points from waited grades.\n")
    print("Calcuating advising grades.\n")
    print("Please wait for Options Menu.\n")

    wks_raw_data.update_cell(row_number, 8, class_ave)
    plot_points(row_number, grades_weighted)
    check_final_grade(assignment)


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
            main()
            break


def main():
    """
    Run's the programs main functions
    """
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
    # else:
    #     print(f"{option} is not a valid response")
    #     end_program()


instructions = ("""Welcome to Grade Center.\n""")
print(instructions)
main()
