# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

        # TODO

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        prob = random.random()
        if prob <= self.clearProb:
            return True
        
        else:
            return False

        # TODO

    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO
        
        prob = random.random()
        if self.maxBirthProb * (1 - popDensity) > prob:
            child = SimpleVirus(self.maxBirthProb, self.clearProb)
            return child
            
        else:
            raise NoChildException()
        

class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop


    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

                
        return len(self.viruses)
        

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        #virus_copy = self.viruses[:]
        
        for virus in self.viruses[:]:
            if virus.doesClear():
                self.viruses.remove(virus)
            
        popDensity = float(len(self.viruses)) / self.maxPop
               
        for virus in self.viruses[:]:
            
            try:
                child = virus.reproduce(popDensity)
                self.viruses.append(child)
            except NoChildException:
                pass
        
        
        return self.getTotalPop()



#
# PROBLEM 2ist
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    
    results = []
    average_results = []
    
    for i in range(numTrials):
        
        VirusList = []
        for i in xrange(0, 100):
            VirusList.append(SimpleVirus(maxBirthProb, clearProb))
            
        Charlie = SimplePatient(VirusList, maxPop)
        
        numSteps = 300
        numVirusesEachStep = []
        for i in xrange(0, numSteps):
            numVirusesEachStep.append(Charlie.update())
            
        results.append(numVirusesEachStep)
        
    for virus_number in range(len(results[0])):
        num_virus = 0
        for virus_event in range(len(results)):
            num_virus += results[virus_event][virus_number]
        average_results.append(float(num_virus/len(results)))
            
    pylab.plot(average_results, '-r', label='Simple Virus')
    pylab.title('Growth of virus population over time')
    pylab.xlabel('number of "steps"')
    pylab.ylabel("number of viruses")
    pylab.legend(loc='lower right')
    pylab.show()            
        
simulationWithoutDrug(100, 1000, .1, .05, 50)
