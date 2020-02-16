# autoGrader
Attempts to reduce the task of manually grading over 190+ students C++ coding assignment submissions.\
Students submit their programs via the handin command.\
Each student has a folder containing the .tar file of all the related file to the assignment.

## Note
This script is for such an environment where the directory contains subdirectories named as StudentKerberosID@something.com.\
Each of these subdirectories must have tar files containing all the required files and the Makefile.

## Dependencies
Python3 is required for all the programs.

## Usage
1. Setup the config.json file as per requirement.
2. Unix Timestamp is in UTC Format.\
   The due date can be converted [here](https://www.unixtimestamp.com/index.php).\
   If the due date is January 28, 2020, 11:59pm, enter January 29, 2020, 07:59am.\
3. <strong>grade.py</strong> - Contains the core logic to grade students
```console
   foo@bar:~$ python3 grade.py
```

## Helper files
1. <strong>mergeFileColumns.py</strong> - Merges the scores of two assignments in one final score file
2. <strong>findMissingStudents.py</strong> - Compares final score file with the total number of students.\
   It also finds the students who have not submitted their homework and assigns 0 score.

## Task
1. Check the file submission date against the due date
2. Untar the file
3. Make the files
4. Execute with the given input and save the result
5. Check the result with given output

## Output
1. A clean comma separated txt file with kerberosID, score
2. A verbose commas separated txt file with kerberosID, Logs

## Analysis
This script was tested on a folder containing over 190 students sub-directories all containing .tar files.\
Overall time it took was just over <strong>150 seconds</strong>, about <strong>2.5 - 3 minutes</strong>\
The manual task on the other hand could take over <strong>20 hours or more</strong>. :P
Accuracy of this script is about 80%, I still had to manually review about 30 submissions.
But, this will improve with time.
