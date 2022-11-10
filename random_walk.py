#!/usr/bin/python

"""Random walks in 2D space"""

###
# Walkers walk either north, south, east or west by increments of 1.
# More advanced version would be of walkers walking in any direction by any length of step.
###

import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Walker(object):
    """
    A class used to represent a walker
        Attributes:
        name : str
            the name of the walker
        location : (x, y)
            current location of the walker, initialized with  with None
    """ 
    
    def __init__(self, name = None):
        self.name = name
        self.source = None
        self.location = None

    def __str__(self):
        desc = []
        if self.name != None:
            desc.append(self.name)
        else:
            desc.append("Nameless")
        if self.location != None:
            x, y = self.location
            desc.append("at (" + str(x) + ", " + str(y) + ")")
        else:
            desc.append("with no location")
        return " ".join(desc)

    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def takeStep(self):
        """Take a random step of length 1 north, south, east or west
            Returns walker's location after taking a step
        """
        step_choice = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        step = random.choice(step_choice)   # randomply select direction
        x, y = self.location
        dx, dy = step
        x = x + dx
        y = y + dy
        self.setLocation(x, y)              # update current location
        return self.getLocation()

    def setLocation(self, x, y):
        self.location = (x, y)

class Field(object):
    """
    A class used to represent 2D field with walkers for random walks.
        Attributes:
        walkers : dict
            walkers in the field
            keys: walkers (type Walker), values: paths (type list of coordinates (x, y))
    """
    
    def __init__(self):
        self.walkers = {}

    def __str__(self):
        field_state = []
        for w in self.walkers:
            temp = []
            temp.append(str(w))
            temp.append("traveled the distance of length")
            temp.append(str(self.getDistance(w.getName())))
            field_state.append(" ".join(temp))
        return "\n".join(field_state)

    def getWalker(self, name):
        for w in self.walkers:
            if w.getName() == name:
                return w
        return None

    def getAllWalkersNames(self):
        walkers = self.walkers.keys()
        names = []
        for w in walkers:
            names.append(w.getName())
        return names

    def addWalker(self, name, source):
        """Adds walker (type Walker) to the field with location source
            name : str
            source : tuple of coordinates (x, y)
                source location in the field
        """
        w = Walker(name)
        s_x, s_y = source
        w.setLocation(s_x, s_y)
        self.walkers[w] = [source]        # initialize path to include starting point

    def generateWalkersName(self):
        """Generates a name for a walker of length no more than 10"""
        name_First = "ABCDEFGHIJKLMNOPQRSTUWXYZ"
        name = "abcdefghijklmnopqrstuwxyz"
        while(True):
            name_length = math.floor(1 + random.random() * 10)
            name = [random.choice(name) for letter_no in range(name_length)]
            name.append(random.choice(name_First))
            name.reverse()
            name = "".join(name)
            if self.getWalker(name) is None:
                return name

    def generateWalkers(self, number, source):
        """Generates number of walkers in the field starting at source"""
        for w in range(number):
            self.addWalker(self.generateWalkersName(), source)

    def moveWalker(self, name):
        """Moves the walker one step in random direction"""
        w = self.getWalker(name)
        self.walkers[w].append(w.takeStep())    # update walked path

    def getDistance(self, name):
        """Return distance walked from the source"""
        w = self.getWalker(name)
        s_x, s_y = self.walkers[w][0]           # get the source of the walk
        d_x, d_y = self.walkers[w][-1]          # get the destination of the walk
        return np.sqrt((d_x - s_x)**2 + (d_y - s_y)**2)

    def meanDistance(self):
        dist = []
        for w in self.walkers:
            dist.append(self.getDistance(w.getName()))
        return np.mean(dist)

    def resetWalkersPaths(self, source):
        s_x, s_y = source
        for w in self.walkers:
            w.setLocation(s_x, s_y)
            self.walkers[w] = [source]

class UpdateMean:
    #TODO more walkers with every frame
    #how many walkers / frames until mean value for distance starts to converge?
    def __init__(self, ax, field, steps, source):
        self.points = ax.scatter(1, 0)
        self.field = field
        self.steps = steps
        self.source = source
    def __call__(self, i):
        # walkers do random walks
        self.field.resetWalkersPaths(source)
        for s in range(self.steps):
            for w in self.field.getAllWalkersNames():
                self.field.moveWalker(w)
        mean_distance = self.field.meanDistance()
        return self.points.set_offsets((mean_distance, 0))

# create a field with no walkers
f = Field()

# add some walkers to the field
#walkers = ["Dorothy", "Wizard of Oz", "Tin Man", "Scarecrow"]
#source = (0, 0)
#for w in walkers:
#    f.addWalker(w, source)
no_of_walkers = 10
source = (0, 0)
f.generateWalkers(no_of_walkers, source)

#trials = [10**x for x in range(1, 5)]
#mean_distance_traveled = []
#for steps in trials:
#    print("A trial with " + str(steps) + " steps:")
#    for s in range(steps):
#        for w in f.getAllWalkersNames():
#            f.moveWalker(w)
#    print(f)
#    print(f.meanDistance())
#    f.resetWalkersPaths()

# mean convergence animation
fig, ax = plt.subplots()                                    # create a plot
ax.set_xlim([0, 100])
ax.set_ylim([-0.5, 1])
um = UpdateMean(ax, f, 100, source)
anim = FuncAnimation(fig, um, repeat = False, frames = 100)  # repeat animation for 10 frames
plt.show()                                                  # show current plot

#TODO how often walkers meet?
#TODO walkers changing color when they meet
#TODO generating many more walkers
#TODO plotting walk (animation)
#TODO plotting distances and mean (animation)
#TODO how many walkers it takes for the mean distance to converge?
