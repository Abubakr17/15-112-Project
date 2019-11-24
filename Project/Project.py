#Name: Abubakr Mohamed
#Andrew ID: aamohame


import pygame
import random
import tkinter
import sys
from tkinter import messagebox


###Credits (Sources for Sprites)

'''Enemy
https://dribbble.com/shots/1467749-Flying-Enemy-Game-Character-Sprite-Sheet#shot-description

Door
https://www.netclipart.com/down/xTTRRR_cartoon-castle-door-png/

Signs
https://pngtree.com/element/down?id=MzU2NTYzNg==&type=1

Background
https://www.gamedevmarket.net/asset/2d-game-background-10014/

Character
https://www.gamedevmarket.net/asset/sporty-boy-game-sprites-4361/

Platform
https://www.clipartwiki.com/downpng/xibhiT_grass-clipart-row-platform-sprite/'''


#################### Classes ####################################

#This class defines the properties that the playable character hold
#such as x and y coordinates, jumping, velocity and the sprite images
class character():

    def __init__(self):

        self.x = 50  
        self.y = 350
        self.width = 50
        self.height = 50 
        self.rightvelocity = 45
        self.leftvelocity = 45
        self.goingRight = False
        self.goingLeft = False
        self.isJumping = False
        self.isFalling = False
        self.walkcount = 0
        self.lives = 3
        self.walkRight = [pygame.image.load('character/run1.png'),
        pygame.image.load('character/run2.png'),
        pygame.image.load('character/run3.png'),
        pygame.image.load('character/run4.png'),
        pygame.image.load('character/run5.png'),
        pygame.image.load('character/run6.png')]
        self.walkLeft = [pygame.transform.flip(x, True, False) for x \
        in self.walkRight]
        self.standingRight = pygame.image.load('character/standingRight.png')
        self.standingLeft = pygame.image.load('character/standingLeft.png')
        self.direction = 1    
        self.jumpcount = 12
        self.hitbox = (self.x + 10, self.y,90,160)
    
    #Function takes a window as input and draws the character into the window
    #the function also defines the sprites hitbox
    def draw(self,win):
       
        if self.x >= game.screenWidth//2 \
        and game.onScreenX<game.stageWidth - game.startScrollingPosX:
           self.x = game.screenWidth//2

        elif game.onScreenX>=game.stageWidth - game.startScrollingPosX:
            self.x = game.screenWidth//2 + game.onScreenX - \
            (game.stageWidth - game.startScrollingPosX)

        if self.goingRight:
            win.blit(self.walkRight[self.walkcount],(self.x,self.y))
            self.walkcount += 1
            self.walkcount = self.walkcount % 6
    
        elif self.goingLeft:
            win.blit(self.walkLeft[self.walkcount],(self.x,self.y))
            self.walkcount += 1
            self.walkcount = self.walkcount % 6

        else:
            if self.direction == 1:
                win.blit(self.standingRight,(self.x,self.y))
            else:
                win.blit(self.standingLeft,(self.x,self.y))
        
        self.hitbox = (self.x + 10, self.y,90,160)
       
#This class loads and draws the backgroud for level 1
class level1():
    def __init__(self):
        self.bg = pygame.image.load("LevelBg/bg1 copy.jpg")
        self.width, self.height = self.bg.get_rect().size
    

    def draw(self,win,x=0,y=0):
        win.blit(self.bg,[x,y])

#This class loads and draws the backgroud for level 2
class level2():
    def __init__(self):
        self.bg = pygame.image.load('LevelBg/bg6.jpg')
        self.width, self.height = self.bg.get_rect().size

    def draw(self,win,x=0,y=0):
        win.blit(self.bg,[x,y])
    
#This class loads and draws the backgroud for level 3
class level3():
    def __init__(self):
        self.bg = pygame.image.load('LevelBg/bg7.png')
        self.width, self.height = self.bg.get_rect().size

    def draw(self,win,x=0,y=0):
        win.blit(self.bg,[x,y])

#This class loads the diamond sprites and draws them into the window
class diamond():
    
    def __init__(self,x,y,offset = 0):
        self.offset = 0
        self.initial = x
        self.x = x
        self.y = y
        self.collected = False
        self.pic = pygame.image.load("Sprite/red2.png")
    
    def draw(self,win):
        self.x = self.initial - self.offset
        win.blit(self.pic,(self.x,self.y))

#This class contains the properties of the platforms (location and sprite)     
class platform():
    
    def __init__(self,x,y,offset = 0):
        self.offset = 0
        self.initial = x
        self.x = x
        self.y = y
        self.onPlatform = False
        self.pic = pygame.image.load('Sprite/plat1.png')

    def draw(self,win):
        
        self.x = self.initial - self.offset
        win.blit(self.pic,(self.x,self.y))

#This class loads in the enemies 
#It holds their x,y coordinates and their different animations
class enemyC():

    def __init__(self,x,y,offset = 0):
    
        self.offset = 0
        self.initial = x
        self.x = x
        self.y = y
        self.isVisible = True
        self.goingLeft = False
        self.goingRight = False
        self.hit = False
        self.pic = pygame.image.load('enemySprite/enemy1.png')
        self.pic2 = pygame.transform.flip(self.pic, True, False)
        self.pic3 = pygame.image.load('enemySprite/enemy4.png')
        self.pic4 = pygame.transform.flip(self.pic3, True, False)

    #this function takes in a window as input and draws the enemy on it
    #The image to be drawn also depends on the enemies action (hitting/idle)
    def draw(self,win):
        
        self.x = self.initial - self.offset

        if self.isVisible:
            
            if self.goingLeft:
                if not self.hit:
                    win.blit(self.pic,(self.x,self.y))
                else:
                    win.blit(self.pic3,(self.x,self.y))
                    

            if self.goingRight:
                if not self.hit:
                    win.blit(self.pic2,(self.x,self.y))
                else:
                    win.blit(self.pic4,(self.x,self.y))

#This class loads in and draws the spikes 
class spike():

    def __init__(self,x,y,offset = 0):
    
        self.offset = 0
        self.initial = x
        self.x = x
        self.y = y
        self.hit = False
        self.pic = pygame.image.load('Sprite/spike.png')
    
    def draw(self,win):
        
        self.x = self.initial - self.offset
        win.blit(self.pic,(self.x,self.y))

#This class contains the door that ends each level 
class door():

    def __init__(self,x,y):

        self.endDoor = pygame.image.load("Sprite/endDoor.png")
        self.offset = 0
        self.initial = x
        self.x = x
        self.y = y
    
    def draw(self,win):
        self.x = self.initial - self.offset
        win.blit(self.endDoor,(self.x,self.y))

#This class contains the signs that are used to provide instructions to users
class sign():

    def __init__(self,x,y,num):

        self.offset = 0
        self.initial = x
        self.x = x
        self.y = y

        if num == 1:
            self.pic = pygame.image.load('signs/Sign copy.png')

        elif num == 2:
            self.pic = pygame.image.load('signs/Sign copy 3.png')

        elif num == 3: 
            self.pic = pygame.image.load('signs/Sign copy 4.png')

        elif num == 4:
            self.pic = pygame.image.load('signs/Sign copy 5.png')
        
        elif num == 5:
            self.pic = pygame.image.load('signs/Sign copy 6.png')
        
        elif num == 6:
            self.pic = pygame.image.load('signs/Sign copy 7.png')

    def draw(self,win):
        self.x = self.initial - self.offset
        win.blit(self.pic,(self.x,self.y))

#This class contains the buttons for the user interface
class button():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
    
    #This function draws the button onto the window
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,400,120))

    #checks whether the button is clickable by the mouse
    def isClickable(self,pos):
        if pos[0] >= self.x and pos[0] <= self.x + 400 and pos[1] >= self.y \
        and pos[1] <= self.y + 120:
            return True
        return False

############## Functions ############################

#This function calls the main window to start the game 
#Part of Checkpoint 2 
def Menu():
    
    run = True

    win = pygame.display.set_mode((500,800))
    pygame.display.set_caption("Tartan Adventure")

    SinglePlayer = button(50,350,(0,0,255))
    Quit = button(50,500,(0,0,255))

    font = pygame.font.SysFont("comicsans", 60, True)
    font2 = pygame.font.SysFont("comicsans", 110, True)

    playy = font.render("PLAY GAME",1,(0,0,0))
    
    QuitB = font.render("QUIT GAME",1,(0,0,0))

    Title = font2.render("Tartan",1,(0,0,0))
    Title2 = font2.render("Adventure",1,(0,0,0))

    menu = pygame.image.load("menu.jpg")
    
    buttonClick = pygame.mixer.Sound("button.wav")

    #main menu loop
    while run:

        for event in pygame.event.get():
            position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SinglePlayer.isClickable(position):
                    run = False
                    buttonClick.play()
                    return True

                if Quit.isClickable(position):
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if SinglePlayer.isClickable(position):
                    SinglePlayer.color = (255,0,0)
                else:
                    SinglePlayer.color = (0,0,255)
                
                if Quit.isClickable(position):
                    Quit.color = (255,0,0)
                else:
                    Quit.color = (0,0,255)

            win.blit(menu,(0,0))
            win.blit(Title,(100,50))
            win.blit(Title2,(20,125))
            SinglePlayer.draw(win)
            win.blit(playy,(100,390))
            Quit.draw(win)
            win.blit(QuitB,(120,550))
            pygame.display.update()
    
    pygame.quit()
    return False

#This function resets the level and decreases the characters lives
#called when the character is hit by enemies or spikes
def death():

    player1.lives -= 1
    if game.levels ==1:
        resetLevel1()

    elif game.levels== 2:
        resetLevel2()

    else:
        resetLevel3()

#This function resets level 1
#Returns back the intial properties of the level
def resetLevel1():
   
    player1.x,game.onScreenX = 50,50
    player1.y = 350
    player1.goingRight = False
    player1.goingLeft = False
    player1.isJumping = False
    player1.walkcount = 0
    player1.direction = 1    
    player1.jumpcount = 12
    player1.hitbox = (player1.x + 10, player1.y,90,160)
    game.diamonds = [diamond(500,250),diamond(850,250),
    diamond(1125,250),diamond(1400,250),diamond(2000,250),
    diamond(3000,250),diamond(2500,250),diamond(4300,250)]
    game.platforms = []
    game.enemies = [enemyC(2000,400),enemyC(4000,400),enemyC(3000,400)]
    sign1 = sign(200,200,3)
    sign2 = sign(600,200,1)
    sign3 = sign(1500,200,2)
    sign4 = sign(3500,200,4)
    game.signs = [sign1,sign2,sign3,sign4]
    game.spikes = []

#This function resets level 2
#Returns back the intial properties of the level
def resetLevel2():
    
    player1.x,game.onScreenX = 50,50
    player1.y = 325
    player1.goingRight = False
    player1.goingLeft = False
    player1.isJumping = False
    player1.walkcount = 0
    player1.direction = 1    
    player1.jumpcount = 12
    player1.hitbox = (player1.x + 10, player1.y,90,160)
    game.diamonds = [diamond(500,250),diamond(850,250),
    diamond(1125,250),diamond(1400,250),diamond(2000,250),
    diamond(3000,250),diamond(2500,250),diamond(4300,250)]
    game.platforms = []
    game.enemies = [enemyC(2000,375),enemyC(4000,375)]
    game.signs = [sign(500,150,5)]
    game.spikes = [spike(1000,420),spike(1500,420),spike(2500,420),
    spike(3100,420),spike(4000,420),spike(5000,420)]

#This function resets level 3
#Returns back the intial properties of the level
def resetLevel3():

    player1.x,game.onScreenX = 50,50
    player1.y = 325
    player1.goingRight = False
    player1.goingLeft = False
    player1.isJumping = False
    player1.walkcount = 0
    player1.direction = 1    
    player1.jumpcount = 12
    player1.hitbox = (player1.x + 10, player1.y,90,160)
    game.diamonds = [diamond(500,250),diamond(900,250),
    diamond(1125,250),diamond(1400,250),diamond(2000,250),
    diamond(3000,250),diamond(2500,250),diamond(4300,250)]
    game.platforms = [platform(900,330),platform(1600,330),
    platform(2500,330),platform(3000,330)]
    game.enemies = [enemyC(2000,375),enemyC(4000,375)]
    game.signs = [sign(350,150,6)]

    game.spikes = [spike(1000,420),spike(1700,420),spike(2650,420),
    spike(3100,420),spike(3950,420),spike(4900,420)]

#This function draws the diamonds onto the screen 
def drawDiamonds():

    for diamond1 in game.diamonds:
        diamond1.offset = game.onScreenX

        if diamond1.x >= player1.x and diamond1.x <= player1.x + 90:
            if diamond1.y >= player1.y and diamond1.y + 41 <= player1.y + 160:
                diamond1.collected = True
                game.score += 1
                game.diamonds.remove(diamond1)
    
        if not diamond1.collected:
            diamond1.draw(game.win)

#This function draws the platforms onto the screen
#function also handles the platform physics (jumping and standing on platfrom)
def drawPlatforms():

    game.onPlatform = False
    for platoi in game.platforms:
        platoi.offset = game.onScreenX

        if player1.x + 90 >= platoi.x and player1.x <= platoi.x + 275:
            if player1.y + 120 <= platoi.y \
            and platoi.y  - player1.y - 140 < 50:
                player1.y = platoi.y - 140
                if not game.onPlatformJump:
                    player1.isJumping = False
                    player1.jumpcount = 12
                game.onPlatform = True
        
        if not game.onPlatform:
            if player1.goingRight:
                
                if player1.x + 120 >= platoi.x \
                and player1.x <= platoi.x + 230 and not player1.isJumping:
                    if player1.y + 140 > platoi.y + 20:
                        
                        player1.x = platoi.x - 120
                        game.onScreenX -= 45

                else:
                    player1.rightvelocity = 45
                    

            if player1.goingLeft:
                if player1.x <= platoi.x + 290 and player1.x > platoi.x:
                    if player1.y + 140 > platoi.y + 20 \
                    and not player1.isJumping:
                        
                        player1.leftvelocity = 0
                        player1.x = platoi.x + 290
                           
                    else:
                        player1.leftvelocity = 45
                        
                else:
                    player1.leftvelocity = 45
                    
        platoi.draw(game.win)

#Function draws enemies and handles collisions with enemies

def drawEnemies():

    for enemy in game.enemies:
        enemy.offset = game.onScreenX
        enemy.hit = False
        
        #Hitboxes are used to detect collisions with player
        if enemy.goingLeft:
            if enemy.x <= player1.x + 90 and enemy.x >= player1.x:
                if player1.y + 140 > enemy.y and player1.y < enemy.y + 90:
                
                    enemy.hit = True
                    enemy.draw(game.win)
                    game.hitSound.play()
                    death()
                else:
                    enemy.hit = False
        
        elif enemy.goingRight:
            if enemy.x + 90 <= player1.x + 110 and enemy.x + 90 >= player1.x:
                if player1.y + 140 > enemy.y and player1.y < enemy.y + 90:
                
                    enemy.hit = True
                    enemy.draw(game.win)
                    game.hitSound.play()
                    death()
                else:
                    enemy.hit = False
    
        enemy.draw(game.win)

#draw the spikes and detect collisions with player
def drawSpikes():

    for spike in game.spikes:
        spike.offset = game.onScreenX
        spike.hit = False

        if player1.x + 80 >= spike.x and player1.x <= spike.x + 100:
            if player1.y + 150 >= spike.y +20 and player1.y < spike.y:
        
                spike.hit = True
                spike.draw(game.win)
                game.hitSound.play()
                death()
                
            else:
                spike.hit = False
        
        spike.draw(game.win)

#This function draws all the sprites and images into the window
def drawWind():
    
    #draw the Background 
    game.level.draw(game.win)

    #Place the level-ending dooor
    game.door1.offset = game.onScreenX
    game.door1.draw(game.win)

    #place all the signs 
    for sign in game.signs:
        sign.offset = game.onScreenX
        sign.draw(game.win)

    #draw the player, their lives and diamonds into the screen
    player1.draw(game.win)
    diamondtext = game.font.render("Diamonds: " + str(game.score), 1, (0,0,0))
    game.win.blit(diamondtext,(game.screenWidth-200,20))

    livestext = game.font.render("Lives: " + str(player1.lives),1,(0,0,0))
    game.win.blit(livestext,(20,20))

    #draw the remaining sprites and characters
    drawDiamonds()
    
    drawPlatforms()
    
    drawEnemies()

    drawSpikes()
    
    #Handle gameOver event 
    #Restart the game from level 1 and remove all diamonds
    if player1.lives == 0:
        gameOver = game.font.render('Game Over',1,(0,0,0))
        gameOver2 = game.font.render('Restarting ...',1,(0,0,0))
        game.win.blit(gameOver,(335,220))
        game.win.blit(gameOver2,(335,255))
    
    #Handling player jumps on Platforms
    if not player1.isJumping and game.onPlatform:
        if game.keys[pygame.K_SPACE]:
            player1.isJumping = True

        else:
            game.onPlatformJump = False
            player1.isJumping = False
            player1.jumpcount = 12 
    
    #This is the gravity mechanism for Level 1
    if game.levels == 1:
        if player1.y < 350 and game.onPlatform == False:
            if player1.isFalling:
                player1.isJumping = False
                player1.jumpcount = 12
            player1.y += game.gravity 
            game.gravity += 10
            if player1.y > 350:
                player1.y = 350
        else:
            game.gravity = 0

    else:
        
        #Gravity mechanism for levels 2 and 3
        if player1.y < 325 and game.onPlatform == False:
            if player1.isFalling:
                player1.isJumping = False
                player1.jumpcount = 12

            player1.y += game.gravity 
            game.gravity += 10
            if player1.y > 325:
                player1.y = 325

        else:
            game.gravity = 0
    
    pygame.display.update()   

#This function checks the keys pressed by the user
#then maps the key to the appropriate function for the character to perform
def checkButtons(keys): 
    
    #These are the directional buttons (Left and Right)
    if keys[pygame.K_LEFT]:
        player1.goingLeft = True
        player1.goingRight = False
        player1.direction = 0

        if not player1.x < 50:
            game.onScreenX -= player1.leftvelocity

        if game.onScreenX <= game.startScrollingPosX:
            player1.x = game.onScreenX
            
    elif keys[pygame.K_RIGHT]:
        player1.goingLeft = False
        player1.goingRight = True
        player1.direction = 1

        game.onScreenX += player1.rightvelocity
        
        if game.onScreenX <= game.startScrollingPosX:
            player1.x = game.onScreenX
            
    else:
        player1.goingLeft = False
        player1.goingRight = False
        player1.walkcount = 0
    
    #Secret code to draw more diamonds ;)
    if keys[pygame.K_p]:
        x = random.randint(1,10000)
        y = random.randint(250,251)
        game.diamonds.append(diamond(x,y))

    #Handle player jumps 
    #This algorithm was inspired by TechwithTim but with modifications
    if not player1.isJumping:
        if keys[pygame.K_SPACE]:
            player1.isJumping = True
 
    else:
        if player1.jumpcount >= -12:
            multip = 1
            if player1.jumpcount < 0:
                multip = 0
                player1.isFalling = True
            else:
                player1.isFalling = False
        
            player1.y -= (player1.jumpcount ** 2) * 0.7 * multip
            player1.jumpcount -= 4
        else:
            player1.isJumping = False
            player1.jumpcount = 12

#This class decides the current level the character is in 
#holds the current state of the game (Level, gameRun, enemies, platforms, etc)
class currentLevel():
    def __init__(self):

        self.gameRun = True
        self.clock = pygame.time.Clock()
        self.level = level1()
        self.font = pygame.font.SysFont("comicsans", 30, True)

        #diamonds to be displayed in current level
        self.diamonds = [diamond(500,250),diamond(850,250),
        diamond(1125,250),diamond(1400,250),diamond(2000,250),
        diamond(3000,250),diamond(2500,250),diamond(4300,250)]

        #platforms to be displayed in current level
        self.platforms = []

        #The enemies to be displayed in current level
        self.enemies = [enemyC(2000,400),enemyC(4000,400),enemyC(3000,400)]
        self.score = 0

        self.screenHeight = self.level.height
        self.screenWidth = self.level.width

        self.win = pygame.display.set_mode((self.screenWidth,
        self.screenHeight))
        pygame.display.set_caption("Tartan Adventure")

        self.music = pygame.mixer.music.load("Music/music.mp3")
        pygame.mixer.music.play(-1)

        self.hitSound = pygame.mixer.Sound("hitSound.wav")
        
        #Setting the size (width) of the level 
        self.stageWidth = 5 * self.screenWidth
        self.startScrollingPosX = self.screenWidth // 2
        self.onScreenX = 0

        #Add door and signs to level
        self.door1 = door(self.stageWidth+425,285)
        self.sign1 = sign(200,200,3)
        self.sign2 = sign(600,200,1)
        self.sign3 = sign(1500,200,2)
        self.sign4 = sign(3500,200,4)

        self.signs = [self.sign1,self.sign2,self.sign3,self.sign4]
        self.spikes = []

        self.levels = 1
        self.gravity = 20

        self.onPlatformJump = False
        self.onPlatform = False

        self.keys = 0

        self.block = False

#This function is the main game loop

def gameLoop(game,player1):
    game = game
    player1 = player1
    screenWidth = game.screenWidth
    screenHeight = game.screenHeight
    pygame.display.set_mode((screenWidth,screenHeight))

    ## GameRun stores the current status of the game
    ## (whether it is on or has been quited)

    while game.gameRun:
        
        game.clock.tick(15) 

        
        player1.goingLeft = False
        player1.goingRight = False

        #Check if the user quits the game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.gameRun = False
    
        #Store the keys pressed by the user
        game.keys = pygame.key.get_pressed()
        checkButtons(game.keys)

        #Camera mechanism to ensure player sprite doesn't
        #go off the screen
        if game.onScreenX > game.stageWidth - 150:
            game.onScreenX = game.stageWidth - 150
        
        if game.onScreenX > game.stageWidth - game.startScrollingPosX:
            player1.x = game.stageWidth - game.onScreenX 
            player1.x += 4 * game.screenWidth + game.startScrollingPosX

        #draw in the sprites and background into the screen
        drawWind()

        for enemy in game.enemies:
            if enemy.x < game.screenWidth:
                enemy.isVisible = True
            else:
                enemy.isVisible = False
            
            if not enemy.x < 100 and player1.x<enemy.x:
                enemy.goingLeft = True
                enemy.goingRight = False
                if enemy.isVisible:
                    enemy.initial -= 10
                
            elif player1.x > enemy.x:
                enemy.goingLeft = False
                enemy.goingRight = True
                if enemy.isVisible:
                    enemy.initial += 10
        
        #This switches levels once player reaches the door
        if player1.x > game.door1.x +50:
            if game.levels == 1:
                resetLevel2()
                game.level = level2()
                game.levels = 2
            elif game.levels == 2:
                resetLevel3()
                game.level = level3()
                game.levels = 3
            else:
                if Menu():
                    pygame.display.set_mode((screenWidth,screenHeight))
                    resetLevel1()
                    game.levels = 1
                    game.level = level1()
                    player1.lives = 3
                else:
                    pygame.quit()
                    game.gameRun = False
                
        #Displaying the game over screen and restarting the game
        if player1.lives == 0:
            for i in range(200):
                if game.gameRun:
                    pygame.time.delay(10)
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            game.gameRun = False
                            pygame.quit()
            
            player1.lives = 3
            game.score = 0
            game.levels = 1
            game.level = level1()
            resetLevel1()


pygame.init()
if Menu():
    player1 = character()
    game = currentLevel()
    gameLoop(game,player1)
pygame.quit()

