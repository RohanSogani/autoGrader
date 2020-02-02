import sys
from subprocess import Popen, PIPE
import platform

print("Number of arguments:", len(sys.argv), "arguments.")
print("Argument List:", str(sys.argv))

if len(sys.argv) < 2:
    print("Usage: python grader.py testInput.in testOutput.out || python grader.py testOutput.out")
    sys.exit()
if len(sys.argv) == 2:
    print("No input file provided")
    if sys.argv[1].endswith('.out'):
        testInputFile = ''
        testOutputFile = str(sys.argv[1])
        print(str(sys.argv[1]), "is the test output file")
    else:
        print("Please provide a .out file for comparison")
        sys.exit()
elif len(sys.argv) == 3:
    if sys.argv[1].endswith('.in'):
        testInputFile = str(sys.argv[1])
        print(str(sys.argv[1]), "is the test input file")
        if sys.argv[2].endswith('.out'):
            testOutputFile = str(sys.argv[1])
            print(str(sys.argv[2]), "is the test output file")
        else:
            print("Usage: python grader.py testInput.in testOutput.out || python grader.py testOutput.out")
    else:
        print("Usage: python grader.py testInput.in testOutput.out || python grader.py testOutput.out")
        sys.exit()
else:
    print("Usage: python grader.py testInput.in testOutput.out || python grader.py testOutput.out")
    sys.exit()
    
#initialize students
students = []

#ls will give all the submitted directories, kerberos@ad3.ucdavis.edu
p1 = Popen(['ls'], stdout=PIPE, stderr=PIPE, encoding='utf8')

out1, err1 = p1.communicate()

out1 = out1.split()
for item in out1:
    if '@' in item:
        students.append(item)

#print(students)

#convert output file to lineList for comparison
testOutputList = [line.rstrip('\n') for line in open(testOutputFile, 'r')]
#print(testOutputList)

results = []
finalResults = []
count = 0
#print('starting')
for s in students:
    print(s)
    total = 20
    if platform.system() ==  'Darwin':
        commands = f'''
        cd {s}
        stat -f "%m" -t "%Y" hw1p1.tar
        tar xvf hw1p1.tar
        make all
        make clean
        make all
        '''
    else:
        commands = f'''
        cd {s}
        stat -c "%Y" hw1p1.tar
        tar xvf hw1p1.tar
        make all
        make clean
        make all
        '''

    p2 = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p2.communicate(commands.encode('utf-8'))
    #print(out)
    outputs = out.decode('utf-8').strip().split('\n')
    errors = err.decode('utf-8').split('\n')
    due = 1580558400
    hour = 3600

    try:
        if int(outputs[0]) <= due+hour*0:
            total = total
            errors.append('on time')
        elif int(outputs[0]) > due+hour*0:
            total *= 0.9
            errors.append('late by 0+ hours')
        elif int(outputs[0]) > (due+hour*1):
            total *= 0.8
            errors.append('late by 1+ hours')
        elif int(outputs[0]) > (due+hour*2):
            total *= 0.7
            errors.append('late by 2+ hours')
        elif int(outputs[0]) > (due+hour*3):
            total *= 0.6
            errors.append('late by 3+ hours')
        else:
            total *= 0
            errors.append('late by 4+ hours')
    except:
        pass
    total = int(total)
    print(outputs)
    print(errors)

    commandsExec = f'''
        cd {s}
        ./useVelocity
        '''

    p3 = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p3.communicate(commandsExec.encode('utf-8'))
    #print(out)
    outputsExec = out.decode('utf-8').strip().split('\n')
    print(outputsExec)
    errorsExec = err.decode('utf-8').split('\n')
    errors.append(errorsExec)
    try:
        if outputsExec == testOutputList:
            outputs.append("Output is expected")
            results.append([s.split('@')[0], total, outputs, errors])
            kerberosID = s.split('@')[0]
            csvLine = kerberosID + ", " + str(total)
            finalResults.append(csvLine)
            count += 1
        else:
            if len(outputsExec) == len(testOutputList):
                for i in range(len(testOutputList)):
                    if testOutputList[i] != outputsExec[i]:
                        #reduce 5 marks
                        total += -1
            else:
                total += -10
            results.append([s.split('@')[0], total, outputs, errors])
            kerberosID = s.split('@')[0]
            csvLine = kerberosID + ", " + str(total)
            finalResults.append(csvLine)
    except:
        total *= 0
        results.append([s.split('@')[0], total, outputs, errors])
        kerberosID = s.split('@')[0]
        csvLine = kerberosID + ", " + str(total)
        finalResults.append(csvLine)

with open('results.txt', 'w+') as f:
    for result in results:
        f.write(str(result)+'\n')
    f.write(f'correct submissions: {str(count)}')
    f.write(f'total submissions: {len(students)}')

with open('StudentIDScores.txt', 'w+') as f:
    for finalResult in finalResults:
        f.write(str(finalResult)+'\n')