from subprocess import Popen, PIPE

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