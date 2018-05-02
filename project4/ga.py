# pylint: disable=unbalanced-tuple-unpacking

# Toy Reid
# CS420 - Project 4

from sys import argv
import random
import csv

# Set seed for space generation
random.seed(135)

# Args
#	[1]: l = Number of genes (bits) in the genetic string
#	[2]: N = Population size
#	[3]: G = Number of generations
#	[4]: Pm = Mutation probability
#	[5]: Pc = Crossover probability

def MakeArray(l, N):
	tmp = []
	space = []
	nums = [str(0), str(1)]

	for _ in range(N):
		tmp.clear()
		for _ in range(l):
			tmp.append(random.choice(nums))
		space.append(tmp[:])

	return space

def ListToInt(list):
	return int("".join(list), 2)

class GA:
	def __init__(self, l, N, Pm, Pc):
		self.l = int(l)
		self.N = int(N)
		self.Pm = float(Pm)
		self.Pc = float(Pc)
		self.curGen = MakeArray(self.l, self.N)
		self.totalFit = 0
		self.fitness = []
		self.normalFit = []
		self.runningTot = []
		self.offspring = []
		self.avgFitness = 0
		self.maxFitness = 0
		self.numCorrect = 0
		self.par1 = -1
		self.par2 = -1

	def CalcFitness(self):
		for i in self.curGen:
			x = ListToInt(i)
			res = (x / (2**self.l))**10
			self.fitness.append(res) # Fitness function
			self.totalFit += res

	def NormalizeFitness(self):
		self.normalFit = self.fitness[:]
		for _ in range(len(self.normalFit)):
			self.runningTot.append(0)
		running = 0

		for i in range(len(self.normalFit)):
			self.normalFit[i] /= self.totalFit
			running += self.normalFit[i]
			self.runningTot[i] = running
	
	def SelectParents(self):
		num1 = random.random()
		for i in range(len(self.runningTot) - 1):
			if (num1 > self.runningTot[i]) and (num1 <= self.runningTot[i + 1]):
				self.par1 = i + 1
				break
					
		same = True
		while(same):
			num2 = random.random()
			for i in range(len(self.runningTot) - 1):
				if (num2 > self.runningTot[i]) and (num2 <= self.runningTot[i + 1]):
					if (i + 1) != self.par1:
						self.par2 = i + 1
						same = False
						break
					else:
						break
	
	def GenOffspring(self):
		doCrossover = random.random()
		if doCrossover <= self.Pc:
			select = random.randint(0, 29)
			off1 = []
			off2 = []
			off1[:select] = self.curGen[self.par1][:select]
			off2[:select] = self.curGen[self.par2][:select]
			off1[select:] = self.curGen[self.par1][select:]
			off2[select:] = self.curGen[self.par2][select:]
			self.offspring.append(off1)
			self.offspring.append(off2)
		elif self.Pc == 0:
			self.offspring.append(self.curGen[self.par1])
			self.offspring.append(self.curGen[self.par2])
		else:
			self.offspring.append(self.curGen[self.par1])
			self.offspring.append(self.curGen[self.par2])

	def MutateAndReplace(self):
		for i in range(self.N):
			for j in range(self.l):
				doMut = random.random()
				if(doMut <= self.Pm):
					#print("i = {0}, j = {1}".format(i, j))
					#print("offspring[{0}] size = {1}".format(i, len(self.offspring[i])))
					self.offspring[i][j] = str(1 - int(self.offspring[i][j])) # Flip bit
				
		self.curGen = self.offspring[:]
		#print("Sizeof offspring = {0}".format(len(self.offspring)))
		self.offspring.clear()

	def CalculateStats(self):
		# Average and Max Fitness
		sum = 0
		max = 0
		for i, val in enumerate(self.fitness):
			sum += val
			if val > max:
				max = val
				self.maxFitness = val
				self.maxIndiv = i
		self.avgFitness = sum / self.N

		# Num. Correct Bits
		self.numCorrect = 0
		for val in self.curGen[self.maxIndiv]:
			if val == '1':
				self.numCorrect += 1

		#print("Average Fitness = {0}, Max Fitness = {1}, Num. Correct = {2}".format(self.avgFitness, self.maxFitness, self.numCorrect))

	def Reset(self):
		self.par1 = -1
		self.par2 = -1
		self.avgFitness = 0
		self.maxFitness = 0
		self.numCorrect = 0
		self.totalFit = 0
		self.fitness = []
		self.normalFit = []
		self.runningTot = []
		self.offspring = []
		
	def CsvOut(self):
		# Fitness, Normalized Fitness, Running Total
		# rows = zip(self.fitness, self.normalFit, self.runningTot)
		# with open("output2.csv", "w") as f:
		# 	writer = csv.writer(f)
		# 	f.write("Fitness,Normalized,Running\n")
		# 	for row in rows:
		# 		writer.writerow(row)

		with open(argv[6], "a") as f:
			#writer = csv.writer(f)
			f.write("{0},{1},{2}\n".format(self.avgFitness, self.maxFitness, self.numCorrect))
			

def main():
	with open(argv[6], "w") as f:
		#writer = csv.writer(f)
		f.write("l = {0},N = {1},G = {2},Pm = {3},Pc = {4}\n\n".format(\
			argv[1], argv[2], argv[3],argv[4], argv[5]))
		f.write("Average Fitness,Best Fitness,Correct Bits\n")

	runs = 10
	for i in range(runs):
		g = GA(argv[1], argv[2], argv[4], argv[5])
		with open(argv[6], "a") as f:
			f.write("Run {0}\n".format(i + 1))
		print("Run {0}".format(i + 1))
		for _ in range(int(argv[3])):
			g.CalcFitness()
			g.NormalizeFitness()
			for _ in range(g.N // 2):
				#print("Num gens / 2 = {0}".format(g.N // 2))
				g.SelectParents()
				#print("Parent 1 = {0}, Parent 2 = {1}".format(g.par1, g.par2))
				g.GenOffspring()
			g.MutateAndReplace()
			g.CalculateStats()
			g.CsvOut()
			g.Reset()
		with open(argv[6], "a") as f:
			f.write("\n")

if __name__ == '__main__':
	main()
	