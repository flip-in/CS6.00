# Problem Set 10
# Name:
# Collaborators:
# Time:

#Code shared across examples
import pylab, random, string, copy, math

class Point(object):
    def __init__(self, name, originalAttrs, normalizedAttrs = None):
        """normalizedAttrs and originalAttrs are both arrays"""
        self.name = name
        self.unNormalized = originalAttrs
        self.attrs = normalizedAttrs
    def dimensionality(self):
        return len(self.attrs)
    def getAttrs(self):
        return self.attrs
    def getOriginalAttrs(self):
        return self.unNormalized
    def distance(self, other):
        #Euclidean distance metric
        difference = self.attrs - other.attrs
        return sum(difference * difference) ** 0.5
    def getName(self):
        return self.name
    def toStr(self):
        return self.name + str(self.attrs)
    def __str__(self):
        return self.name

class County(Point):
    weights = pylab.array([1.0] * 14)
    
    def setWeight(self, dimension):
        for d in dimension:
            self.weights[d] = 0.0
#            print d, 'set weight equal to: ',self.weights[d]
   
    
    # Override Point.distance to use County.weights to decide the
    # significance of each dimension
    def distance(self, other):
        difference = self.getAttrs() - other.getAttrs()
        return sum(County.weights * difference * difference) ** 0.5
    
class Cluster(object):
    def __init__(self, points, pointType):
        self.points = points
        self.pointType = pointType
        self.centroid = self.computeCentroid()
    def getCentroid(self):
        return self.centroid
    def computeCentroid(self):
        dim = self.points[0].dimensionality()
        totVals = pylab.array([0.0]*dim)
        for p in self.points:
            totVals += p.getAttrs()
        meanPoint = self.pointType('mean',
                                   totVals/float(len(self.points)),
                                   totVals/float(len(self.points)))
        return meanPoint
    def update(self, points):
        oldCentroid = self.centroid
        self.points = points
        if len(points) > 0:
            self.centroid = self.computeCentroid()
            return oldCentroid.distance(self.centroid)
        else:
            return 0.0
    def getPoints(self):
        return self.points
    def contains(self, name):
        for p in self.points:
            if p.getName() == name:
                return True
        return False
    def toStr(self):
        result = ''
        for p in self.points:
            result = result + p.toStr() + ', '
        return result[:-2]
    def __str__(self):
        result = ''
        for p in self.points:
            result = result + str(p) + ', '
        return result[:-2]
        

    
def kmeans(points, k, cutoff, pointType, minIters = 3, maxIters = 100, 
           toPrint = False):
    """ Returns (Cluster list, max dist of any point to its cluster) """
    #Uses random initial centroids
    initialCentroids = random.sample(points,k)
    clusters = []
    for p in initialCentroids:
        clusters.append(Cluster([p], pointType))
    numIters = 0
    biggestChange = cutoff
    while (biggestChange >= cutoff and numIters < maxIters) or numIters < minIters:
        print "Starting iteration " + str(numIters)
        newClusters = []
        for c in clusters:
            newClusters.append([])
        for p in points:
            smallestDistance = p.distance(clusters[0].getCentroid())
            index = 0
            for i in range(len(clusters)):
                distance = p.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            newClusters[index].append(p)
        biggestChange = 0.0
        for i in range(len(clusters)):
            change = clusters[i].update(newClusters[i])
            #print "Cluster " + str(i) + ": " + str(len(clusters[i].points))
            biggestChange = max(biggestChange, change)
        numIters += 1
        if toPrint:
            print 'Iteration count =', numIters
    maxDist = 0.0
    for c in clusters:
        for p in c.getPoints():
            if p.distance(c.getCentroid()) > maxDist:
                maxDist = p.distance(c.getCentroid())
    print 'Total Number of iterations =', numIters, 'Max Diameter =', maxDist
    print biggestChange
    return clusters, maxDist

#US Counties example
def readCountyData(fName, numEntries = 14):
    dataFile = open(fName, 'r')
    dataList = []
    nameList = []
    maxVals = pylab.array([0.0]*numEntries)
    #Build unnormalized feature vector
    for line in dataFile:
        if len(line) == 0 or line[0] == '#':
            continue
        dataLine = string.split(line)
        name = dataLine[0] + dataLine[1]
        features = []
        #Build vector with numEntries features
        for f in dataLine[2:]:
            try:
                f = float(f)
                features.append(f)
                if f > maxVals[len(features)-1]:
                    maxVals[len(features)-1] = f
            except ValueError:
                name = name + f
        if len(features) != numEntries:
            continue
        dataList.append(features)
        nameList.append(name)
    return nameList, dataList, maxVals
    
def buildCountyPoints(fName):
    """
    Given an input filename, reads County values from the file and returns
    them all in a list.
    """
    nameList, featureList, maxVals = readCountyData(fName)
    points = []
    for i in range(len(nameList)):
        originalAttrs = pylab.array(featureList[i])
        normalizedAttrs = originalAttrs/pylab.array(maxVals)
        points.append(County(nameList[i], originalAttrs, normalizedAttrs))
    return points

def randomPartition(l, p):
    """
    Splits the input list into two partitions, where each element of l is
    in the first partition with probability p and the second one with
    probability (1.0 - p).
    
    l: The list to split
    p: The probability that an element of l will be in the first partition
    
    Returns: a tuple of lists, containing the elements of the first and
    second partitions.
    """
    l1 = []
    l2 = []
    for x in l:
        if random.random() < p:
            l1.append(x)
        else:
            l2.append(x)
    return (l1,l2)

def getAveIncome(cluster):
    """
    Given a Cluster object, finds the average income field over the members
    of that cluster.
    
    cluster: the Cluster object to check
    
    Returns: a float representing the computed average income value
    """
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[1]

    return float(tot) / len(cluster.getPoints())

def getAveAttributes(cluster):
    
    avgs = []
    tot = pylab.array([0.0] * 14)
#    tot = 0.0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()

    if len(cluster.getPoints()) == 0:
        pass
    else:
        tot = tot/len(cluster.getPoints())
#    tot = tot/len(cluster.getPoints())

    for num in tot:
        avgs.append(round(num,1))
    
    return avgs

def test(points, k = 200, cutoff = 0.1):
    """
    A sample function to show you how to do a simple kmeans run and graph
    the results.
    """
    incomes = []
    print ''
    clusters, maxSmallest = kmeans(points, k, cutoff, County)

    for i in range(len(clusters)):
        if len(clusters[i].points) == 0: continue
        incomes.append(getAveIncome(clusters[i]))

    pylab.hist(incomes)
    pylab.xlabel('Ave. Income')
    pylab.ylabel('Number of Clusters')
    pylab.show()

        
allPoints = buildCountyPoints('counties.txt')
random.seed(123)
testPoints = random.sample(allPoints, len(allPoints)/10)
#test(testPoints)


    
    
def graphRemovedErr(points, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Should produce graphs of the error in training and holdout point sets, and
    the ratio of the error of the points, after clustering for the given values 
    of k. For details see Problem 1.
    """

    # Your Code Here
    errorList = []
    holdoutErrorList = []
    for k in kvals: 
        errors = []
        holdoutErrors = []
#        trainingErrors = point.distance()
        partition = randomPartition(points, .8)
        trainingPoints = partition[0]
        holdoutPoints = partition[1]
        clusters, maxDistance = kmeans(trainingPoints, k, cutoff, County)
        
        for cluster in clusters:
            for point in cluster.getPoints():
                trainingErrors = point.distance(cluster.getCentroid())**2
                errors.append(trainingErrors)
        errorList.append(sum(errors))

        
        for point in holdoutPoints:
            closestCentroids = []
            for cluster in clusters:
                closestCentroids.append(point.distance(cluster.getCentroid())**2)
            closestCentroids.sort()
            holdoutErrors.append(closestCentroids[0])

        holdoutErrorList.append(sum(holdoutErrors))      
    
    ratioList = []
    for i in range(len(errorList)):
        ratioList.append(holdoutErrorList[i]/errorList[i])
                
    pylab.figure()                  
    pylab.plot(kvals, errorList, label ='training set')
    pylab.plot(kvals, holdoutErrorList, label='holdout set')
    pylab.xlim(25, 150)
    pylab.legend(loc='best')
    pylab.title('Comparing holdout error to training error')
    pylab.xlabel('kvals"')
    pylab.ylabel("error")
    pylab.figure()
    pylab.plot(kvals, ratioList, label = 'ratio of holdout to training')
    pylab.xlim(25,150)
    pylab.legend(loc='best')
    pylab.xlabel('kvals')
    pylab.ylabel('ratio of errors')
    pylab.show() 
    
    return errorList, holdoutErrorList
    
        
    
#print graphRemovedErr(testPoints)   


def graphPredictionErr(points, dimension=2, filters='all', 
                       kvals = [25, 50, 75, 100, 125, 150], 
                       cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """
    """
    dimension(0-13) corresponds to the feature categories of county data
    """

	# Your Code Here
    totalDimensionError = []
    
    '''set only poverty weight to 0.0'''
    if filters=='poverty':
        for p in points:
            p.setWeight([2])
#            print 'set weight equal to: ',p.weights[dimension]
       
            
    """set all weights equal to 0 except poverty"""        
    if filters == 'all':
        for p in points:
            p.setWeight([0,1,3,4,5,6,7,8,9,10,11,12,13])

    """"""
        
    for k in kvals:
        dimensionError = []
        partition = randomPartition(points, .8)
        trainingPoints = partition[0]
        holdoutPoints = partition[1]
        
        trainingClusters = kmeans(trainingPoints, k, cutoff, County)[0]
        
        closestCluster = None
        
        for point in holdoutPoints:
            clusterDistance = []
            for cluster in trainingClusters:
                clusterDistance.append((cluster, point.distance(cluster.getCentroid())))
            clusterDistance.sort(key=lambda x: x[1])
        
            closestCluster = clusterDistance[0][0]
            

            averageDimension = getAveAttributes(closestCluster)[dimension]
       
            dimensionError.append((averageDimension - point.getOriginalAttrs()[dimension])**2)
           
        totalDimensionError.append(sum(dimensionError))
        
 
    if dimension == 2:
        dimension = 'Poverty'
    else:
        dimension = 'Dimension'


    pylab.figure()                  
    pylab.plot(kvals, totalDimensionError, label ='%s error' %dimension)
    
    pylab.xlim(25, 150)
    pylab.legend(loc='best')
    pylab.title('%s error for Counties' %dimension)
    pylab.ylabel('Error')
    pylab.xlabel("K Values")
    pylab.show
    return totalDimensionError

print graphPredictionErr(testPoints)            

def myCounty(county, points, numIter, kval = 50):
    
####GET CLUSTERS FROM KMEANS
    kmeansClusters = []
    for i in range(numIter):
        kmeansClusters.append(kmeans(points, kval, .1, County)[0])

####FIND CLUSTERS WITH COUNTY##############
    countyClusters = []   
    for result in kmeansClusters:
        for cluster in result:
            if cluster.contains(county):
                countyClusters.append(cluster)
#    clusterPoints = [] 
#    for c in countyClusters:
#        clusterPoints.append(c.getPoints())
#    
#    for list in clusterPoints:
#        for p in list:
#            print p.getName()
                
####GET AVG INCOME FROM CLUSTERS###########
#    avgIncome = 0.0
#    for c in countyClusters:
#        avgIncome += getAveIncome(c)
#    print float(avgIncome) / len(countyClusters)
            
####GET MORE AVERAGES!
    for c in countyClusters:
        return 'Average Attributes of Cluster \n [%s]:' % c, getAveAttributes(c)

#print myCounty('INClark', allPoints, 3)

   