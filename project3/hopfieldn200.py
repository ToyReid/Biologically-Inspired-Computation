import random
import numpy as np

numNeurons = 200

class Network:
	def __init__(self):
		self.patterns = np.zeros((50, numNeurons), int)
		self.weights = np.zeros((numNeurons, numNeurons), float)
		self.net = np.zeros(numNeurons, int)
		self.stableCount = np.zeros(50, int)
		self.unstableCount = np.zeros(50, int)
		
	def RandVector(self):
		nums = [-1, 1]

		for i in range(len(self.patterns)):
			for j in range(len(self.patterns[0])):
				self.patterns[i, j] = random.choice(nums)

	def Imprint(self, p):
		for i in range(len(self.weights)):
			for j in range(len(self.weights[0])):
				sum = 0
				if i == j:
					self.weights[i][j] = 0
				else:
					for k in range(p):
						sum += self.patterns[k][i] * self.patterns[k][j]
					self.weights[i][j] = float(sum / numNeurons)
	
	def TestStability(self, p):
		usCount = 0
		for k in range(p):
			self.net = self.patterns[k]
			for i in range(len(self.net)):
				localfield = 0
				for j in range(len(self.net)):
					localfield += self.weights[i][j] * self.net[j]
				if localfield < 0:
					newState = -1
				else:
					newState = 1
				if self.net[i] != newState:
					usCount += 1
					break
		self.stableCount[p - 1] += p - usCount
		self.unstableCount[p - 1] += usCount
		

	def Print(self):
		print(self.stableCount)
		print(self.unstableCount)

def main():
	avgStableCount = np.zeros(50, float)
	avgUnstableCount = np.zeros(50, float)
	avgStableProb = np.zeros(50, float)
	avgUnstableProb = np.zeros(50, float)
	numRuns = 100

	for i in range(numRuns):
		print("Run #{0}".format(i + 1))
		n = Network()
		n.RandVector()
		for p in range(1, len(n.patterns) + 1):
			n.Imprint(p)
			n.TestStability(p)
		for j in range(len(n.stableCount)):
			avgStableCount[j] += n.stableCount[j]
			avgUnstableCount[j] += n.unstableCount[j]
		#n.Print()
	
	for i in range(len(avgStableCount)):
		avgStableProb[i] = avgStableCount[i] / numRuns
		avgUnstableProb[i] = avgUnstableCount[i] / numRuns

	with open('output50.csv', 'ab') as f:
		np.savetxt(f, avgStableCount, delimiter=',')
		np.savetxt(f, avgUnstableCount, delimiter=',')
		np.savetxt(f, avgStableProb, delimiter=',')
		np.savetxt(f, avgUnstableProb, delimiter=',')

if __name__ == '__main__':
	main()
	