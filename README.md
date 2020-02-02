# autoGrader
Attempts to reduce the task of manually grading over 190+ students coding assignment submissions.
Students submit their programs via the handin command.
Each student has a folder containing the .tar file of all the related file to the assignment.

Task is to:
1. Check the file submission date against the due date
2. Untar the file
3. Make the files
4. Execute with the given input and save the result
5. Check the result with given output

Usage
```console
   foo@bar:~$ python3 grade.py <testInputFile.in> <testOutputFile.out>
```
Output is 
1. A clean comma separated txt file with kerberosID, score
2. A verbose commas separated txt file with kerberosID, Logs