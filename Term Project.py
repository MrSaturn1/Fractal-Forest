#TERM PROJECT
#Fractal Forest

from tkinter import *
import math
import random

#getPlayerBounds, movePlayer, run function adapted from 15-112 sidescroller demo

def init(data):
    #scrolling
    data.scrollX = 0  # amount view is scrolled to the right
    data.scrollMargin = data.width//2 # closest player may come to either canvas edge
    #player
    data.playerX = data.scrollMargin # player's left edge
    data.playerY = 0  # player's bottom edge (distance above the base line)
    data.playerWidth = 10
    data.playerHeight = 20
    data.walkFrame = 1
    #pyramid
    data.colorList = ["red","yellow","blue"]
    data.pyramidLevel = 1
    data.deathTimer = 0
    #balls
    data.balls = []
    data.ballWidth = 5
    data.ballSpeed = 20
    #general
    data.counter = 0
    data.timer = 0
    data.mode = "splash"
    
    #bird
    data.birdWidth = 10
    data.birdHeight = 8
    data.birdSpeeds = []
    data.birdList = []
    data.stars = []
    data.birdAnimations = []
    data.birdDirs = []
    data.left = True
    data.birdsDown = []
    data.birdScore = 0
    
    #snowflakes
    data.top = True
    data.snowNum = 30
    data.snowflakes = []
    data.snowLevels = []
    data.snowSpeeds = []
    data.snowSizes = []
    data.snowDirs = []
    data.fallColors = ["indian red", "orange", "salmon4", "dark khaki"]
    data.fallColorList = []
    for i in range(data.snowNum):
        data.snowflakes.append((random.randint(0, data.width), random.randint(0, data.height)))
        data.snowLevels.append(random.randint(0,1))
        data.snowSpeeds.append(0)
        data.snowSizes.append(random.randint(3, 7))
        data.snowDirs.append(random.randint(6,10))
        data.fallColorList.append(data.fallColors[random.randint(0,3)])
    #seasons
    data.seasonTimer = 0
    data.season = "spring"#spring
    data.seasonList = ["spring", "summer", "fall", "winter"]
    data.backgroundColor = "light yellow"
    #tree
    data.tree3FallColor = "indian red"
    data.treeFallColor = "orange"
    data.treeNum = 50
    data.levels = []
    data.dirs = []
    data.posns = []
    data.angle = 0
    data.angleChanges = []
    data.lengths = []
    data.lineWidths = []
    data.treeType = []
    for i in range(data.treeNum):
        data.levels.append(random.randint(1,6))
        data.dirs.append(-math.pi/2 + random.randint(-1, 1)/40)
        data.posns.append((data.width//2 + random.randint(-2400, 2400), 3*data.height//4))
        data.treeType.append(random.randint(1,2))
        data.angleChanges.append(random.randint(10, 33)/100)
        data.lengths += [random.randint(300, 700)]
        data.lineWidths.append(random.randint(1,4))
    #falling leaves
    data.leaves = []
    data.curTree = []
    data.leafIndex = -1
    data.curColor = ""
    data.leafColors = []
    data.leafSpeed = 10
    data.curSize = 3
    data.leafSizes = []
    

#####################################################
#SPLASH SCREEN
#####################################################

def redrawAllSplash(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="PaleTurquoise1")
    makeTree(canvas, data, 8, 0, .29, 480, (data.width//2, 3*data.height//4 - 25), -math.pi/2, 2)
    canvas.create_text(data.width//2, 3*data.height//4, text="FRACTAL FOREST", font=("Times", 60))
    canvas.create_text(data.width//2, 3*data.height//4 + 50, text="By Ian Sears", font=("Times", 40))
    canvas.create_text(data.width//2, 3*data.height//4 + 100, text="Press 'Space' to Start, 'h' For Help", font=("Times", 40))

def timerFiredSplash(data):
    pass

def mousePressedSplash(event, data):
    pass

def keyPressedSplash(event, data):
    if event.keysym == "space":
        data.mode = "forest"
    elif event.keysym == "h":
        data.mode = "help"
        
#####################################################
#HELP
#####################################################

def redrawAllHelp(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="PaleTurquoise1")
    canvas.create_text(data.width//2, data.height//4, text="Press 'Space' to shoot at the birds.", font=("Times", 30))
    canvas.create_text(data.width//2, data.height//3, text="Shoot as many as you can, if you want.", font=("Times", 30))
    canvas.create_text(data.width//2, data.height//2, text="Use 'WASD' to move.", font=("Times", 30))
    canvas.create_text(data.width//2, 2*data.height//3, text="Press 'Space' to play!", font=("Times", 30))
    
def timerFiredHelp(data):
    pass

def keyPressedHelp(event, data):
    if event.keysym == "space":
        data.mode = "forest"
#####################################################
#PLAYER
#####################################################
    
def getPlayerBounds(data):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = (data.playerX, 3*data.height//4 - data.playerY)
    (x1, y0) = (x0 + data.playerWidth, y1 - data.playerHeight)
    return (x0, y0, x1, y1)
    
def movePlayer(dx, dy, data):
    data.playerX += dx
    data.playerY += dy
    # scroll to make player visible as needed
    if (data.playerX < data.scrollX + data.scrollMargin):
        data.scrollX = data.playerX - data.scrollMargin
    if (data.playerX > data.scrollX + data.width - data.scrollMargin):
        data.scrollX = data.playerX - data.width + data.scrollMargin
        
def drawPlayer(canvas, data):
    (x0, y0, x1, y1) = getPlayerBounds(data)
    sx = data.scrollX
    if data.walkFrame == 1:
        #body
        canvas.create_rectangle(x0 - sx, y0, x1 -sx, y1, fill="gray")
        #head
        canvas.create_oval(x0 - 5 -sx, y0 - 10, x1 -sx + 5, y1 - 8, fill="light grey")
        #legs
        #right
        #canvas.create_rectangle(x0 + 2 - sx, y1-5, x1 -2 - sx, y1 + 10, fill="slate gray", outline="slate gray")
        #canvas.create_rectangle(x0 + 2 - sx, y1 + 8, x1 + 4 - sx, y1 + 12, fill="slate gray", outline="slate gray")

#####################################################
#BALLS!
#####################################################

def getBallBounds(data, pos):
    (x0, y0) = (pos[0] - data.ballWidth, pos[1] - data.ballWidth)
    (x1, y1) = (pos[0] + data.ballWidth, pos[1] + data.ballWidth)
    return (x0, y0, x1, y1)

#draws one ball
def makeBall(canvas, data, pos):
    (x0, y0, x1, y1) = getBallBounds(data, pos)
    sx = data.scrollX
    canvas.create_oval(x0 - sx, y0, x1 - sx, y1, fill="red")

#tells makeBall which balls to draw
def drawBalls(canvas, data):
    if data.balls != []:
        for i in range(len(data.balls)):
            sx = data.scrollX
            #bs = data.ballSpeeds[i]
            pos = data.balls[i]
            #only draw if it's onscreen
            if (pos[0] > sx) and (pos[0] < data.width + sx) and (pos[1] >= 0):
                makeBall(canvas, data, (pos[0], pos[1]))#pos[1] - bs
                
#####################################################
#WHERE THE BALLS MEET THE BIRDS
#####################################################

#adapted from 15-112 sidescroller demo
def boundsIntersect(boundsA, boundsB):
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

def getBirdHit(data, bird, ball, birdIndex): 
    #list of false values, sets value at index to true
    sx = data.scrollX
    birdBounds = getBirdBounds(data, bird)
    sBirdBounds = (birdBounds[0] + sx, birdBounds[1], birdBounds[2] + sx, birdBounds[3])
    #print("ball:", ball)
    ballBounds = getBallBounds(data, ball)
    sBallBounds = (ballBounds[0] + sx, ballBounds[1], ballBounds[2] + sx, ballBounds[3])
    #print("birdBounds:", sBirdBounds, "ballBounds", sBallBounds)
    if boundsIntersect(ballBounds, birdBounds):
        data.birdsDown[birdIndex] = True
        data.birdScore += 1
        #print("bird down at:", sBallBounds, sBirdBounds)
#This is to change the value in the list that makes the bird the same color as
#the background
#####################################################
#DEATH
#####################################################

def drawPyramid(canvas, data, pos, size, level, depth=0):
    if level == 0:
        canvas.create_polygon(pos[0], pos[1], 
                              pos[0] + size, pos[1],
                              pos[0] + size/2, pos[1] - size*(3/4),
                              fill="blue")
    else:
        drawPyramid(canvas, data, pos, size/2, level-1, depth+1)
        drawPyramid(canvas, data, (pos[0] + size/2, pos[1]), size/2, level-1, depth+1)
        drawPyramid(canvas, data, (pos[0] + size/4, pos[1] - size*(3/8)), size/2, level-1, depth+1)
            
#####################################################
#THE BIRD ZONE
#####################################################
    
def getBirdBounds(data, pos):
    (x0, y0) = (pos[0] - data.birdWidth, pos[1] - data.birdHeight)
    (x1, y1) = (pos[0] + 2*data.birdWidth, pos[1] + data.birdHeight)
    return (x0, y0, x1, y1)
    
def makeBirdBounds(data, pos):
    (x0, y0) = (pos[0] - data.birdWidth, pos[1] - data.birdHeight)
    (x1, y1) = (pos[0] + data.birdWidth, pos[1] + data.birdHeight)
    return (x0, y0, x1, y1)
#messed up the way I named things, but I'm gonna keep it consistent.
#makeBird draws one bird.
def makeBird(canvas, data, pos, stage, color="black"):
    (x0, y0, x1, y1) = makeBirdBounds(data, pos)
    #only draw if it's onscreen
    if (pos[0] > (data.scrollX)) and (pos[0] < (data.width + data.scrollX))\
        and (pos[1] >= 0):
        sx = data.scrollX
        #bs = data.birdSpeed
        if stage == 1:
            canvas.create_line(x0 - sx, y0, x1 - sx, y0, x1 - sx, y1, smooth = True, width=2, fill=color)
            canvas.create_line(x1 - sx, y1, x1 - sx, y0, x1+2*data.birdWidth - sx, y0, smooth=True, width=2, fill=color)
        elif stage == 2:
            canvas.create_line(x0 - sx, y0 - data.birdHeight//2, x1 - sx, y0, x1 - sx, y1, smooth = True, width=2, fill=color)
            canvas.create_line(x1 - sx, y1, x1 - sx, y0, x1+2*data.birdWidth - sx, y0 - data.birdHeight//2, smooth=True, width=2, fill=color)
        elif stage == 3:
            canvas.create_line(x0 - sx, y1, x1 - sx, y0, x1 - sx, y1, smooth = True, width=2, fill=color)
            canvas.create_line(x1 - sx, y1, x1 - sx, y0, x1+2*data.birdWidth - sx, y1, smooth=True, width=2, fill=color)
            
def getBirdColor(data):
    if data.season == "spring":
        return "black"
    elif data.season == "summer":
        return "black"
    elif data.season == "fall":
        return "black"
    elif data.season == "winter":
        return "white"

#drawBirds tells makeBird all the birds it needs to draw.
def drawBirds(canvas, data):
    if data.birdList != []:
        for i in range(len(data.birdList)):
            bs = data.birdDirs[i]
            data.birdList[i] = (data.birdList[i][0] - bs, data.birdList[i][1] - math.fabs(bs))
            pos = data.birdList[i]
            stage = data.birdAnimations[i]
            sx = data.scrollX
            if data.birdsDown[i] == False:
                color = getBirdColor(data)
                makeBird(canvas, data, pos, stage, color)
                (x0, y0, x1, y1) = getBirdBounds(data, pos)
                canvas.create_oval(x0 - sx, y0, x1 - sx, y1, fill=None)
            else:
                continue
#####################################################
#TREES ONLY!
#####################################################
    
#NOTE: modify these two functions for making the trees different colors,
#only make different tree functions if the trees are gonna work differently
def pickTrunkColor(data, lineWidth):
    if lineWidth == 4:
        return "goldenrod"
    elif lineWidth == 3:
        return "dark goldenrod"
    elif lineWidth == 2:
        return "orange3"
    elif lineWidth == 1:
        return "orange4"
        
def pickBranchColor(data, lineWidth):
    if data.season == "spring":
        if lineWidth == 4:
            return "PaleGreen1"
        elif lineWidth == 3:
            return "PaleGreen2"
        elif lineWidth == 2:
            return "PaleGreen3"
        elif lineWidth == 1:
            return "PaleGreen4"
    elif data.season == "summer":
        if lineWidth == 4:
            return "PaleGreen1"
        elif lineWidth == 3:
            return "PaleGreen2"
        elif lineWidth == 2:
            return "PaleGreen3"
        elif lineWidth == 1:
            return "PaleGreen4"
    elif data.season == "fall":
        if lineWidth == 4:
            return "PaleGreen1"
        elif lineWidth == 3:
            return "PaleGreen2"
        elif lineWidth == 2:
            return "PaleGreen3"
        elif lineWidth == 1:
            return "PaleGreen4"
    elif data.season == "winter":
        if lineWidth == 4:
            return "PaleGreen1"
        elif lineWidth == 3:
            return "PaleGreen2"
        elif lineWidth == 2:
            return "PaleGreen3"
        elif lineWidth == 1:
            return "PaleGreen4"
            
############################################
#SPRING TREES
############################################
def makeTree(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth, color="dark goldenrod", depth=0):
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    ovalDist= 4 + lineWidth
    if depth == 0:
        color = pickTrunkColor(data, lineWidth)
    if level > -1:
        canvas.create_line(pos[0] - data.scrollX, pos[1], newPos[0] - data.scrollX,\
        newPos[1], fill=color, width=lineWidth)
    if level == 0:
        canvas.create_oval(newPos[0] - ovalDist - data.scrollX, newPos[1] - ovalDist,\
        newPos[0] + ovalDist - data.scrollX, newPos[1] + ovalDist, fill="pink", outline="grey")
    
    if level > 0:
        if depth >= 1:
            color = pickBranchColor(data, lineWidth)
        angle += angleChange
        newSize = size*(1 - trunkRatio)
        makeTree(canvas, data, level-1, angle, angleChange, newSize, newPos, dir + angle, lineWidth, color, depth+1)
        makeTree(canvas, data, level-1, angle, angleChange, newSize, newPos, dir - angle, lineWidth, color, depth+1)
        
def makeTree3(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth, color="dark goldenrod", depth=0):
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    ovalDist= 4 + lineWidth
    if depth == 0:
        color = pickTrunkColor(data, lineWidth)
    if level > -1:
        canvas.create_line(pos[0] - data.scrollX, pos[1], newPos[0] - data.scrollX,\
        newPos[1], fill=color, width=lineWidth)
    if level == 0:
        canvas.create_oval(newPos[0] - ovalDist - data.scrollX, newPos[1] - ovalDist,\
        newPos[0] + ovalDist - data.scrollX, newPos[1] + ovalDist, fill="firebrick1", outline="grey")
    
    if level > 0:
        if depth >= 1:
            color = pickBranchColor(data, lineWidth)
        angle += angleChange
        newSize = size*(1 - trunkRatio)
        makeTree3(canvas, data, level-1, angle, angleChange, newSize, newPos, dir + angle, lineWidth, color, depth+1)
        makeTree3(canvas, data, level-1, angle, angleChange, newSize, newPos, dir - angle, lineWidth, color, depth+1)
        makeTree3(canvas, data, level-1, angle, 0, newSize, newPos, dir, lineWidth, color, depth+1)
        
"""def makePythagorasTree(canvas, data, level, angle, size, pos, dir, color="forest green", depth=0):
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    if depth == 0:
        color = pickTrunkColor(data, lineWidth)
    if level > -1:
        canvas.create"""
        
############################################
#WINTER TREES AND SNOWFLAKES
############################################

def makeTreeWinter(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth, color="dark goldenrod", depth=0):
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    if depth == 0:
        color = pickTrunkColor(data, lineWidth)
    if level > -1:
        canvas.create_line(pos[0] - data.scrollX, pos[1], newPos[0] - data.scrollX,\
        newPos[1], fill=color, width=lineWidth)
    if level > 0:
        if depth >= 1:
            color = pickTrunkColor(data, lineWidth)
        angle += angleChange
        newSize = size*(1 - trunkRatio)
        makeTreeWinter(canvas, data, level-1, angle, angleChange, newSize, newPos, dir + angle, lineWidth, color, depth+1)
        makeTreeWinter(canvas, data, level-1, angle, angleChange, newSize, newPos, dir - angle, lineWidth, color, depth+1)
        
def makeTree3Winter(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth, color="dark goldenrod", depth=0):
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    if depth == 0:
        color = pickTrunkColor(data, lineWidth)
    if level > -1:
        canvas.create_line(pos[0] - data.scrollX, pos[1], newPos[0] - data.scrollX,\
        newPos[1], fill=color, width=lineWidth)
    if level > 0:
        if depth >= 1:
            color = pickTrunkColor(data, lineWidth)
        angle += angleChange
        newSize = size*(1 - trunkRatio)
        makeTree3Winter(canvas, data, level-1, angle, angleChange, newSize, newPos, dir + angle, lineWidth, color, depth+1)
        makeTree3Winter(canvas, data, level-1, angle, angleChange, newSize, newPos, dir - angle, lineWidth, color, depth+1)
        makeTree3Winter(canvas, data, level-1, angle, 0, newSize, newPos, dir, lineWidth, color, depth+1)
        
#initially recursed on all 8 points, but that proved too much for tkinter
def makeSnowFlake(canvas, data, level, size, pos):
    if level == 0:
        canvas.create_line(pos[0] - size, pos[1] - size, pos[0] + size, pos[1] + size, fill="white")
        canvas.create_line(pos[0], pos[1] - size, pos[0], pos[1] + size, fill="white")
        canvas.create_line(pos[0] - size, pos[1], pos[0] + size, pos[1], fill="white")
        canvas.create_line(pos[0] + size, pos[1] - size, pos[0] - size, pos[1] + size, fill="white")
    else:
        canvas.create_line(pos[0] - size, pos[1] - size, pos[0] + size, pos[1] + size, fill="white")
        canvas.create_line(pos[0], pos[1] - size, pos[0], pos[1] + size, fill="white")
        canvas.create_line(pos[0] - size, pos[1], pos[0] + size, pos[1], fill="white")
        canvas.create_line(pos[0] + size, pos[1] - size, pos[0] - size, pos[1] + size, fill="white")
        makeSnowFlake(canvas, data, level-1, size//3, (pos[0] - size, pos[1] - size))#TL
        #makeSnowFlake(canvas, data, level-1, size//3, (pos[0] - size, pos[1]))#L
        makeSnowFlake(canvas, data, level-1, size//3, (pos[0] - size, pos[1] + size))#BL
        #makeSnowFlake(canvas, data, level-1, size//3, (pos[0], pos[1] - size))#T
        #makeSnowFlake(canvas, data, level-1, size//3, (pos[0], pos[1] + size))#B
        #makeSnowFlake(canvas, data, level-1, size//3, (pos[0] + size, pos[1]))#R
        makeSnowFlake(canvas, data, level-1, size//3, (pos[0] + size, pos[1] - size))#TR
        makeSnowFlake(canvas, data, level-1, size//3, (pos[0] + size, pos[1] + size))#BR

        
def drawSnowFlakes(canvas, data):
    for i in range(len(data.snowflakes)):
        pos = data.snowflakes[i]
        level = data.snowLevels[i]
        size = data.snowSizes[i]
        makeSnowFlake(canvas, data, level, size, (pos[0], pos[1]))
        
############################################
#SUMMER TREES
############################################
#summer tree 1

def makeSummerTree(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth, color="dark goldenrod", depth=0):
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    sx = data.scrollX
    ovalDist = 6 + lineWidth
    if level > -1:
        canvas.create_line(pos[0] - sx, pos[1], newPos[0] - sx, newPos[1], fill=color, width=lineWidth)
    if level == 0:
        canvas.create_polygon(newPos[0] - ovalDist - sx, newPos[1] - ovalDist,\
        newPos[0] + ovalDist - sx, newPos[1] - ovalDist, newPos[0] - sx, newPos[1] + ovalDist, fill="forest green", outline="dark green")
    if level > 0:
        if depth >= 1:
            color = "forest green"
        angle += angleChange
        newSize = size*(1 - trunkRatio)
        makeSummerTree(canvas, data, level-1, angle, angleChange, newSize, newPos, dir + angle, lineWidth, color, depth+1)
        makeSummerTree(canvas, data, level-1, angle, angleChange, newSize, newPos, dir - angle, lineWidth, color, depth+1)
        
def makeSummerTree3(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth, color="dark goldenrod", depth=0):
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    sx = data.scrollX
    ovalDist = 6 + lineWidth
    if level > -1:
        canvas.create_line(pos[0] - sx, pos[1], newPos[0] - sx, newPos[1], fill=color, width=lineWidth)
    if level == 0:
        canvas.create_polygon(newPos[0] - ovalDist - sx, newPos[1] - ovalDist,\
        newPos[0] + ovalDist - sx, newPos[1] - ovalDist, newPos[0] - sx, newPos[1] + ovalDist, fill="forest green", outline="dark green")
    if level > 0:
        if depth >= 1:
            color = "forest green"
        angle += angleChange
        newSize = size*(1 - trunkRatio)
        makeSummerTree(canvas, data, level-1, angle, angleChange, newSize, newPos, dir + angle, lineWidth, color, depth+1)
        makeSummerTree(canvas, data, level-1, angle, angleChange, newSize, newPos, dir - angle, lineWidth, color, depth+1)
        makeSummerTree(canvas, data, level-1, angle, 0, newSize, newPos, dir - angle, lineWidth, color, depth+1)
    
####################################################
#FALL
####################################################

def makeTreeFall(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth, color="dark goldenrod", depth=0):
    sx = data.scrollX
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    ovalDist= 4 + lineWidth
    if depth == 0:
        color = pickTrunkColor(data, lineWidth)
    if level > -1:
        canvas.create_line(pos[0] - data.scrollX, pos[1], newPos[0] - data.scrollX,\
        newPos[1], fill=color, width=lineWidth)
    if level == 0:
        canvas.create_oval(newPos[0] - ovalDist - data.scrollX, newPos[1] - ovalDist,\
        newPos[0] + ovalDist - data.scrollX, newPos[1] + ovalDist, fill=data.treeFallColor, outline="grey")
        if depth == 6:
            data.curTree.append((newPos[0], newPos[1]))
            data.curColor = color
            data.curSize = ovalDist
    if level > 0:
        if depth >= 1:
            color = pickBranchColor(data, lineWidth)
        angle += angleChange
        newSize = size*(1 - trunkRatio)
        makeTreeFall(canvas, data, level-1, angle, angleChange, newSize, newPos, dir + angle, lineWidth, color, depth+1)
        makeTreeFall(canvas, data, level-1, angle, angleChange, newSize, newPos, dir - angle, lineWidth, color, depth+1)
        
def makeTreeFall3(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth, color="dark goldenrod", depth=0):
    sx = data.scrollX
    trunkRatio = .29
    trunk = size*trunkRatio
    changeX = trunk*math.cos(dir)
    changeY = trunk*math.sin(dir)
    (u, v) = pos
    newPos = (u + changeX, v + changeY)
    ovalDist= 4 + lineWidth
    if depth == 0:
        color = pickTrunkColor(data, lineWidth)
    if level > -1:
        canvas.create_line(pos[0] - data.scrollX, pos[1], newPos[0] - data.scrollX,\
        newPos[1], fill=color, width=lineWidth)
    if level == 0:
        canvas.create_oval(newPos[0] - ovalDist - data.scrollX, newPos[1] - ovalDist,\
        newPos[0] + ovalDist - data.scrollX, newPos[1] + ovalDist, fill=data.tree3FallColor, outline="grey")
        if depth == 4:
            data.curTree.append((newPos[0], newPos[1]))
            data.curColor = color
            data.curSize = ovalDist
    if level > 0:
        if depth >= 1:
            color = pickBranchColor(data, lineWidth)
        angle += angleChange
        newSize = size*(1 - trunkRatio)
        makeTreeFall3(canvas, data, level-1, angle, angleChange, newSize, newPos, dir + angle, lineWidth, color, depth+1)
        makeTreeFall3(canvas, data, level-1, angle, angleChange, newSize, newPos, dir - angle, lineWidth, color, depth+1)
        makeTreeFall3(canvas, data, level-1, angle, 0, newSize, newPos, dir - angle, lineWidth, color, depth+1)

#size should be 4 +lineWidth (ovaldist)
def drawLeaf(canvas, data, size, pos, color):
    canvas.create_oval(pos[0] - size, pos[1] - size, pos[0] + size, pos[1] + size, fill=color)
    
def makeFallingLeaves(canvas, data, i):
    leafList = data.leaves[i]
    color = data.leafColors[i]
    size = data.leafSizes[i]
    for j in range(len(leafList)):
        pos = leafList[j]
        if (pos[0] > 0) and (pos[0] < data.width) and (pos[1] < 3*data.height//4):
            drawLeaf(canvas, data, size, pos, color)
            
def drawBlownLeaves(canvas, data):
    for i in range(len(data.snowflakes)):
        pos = data.snowflakes[i]
        size = data.snowSizes[i]
        color = data.fallColorList[i]
        drawLeaf(canvas, data, size, pos, color)
####################################################
#SEASONS
####################################################

#REDRAW
def redrawSpring(canvas, data):
    #drawing the trees in spring
    for tree in range(data.treeNum):
        level = data.levels[tree]
        angle = data.angle
        angleChange = data.angleChanges[tree]
        size = data.lengths[tree]
        pos = data.posns[tree]
        dir = data.dirs[tree]
        lineWidth = data.lineWidths[tree]
        treeType = data.treeType[tree]
        #Make sure the tree's on screen
        if (pos[0] > (0 + data.scrollX)) and (pos[0] < (data.width + data.scrollX)):
            if treeType == 1:
                makeTree(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth)
            elif treeType == 2:
                makeTree3(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth)
            #makeRoots(canvas, data, level, angle*2, angleChange*4, size//4, pos, -dir)
    #birds
    drawBirds(canvas, data)
    
def redrawSummer(canvas, data):
    #drawing the trees in spring
    for tree in range(data.treeNum):
        level = data.levels[tree]
        angle = data.angle
        angleChange = data.angleChanges[tree]
        size = data.lengths[tree]
        pos = data.posns[tree]
        dir = data.dirs[tree]
        lineWidth = data.lineWidths[tree]
        treeType = data.treeType[tree]
        #Make sure the tree's on screen
        if (pos[0] > (0 + data.scrollX)) and (pos[0] < (data.width + data.scrollX)):
            if treeType == 1:
                makeSummerTree(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth)
            elif treeType == 2:
                makeSummerTree3(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth)
            #makeRoots(canvas, data, level, angle*2, angleChange*4, size//4, pos, -dir)
    #birds
    drawBirds(canvas, data)
    
def redrawWinter(canvas, data):
    for tree in range(data.treeNum):
        level = data.levels[tree]
        angle = data.angle
        angleChange = data.angleChanges[tree]
        size = data.lengths[tree]
        pos = data.posns[tree]
        dir = data.dirs[tree]
        lineWidth = data.lineWidths[tree]
        treeType = data.treeType[tree]
        #Make sure the tree's on screen
        if (pos[0] > (0 + data.scrollX)) and (pos[0] < (data.width + data.scrollX)):
            if treeType == 1:
                makeTreeWinter(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth)
            elif treeType == 2:
                makeTree3Winter(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth)
                
def redrawFall(canvas, data):
    for tree in range(data.treeNum):
        level = data.levels[tree]
        angle = data.angle
        angleChange = data.angleChanges[tree]
        size = data.lengths[tree]
        pos = data.posns[tree]
        dir = data.dirs[tree]
        lineWidth = data.lineWidths[tree]
        treeType = data.treeType[tree]
        sx = data.scrollX
        if (pos[0] > (0 + sx)) and (pos[0] < (data.width + sx)):
            if treeType == 1:
                makeTreeWinter(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth)
            elif treeType == 2:
                makeTree3Winter(canvas, data, level, angle, angleChange, size, pos, dir, lineWidth)
    drawBirds(canvas, data)
        
#TIMER FIRED
def timerFiredSpring(data):
    data.seasonTimer += .5
    print(data.seasonTimer)
    data.timer += 10
    #animate birds, make them fly up
    if data.birdSpeeds != []:
        for i in range(len(data.birdSpeeds)):
            #data.birdSpeeds[i] += data.birdDirs[i]
            if data.birdAnimations[i] < 3:
                data.birdAnimations[i] += 1
            else:
                data.birdAnimations[i] = 1
    #make trees grow
    if data.timer > 100:
        for i in range(len(data.levels)):
            data.levels[i] += 1
            limit = 1
            if data.treeType[i] == 1:
                limit = 6
            elif data.treeType[i] == 2:
                limit = 4
            if data.levels[i] > limit:
                #if the tree grows too tall, start over and make a bird
                data.levels[i] = -1
                data.birdList.append(data.posns[i])
                data.birdSpeeds.append(0)
                data.birdAnimations.append(1)
                data.birdsDown.append(False)
                if data.left:
                    data.birdDirs.append(random.randint(4, 7))
                    data.left = False
                else:
                    data.birdDirs.append(random.randint(-7, -4))
                    data.left = True
            data.timer = 0
    print(data.season)
    if data.seasonTimer > 100:
        data.season = "summer"
    elif data.seasonTimer > 200:
        data.season = "fall"
        
def timerFiredFall(data):
    data.seasonTimer += .5
    data.timer += 10
    #animate birds, make them fly up
    if data.birdSpeeds != []:
        for i in range(len(data.birdSpeeds)):
            data.birdSpeeds[i] += data.birdDirs[i]
            if data.birdAnimations[i] < 3:
                data.birdAnimations[i] += 1
            else:
                data.birdAnimations[i] = 1
    #make trees grow
    if data.timer > 100:
        for i in range(len(data.levels)):
            data.levels[i] += 1
            limit = 1
            if data.treeType[i] == 1:
                limit = 6
            elif data.treeType[i] == 2:
                limit = 4
            if data.levels[i] > limit:
                #if the tree grows too tall, start over and make a bird
                data.levels[i] = -1
                data.birdList.append(data.posns[i])
                data.birdSpeeds.append(0)
                data.birdAnimations.append(1)
                data.birdsDown.append(False)
                if data.left:
                    data.birdDirs.append(random.randint(4, 7))
                    data.left = False
                else:
                    data.birdDirs.append(random.randint(-7, -4))
                    data.left = True
        data.timer = 0
    for i in range(len(data.snowflakes)):
        data.snowflakes[i] = (data.snowflakes[i][0] - data.snowDirs[i], data.snowflakes[i][1] + data.snowDirs[i])
        pos = data.snowflakes[i]
        if (pos[0] < 0) or (pos[1] > 3*data.height//4):
            if data.top:
                data.snowflakes[i] = (random.randint(0, data.width), 0)
                data.top = False
            else:
                data.snowflakes[i] = (data.width, random.randint(0, data.height))
                data.top = True
            

def timerFiredWinter(data):
    data.seasonTimer += .5
    for i in range(len(data.snowflakes)):
        data.snowflakes[i] = (data.snowflakes[i][0] - data.snowDirs[i], data.snowflakes[i][1] + data.snowDirs[i])
        pos = data.snowflakes[i]
        if (pos[0] < 0) or (pos[1] > 3*data.height//4):
            if data.top:
                data.snowflakes[i] = (random.randint(0, data.width), 0)
                data.top = False
            else:
                data.snowflakes[i] = (data.width, random.randint(0, data.height))
                data.top = True
            #data.snowSpeeds[i] = 0
    
####################################################
#ADMINISTRATION
####################################################

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if data.mode == "forest":
        if (event.keysym == "a"):
            movePlayer(-10, 0, data)
        elif (event.keysym == "d"):
            movePlayer(+10, 0, data)
        elif (event.keysym == "space"):
            data.balls.append((data.playerX, 3*data.height//4 - 10))
        elif (event.keysym == "h"):
            data.mode = "help"
    elif data.mode == "end":
        if event.keysym == "space":
            init(data)
    elif data.mode == "splash":
        keyPressedSplash(event, data)
    elif data.mode == "help":
        keyPressedHelp(event, data)

def timerFired(data):
    if (data.mode == "forest") or (data.mode == "end"):
        if data.seasonTimer < 400:
            data.season = data.seasonList[data.seasonTimer//100]
        else:
            data.season = "winter"
            data.mode = "end"
        if data.balls != []:
            for i in range(len(data.balls)):
                #data.ballSpeeds[i] += 20
                p0s = data.balls[i]
                data.balls[i] = (p0s[0], p0s[1] - data.ballSpeed)
        if data.balls != []:
            for i in range(len(data.birdList)):
                for j in range(len(data.balls)):
                    pos = data.birdList[i]
                    ballPos = data.balls[j]
                    if (pos[0] >= 0) and (pos[0] <= data.width) and (pos[1] >= 0) and (pos[1] <= data.height):
                        if (ballPos[0] >= 0) and (ballPos[0] <= data.width) and (ballPos[1] >= 0) and (ballPos[1] <= data.height):
                            #if ball is in view
                            #print("birdindex:", i)
                            #print("ball index:", j)
                            #print("ball pos:", ballPos)
                            getBirdHit(data, data.birdList[i], data.balls[j], i)
        if data.season == "spring":
            timerFiredSpring(data)
        elif data.season == "summer":
            timerFiredSpring(data)
        elif data.season == "fall":
            timerFiredFall(data)
        elif data.season == "winter":
            timerFiredWinter(data)
        if data.mode == "end":
            if data.pyramidLevel < 5:
                data.deathTimer += 15
                if data.deathTimer > 100:
                    data.pyramidLevel += 1
                    data.deathTimer = 0
    elif data.mode == "splash":
        timerFiredSplash(data)
    elif data.mode == "help":
        timerFiredHelp(data)
                
def redrawAllForest(canvas, data):
    if data.season == "spring":
        data.backgroundColor = "light yellow"
        canvas.create_rectangle(0, 0, data.width, 3*data.height//4,\
        fill=data.backgroundColor, outline=data.backgroundColor)
        redrawSpring(canvas, data)
    elif data.season == "summer":
        data.backgroundColor = "peach puff"
        canvas.create_rectangle(0, 0, data.width, 3*data.height//4,\
        fill=data.backgroundColor, outline=data.backgroundColor)
        redrawSummer(canvas, data)
    elif data.season == "fall":
        data.backgroundColor = "snow2"
        canvas.create_rectangle(0, 0, data.width, 3*data.height//4,\
        fill=data.backgroundColor, outline=data.backgroundColor)
        redrawFall(canvas, data)
        drawBlownLeaves(canvas, data)
    elif data.season == "winter":
        canvas.create_rectangle(0, 0, data.width, 3*data.height//4, fill="light blue", stipple = "gray50")
        redrawWinter(canvas, data)
        if data.mode != "end":
            canvas.create_text(data.width//2, data.height//3, text="the birds have flown south for the winter",
            font=("Arial", 16))
        drawSnowFlakes(canvas, data)
    # draw the base line
    lineY = 3*data.height//4
    lineHeight = 5
    canvas.create_rectangle(0, lineY, data.width, data.height,fill="sienna4", outline="sienna4")
    #draw the player
    if data.mode != "end":
        drawPlayer(canvas, data)
    elif data.mode == "end":
        drawPyramid(canvas, data, (data.width//4, 3*data.height//4), data.width//2, data.pyramidLevel)
        canvas.create_text(data.width//2, data.height//4, text="THE END", fill="black", font=("Times", 100))
        canvas.create_text(data.width//2, data.height//8, text="You killed %d birds" % data.birdScore, font=("Times", 50))
    drawBalls(canvas, data)
        
            
            
def redrawAll(canvas, data):
    if (data.mode == "forest") or (data.mode == "end"):
        redrawAllForest(canvas, data)
    elif data.mode == "splash":
        redrawAllSplash(canvas, data)
    elif data.mode == "help":
        redrawAllHelp(canvas, data)

###########################################
#RUN FUNCTION
###########################################

def run(width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)