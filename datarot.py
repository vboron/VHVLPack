#!/usr/bin/python3
import os
import sys
import math
import argparse
import pandas as pd

# -----------------------------------------------------------------------
# Defaults
m = 0.285
c = -32.477
dataFile = "Everything/Everything_NR2_GBReg.csv"

# -----------------------------------------------------------------------
# Defines
SMALL = 0.001  # Angle close enough to zero we don't need to rotate


# -----------------------------------------------------------------------
def FindIntersection(m1, c1, m2, c2):
    """
       Takes the equations for 2 lines and finds the intersection
       Returns the intersection (x,y) and a Boolean flag to indicate
       that they did indeed intersect

       Line 1: y=m1*x + c1
       Line 2: y=m2*x + c2

       When y matches,
       m1*x + c1 = m2*x + c2
       So...
       m1*x - m2*x = c2 - c1
       x(m1-m2) = c2 - c1
       x = (c2-c1)/(m1-m2)

       and
       y = m1*x + c1
    """

    if(abs(m1-m2) < SMALL):
        return(0.0, 0.0, False)

    x = (c2-c1)/(m1-m2)
    y = m1*x + c1

    return(x, y, True)

# -----------------------------------------------------------------------


def TranslateDataPoint(x, y, transX, transY):
    x = x + transX
    y = y + transY
    return(x, y)


# -----------------------------------------------------------------------
def TranslateDataArrays(xData, yData, ndata, transX, transY):
    """
       Takes x and y data arrays, the number of items and an x and y
       translation. Applies the translation to each data point and
       returns the new arrays
    """
    for i in range(ndata):
        (xData[i], yData[i]) = TranslateDataPoint(xData[i], yData[i],
                                                  transX,   transY)
    return(xData, yData)


# -----------------------------------------------------------------------
def FindAngle(m1, m2):
    """
       Finds the angle between two lines based on their slopes.
       Returns the angle (0.0 if the slopes are the same)

       $ tan(\theta) = (m1-m2)/(1 + m1*m2) $
    """
    if(abs(m1-m2) < SMALL):
        return(0.0)

    tanTheta = (m1-m2)/(1 + m1*m2)
    return(math.atan(tanTheta))

# -----------------------------------------------------------------------


def RotateDataPoint(x, y, theta):
    xNew = x * math.cos(theta) - y * math.sin(theta)
    yNew = x * math.sin(theta) + y * math.cos(theta)
    return(xNew, yNew)


# -----------------------------------------------------------------------
def RotateDataArray(xData, yData, nData, theta):
    """
       Takes two arrays of (2D) data points, the number of points and an angle.
       Rotates each data 2D point about the origin by the specified angle
    """

    for i in range(nData):
        (xData[i], yData[i]) = RotateDataPoint(xData[i], yData[i], theta)
    return(xData, yData)

# -----------------------------------------------------------------------


def CorrectAndPrintDataFile(dataFile, m, c):
    df = pd.read_csv(dataFile)
    
    ndata = df. iloc[:, 0].count()
    xData = df['angle'].tolist()
    xDataOrig = df['angle'].tolist()
    yData = df['predicted'].tolist()

    # for i in range(ndata):
    #     print("%f,%f" % (xData[i], yData[i]))

    intersectX, intersectY, ok = FindIntersection(m, c, 1, 0)
    if(ok):
        xData, yData = TranslateDataArrays(yData, yData, ndata,
                                            -intersectX, -intersectY)
        angle = FindAngle(m, 1)
        xData, yData = RotateDataArray(xData, yData, ndata, -angle)
        xData, yData = TranslateDataArrays(xData, yData, ndata,
                                            intersectX, intersectY)

    # print("Int: %.3f %.3f" % (intersectX, intersectY))
    # print("Ang: %.3f" % (180.0 * angle / math.pi))

    # print("Rotated Data:")
    # for i in range(ndata):
    #     print("%f,%f" % (xData[i], yData[i]))
    data = []
    # print("Rotated Y Data (X original):")
    for i in range(ndata):
        # print("%f,%f" % (xDataOrig[i], yData[i]))
        error = yData[i] - xDataOrig[i]
        data.append([xDataOrig[i], yData[i], error])
    df2 = pd.DataFrame(data, columns=['angle', 'predicted', 'error'])
    return df2

# -----------------------------------------------------------------------


def CorrectDataPoint(x, y, m, c, useOrigX):
    xOrig = x

    intersectX, intersectY, ok = FindIntersection(m, c, 1, 0)
    if(ok):
        x, y = TranslateDataPoint(x, y, -intersectX, -intersectY)
        angle = FindAngle(m, 1)
        x, y = RotateDataPoint(x, y, -angle)
        x, y = TranslateDataPoint(x, y,  intersectX,  intersectY)

        if(useOrigX):
            return(xOrig, y)
        return(x, y)

# -----------------------------------------------------------------------


def CorrectAndPrintDataPoint(x, y, m, c, useOrigX):
    x, y = CorrectDataPoint(x, y, m, c, useOrigX)
    # print("%f %f" % (x, y))


# -----------------------------------------------------------------------
# Main program

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--slope", dest="m", default=m, type=float,
                        help="Slope of best-fit line")
    parser.add_argument("-c", "--intercept", dest="c", default=c, type=float,
                        help="Y intercept of best-fit line")
    parser.add_argument("--dataFile", nargs='?', default=dataFile)
    parser.add_argument("-Y",           nargs='?', default='undef')
    parser.add_argument("-x", type=float,
                        help='the x value used for the prediction')
    parser.add_argument("-o", help='dataframe output name')

    args = parser.parse_args()
    m = args.m
    c = args.c
    x = 0.0
    y = 0.0

    if(args.Y == "undef"):
        dataFile = args.dataFile
    else:
        dataFile = ''
        x = float(args.x)
        y = float(args.Y)

#   print("datafile: " + dataFile)
#   print("X: " + str(x))
#   print("Y: " + str(y))

    if(dataFile == ''):
        CorrectAndPrintDataPoint(x, y, m, c, True)
    else:
        CorrectAndPrintDataFile(dataFile, m, c).to_csv(args.o, index=False)
        
