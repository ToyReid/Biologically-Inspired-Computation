from sys import argv
import numpy as np
import random
import math

# Number of particles: A typical range is 20 to 40.
# Particle.inertia: Generally the range is [0, 1], typically very close to 1. 
# Particle.cognition and Particle.social parameters: Usually they are nearly equal and typically around 2, but they can range from 0 to 4. 
# World Particle.width and world Particle.height: A good range is –50 to 50 in both directions.
# Maximum velocity: Limits how much a particle can move for a given iteration. Typical values to try are 1, 2, and 10. 

# argv[1] = Particle.epochMax; argv[2] = Particle.numPar; argv[3] = Particle.inertia; argv[4] = Particle.cognition; argv[5] = social

class Particle:
	def __init__(self):
		self.xcur = random.randint(0, 100)
		self.ycur = random.randint(0, 100)
		self.xbest = self.xcur
		self.ybest = self.ycur
		self.xvel = 0
		self.yvel = 0
	
	def update(self):
		# Update velocity
		self.xvel = Particle.inertia * self.xvel + Particle.cognition * random.random() * (self.xbest - self.xcur) \
			+ Particle.social * random.random() * (Particle.xglobal - self.xcur)
		self.yvel = Particle.inertia * self.yvel + Particle.cognition * random.random() * (self.ybest - self.ycur) \
			+ Particle.social * random.random() * (Particle.yglobal - self.ycur)
		# Scale velocity if necessary
		if self.xvel**2 + self.yvel**2 > Particle.maxvel**2:
			self.scalefac = Particle.maxvel / math.sqrt(self.xvel**2 + self.yvel**2)
			self.xvel *= self.scalefac
			self.yvel *= self.scalefac
		
		# Update position
		self.xcur += self.xvel
		self.ycur += self.yvel

		# Update bests
		self.curPer = performance(self.xcur, self.ycur)
		if self.curPer > performance(self.xbest, self.ybest):
			self.xbest = self.xcur
			self.ybest = self.ycur
		
		# Update global best
		if self.curPer > performance(Particle.xglobal, Particle.yglobal):
			Particle.xglobal = self.xcur
			Particle.yglobal = self.ycur

def performance(x, y):
	mdist = math.sqrt(Particle.width**2 + Particle.height**2) / 2
	pdist = math.sqrt((x - 20)**2 + (y - 7)**2)
	ndist = math.sqrt((x + 20)**2 + (y + 7)**2)

	if Particle.problem == 1:
		rv =  100 * (1 - pdist / mdist)
	elif Particle.problem == 2:
		rv = (9 * max(0, 10 - pdist**2)) + (10 * (1 - pdist / mdist)) + (70 * (1 - ndist / mdist))

	return rv

def makePGM(it, population):
	img = np.full((Particle.height, Particle.width), 255)

	count = 1
	
	for p in population:
		print("Particle #{0}".format(count))
		#x = int((Particle.width / 2) + math.floor(p.xcur))
		x = int(math.floor(p.xcur))
		y = int(math.floor(p.ycur))
		#y = int((Particle.height / 2) - math.floor(p.ycur))

		if ((x < Particle.width and x >= 0) and (y < Particle.height and y >= 0)):
			if img[y][x] == 255:
				print("\tp({0}, {1}) = 192".format(x, y))
				img[y][x] = 192
			elif img[y][x] != 0:
				img[y][x] -= 8
				print("\tp({0}, {1}) = {2}".format(x, y, img[y][x]))
		
		count += 1

	with open("test.pgm", 'w') as f:
		f.write("P2\n{0} {1}\n255\n".format(Particle.width, Particle.height))

		for i in img:
			for j in i:
				f.write("{0} ".format(str(j)))
			f.write("\n")

def main():
	bestPer = 0
	population = []

	Particle.epochMax = int(argv[1])
	Particle.numPar = int(argv[2])
	Particle.inertia = float(argv[3])
	Particle.cognition = int(argv[4])
	Particle.social = int(argv[5])
	Particle.maxvel = int(argv[6])
	Particle.problem = 1
	Particle.width = 100
	Particle.height = 100

	for _ in range(Particle.numPar):
		p = Particle()
		population.append(p)

	for p in population:
		curPer = performance(p.xcur, p.ycur)
		if curPer > bestPer:
			Particle.xglobal = p.xcur
			Particle.yglobal = p.ycur
			bestPer = curPer

	# Do first iteration
	for p in population:
		p.update()

	xError = yError = 0
	for p in population:
		xError += (p.xcur - Particle.xglobal)**2
		yError += (p.ycur - Particle.yglobal)**2
	xError = math.sqrt((1 / (2 * Particle.numPar)) * xError)
	yError = math.sqrt((1 / (2 * Particle.numPar)) * yError)
	epoch = 1
	threshold = 0.01
	makePGM(epoch, population)

	while (epoch < Particle.epochMax) and ((xError > threshold) or (yError > threshold)):
		# Update population
		for p in population:
			p.update()

		xError = yError = 0
		for p in population:
			xError += (p.xcur - Particle.xglobal)**2
			yError += (p.ycur - Particle.yglobal)**2
		xError = math.sqrt((1 / (2 * Particle.numPar)) * xError)
		yError = math.sqrt((1 / (2 * Particle.numPar)) * yError)

		epoch += 1
		makePGM(epoch, population)
	
	print("Converged at epoch #{0}".format(epoch))
	print("Error: X({0}) Y({1})\n".format(xError, yError))

if __name__ == '__main__':
	main()
	