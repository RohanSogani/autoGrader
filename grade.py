from subprocess import Popen, PIPE
import platform

#initialize students
students = []

#ls will give all the submitted directories, kerberos@ad3.ucdavis.edu
p1 = Popen(['ls'], stdout=PIPE, stderr=PIPE, encoding='utf8')

out1, err1 = p1.communicate()

out1 = out1.split()
for item in out1:
    if '@' in item:
        students.append(item)

print(students)

results = []
count = 0
print('starting')
for s in students:
    print(s)
    total = 20
    if platform.system() ==  'Darwin':
        commands = f'''
        cd {s}
        stat -f "%m" -t "%Y" hw1p1.tar
        tar xvf hw1p1.tar
        make all
        ./useVelocity
        make clean
        '''
    else:
        commands = f'''
        cd {s}
        stat -c "%Y" hw1p1.tar
        tar xvf hw1p1.tar
        make all
        ./useVelocity
        make clean
        '''

    p2 = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p2.communicate(commands.encode('utf-8'))
    print(out)
    outputs = out.decode('utf-8').strip().split('\n')
    errors = err.decode('utf-8').split('\n')
    due = 1580500800
    hour = 3600

    try:
        #print("Time-->", outputs[0])
        if int(outputs[0]) <= due+hour*0:
            print("here")
            total = total
            errors.append('on time')
        elif int(outputs[0]) > due+hour*0:
            print("musthere")
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
    print(outputs)
    print(errors)