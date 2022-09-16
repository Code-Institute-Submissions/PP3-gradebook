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