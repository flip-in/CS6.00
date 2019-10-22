# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.cleaned = []
        
        self.width = width
        self.height = height
        
        
        #raise NotImplementedError
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        if self.isTileCleaned(int(pos.getX()), int(pos.getY())) == False:
            return self.cleaned.append((int(pos.getX()), int(pos.getY())))
        else:
            pass                               
        
        #raise NotImplementedError

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return (m, n) in self.cleaned
        
        raise NotImplementedError
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height
        
        raise NotImplementedError

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleaned)
        
        raise NotImplementedError

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        
        return Position(random.randint(1, self.width), random.randint(1, self.height))
    
        raise NotImplementedError

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return pos.getX() <= self.width and pos.getX() > 0 and  \
            pos.getY() <= self.height and pos.getY() > 0
    
        raise NotImplementedError


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition()
        self.direction = random.randint(1, 360)
        room.cleanTileAtPosition(self.position)
        
             
        
        #raise NotImplementedError

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
        
        raise NotImplementedError
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
        
        raise NotImplementedError

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position
        
        raise NotImplementedError

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction
        
        raise NotImplementedError

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.position = self.position.getNewPosition(self.direction, self.speed)
        
        self.room.cleanTileAtPosition(self.position)
        
        
        
        #raise NotImplementedError



# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        for step in range(int(self.speed)):
           
            if self.room.isPositionInRoom(self.position.getNewPosition(self.direction, 1)) == True:
                self.position = self.position.getNewPosition(self.direction, 1)
                self.room.cleanTileAtPosition(self.position)
            
            else:
                self.direction = random.randint(1, 360)
                #self.updatePositionAndClean()
        
            
            
        #raise NotImplementedError
    
   

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    avg_time = 0
    counter = 0
    for n in range(num_trials):
        #anim = ps6_visualize.RobotVisualization(num_robots, width, height, 1)
        robot_dict = {}
        time_steps = 0
        counter += 1
        room = RectangularRoom(width, height)
        
        for i in range(num_robots): #instantiates robots
            robot_dict[i] = robot_type(room,speed)
            
        while room.getNumCleanedTiles() < min_coverage * (width*height):
            for r in robot_dict:
                #anim.update(room, robot_dict)
                robot_dict[r].updatePositionAndClean()
            
            time_steps+=1    
        #anim.done()
        avg_time += time_steps
        
       
        
    avg_time = avg_time / counter
 
        
    print num_robots, 'robot takes around', '{} seconds to clean'.format(avg_time), \
    '{}% of a'.format(min_coverage*100), width,'x',height, 'room.'
    return avg_time  
        
    
    
#print runSimulation(1, 1.0, 20, 20, 1.0, 500, StandardRobot)        
    


    
    #raise NotImplementedError


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20x20 room with each of 1-10 robots
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20x20, 25x16, 40x10, 50x8, 80x5, and 100x4

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    plot_y = []
    plot_x = []
    for s in range(1,11):
        plot_y.append(runSimulation(s, 1.0, 20, 20, .8, 1, StandardRobot))
        plot_x.append(s)
   
    pylab.plot(plot_x, plot_y)
    pylab.title('Time to Clean 80% of a 20x20 room for various # of robots')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Time to Clean (s)')
    pylab.xticks([1,2,3,4,5,6,7,8,9,10])
    pylab.xlim([1,10])
    pylab.show()
     
    #raise NotImplementedError
print "hello World"
showPlot1()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    rooms = [[20,20],[25,16],[40,10],[50,8],[80,5],[100,4]]
    plot_y = []
    plot_x = []
    
    for s in range(len(rooms)):
        plot_y.append(runSimulation(2, 1.0, rooms[s][0], rooms[s][1], .8, 50, StandardRobot))
        plot_x.append(s)
    my_xticks = ['20x20', '25x16', '40x10', '50x8', '80x5', '100x4']
    pylab.xticks(plot_x, my_xticks)
    pylab.plot(plot_x, plot_y)    
    pylab.title('Time to Clean 80% of various rooms for 2 robots')
    pylab.xlabel('size of room')
    pylab.ylabel('Time to Clean (s)')
    pylab.xlim([1,5])
    pylab.show()
    
#showPlot2()
# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        for step in range(int(self.speed)):
            
            self.direction = random.randint(1, 360)
            
            if self.room.isPositionInRoom(self.position.getNewPosition(self.direction, 1)) == True:
                self.position = self.position.getNewPosition(self.direction, 1)
                self.room.cleanTileAtPosition(self.position)
                
            
            else:
                self.direction = random.randint(1, 360)
                
    
#print runSimulation(1, 1.0, 20, 20, 1.0, 1, RandomWalkRobot)

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    #raise NotImplementedError
    plot_y = []
    plot_x = []
    for s in range(1,11):
        plot_y.append(runSimulation(s, 1.0, 20, 20, .8, 10, StandardRobot))
        plot_x.append(s)
    pylab.plot(plot_x, plot_y)
    plot_y = []
    plot_x = []
    for s in range(1,11):
        plot_y.append(runSimulation(s, 1.0, 20, 20, .8, 10, RandomWalkRobot))
        plot_x.append(s)
    pylab.plot(plot_x, plot_y)
    pylab.title('Time to Clean 80% of a 20x20 room for various # of robots')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Time to Clean (s)')
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xticks([1,2,3,4,5,6,7,8,9,10])
    pylab.xlim([1,10])
    pylab.show()
#showPlot3()