original = [line.rstrip('\n') for line in open('totalStudents.txt', 'r')]
submitted = [line.rstrip('\n') for line in open('final.txt', 'r')]
myFile = open('uploadFinal.txt', 'w')
j = 0
coutMissing = 0
for i in range(len(original)):
    submittedSplit = submitted[j].split(", ")
    if original[i] == submittedSplit[0]:
        print("Found", original[i], "in submissions as", submittedSplit[0])
        updateFileLine = submittedSplit[0] + ", " + submittedSplit[1]
        myFile.write("%s\n" %updateFileLine)
        j += 1
    else:
        print("Adding Missing Student ", original[i])
        addMissing = original[i] + ", 0"
        myFile.write("%s\n" %addMissing)
        coutMissing += 1
print("Total missing students -->", coutMissing)
myFile.close()