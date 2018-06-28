#!/bin/python3

frames  = [
[28.47, 137.70, 183.14, 211.43],
[48.28, 115.76, 153.75, 202.67],
[124.36, 193.92, 68.10, 93.82],
[94.98, 185.17, 87.91, 71.88],
[107.72, 49.94, 65.59, 176.42],
        ]


#!/bin/python3

import math
import os
import random
import re
import sys
from decimal import *

class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    def __init__(self, x, y):
        '''Defines x and y variables'''
        self.X = x
        self.Y = y
    def move(self, dx, dy):
        '''Determines where x and y move'''
        self.X = self.X + dx
        self.Y = self.Y + dy
    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y)
    def __eq__(self, other):
        return self.X==other.X and self.Y==other.Y
    def getX(self):
        return self.X
    def getY(self):
        return self.Y
    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return math.sqrt(dx**2 + dy**2)
    def change(self,other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return Point(dx,dy)
    def __hash__(self):
        return hash(self.X)+32*hash(self.Y)
def computePairChange(pointList):
    changeBetweenFrames = []
    for i in range(0,len(pointList)-1):
        #distance between all other pairs for every point in frame
        frameDists = []
        for point in pointList[i]:
            #distance for this pair to all other pairs
            pointDists=[]
            if(i+1<len(pointList)):
                for toCompare in pointList[i+1]:
                    pointDists.append(point.change(toCompare))
            frameDists.append(pointDists)
        changeBetweenFrames.append(frameDists)
    return changeBetweenFrames

def solve(blimps,frames):
    getcontext().prec = 3
    pointsInFrames= []
    for frame in frames:
        pointsInCurFrame = []
        for i in range(0,len(frame)-1,2):
            pointsInCurFrame.append(Point(Decimal(frame[i]),Decimal(frame[i+1])))
        pointsInFrames.append(pointsInCurFrame)
    changeBetweenFrames = computePairChange(pointsInFrames)
    #changeBetweenFrames now has distance between every frame
    #the one that stays the same is the correct one
    rateOfChangePerBlimp = []
    for i in range(0, blimps):
        maxPresent = 1
        seenDistances={}
        canditeChange = None
        #first get candidate changes
        for change in changeBetweenFrames[0][i]:
            seenDistances[change] = 1
        for k in range(1,len(changeBetweenFrames)):
            for changes in changeBetweenFrames[k]:
                for change in changes:
                    if change in seenDistances and change not in rateOfChangePerBlimp:
                        seenDistances[change] += 1
                        newPresentCount = seenDistances[change]
                        if(newPresentCount>maxPresent):
                            canditeChange = change
                            maxPresent = newPresentCount
                    else:
                        seenDistances[change] = 1
        rateOfChangePerBlimp.append(canditeChange)
    #now build our string
    valPerIndex = [[0 for i in range(0,int(blimps))] for i in range(0,len(frames))]
    rateOfChangeMap = {}
    for i in range(0,len(rateOfChangePerBlimp)):
        valPerIndex[0][i] = rateOfChangeMap[rateOfChangePerBlimp[i]] = i

    for i in range(1,len(frames)):
        for k in range(0,len(changeBetweenFrames[i-1])):
            for j in range(0,len(changeBetweenFrames[i-1][k])):#point in changeBetweenFrames[i-1][k]:
                if changeBetweenFrames[i-1][k][j] in rateOfChangePerBlimp:
                    valPerIndex[i][j] = rateOfChangeMap[changeBetweenFrames[i-1][k][j]]
    for row in valPerIndex:
        string =""
        for val in row:
            string = string + str(val) + " "
        print(string.strip())
    return

if __name__ == '__main__':
    num_framesDetections_per_frame = [2,5]#input().split()

    num_frames = int(num_framesDetections_per_frame[0])

    detections_per_frame = int(num_framesDetections_per_frame[1])

    detection_components = []

    #for _ in range(num_frames):
     #   detection_components.append(list(map(float, input().rstrip().split())))
   # print(num_framesDetections_per_frame[0]+' '+num_framesDetections_per_frame[1])
    solve(num_framesDetections_per_frame[0],frames)