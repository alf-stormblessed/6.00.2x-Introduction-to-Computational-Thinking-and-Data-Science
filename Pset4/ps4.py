# 6.00.2x Problem Set 4
##300->128/1000 cured
##150->117/1000 cured
##75->cured:  476/1000 
##0->cured:  831/1000  :  0.831

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    # TODO
    Patients = []
    for i in range(numTrials):
        print "simulating patient number ", i
        Patients.append(getPatientPopulation())
    cured = 0
    
    for pats in Patients:
        if (pats<=50):
            cured += 1
    print "cured: ", cured, " : ", float(cured)/numTrials
    pylab.figure()
    pylab.hist(Patients,20)
    pylab.show()
        

def getPatientPopulation():

    population = [0.0]*300
    resistantPopulation = [0.0]*300
    for j in range(1):
        
        viruses = []
        for i in range(100):
            viruses.append(ResistantVirus(0.1, 0.05, {'guttagonol': False}, 0.005))

        patient = TreatedPatient(viruses,100000)
        
        
        for i in range(150):
            
            patient.update()
            population[i] += patient.getTotalPop()
            
            resistantPopulation[i] += patient.getResistPop(["guttagonol"])
            
            
        patient.addPrescription("guttagonol")
        
        
        for i in range(150):
            
            patient.update()
            population[i+150] += patient.getTotalPop()
            resistantPopulation[i+150] += patient.getResistPop(["guttagonol"])
        
    for i in range(len(population)):
        
         population [i] /= float(1)

    for i in range(len(resistantPopulation)):
        
         resistantPopulation [i] /= float(1)    
    
    return population[len(population)-1]

#
# PROBLEM 2
#

def getPatientPopulation2():

    population = [0.0]*300
    resistantPopulation = [0.0]*300
    for j in range(1):
        
        viruses = []
        for i in range(100):
            viruses.append(ResistantVirus(0.1, 0.05, {'guttagonol': False, 'grimpex': False}, 0.15))

        patient = TreatedPatient(viruses,1000)
        
        
        for i in range(150):
            
            patient.update()
            population[i] += patient.getTotalPop()
            
            resistantPopulation[i] += patient.getResistPop(["guttagonol"])
            
            
        patient.addPrescription("guttagonol")
        
        ##delay_init
        
        for i in range(0):
            
            patient.update()
            population[i+150] += patient.getTotalPop()
            resistantPopulation[i+150] += patient.getResistPop(["guttagonol"])
            
        ##delay_end
        patient.addPrescription("grimpex")
        
        for i in range(150):
            
            patient.update()
            population[i+150] += patient.getTotalPop()
            resistantPopulation[i+150] += patient.getResistPop(["guttagonol"])

    variance = 0.0
    mean = 0.0
    for i in range(len(population)):
         
         mean += population[i]
         population [i] /= float(1)
    mean /= float(len(population))
    
    for i in range(len(population)):
         
         variance += (population[i]-mean)**2 
         population [i] /= float(1)
    variance /= len(population)
    print "var: ", variance     
    for i in range(len(resistantPopulation)):
        
         resistantPopulation [i] /= float(1)    
    
    return population[len(population)-1]

def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
    Patients = []
    for i in range(numTrials):
        print "simulating patient number ", i
        Patients.append(getPatientPopulation2())
    cured = 0
    
    for pats in Patients:
        if (pats<=50):
            cured += 1
    print "cured: ", cured, " : ", float(cured)/numTrials
    pylab.figure()
    pylab.hist(Patients,20)
    pylab.show()