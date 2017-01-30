import random
import pylab
def montyHallmod(numTrials):
    winsSwitch = 0.0
    losesSwitch = 0.0
    for i in range(numTrials):
        space = [1,2,3,4]
        cars = []
        goats = []

        
        cars.append(random.choice(space))
        space.remove(cars[0])
        cars.append(random.choice(space))
        space.remove(cars[1])
        goats = space
        
        space = [1,2,3,4]
        montySpace = space
        guess = random.choice(space)
        ## problem defined
        

        montySpace.remove(guess)
        if (cars[0] in montySpace):
            montySpace.remove(cars[0])
        if (cars[1] in montySpace):
            montySpace.remove(cars[1])
        
        showGoat = random.choice(montySpace)   
        
        space = [1,2,3,4]     

        space.remove(guess)
        space.remove(showGoat)

        switchGuess = random.choice(space)
        if (switchGuess in cars):
            winsSwitch += 1
        else:
            losesSwitch += 1    
    print winsSwitch, losesSwitch
    pylab.pie([winsSwitch,losesSwitch])
    pylab.show()