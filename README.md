# autoGrader
<strong>Problem Description</strong>\
Attempts to reduce the task of manually grading over 190+ students C++ coding assignment submissions.\
Students submit their programs via the handin command.\
Each student has a folder containing the .tar file of all the related file to the assignment.

<strong>Note</strong>
This script is for such an environment where the directorty contains subdirectories named as StudentKerberosID@something.com.
Each of these subdirectories must have tar files with containing the all the required files and the Makefile.

<strong>Helper files</strong>
1. <strong>mergeFileColumns.py</strong> - Merges the scores of two assignments in one final score file
2. <strong>findMissingStudents.py</strong> - compares final score file with the total number of students. Further it finds the students who have not submitted their homework and assigns 0 score.

<strong>Task</strong>
1. Check the file submission date against the due date
2. Untar the file
3. Make the files
4. Execute with the given input and save the result
5. Check the result with given output


<strong>Usage</strong>
```console
   foo@bar:~$ python3 grade.py <DueTimeStamp> <testInputFile.in> <testOutputFile.out>
```
The input file is not mandatory, in that case the script needs to be hardcoded to supply proper input.

<strong>Output</strong>
1. A clean comma separated txt file with kerberosID, score
2. A verbose commas separated txt file with kerberosID, Logs

<strong>Analysis</strong>\
This script was tested on a folder containing over 190 students sub-directories all containing .tar files.\
Overall time it took was just over <strong>150 seconds</strong>, about <strong>2.5 - 3 minutes</strong>\
The manual task on the other hand could take over <strong>20 hours or more</strong>. :P
Accuracy of this script is about 80%, I still had to manually review about 30 submissions. But, this will improve with time.
