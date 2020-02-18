import sys, time, platform, json
from subprocess import Popen, PIPE

# start processing timer
start_time = time.time()

# load user setting
with open('config.json') as f:
    config = json.load(f)
 
# initialize students
students = []

# ls will give all the submitted directories
listStudents = Popen(['ls'], stdout=PIPE, stderr=PIPE, encoding='utf8')

outlistStudents, errlistStudents = listStudents.communicate()

outlistStudents = outlistStudents.split()
for item in outlistStudents:
    # only consider kerberos@ad3.ucdavis.edu
    if '@' in item:
        students.append(item)

testInputFile = config.get('testInputFileName')

# put test input file in a list for partial checking
testOutputList = [line.rstrip('\n') for line in open(config.get('testOutputFileName'), 'r')]

results = []
finalResults = []
count = 0

for s in students:
    print(s)
    total = config.get('maxScore')
    if platform.system() == 'Darwin':
        commands = f'''
        cd {s}
        stat -f "%m" -t "%Y" {config.get('tarFileName')}
        tar xvf {config.get('tarFileName')}
        make
        make clean
        make
        '''
    else:
        commands = f'''
        cd {s}
        stat -c "%Y" {config.get('tarFileName')}
        tar xvf {config.get('tarFileName')}
        make
        make clean
        make
        '''

    timeCheck = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = timeCheck.communicate(commands.encode('utf-8'))
    outputs = out.decode('utf-8').strip().split('\n')
    errors = err.decode('utf-8').split('\n')
    due = config.get('timeStamp')
    hour = 3600

    try:
        if int(outputs[0]) <= int(due)+hour*0:
            total = total
            errors.append('on time')
            print("On Time")
        elif int(outputs[0]) > int(due)+hour*0 and int(outputs[0]) <= int(due)+hour*1:
            total *= 0.9
            errors.append('late by 0+ hour')
            print("late by 0+ hour")
        elif int(outputs[0]) > int(due)+hour*1 and int(outputs[0]) <= int(due)+hour*2:
            total *= 0.8
            errors.append('late by 1+ hours')
            print("late by 1+ hour")
        elif int(outputs[0]) > int(due)+hour*2 and int(outputs[0]) <= int(due)+hour*3:
            total *= 0.7
            errors.append('late by 2+ hours')
            print("late by 2+ hour")
        elif int(outputs[0]) > int(due)+hour*3 and int(outputs[0]) <= int(due)+hour*4:
            total *= 0.6
            errors.append('late by 3+ hours')
            print("late by 3+ hour")
        else:
            total *= 0
            errors.append('late by 4+ hours')
            print("late by 4+ hour")
    except:
        print("Is it exception")
        pass
    total = int(total)

    # no multi file means 2 cases
    # 1. either the executable requires no input
    # 2. or it requires a single input file 
    if not (config.get('isMultiFileInput')):
        if testInputFile == '':
            commandsExec = f'''
                cd {s}
                ./{config.get('execFileName')}
                '''
        else:
            commandsExec = f'''
                cd {s}
                ./{config.get('execFileName')} < {testInputFile}
                '''
    else:
        maxInFile = config.get('multipleInFile')
        commandString = ""
        if maxInFile != 0:
            # form multiple input command strings
            for inFileCount  in range(1, maxInFile + 1):
                commandString = commandString + "./" + config.get('execFileName') + " < ../" + config.get('testMultiInputFileName') + str(inFileCount) + ".in\n"
            commandsExec = f'''
                cd {s}
                {commandString}
                '''
        else:
            print("No of Max File must be greater than 0")
            exit

    runExecutable = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = runExecutable.communicate(commandsExec.encode('utf-8'))
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
                        # deduct marks
                        outputs.append("Output is partially expected")
                        total -= config.get('deductScore')
            else:
                spaceRemovedOutputsExec = []
                for i in outputsExec:
                    j = i.replace(' ', '')
                    spaceRemovedOutputsExec.append(j)
                if spaceRemovedOutputsExec == testInputFile:
                    outputs.append("Output had extra spaces")
                    total -= 2*config.get('deductScore')
                else:
                    outputs.append("Output is completely different")
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

with open(config.get('verboseResultFileName'), 'w+') as f:
    for result in results:
        f.write(str(result)+'\n')
    f.write(f'correct submissions: {str(count)}')
    f.write(f'total submissions: {len(students)}')

with open(config.get('resultsFileName'), 'w+') as f:
    for finalResult in finalResults:
        f.write(str(finalResult)+'\n')

print("Time to process", len(students), "students was %s seconds" % (time.time() - start_time))