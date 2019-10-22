# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    sub_dict = {}
    inputFile = open(filename)
    for line in inputFile:
        line = line.split(',')
        sub_dict[line[0]] = int(line[1]), int(line[2])

    return sub_dict
    

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    # TODO...
    return subInfo1[0] > subInfo2[0]
        

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    # TODO...
    return subInfo1[1] < subInfo2[1]
    
def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    # TODO...
    ratio1 = float(subInfo1[0]) / float(subInfo1[1])
    ratio2 = float(subInfo2[0]) / float(subInfo2[1])
    return ratio1 > ratio2

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    dict_copy = {}
    sub_list = []
    for key, value in dict.iteritems(subjects):
        sub_list.append([key, value])
        
    work = 0

    loops = 1
    while len(sub_list)-loops > 0:
        #print 'first'
        for i in xrange(len(sub_list)-loops):
            if not comparator(sub_list[i][1], sub_list[i+1][1]):
                sub_list[i], sub_list[i+1] = \
                sub_list[i+1], sub_list[i]
        loops+=1

    i=0
    while work < maxWork and i < len(sub_list):
        #print 'second'
        if work + sub_list[i][1][1] <= maxWork:
            dict_copy[sub_list[i][0]] = sub_list[i][1]
            work += sub_list[i][1][1]
        i+=1
    
    return dict_copy   
#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    pset = genPset(subjects)
    finalDict={}
#    work = 0
    bestVal = 0
    bestSet = None
    for Items in pset:
        ItemsVal = 0
        ItemsWork = 0
        for item in Items:
            ItemsVal += item[1][0]
            ItemsWork += item[1][1]
        if ItemsWork <= maxWork and ItemsVal > bestVal:
            bestVal = ItemsVal
            bestSet = Items
    for item in bestSet:
        finalDict[item[0]] = item[1]
    return finalDict
   

def dToB(n, numDigits):
    """requires: n is a natural number less than 2**numDigits
      returns a binary string of length numDigits representing the
              the decimal number n."""
    assert type(n)==int and type(numDigits)==int and n >=0 and n < 2**numDigits
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n//2
    while numDigits - len(bStr) > 0:
        bStr = '0' + bStr
    return bStr

def genPset(subjects):
    """Generate a list of lists representing the power set of Items"""
    dataList = []
    for key, value in dict.iteritems(subjects):
        dataList.append([key, value])
    numSubsets = 2**len(dataList)
    templates = []
    for i in range(numSubsets):
        templates.append(dToB(i, len(dataList)))
    pset = []
    for t in templates:
        elem = []
        for j in range(len(t)):
            if t[j] == '1':
                elem.append(dataList[j])
        pset.append(elem)
        
    return pset

#print bruteForceAdvisor(loadSubjects(SHORT_SUBJECT_FILENAME), 15)
#print greedyAdvisor(loadSubjects(SUBJECT_FILENAME), 15, cmpValue)
#print greedyAdvisor(loadSubjects(SUBJECT_FILENAME), 15, cmpWork)
#print greedyAdvisor(loadSubjects(SUBJECT_FILENAME), 15, cmpRatio)
print bruteForceAdvisor(loadSubjects(SUBJECT_FILENAME), 15)
