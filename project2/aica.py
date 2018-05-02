import numpy as np
import random
from itertools import product
from sys import argv
import math

# Args = J1, J2, h, R1, R2, ID
# J1/J2 = Interaction strengths
# R1/R2 = Interaction ranges
# h = bias parameter
# r_ij = distance between cells i and j

class Info:
    def __init__(self, h, J1, J2, R1, R2):
        self.h = h
        self.J1 = J1
        self.J2 = J2
        self.R1 = R1
        self.R2 = R2

class AvActIn:
    def __init__(self, info):
        self.h = info.h
        self.J1 = info.J1
        self.J2 = info.J2
        self.R1 = info.R1
        self.R2 = info.R2
        self.entropy = 0
        self.distCorr = [float(0)] * 15
        self.jointEnt = [float(0)] * 15
        self.mutInf   = [float(0)] * 15
        self.lamb     = []
    def AddVals(self, aica):
        self.entropy += aica.entropy
        self.distCorr = np.add(self.distCorr, aica.distCorr)
        self.jointEnt = np.add(self.jointEnt, aica.jointEnt)
        self.mutInf   = np.add(self.mutInf, aica.mutInf)
        self.lamb.append(aica.lamb)
    def GetAvg(self, numIts):
        self.entropy /= numIts
        self.distCorr = np.divide(self.distCorr, numIts)
        self.jointEnt = np.divide(self.jointEnt, numIts)
        self.mutInf   = np.divide(self.mutInf, numIts)
        self.lamb     = np.average(self.lamb)
    def Print(self):
        print("Entropy              = {0}".format(self.entropy))
        print("Distance Correlation = {0}".format(self.distCorr))
        print("Joint Entropy        = {0}".format(self.jointEnt))
        print("Mutual Information   = {0}".format(self.mutInf))
        print("Correlation Length   = {0}".format(self.lamb))

class ActIn:
    def __init__(self, info):
        self.h = info.h
        self.J1 = info.J1
        self.J2 = info.J2
        self.R1 = info.R1
        self.R2 = info.R2
        self.entropy = 0
        self.changed = True # Used to detect changes in state
        self.space = np.zeros((30,30), int)
        self.distCorr = [float(0)] * 15
        self.jointEnt = [float(0)] * 15
        self.posConv  = [float(0)] * 15
        self.negConv  = [float(0)] * 15
        self.mutInf   = [float(0)] * 15
        self.firstSumArr = [float(0)] * 15

        #self.updated = np.zeros((30,30), bool)
    
    def Reset(self):
        self.entropy = 0
        self.changed = True # Used to detect changes in state
        self.space = np.zeros((30,30), int)
        self.distCorr = [float(0)] * 15
        self.jointEnt = [float(0)] * 15
        self.posConv  = [float(0)] * 15
        self.negConv  = [float(0)] * 15
        self.mutInf   = [float(0)] * 15

    def RandArray(self):
        nums = [-1, 1]
        for i in range(len(self.space)):
            for j in range(len(self.space[0])):
                #self.updated[i, j] = False
                self.space[i, j] = random.choice(nums)

    def CalcDistance(self, i, j):
        x = abs(i[0] - j[0])
        if x > 15:
            x = 30 - x
        y = abs(i[1] - j[1])
        if y > 15:
            y = 30 - y
        return x + y

    def Find(self, coord):
        return self.space[coord[0], coord[1]]

    def UpdateCell(self, i):
        near = 0
        far = 0

        for j, x in np.ndenumerate(self.space):
            if i != j:
                dist = self.CalcDistance(i, j)
                if dist < self.R1:
                    near += x
                if self.R1 <= dist and dist < self.R2:
                    far += x

        total = float(self.h) + float(self.J1) * float(near) + float(self.J2) * float(far)

        if total >= 0:
            if self.space[i] == -1:
                self.changed = True
            self.space[i] = 1
        elif total < 0:
            if self.space[i] == 1:
                self.changed = True
            self.space[i] = -1

    def UpdateSpace(self):
        # Generate cartesian product of all coordinates
        coords = list(product(range(30), range(30)))

        while(self.changed == True):
            self.changed = False
            uniques = random.sample(coords, len(coords))

            for it in uniques:
                self.UpdateCell(it)

        return self.space
    
    def CalcCorrelation(self):
        secondSum = 0
        for i, x in np.ndenumerate(self.space):
            secondSum += x

            for j, y in np.ndenumerate(self.space):
                # Prevent duplicates
                if i[0] > j[0] or (i[0] == j[0] and j[1] < i[1]):
                    continue
                dist = self.CalcDistance(i, j)
                if dist < 15:
                    self.firstSumArr[dist] += (x * y)
                    self.posConv[dist] += ((x + 1) / 2) * ((y + 1) / 2)
                    self.negConv[dist] += ((-1 * x + 1) / 2) * ((-1 * y + 1) / 2)

        self.distCorr[0] = abs(float(1 - ((1 / 30**2) * secondSum)**2))
        #print("distCorr[0] = %.12f" % (self.distCorr[0]))

        for l in range(1, 15):
            self.distCorr[l] = abs(((2/(30**2 * 4 * l)) * self.firstSumArr[l]) - ((1/30**2) * secondSum)**2)
            #print("distCorr[%d] = %.12f" % (l, self.distCorr[l]))

    def CalcLambda(self):
        close = self.distCorr[0] / math.exp(1)
        min = 100
        self.lamb = 0

        for l in range(1, 15):
            find = abs(self.distCorr[l] - close)
            if find < min:
                min = find
                self.lamb = l
        #print("Lambda = {0}".format(self.lamb))
    
    def CalcEntropy(self):
        sumConv = 0

        for _, s in np.ndenumerate(self.space):
            sumConv += (s + 1) / 2

        posProb = sumConv / 30**2
        negProb = 1 - posProb

        if posProb == 0 and negProb == 0:
            self.entropy = 0
        elif posProb == 0:
            self.entropy = -(negProb * math.log(negProb))
        elif negProb == 0:
            self.entropy = -(posProb * math.log(posProb))
        else:
            self.entropy = -(posProb * math.log(posProb) + negProb * math.log(negProb))
        
        #print("entropy = %.12f" % self.entropy)

    def CalcJointEnt(self):
        for l in range(1, 15):
            posProb = (2 / (30**2 * l * 4)) * self.posConv[l]
            negProb = (2 / (30**2 * l * 4)) * self.negConv[l]
            mixed = 1 - posProb - negProb

            if posProb == 0:
                posResult = 0
            else:
                posResult = posProb * math.log(posProb)
            if negProb == 0:
                negResult = 0
            else:
                negResult = negProb * math.log(negProb)
            if mixed <= 0:
                mixResult = 0
            else:
                mixResult = mixed * math.log(mixed)
            
            self.jointEnt[l] = -1 * (posResult + negResult + mixResult)
            #print("jointEnt[%d] = %f" % (l, self.jointEnt[l]))
        #print("Joint Entropy")

    def CalcMI(self):
        for l in range(0, 15):
            self.mutInf[l] = 2 * self.entropy - self.jointEnt[l]
            #print("mutInf[%d] = %f" % (l, self.mutInf[l]))
        #print("Mutual Information")

    def CalculateAll(self):
        self.CalcCorrelation()
        self.CalcEntropy()
        self.CalcJointEnt()
        self.CalcMI()
        self.CalcLambda()