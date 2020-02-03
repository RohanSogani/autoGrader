studentScoreHW1 = [line.rstrip('\n') for line in open('StudentIDScores.txt', 'r')]
studentScoreHW2 = [line.rstrip('\n') for line in open('StudentIDScores2.txt', 'r')]

myFile = open('final.txt', 'w')
if len(studentScoreHW1) == len(studentScoreHW2):
    for i in range(len(studentScoreHW1)):
        hw1Split = studentScoreHW1[i].split(", ")
        hw2Split = studentScoreHW2[i].split(", ")
        if hw1Split[0] == hw2Split[0]:
            finalTotal = int(hw1Split[1]) + int(hw2Split[1])
            finalReport = hw1Split[0] + ", " + str(finalTotal)
            myFile.write("%s\n" %finalReport)
        else:
            #should not go here though
            print("Line Mismatch")
else:
    print("student mismatch may occur, total is not the same")

myFile.close()