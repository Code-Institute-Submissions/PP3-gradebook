import gspread
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

def main():
    print("The program is starting")


instructions = ("""You will be prompted to enter grades for each student for
the next homework or exam due.\n
After each grade, please confirm if the grade you entered is correct.
If you enter an incorrect grade, you will have the chance to enter it again.
After all the grades are entered, you will be given the class average, and 
and you will be asked if you would like to add a curve to the results.\n
The orinal scores and adjusted grades will be added to the spreadsheet on 
separate sheets. Students scores will be averaged, with and calculations will be
made for what the student needs to gain a pass, reach the class average
or acheive an A.""")
print(instructions)
main()