# Grade Center
This Grade Center program is a tool to help teachers and professors keep track of student grading and results. It supports teachers to advise students by performing a calculation that shows what average a student needs to maintain to achieve an A through a Pass. It works by accessing a Google spreadsheet and using, manipulationg and adding information to it. 

You can view the live project [here](https://ci-pp33-gradebook.herokuapp.com/).

This project was choosen, because I have been working in higher education for study abroad programs for a number of years. They are often cut off from the more advanced systems of attendance and grading available on their home campuses, and they must resort to old-fashioned, time-consuming methods.

For this program to work the following Google sheets need to be set up:
- A roster/class list, which is a numbered list of students in the class.
- A worksheet for the "raw data". This is where unweighted results are stored as percentages. The user is asked how many points an exam or assignment was worth, and then asks for the score for each student. For example, if a student scores 20 points of 20 possible points, the grade recorded on the spreadsheet is 100.
- A worksheet for the adjusted and final results. This contains a tally of weighted points for each assignment. For example, for example if a student got a 100% result on a final exam worth 40% of the overall score, the grade with be worth 40 points of the overall term grade. These points are calcuated and plotted once the user enters the grades. 
- A worksheet that can store advising results. For any assignment which is not a the final exam, a calculation is made to show what average students need to achieve on any remaining assignments to achieve either an A, B, C, D or a Pass. In the situation a grade is unobtainable, "not possible" is written into the relevant field.

I believe it would be possible to create low cost tools for such educational programs that could perform such simple tasks. For example, most institutions I've worked with use Google. I have been able to create an attendance system using Google Apps Scripts. I think that Python offers a great deal more, and I would be excited to further develop this project into something fit for use for my employer. 

## How to use Grade Center
Grade Center initiates by offer users a set of options, for which they are prompted to enter the corresponding number. 
1. Enter grades
2. View individual student results
3. View class averages
4. Quit

### Option 1: Enter grades
When a user selects Option 1, they get the following information and prompts:
1. The user is informed for which assignment the program is collecting grades. For example, "Accepting grades for Homework." This will be the next item the list for which there is a "due" status.
2. They are asked for the total possible points. 
3. Once a points value is entered, they are asked to confirm it, in case it was mistyped. 
4. The teacher is then given the names of the students in alphabetical order and asked to enter the student's score. 
5. Once the student score is entered, the teacher is asked to confirm it is right, and, as above, the teacher has the option to enter a new grade.
6. Once all the grades are entered, the user is given statements to let them know the class average, 2 statements to let the user know what calculations the program is performing, and a final statement to ask them to wait for the options menu to appear.
7. The user is brought back to the Options menu.

### Option 2: View individual student results
When a user selects this option, they are shown their class roster, which is a numbered list of students, and they are prompted to select the student by their number. Once a student is selected, the user is shown 2 tables:
1. The first table is a list of all the assignments and the grades achieved by the students. 
2. The second table shows the averages a student must maintain on upcoming assignments/exams in order to achieve an A, B, C, D or a pass.
3. Under the table is a prompt asking the teacher if they'd like to view another student record. A positive reply brings you back to the class list, a negative reply brings you back to the Options menu.

### Option 3: View Class Averages
When a user selects option three they are shown a table with three columns:
- The date the grades were entered.
- The assignment
- The class average for each assignment.

### Option 4: Quit
This allows the user to exit the program. When the user enters "4", they are asked if they want to exit, and if confirmed the receive the message, "Thank you for using Grade Center," a negative response brings them back to the Options menu.

## User Experience
The target audience for this app are faculty members or teachers working within small educational institutions that don't resources for a CRM.  

As a user I want:
- An easy to access app that is easy to understand. It should require no or very little training/instruction.
- To be able to correct mistakes. 
- To have scores weighted and calculated automatically
- View student records.
- View my class list and average results.
- To be able to better advise students, and intervene before any student is at risk of failing or underachieving. 

Examples of how the above is achieved is detailed in the features section below.

## Features

### User Story
I would like this app to be easy to understand, without any or much training.

Implementation
- Options menu: when the app starts, the user has a simple options menu with choices to enter grades, view student records, view their class list with averages of previously entered grades or to leave the program. 

It is clear from this menu what information is available and what you can do at each menu option. 

![Options Menu](assets/options_screen.JPG)

When the user selects Option 1, the program tells them for which assignmet the user is entering grades and asks for input. The teacher is asked to make this input as an integrer. 

It won't matter if those points have already been turned into a percent or if they want to enter the actual points the student scored based on a certain amount. For example, if an assignment or exam was worth 30 points, the teacher can enter that value and subsequently the scores earned by the student, such as 27, 28, 29. The figure will be converted into a percent. In the case the score has been calcuated by the teacher, then they can enter the total possible score as 100 and proceed to enter the numbers.

![Entering Grades](assets/enter_grades_inst.JPG)


## Libraries and Technologies Used
The following packages/libraries have been imported:
- google-auth:This uses the creds.json file to set up the authentication needed to access the Google Cloud project. 
    - google.oauth2.service_account: To allow the app to access Google Sheets, I followed the Love Sandwiches walk through to enable the Google Drive and Google Sheets APIs. This is described in the Deployment section below. 
    
- gspread: gspread is a Python API for Google Sheets, which we learned about in the Love Sandwiches walkthrough. In this app, I am using it to access my spreadsheet's data and to write data into it. 
- PANDAS: This is a Python packgage that is using widely by data scientists. I've used it here to easily display back information to the user, and I found it useful for creating variables (for example the length of a row).

USER STORY
I would like to be able to correct a mistake

IMPLEMENTATION
Every time a user makes an input they have the opportunity to correct a mistake. For example, on our current screen, the user will make a number of mistakes:
- Entry 1: Wrong number (1001). They are asked if this is correct.
- Entry 2: The user responds with "n" (no) and they are asked what the total score was again.
- Entry 3: They make a different kind of mistake this time with a slip of the fingers at the top of the keyboard, entering "10-). They are asked to enter a valid integer, and once again given the prompt, "What was the total possible score?
- Entry 4: This time they enter "100", and they are asked to validate it. 
- Entry 5: This time they presss the "enter key" by accident. They prompted again, "Please answer yes/y or no/n".
- Entry 6: This time they hit the space bar and enter, with the same response as in 5.
- Entry 7: The cat walks across the key board and ladfjlf is entered. Same response as above.
- Entry 8: Finally, success! The user enters "y".

## Deployment

### Setting up the Google Spreadsheet and repository
###Create a new project on Google Cloud Platform.
- Enable the Google Drive and Google Sheets APIs, to allow data sharing. To do this, go to the the APIs & Service menu then to libraries where you can search for these APIs.
- Generate credentials. Click the credentials button within the APIs and Services menu, and complete the fields. 
- Once the above is complete, you click the "Add Credentials Button" to create a service account name, selecting JSON for the key type. - Once the above is completed, a file is downloaded with credentials. 
### Set up GitHub repository and GitPod workspace, and link to Google
- Set up repository for the project on Git Hub and create a GitPod workspace. 
- Add the downloaded credentials file into the GitPod workspace and rename it creds.json.
- Find the client email in the credentials. Go to the Google Sheet, share the spreadsheet with this email and give it full access to the spreadsheet.
- Add the creds.json file to "gitignore" to prevent it from being commited or sent to GitHub. 
### Install libraries and set global variables for access to the spreadshett
- Install the libraries needed by entering "pip3 install + library_name" on the command line. e.g. "pip3 install google-auth".
- Import the libraries into the run.py file. For example, for google-auth write "from google.oauth2.service_account import Credentials" at the top of the file. 
- Set the scope by creating a global variable of the same name and listing the APIs the program has access to. 
- Create the the following variables to link up with the service account, create the gspread client and access the project's spreadsheet. 

        CREDS = Credentials.from_service_account_file('creds.json')
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
        SHEET = GSPREAD_CLIENT.open('gradebook')

