window = 0
level = 1
score = 0
bestScore = 0
life = 0

# start
bgColorList = [[255, 255, 255], [255, 0, 0], [255, 127, 0], [255, 255, 0], [0, 255, 0], [0, 0, 255], [0, 0, 128], [180, 85, 162]]
bgColor = 0

#game
bg1X = 0
bg2X = 1080
playerY = 270
playerNum = 0
spawnInterval = 700
obstaclesList = []
gameOver = False


def setup():
    global bg, player, obstacleImg, heart, lastSpawnTime
    size(1080, 540)
    # Image Load
    bg = loadImage("sky1.png")
    player = []
    for i in range(1, 13):
        player.append(loadImage("p{}.png".format(i)))
    obstacleImg = []
    for i in range(1, 4):
        obstacleImg.append(loadImage("obs{}.png".format(i)))
    heart = loadImage("heart.png")
    
    lastSpawnTime = millis()
        
def draw():
    global window
    if window == 0:
        start()
    elif window == 1:
        game()
        
        
        
def start():
    global window, bgColorList, bgColor, level, score, bestScore, gameOver, life, reStart
    
    background(bgColorList[bgColor][0], bgColorList[bgColor][1], bgColorList[bgColor][2])
    
    # Title
    textSize(70)
    textAlign(CENTER)
    if bgColor in [0,3,4]:
        fill(0)
    else:
        fill(255)
    text("Title", width/2, 200)
    
    # Score
    textSize(30)
    fill(0)
    textAlign(LEFT)
    text("Best Score: {}".format(bestScore), 30, 50)
    text("Score: {}".format(score), 30, 80)
    
    
    
    # Level Button
    for i in range(3):
        rectMode(CENTER)
        strokeWeight(1)
        fill(255)
        rect(360+180*i, 300, 80, 80)
        textSize(30)
        textAlign(CENTER)
        fill(0)
        text("Level\n{}".format(i+1), 360+180*i, 290)
    
    # Background Color
    for i in range(8):
        rectMode(CENTER)
        fill(bgColorList[i][0], bgColorList[i][1], bgColorList[i][2])
        rect(700+40*i, 450, 30, 30)
    
    if mousePressed:
        # Background Color Change
        if 435<=mouseY<=465:
            for i in range(8):
                if 700+40*i-15<=mouseX<=700+40*i+15:
                    bgColor = i
        # Level Select
        if 260<=mouseY<=340:
            for i in range(3):
                if 360+180*i-40<=mouseX<=360+180*i+40:
                    window = 1
                    level = i+1
                    reStart = True
    

    
def game():
    global bg, bg1X, bg2X, window, level, score, bestScore, playerY, player, playerNum, obstacleImg, heart, obstaclesList, lastSpawnTime, spawnInterval, gameOver, life, reStart
    
    # Background
    imageMode(CORNER)
    image(bg, bg1X, 0, 1080, 675)
    image(bg, bg2X, 0, 1080, 675)
    if not gameOver:
        bg1X -= 5
        bg2X -= 5
        if bg1X <= -1080:
            bg1X = 1080
        if bg2X <= -1080:
            bg2X = 1080
        score += 1 # Score
    textSize(30)
    fill(0)
    for i in range(life):
        image(heart, 50+50*i, 50)
    text("score: {}".format(score), 100, 120)
    
    # Reset
    if reStart == True:
        playerNum = 0
        playerY = 270
        score = 0
        life = 3
        reStart = False
        gameOver = False
        obstaclesList = []
    
    # Player
    if not gameOver:
        playerNum = millis()/100%12 # Player Animation
    imageMode(CENTER)
    image(player[playerNum], 100, playerY, 60, 100)
    if not gameOver and keyPressed:
        # if keyCode == UP and playerY>50:
        #     playerY -= 8
        # elif keyCode == DOWN and playerY<490:
        #     playerY += 8
        playerY += -8 if keyCode == UP and playerY>50 else (8 if keyCode == DOWN and playerY<490 else 0)

    # Obstacles
    if not gameOver and millis() - lastSpawnTime > spawnInterval:
        obstaclesList.append({'img': int(random(0,3)), 'x': width+50, 'y': random(50, 490), 'isCollided': False})
        lastSpawnTime = millis()

    for i in obstaclesList:
        if not gameOver:
            i['x'] -= 10 + 5 * (level-1)
        image(obstacleImg[i['img']], i['x'], i['y'], 50*obstacleImg[i['img']].width/obstacleImg[i['img']].height, 50)
        
        if ( 70 < i['x'] - (50*obstacleImg[i['img']].width/obstacleImg[i['img']].height)/2 < 100 ) and ( playerY-50 < i['y']+25 < playerY+50 or playerY-50 < i['y']-25 < playerY+50 ) and i['isCollided'] == False:
            # if playerY-50 < i['y'] < playerY+50:
            #     if i['isCollided'] == False:
            i['isCollided'] = True
            life -= 1
            i['x'] = -50
        
    obstaclesList = [i for i in obstaclesList if i['x'] > -obstacleImg[i['img']].width] # Show Obstacles When they are in screen


    # Game Over
    if life == 0:
        gameOver = True

    if gameOver:
        filter(GRAY)
        textSize(70)
        fill(0)
        text("Game Over", width/2, height/2)
        textSize(30)
        noFill()
        strokeWeight(3)
        rect(410, 440, 100, 100)
        rect(670, 440, 100, 100)
        text("Menu", 540-130, 445)
        text("Restart", 540+130, 445)
        if mousePressed and 390 <= mouseY <= 490:
            if 360 <= mouseX <= 460:
                window = 0
            elif 620 <= mouseX <= 720:
                reStart = True            
        
        # Best Score
        if bestScore < score:
            bestScore = score
        
        
    
    
