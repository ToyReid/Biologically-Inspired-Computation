import aica
import png
import csv
import numpy as np
import sheet
from sys import argv

# pylint: disable=E0632
#script, h, J1, J2, R1, R2, numIts = argv
script, numIts = argv

# Experiment 1
# harr  = [-1, -1, -2]
# R1arr = [ 1,  3,  6]
# R2arr = [15, 15, 15]
# J1arr = [ 1,  1,  1]
# J2arr = [0,  0,  0]

# Experiment 2
# harr  = [0, -2, -1, 0, -5, -3, 0, 0,  0, 0, -5, -3, 0,  0, -6, -3,  0]
# R1arr = [1,  1,  1, 1,  1,  1, 1, 1,  1, 4,  4,  4, 4,  4,  9,  9,  9]
# R2arr = [2,  4,  4, 4,  6,  6, 6, 9, 13, 5,  7,  7, 7, 12, 12, 12, 12]
# J1arr = [0,  0,  0, 0,  0,  0, 0, 0,  0, 0,  0,  0, 0,  0,  0,  0,  0]
# J2arr = [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1]

# Experiment 3
harr  = [0, -4, -2, 0, 2,  4, -6, -3, 0, 3, 6, -6, -3,  0,  3,  6, -1, 0, 1, -6, -3, 0, 3, 6, -6, -3,  0,  3,  6, -1, 0, 1, -3,  0,  3, -2,  0,  2]
R1arr = [1,  1,  1, 1, 1,  1,  1,  1, 1, 1, 1,  1,  1,  1,  1,  1,  3, 3, 3,  3,  3, 3, 3, 3,  3,  3,  3,  3,  3,  7, 7, 7,  7,  7,  7, 12, 12, 12]
R2arr = [2,  5,  5, 5, 5,  5,  9,  9, 9, 9, 9, 14, 14, 14, 14, 14,  5, 5, 5,  9,  9, 9, 9, 9, 14, 14, 14, 14, 14,  9, 9, 9, 14, 14, 14, 14, 14, 14]
J1arr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
J2arr = [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1]

if __name__ == "__main__":
    np.set_printoptions(linewidth=150, precision=5)

    numIts = int(numIts)
    img = png.PNG()
    html = sheet.HTMLout()

    csvfile = open('out3/output2.csv', 'w', newline='')
    csvOut = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
    html.StartHTML()

    for i in range(0, len(R1arr)):
        print("\nOn run #{0}".format(i))
        if i == 6:
            break
        info = aica.Info(harr[i], J1arr[i], J2arr[i], R1arr[i], R2arr[i])
        average = aica.AvActIn(info)
        
        csvOut.writerow(['Run'] + ['J1'] + ['J2'] + ['h'] + ['R1'] + ['R2'])
        csvOut.writerow([i] + [info.J1] + [info.J2] + [info.h] + [info.R1] + [info.R2])
        csvOut.writerow([''])

        for j in range(0, numIts):
            print("Image #{0}".format(j))
            actin = aica.ActIn(info)
            actin.RandArray()
            space = actin.UpdateSpace()
            img.MakeImage(space, i, j)
            actin.CalculateAll()

            average.AddVals(actin)
            actin.Reset()
        
        html.AddToHTML(i, numIts, info)
    
        average.GetAvg(numIts)
        average.Print()

        csvOut.writerow(['entropy:'] + [average.entropy] + [' '] + ['lambda:'] + [average.lamb])
        csvOut.writerow([' '] + [0] + [1] + [2] + [3] + [4] + [5] + [6] + [7] + [8] + [9] + [10] + [11] + [12] + [13] + [14])
        csvOut.writerow(['rho_l:'] + [average.distCorr[0]] + [average.distCorr[1]] + [average.distCorr[2]]\
            + [average.distCorr[3]] + [average.distCorr[4]] + [average.distCorr[5]] + [average.distCorr[6]]\
            + [average.distCorr[7]] + [average.distCorr[8]] + [average.distCorr[9]] + [average.distCorr[10]]\
            + [average.distCorr[11]] + [average.distCorr[12]] + [average.distCorr[13]] + [average.distCorr[14]])
        csvOut.writerow(['H_l:'] + [average.jointEnt[0]] + [average.jointEnt[1]] + [average.jointEnt[2]]\
            + [average.jointEnt[3]] + [average.jointEnt[4]] + [average.jointEnt[5]] + [average.jointEnt[6]]\
            + [average.jointEnt[7]] + [average.jointEnt[8]] + [average.jointEnt[9]] + [average.jointEnt[10]]\
            + [average.jointEnt[11]] + [average.jointEnt[12]] + [average.jointEnt[13]] + [average.jointEnt[14]])
        csvOut.writerow(['I_l:'] + [average.mutInf[0]] + [average.mutInf[1]] + [average.mutInf[2]]\
            + [average.mutInf[3]] + [average.mutInf[4]] + [average.mutInf[5]] + [average.mutInf[6]]\
            + [average.mutInf[7]] + [average.mutInf[8]] + [average.mutInf[9]] + [average.mutInf[10]]\
            + [average.mutInf[11]] + [average.mutInf[12]] + [average.mutInf[13]] + [average.mutInf[14]])
        csvOut.writerow([''])
        csvOut.writerow([''])

    html.EndHTML()