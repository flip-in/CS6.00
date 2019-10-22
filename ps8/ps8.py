# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb

        # TODO



    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances[drug]

        # TODO


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # TODO
        prob = random.random()
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()
        
        if self.maxBirthProb * (1 - popDensity) > prob:
            child_res = {}
            for key in self.resistances:
                if random.random() > 1 - self.mutProb:
                    child_res[key] = not self.resistances[key]
                else:
                    child_res[key] = self.resistances[key]
                    
            child = ResistantVirus(self.maxBirthProb, self.clearProb, child_res, 
                                   self.mutProb)
            
            
            return child
        
        else:
            raise NoChildException()
        

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        self.activeDrugs = []
        self.viruses = viruses
        self.maxPop = maxPop

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)
            
        else:
            pass

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.activeDrugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        #All_res = 0
        Virus_copy = self.viruses[:]
        for virus in Virus_copy:
            for drug in drugResist:
                if not virus.isResistantTo():
                    Virus_copy.remove(virus)
                    
        return len(Virus_copy)            

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO
        
        for virus in self.viruses[:]:
            if virus.doesClear():
                self.viruses.remove(virus)
            
        popDensity = float(len(self.viruses)) / self.maxPop
               
        for virus in self.viruses[:]:
            
            try:
                child = virus.reproduce(popDensity, self.activeDrugs)
                self.viruses.append(child)
            except NoChildException:
                pass
        
        
        return self.getTotalPop()



#
# PROBLEM 2
#

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numStepsBeforeDrugApplied, totalNumSteps):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    

    VirusList = []
    for i in xrange(0, numViruses):
        VirusList.append(ResistantVirus(maxBirthProb, clearProb, 
                                        resistances, mutProb))
        
    Charlie = Patient(VirusList, maxPop)
    
    numVirusesEachStep = []
    numResistantVirusesEachStep = []
    for i in xrange(0, totalNumSteps):
        if i == numStepsBeforeDrugApplied:
             Charlie.addPrescription("guttagonol")
        numVirusesEachStep.append(Charlie.update())

    return numVirusesEachStep
        


# PROBLEM 3
#        

def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, 
                               resistances, mutProb, numTrials):

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    # TODO
 
    delays = [300, 150, 75, 0]
    finalResults = {}
    
    for delay in delays:
        finalNumViruses = []
        for n in xrange(0, numTrials):
            total = simulationWithDrug(numViruses, maxPop, maxBirthProb, 
                                      clearProb, resistances, mutProb, delay, 
                                      delay + 150)
                                      
            finalNumViruses.append(total[-1])

        finalResults[delay] = finalNumViruses
    
#    plotNum = 1
#    for n in delays:
#        pylab.subplot(2, 2, plotNum)
#        pylab.title("delay: " + str(n))
#        pylab.xlabel("final virus counts")
#        pylab.ylabel("# trials")
#        pylab.hist(finalResults[n], bins=12, range=(0, 600)) # each bin of size 50
#        plotNum += 1
#
#    pylab.show()
        

##
# PROBLEM 4
#
#simulationDelayedTreatment(100, 1000, .1, .05, {'guttagonol':False}, .005, 30)
def simulationTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, 
                                       resistances, mutProb, numTrials):

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO
    delays = [300, 150, 75, 0]
    finalResults = {}
    for delay in delays:
        finalNumViruses = []
        for t in xrange(0, numTrials):
            VirusList = []
            for i in xrange(0, numViruses):
                VirusList.append(ResistantVirus(maxBirthProb, clearProb, 
                                                resistances, mutProb))
                
            #numResistantVirusesEachStep = []
            numVirusesEachStep = []   
            Charlie = Patient(VirusList, maxPop)
            
            for i in xrange(0, 150):
                numVirusesEachStep.append(Charlie.update())
                
            Charlie.addPrescription("guttagonol")     
            
            for i in xrange(0, delay):
                if not delay == 0:
                    numVirusesEachStep.append(Charlie.update())
           
            Charlie.addPrescription("grimpex")
            
            for i in xrange(0, 150):
                numVirusesEachStep.append(Charlie.update())
                
            finalNumViruses.append(numVirusesEachStep[-1])    
            
        finalResults[delay] = finalNumViruses
        
    plotNum = 1
    for n in delays:
        pylab.subplot(2, 2, plotNum)
        pylab.title("delay: " + str(n))
        pylab.xlabel("final virus counts")
        pylab.ylabel("# trials")
        pylab.hist(finalResults[n], bins=12, range=(0, 600)) # each bin of size 50
        plotNum += 1
    
    pylab.subplots_adjust(left=None, bottom=None, right=None, top=None, 
                          wspace=0.25, hspace=0.5)
    pylab.show()

#simulationTwoDrugsDelayedTreatment(100, 1000, .1, .05, 
                                  # {'guttagonol':False, 'grimpex':False}, .005, 
                                   #50)
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations(numViruses, maxPop, maxBirthProb, clearProb, 
                                       resistances, mutProb, numTrials):

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO
    
 
    finalResults = {}
    Simulation = 2
    for t  in xrange(0,numTrials):
#        VirusList = []
#        #finalNumViruses = []
#        for i in xrange(0, numViruses):
#                VirusList.append(ResistantVirus(maxBirthProb, clearProb, 
#                                                resistances, mutProb))
                                                
        for sim in range(Simulation):
            if sim == 0:
                VirusList = []
                #finalNumViruses = []
                for i in xrange(0, numViruses):
                    VirusList.append(ResistantVirus(maxBirthProb, clearProb, 
                                                resistances, mutProb))
                Charlie = Patient(VirusList, maxPop)
                numVirusesEachStep = [] 
                for i in xrange(0, 150):
                    numVirusesEachStep.append(Charlie.update())
                
                Charlie.addPrescription("guttagonol")
                for i in xrange(0, 300):
                    numVirusesEachStep.append(Charlie.update())
                Charlie.addPrescription("grimpex")
                
                for i in xrange(0,150):
                    numVirusesEachStep.append(Charlie.update())
                
                finalResults[sim] = numVirusesEachStep
                
            if sim == 1:
                VirusList = []
                #finalNumViruses = []
                for i in xrange(0, numViruses):
                    VirusList.append(ResistantVirus(maxBirthProb, clearProb, 
                                                resistances, mutProb))
                numVirusesEachStep = []
                Charlie = Patient(VirusList, maxPop)
                
                for i  in xrange(0, 150):
                    numVirusesEachStep.append(Charlie.update())
                Charlie.addPrescription("guttagonol")
                Charlie.addPrescription("grimpex")
                
                for i in xrange(0, 150):
                    numVirusesEachStep.append(Charlie.update())
                    
                finalResults[sim] = numVirusesEachStep
    
    pylab.figure()                  
    pylab.plot(finalResults[0], label='Staggered Treatment')
    pylab.plot(finalResults[1], '-r', label='Simul Treatment')
    pylab.title('Growth of virus population over time')
    pylab.xlabel('number of "steps"')
    pylab.ylabel("number of viruses")
    pylab.legend(loc='lower right')
    pylab.show() 

simulationTwoDrugsVirusPopulations(100, 1000, .1, .05, 
                                   {'guttagonol':False, 'grimpex':False}, .005, 
                                   10)