#Abubakr Mohamed
#aamohame

import os
from tkinter import *
from socket import *
from tkinter import messagebox
import pygame
import random
import sys

### Seperate file had to be made for multiplayer
### as tkinter does not work after intializing pygame


######Credits (Sources for Sprites)#################

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

    def __init__(self,number):

        self.number = number

        #Defining the size and location of the sprite
        self.x = 50  
        self.y = 350
        self.width = 50
        self.height = 50 

        #Set variables to handle motion of player 
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

        #Hitboxes to handle collisions 
        self.hitbox = (self.x + 10, self.y,90,160)

        #Properties of the second player (different sprite)
        if self.number == 2:
            self.initial = self.x
            self.offset = 0
            self.walkRight = [pygame.image.load('GAME SPRITE/Edited/char 1/Run1.png'),
            pygame.image.load('GAME SPRITE/Edited/char 1/Run2.png'),
            pygame.image.load('GAME SPRITE/Edited/char 1/Run3.png'),
            pygame.image.load('GAME SPRITE/Edited/char 1/Run4.png'),
            pygame.image.load('GAME SPRITE/Edited/char 1/Run5.png'),
            pygame.image.load('GAME SPRITE/Edited/char 1/Run6.png')]
            self.walkLeft = [pygame.transform.flip(x, True, False) for x \
            in self.walkRight]
            self.standingRight = pygame.image.load('GAME SPRITE/Edited/char 1/StandingRight.png')
            self.standingLeft = pygame.image.load('GAME SPRITE/Edited/char 1/StandingLeft.png')
        
    #Function takes a window as input and draws the character into the window
    #the function also defines the sprites hitbox
    def draw(self,win):

        if self.number == 2:
            self.x = self.x - self.offset
            if self.goingRight:
                win.blit(self.walkRight[self.walkcount],(self.x,self.y))
            elif self.goingLeft:
                win.blit(self.walkLeft[self.walkcount],(self.x,self.y))

            else:
                if self.direction == 1:
                    win.blit(self.standingRight,(self.x,self.y))
                else:
                    win.blit(self.standingLeft,(self.x,self.y))
            
        #Place the sprite image on the screen ensuring that the player
        #can't move offscreen 
        else:
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

            #Handle the idle position of player (user not moving)
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

    def __init__(self,x,y,offset = 0,num=0):
    
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

        #Loading the boss sprite
        if num == 1:
            self.pic = pygame.image.load('enemySprite/enemy1 copy.png')
            self.pic2 = pygame.transform.flip(self.pic, True, False)
            self.pic3 = pygame.image.load('enemySprite/enemy4 copy.png')
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
        self.onScreenX = 50

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

############## Functions ############################

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

    player1.x,game.onScreenX = 200,200
    player1.y = 325
    player1.goingRight = False
    player1.goingLeft = False
    player1.isJumping = False
    player1.walkcount = 0
    player1.direction = 1    
    player1.jumpcount = 12
    player1.hitbox = (player1.x + 10, player1.y,90,160)
    game.diamonds = [diamond(500,250),diamond(1050,160),
    diamond(1125,160),diamond(1450,110),diamond(2000,250),
    diamond(3000,250),diamond(2850,110),diamond(4300,250)]

    game.platforms = [platform(900,330),platform(1600,330),
    platform(2670,330),platform(3100,330),platform(1150,265)]

    game.enemies = [enemyC(0,110,num=1)]
    game.signs = [sign(350,150,6)]

    game.spikes = [spike(1000,420),spike(1250,420),spike(1500,420),
    spike(1750,420),spike(2020,420),spike(2290,420),spike(2610,420),
    spike(2900,420),spike(3000,420),spike(3250,420),spike(3500,420),
    spike(3800,420),spike(4100,420)]

#This function draws the diamonds onto the screen 
def drawDiamonds():

    for diamond1 in game.diamonds:
        diamond1.offset = game.onScreenX

        #Handle the event of collecting a diamond
        if player1.goingRight or player1.direction == 1:
            if abs(diamond1.x - player1.x) <= 45 or abs(diamond1.x - player1.x - 90) <=45:
                if diamond1.y + 20 >= player1.y and diamond1.y + 41 <= player1.y + 160:
                    diamond1.collected = True
                    game.score += 1
                    game.diamonds.remove(diamond1)

        if player1.goingLeft or player1.direction == 0:
            if abs(diamond1.x + 41 - player1.x) <= 30 or abs(diamond1.x - player1.x)<=45:
                if diamond1.y + 20 >= player1.y and diamond1.y + 41 <= player1.y + 160:
                    diamond1.collected = True
                    game.score += 1
                    game.diamonds.remove(diamond1)

        #Display the diamond if it's not collected
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
                    
        platoi.draw(game.win)

#Function draws enemies and handles collisions with enemies

def drawEnemies():

    for enemy in game.enemies:
        enemy.offset = game.onScreenX
        enemy.hit = False
        
        #Hitboxes are used to detect collisions with player
        if game.levels != 3:
            if enemy.goingLeft:
                if enemy.x <= player1.x + 91 and enemy.x >= player1.x:
                    if player1.y + 120 > enemy.y + 20 and player1.y < enemy.y + 90:
                    
                        enemy.hit = True
                        enemy.draw(game.win)
                        game.hitSound.play()
                        death()
                    else:
                        enemy.hit = False
            
            elif enemy.goingRight:
                if enemy.x + 90 <= player1.x + 90 and enemy.x + 90 >= player1.x:
                    if player1.y + 120 > enemy.y and player1.y < enemy.y + 90:
                    
                        enemy.hit = True
                        enemy.draw(game.win)
                        game.hitSound.play()
                        death()
                    else:
                        enemy.hit = False
        
        enemy.draw(game.win)
    
    #Special hitbox specification for the boss
    if game.levels == 3:
        if game.enemies[0].y<player1.y - 100:
            game.enemies[0].y += 10
        elif game.enemies[0].y > player1.y - 100:
            game.enemies[0].y -= 10

        if game.enemies[0].x + 200 <= player1.x + 90 and game.enemies[0].x + 200 >= player1.x:
                if player1.y + 120 > game.enemies[0].y and game.enemies[0].y < enemy.y + 90:
                
                    game.enemies[0].hit = True
                    game.enemies[0].draw(game.win)
                    game.hitSound.play()
                    death()
                else:
                    game.enemies[0].hit = False
    

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

    global s,friend, SecondPlayeronScreenX, otherPlayerLevel

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

    mail = getMail(s) 
    messages = mail[0]

    #check the messages to receive the coordinates and relative
    #location of player 2.
    for i in messages:
        friend1 = i[0]
        message = i[1]
        
        if friend1 == friend:
            messageData = message.split()
            if messageData[0] == "Game":
                SecondPlayeronScreenX = float(messageData[1])
                player2.y = float(messageData[2])
                
                if messageData[3] == "True":
                    player2.goingLeft = True
                else:
                    player2.goingLeft = False

                if messageData[4] == "True":
                    player2.goingRight = True
                else:
                    player2.goingRight = False
                
                player2.walkcount = int(messageData[5])
                otherPlayerLevel = int(messageData[6])
                player2.direction = int(messageData[7])
                player2.x = int(messageData[8])

            #Check for end of game or quitting 
            elif message == "There's a winner":
                messagebox.showinfo("Game Over",friend+" won the game")
                game.gameRun = False
                

            elif message == "I quit":
                messagebox.showinfo("Game Over",friend + " has quit the game. You win !!!")
                game.gameRun = False

    #Only draw player 2 if they are on the same level       
    if otherPlayerLevel == game.levels:
        
        player2.offset = game.onScreenX - SecondPlayeronScreenX
        
        player2.draw(game.win)
    
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
    if player1.lives <= 0:
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

    #Send currrent player information over the server to the friend
    sendMessage(s,friend,"Game "+str(game.onScreenX)+" "+str(player1.y)+\
    " "+str(player1.goingLeft)+" "+str(player1.goingRight)+\
    " " +str(player1.walkcount)+" "+str(game.levels)+" "+str(player1.direction)\
    +" "+str(player1.x))

#This function checks the keys pressed by the user
#then maps the key to the appropriate function for the character to perform
def checkButtons(keys): 
    global SecondPlayeronScreenX
    
    #These are the directional buttons (Left and Right)
    if keys[pygame.K_LEFT]:
        player1.goingLeft = True
        player1.goingRight = False
        player1.direction = 0

        #Ensure that the player isn't blocked by a platform
        if not player1.x < 50:
            blocked1 = {}

            for i in game.platforms:
                blocked1[i] = False

            for platoi in game.platforms:
                if player1.x >= platoi.x + 230 \
                and player1.x <= platoi.x + 320 and not player1.isJumping:
                    if player1.y + 140 > platoi.y + 20:
                        blocked1[platoi] = True
    
            if game.platforms == []:
                block = False

            if blocked1:
                valuee = blocked1.values()
                if True in valuee:
                    block = True
                else:
                    block = False
            
            if not block:
            
                game.onScreenX -= player1.leftvelocity

        #Ensure that player's sprite doesn't leave the screen
        if game.onScreenX <= game.startScrollingPosX:
            player1.x = game.onScreenX
            
    #Handle player movement to the right
    elif keys[pygame.K_RIGHT]:
        player1.goingLeft = False
        player1.goingRight = True
        player1.direction = 1

        blocked = {}
        for i in game.platforms:
            blocked[i] = False

        for platoi in game.platforms:
            if player1.x + 120 >= platoi.x \
            and player1.x <= platoi.x + 230 and not player1.isJumping:
                if player1.y + 140 > platoi.y + 20:
                    blocked[platoi] = True
                    
        if game.platforms == []:
            block = False

        if blocked:
            valuee = blocked.values()
            if True in valuee:
                block = True
            else:
                block = False
        
        jumpBlocked = {}

        for platoi in game.platforms:
            jumpBlocked[platoi] = False
        
        for platoi in game.platforms:
            if player1.isFalling and player1.x + 155>= platoi.x\
            and not game.onPlatform and player1.y+160>platoi.y+20\
            and player1.x<=platoi.x+230:
                jumpBlocked[platoi] = True
        
        if game.platforms == []:
            jumpBlock = False

        if jumpBlocked:
            value2 = jumpBlocked.values()
            if True in value2:
                jumpBlock = True
            else:
                jumpBlock = False
            
        if not block and not jumpBlock:
            game.onScreenX += player1.rightvelocity
        
        if game.onScreenX <= game.startScrollingPosX:
            player1.x = game.onScreenX
              
    else:
        player1.goingLeft = False
        player1.goingRight = False
        player1.walkcount = 0
    
    #Secret code to draw more diamonds :)
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

#This function is the main game loop
def gameLoop(game,player1):

    global s,friend

    game = game
    player1 = player1
    screenWidth = game.screenWidth
    screenHeight = game.screenHeight
    pygame.display.set_mode((screenWidth,screenHeight))

    ## GameRun stores the current status of the game
    ## (whether it is on or has been quited)

    while game.gameRun:
        
        game.clock.tick(20) 

        player1.goingLeft = False
        player1.goingRight = False

        #Check if the user quits the game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.gameRun = False
                sendMessage(s,friend,"I quit")
    
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

        #Allow enemies to follow the player's path
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
            
            if game.levels == 3:
                enemy.initial += 20
        
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
                
                #Send the game-ending message once a player wins
                sendMessage(s,friend,"There's a winner")
                messagebox.showinfo("Game Over","You have won the game")
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

##############  HW 8 server helper functions   #############

#function takes in user's password and challenge received from server
#returns the chunks of ASCII values needed for MD5 hash
def createBlock(password,challenge):

    #concatenate the password and challenge 
    message = password+challenge
    block = message + "1"

    #add the zeros to create 509 character block
    while len(block) < 509:
        block += "0"
    
    #add the last three digits needed to complete 512 character block
    length = len(str(len(message)))
    block += "0" * (3-length) + str(len(message))

    M = []

    #find ASCII value of each element in 32 character blocks
    #store sum in list
    for i in range(0,len(block),32):
        sum = 0
        for k in range(i,i+32):
            sum += ord(block[k])
        M.append(sum)
    
    return M

#function returns the lists required for MD5 hash
def hashLists():

    s = [0]*64
    s[0:16] = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22]
    s[16:32] = [5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20]
    s[32:48] = [4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23]
    s[48:64] = [6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
    
    K = [0] * 64
    K[0:4] = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee]
    K[4:8] = [0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501]
    K[8:12] = [0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be]
    K[12:16] = [0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821]
    K[16:20] = [0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa]
    K[20:24] = [0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8]
    K[24:28] = [0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed]
    K[28:32] = [0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a]
    K[32:36] = [0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c]
    K[36:40] = [0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70]
    K[40:44] = [0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05]
    K[44:48] = [0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665]
    K[48:52] = [0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039]
    K[52:56] = [0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1]
    K[56:60] = [0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1]
    K[60:64] = [0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]

    return s,K

#function performs the necessary calculation as part of the Hash function
def leftrotate(x,c):
    return ((x << c) & 0xFFFFFFFF | (x >> (32 - c) & 0x7FFFFFFF >> (32-c)))

#function takes in user's password and challenge received from server
#returns the MD5 (message digest) required to login into server 
def hashFunction(password,challenge):

    #create the chunks and lists needed for hash
    M = createBlock(password,challenge)
    s,K = hashLists()

    for i in range(16):

        ##Initialize Variables
        a0 = 0x67452301
        b0 = 0xefcdab89
        c0 = 0x98badcfe
        d0 = 0x10325476
        A = a0
        B = b0
        C = c0
        D = d0

        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | ((~B) & D)
                F = F & 0xFFFFFFFF
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | ((~D) & C)
                F = F & 0xFFFFFFFF
                g = (5 * i + 1) % 16
            elif 32<= i <= 47:
                F = B ^ C ^ D
                F = F & 0xFFFFFFFF
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | (~D))
                F = F & 0xFFFFFFFF
                g = (7 * i) % 16

            dTemp = D
            D = C
            C = B
            B = B + leftrotate((A + F + K[i] + M[g]), s[i])
            B = B & 0xFFFFFFFF
            A = dTemp
    
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    result = str(a0) + str(b0) + str(c0) + str(d0)
    return result 

#function creates a socket and connects it to given IP address / Port Number
#returns the created socket 
def StartConnection (IPAddress, PortNumber):
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((IPAddress,PortNumber))
        
        return s

#function takes a socket, username and password and logs in to chat server
#Returns true if login successful / False otherwise
def login (s, username, password):

    #Send initial login command and receive reply
    s.send(bytes("LOGIN "+username+"\n","utf-8"))
    data = str(s.recv(512),"utf-8")
    data = data.strip()

    #ensure that username exists
    if data == "USER NOT FOUND":
        return False

    if len(data.split()) < 3:
        return False

    #extract challenge from reply and use challenge in hash function
    challenge = data.split()[2]
    messageDigest = hashFunction(password,challenge)

    #Send finalized login command with message Digest
    s.send(bytes("LOGIN "+username+" "+messageDigest+"\n","utf-8"))
    bdata = str(s.recv(512),"utf-8")

    if "WRONG PASSWORD!" in bdata:
        return False

    return True

#function to receive data from the server and split data into a list
def getData(s):
    data = str(s.recv(2048),"utf-8")
    Data = data.split("@")
    return Data

#function returns the list of active users on chat server
def getUsers(s):

    s.send(b"@users")
    userList = getData(s)[4:]
    
    return userList

#function returns the list of friends on chat server
def getFriends(s):

    s.send(b"@friends")
    friendList = getData(s)[4:]
    
    return friendList

#function returns the list of friend requests received
def getRequests(s):

    s.send(b"@rxrqst")

    requestData = getData(s)[3:]
    
    return requestData

#function takes friend's username and a message and sends it to them 
def sendMessage(s, friend, message):
    
    #caclulate total size of the command string
    #and send the send message command to server
    size = 16 + len(friend) + len(message)
    length = len(str(size))
    command = "@" + "0" * (5 - length) + str(size) 
    command += "@sendmsg@" + friend + "@" + message
    s.send(bytes(command,"utf-8"))
    reply = str(s.recv(512),"utf-8")

    if "message sent" in reply:
        return True
    return False

#function returns lists of tuples containing messages and files
#saves files that are received to local directory 
def getMail(s):

    s.send(b"@rxmsg")

    data = getData(s)
    i = 3
    
    #parse the reply from server using the keywords msg and file
    #append usernames and messages or usernames and filenames to tuples
    #save any files received 
    messages = []
    files = []
    while i < len(data):
        if data[i] == "msg":
            messages.append((data[i+1],data[i+2]))
            i += 3
        elif data[i] == "file":
            files.append((data[i+1],data[i+2]))
            filoi = open(data[i+2],"a")
            filoi.write(data[i+3])
            filoi.close
            i += 4

    return (messages,files)

#define the class for the login window
#allows user to proceed to main game client if login is successful
#Exit if login is unsuccessful
class loginWindow():
    
    #set the window's properties such as size and create labels and a button
    def __init__(self,root,socket):
        root.title("Multiplayer Login")
        root.geometry("200x200")
        self.lbl1 = Label(root,text="Username")
        self.username = Entry(root)
        self.lbl2 = Label(root,text="Password")
        self.password = Entry(root,show="*")
        self.okay = Button(root,text="OK",
        command=lambda : self.checkLogin(root,socket))
        self.align()
        self.lbl3 = Label(root,text="Incorrect Username/Password")

    #place all the content into the window
    def align(self):
        self.lbl1.pack()
        self.username.pack()
        self.username.focus()
        self.lbl2.pack()
        self.password.pack()
        self.okay.pack()

    #check the inputted username and password and attempt to login
    #Proceed to main game client if login is successful 
    def checkLogin(self,root,socket):
        user = self.username.get()
        password = self.password.get()
        if login(socket,user,password):
            root.destroy()
            mainWnd = Tk()
            gameRequestWindow(mainWnd,socket,user)
            mainWnd.mainloop()
            
        else:
            if not self.lbl3.winfo_ismapped():
                self.lbl3.pack()
         
#create the main game client window with all the features (sending,
#accepting requests and starting games)
class gameRequestWindow():

    #set the window's properties such as title
    #create labels and buttons and lists of users / friends
    def __init__(self,root,socket,username):
        self.username = username
        root.title("Multiplayer Client")
        root.minsize(height=230, width=570)
        self.mainframe = Frame(root)
        self.emptylabel = Label(self.mainframe)
        self.emptylabel2 = Label(self.mainframe)

        self.pendingRequest = []
        root.protocol("WM_DELETE_WINDOW",
        lambda:self.closeWnd(root,self.pendingRequest,socket))

        #list to store the currently received game requests
        self.currentRequests = []

        self.frame2 = Frame(self.mainframe)
        self.frame3 = Frame(self.mainframe)
    
        self.lbl2 = Label(self.frame2,text="Your Friends")
        self.lbl3 = Label(self.frame3,text="Pending Requests")

        self.bttn2 = Button(self.frame2,text="Send Game Request",
        command = lambda: self.sendGameRequest(socket,username))
        self.bttn3 = Button(self.frame3,text="Accept Request",
        command = lambda : self.acceptRequest(socket))
  
        self.list2 = Listbox(self.frame2)
        self.list3 = Listbox(self.frame3)

        self.root = root

        self.updateLists(socket)
        self.displayWnd()
       

        self.checkRequests(socket)
    
    #display the contents of the window into main frame
    def displayWnd(self):
       
        self.mainframe.pack(fill=BOTH,expand=TRUE)
        self.emptylabel.pack(side=LEFT)
     
        self.frame2.pack(side=LEFT,fill=BOTH,expand=TRUE)
        self.frame3.pack(side=LEFT,fill=BOTH,expand=TRUE)
        self.emptylabel2.pack(side=LEFT)

        self.lbl2.pack(fill=X)
        self.lbl3.pack(fill=X)

        self.list2.pack(fill=BOTH,expand = True)
        self.list3.pack(fill=BOTH,expand = True)

        self.bttn2.pack(fill=X)
        self.bttn3.pack(fill=X)
    

    #refresh the friends and requests lists from the server
    def updateLists(self,socket):
        currentFriend = list(self.list2.get(0,END))
        currentDisplayedRequests = list(self.list3.get(0,END))
        
        friends = getFriends(socket)
        
        #compare current friend list with new version
        #refresh if there is a change in the list
        if currentFriend != friends:
            self.list2.delete(0,END)
            for i in range(len(friends)):
                self.list2.insert(i,friends[i])
        
        #get list of requests and remove repeated requests
        #self.requests = getRequests(socket)
        nonrep = []

        for i in self.currentRequests:
            if i not in nonrep:
                nonrep.append(i)

        if currentDisplayedRequests != nonrep:
            self.list3.delete(0,END)
            for i in range(len(nonrep)):
                self.list3.insert(i,nonrep[i])
        
        self.list2.after(1000,lambda : self.updateLists(socket))
       
    #function for accepting game requests 
    def acceptRequest(self,socket):
        global player1, game, player2, friend

        if self.list3.curselection() != ():
            friend = self.list3.get(self.list3.curselection())
            self.currentRequests.remove(friend)
            
            sendMessage(socket,friend,"Game Accepted")
            
            pygame.init()
            player1 = character(1)
            player2 = character(2)
            game = currentLevel()
            gameLoop(game,player1)
            pygame.quit()

            self.root.destroy()

    #Function takes in friend name and sends a game request
    def sendGameRequest(self,socket,username,friend=0):

        if friend == 0 and self.list2.curselection() != ():
            friend = self.list2.get(self.list2.curselection())
        
        #Ensure that player doesn't send a request to themself
        if friend != 0 and friend != username:
       
            sendMessage(socket,friend,"Game Request")
            messagebox.showinfo("Success","Request to "\
            + friend + " sent successfully")

            if not friend in self.pendingRequest:
                self.pendingRequest.append(friend)

    #function removes game requests once a user closes the game client
    def closeWnd(self,root,Requests,socket):
        for friend in self.pendingRequest:
            sendMessage(socket,friend,"Request Cancelled")
        
        self.root.destroy()
    
    #function checks servers for messages
    #Updates the request list if a game request has been received
    def checkRequests(self,socket):
        mail = getMail(socket) 
        messages = mail[0]

        #check all the messages and display them on chat windows
        #create chat window if not already present
        if messages:
            for i in messages:
                friend1 = i[0]
                message = i[1]
                if message == "Game Request":
                    if not friend1 in self.currentRequests:
                        self.currentRequests.append(friend1)
                
                elif message == "Request Cancelled":
                    if friend1 in self.currentRequests:
                        self.currentRequests.remove(friend1)
                
                #Start a game if a request has been accepted
                elif message == "Game Accepted":
                    global friend, player1, player2, game

                    friend = friend1
                    
                    pygame.init()
                    player1 = character(1)
                    player2 = character(2)
                    game = currentLevel()
                    gameLoop(game,player1)
                    pygame.quit()

                    self.root.destroy()

        self.list2.after(50,lambda : self.checkRequests(socket))

#Create a socket and connect to server       
#Display the multiplayer login window
def startMulti():

    global s
    s = StartConnection("86.36.46.10",15112)
    l = Tk()
    loginWindow(l,s)
    l.mainloop()

SecondPlayeronScreenX = 0
otherPlayerLevel = 1
startMulti()
