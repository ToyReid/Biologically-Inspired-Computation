import aica
import sys
import numpy as np
from PIL import Image

class PNG:
    def ConvertMatrix(self):
        self.converted = np.copy(self.space)
        for _, x in np.ndenumerate(self.converted):
            if x == -1:
                x = 0
            elif x == 1:
                x = 255

    def MatrixToPNG(self):
        im = Image.fromarray(np.uint8(self.converted), 'L')
        im.save("out2/exp{0}/run{1}.png".format(self.exp, self.run))

    def MakeImage(self, space, exp, run):
        self.space = space
        self.exp = exp
        self.run = run
        self.ConvertMatrix()
        self.MatrixToPNG()