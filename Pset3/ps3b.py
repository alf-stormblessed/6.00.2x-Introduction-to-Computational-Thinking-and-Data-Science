# -*- coding: utf-8 -*-
# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 
from ps3b_precompiled_27 import *
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
# PROBLEM 2
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

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb
        
    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        # TODO
        if (random.random()<self.clearProb):
            return True
        else:
            return False
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
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

        if (random.random() < self.maxBirthProb * (1-popDensity)):
            return SimpleVirus(self.maxBirthProb,self.clearProb)
        else:
            raise NoChildException()
            
class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the vip1ruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        # TODO
        
        self.viruses = viruses
        self.maxPop = maxPop
        
        

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        # TODO        
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        auxVirus = []

        for virus in self.viruses:
            if not virus.doesClear():

                auxVirus.append(virus)


        popDensity = float(len(auxVirus))/float(self.maxPop)
        
        self.viruses = auxVirus
        
        auxVirus = []
        for virus in self.viruses:
            try:
                auxVirus.append(virus.reproduce(popDensity))
                auxVirus.append(virus)
                
            except NoChildException: 
                auxVirus.append(virus)
                pass

        self.viruses = auxVirus
          
        return (len(self.viruses))
#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    # INIT
    viruses = []
    virusSize = [0.0]*300
    for j in range(numTrials):
        
        for i in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb,clearProb))
        
        patient = Patient(viruses, maxPop)
        
        for i in range(300):
            patient.update()
            virusSize[i] += (patient.getTotalPop())
    for i in range(numTrials):
        virusSize[i]  /= numTrials      
    
    pylab.figure()
    pylab.plot(virusSize)
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend()
    pylab.show()
    
    
#
# PROBLEM 4
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
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # TODO
        SimpleVirus.__init__(self, maxBirthProb,clearProb)
        self.resistances = resistances
        self.mutProb = mutProb
        
        

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if (drug in self.resistances and self.resistances[drug]): return True
        else: return False


    def reproduce(self, popDensity, activeDrugs):
        
        
        isAbletoReproduce = True
        
        for drugs in self.resistances:

            if (self.resistances.get(drugs)):
                if (random.random()<self.mutProb):#si es resistente, su hijo lo será con mutProb 
                    self.resistances[drugs] = True

                else:
                    self.resistances[drugs] = False#si es resistente, su hijo no lo será con 1-mutProb 

            elif (drugs in activeDrugs):
                isAbletoReproduce = False
            else:
                if (random.random()>self.mutProb):#si no es resistente, su hijo lo será con mutProb
                    self.resistances[drugs] = True             
                else:
                    self.resistances[drugs] = False
                        
        if isAbletoReproduce:  

            if (random.random() < self.maxBirthProb * (1-popDensity)):
                
                return ResistantVirus(self.maxBirthProb,self.clearProb,self.resistances,self.mutProb)
            else:
                raise NoChildException()    
        else:
            raise NoChildException()
            
class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        # TODO
        Patient.__init__(self, viruses, maxPop)
        self.activeDrugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        # TODO
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)
        
        

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
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        # TODO
        count = 0
        for virus in self.viruses:
            aux = False
            for drug in drugResist:
                
                if not virus.isResistantTo(drug):
                    aux = False
                    
                    break
                else:
                    
                    aux = True
            
            if (aux):
                
                count += 1
                
        return count                


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        auxVirus = []

        for virus in self.viruses:
            if not virus.doesClear():

                auxVirus.append(virus)


        popDensity = float(len(auxVirus))/float(self.maxPop)
        
        self.viruses = auxVirus
        
        auxVirus = []
        
        for virus in self.viruses:

            auxVirus.append(virus)
            try:
                auxVirus.append(virus.reproduce(popDensity,self.activeDrugs))

                
            except NoChildException: 

                pass

        self.viruses = auxVirus
          
        return (len(self.viruses))


#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    # TODO
    population = [0.0]*450
    resistantPopulation = [0.0]*450
    for j in range(numTrials):
        
        viruses = []
        for i in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

        patient = TreatedPatient(viruses,maxPop)
        
        
        for i in range(300):
            
            patient.update()
            population[i] += patient.getTotalPop()
            
            resistantPopulation[i] += patient.getResistPop(["guttagonol"])
            
            
        patient.addPrescription("guttagonol")
        
        
        for i in range(150):
            
            patient.update()
            population[i+300] += patient.getTotalPop()
            resistantPopulation[i+300] += patient.getResistPop(["guttagonol"])
        
    for i in range(len(population)):
        
         population [i] /= float(numTrials)

    for i in range(len(resistantPopulation)):
        
         resistantPopulation [i] /= float(numTrials)    
    print "resistant: " , resistantPopulation[len(resistantPopulation)-1]
    return population[len(population)-1]
#    pylab.figure()
#    pylab.plot(population)

#    pylab.plot(resistantPopulation,'ob')
#    pylab.title("SimpleVirus simulation")
#    pylab.xlabel("Time Steps")
#    pylab.ylabel("# viruses")
#    pylab.legend()
#    pylab.show()
    
def plotPatients():
    
    patients = []
    for i in range(0,1000):
        patients.append(simulationWithDrug(100,1000,0.1,0.05,{'guttagonol': False},0.005,1))
        print "patient ", i, " Pop: ", patients[i]
    pylab.figure()
    pylab.hist(patients,10)
    pylab.show()
    pylab.figure()
    pylab.plot(patients)
    pylab.show()