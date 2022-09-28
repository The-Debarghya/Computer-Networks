#!/usr/bin/env python3
def nextPowerOf2(num):
    power = 1
    while(power < num):
        power *= 2
    return power

def generateWalshTable(wtable, length, x1, x2, y1, y2, compFlag: bool):
    if length == 2:
        if not compFlag:
            wtable[x1][y1] = 1
            wtable[x1][y2] = 1
            wtable[x2][y1] = 1
            wtable[x2][y2] = -1
        else:
            wtable[x1][y1] = -1
            wtable[x1][y2] = -1
            wtable[x2][y1] = -1
            wtable[x2][y2] = 1
        return
    
    midx = (x1+x2)//2
    midy = (y1+y2)//2
    generateWalshTable(wtable, length/2, x1, midx, y1, midy, compFlag)
    generateWalshTable(wtable, length/2, x1, midx, midy+1, y2, compFlag)
    generateWalshTable(wtable, length/2, midx+1, x2, y1, midy, compFlag)
    generateWalshTable(wtable, length/2, midx+1, x2, midy+1, y2, compFlag)

def getWalshTable(senders):
    n = nextPowerOf2(senders)
    wTable = [[0 for i in range(n)] for j in range(n)]
    if senders == 1:
        return [[1]]
    generateWalshTable(wTable, n, 0, n-1, 0, n-1, False)
    return wTable