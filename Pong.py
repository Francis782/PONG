#import pygame
import pygame
import sys
import random
import subprocess
import os

def fileExist(path):
    if os.path.exists(path):
        return True
    else:
        return False
    
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # Running as .exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)



    
def fileSearch(fileName):
    if fileExist(fileName):
        return fileName
    elif fileExist(get_resource_path(os.path.join("Resources", fileName))):
        return get_resource_path(os.path.join("Resources", fileName))
    elif fileExist(get_resource_path(os.path.join("Scripts", fileName))):
        return get_resource_path(os.path.join("Scripts", fileName))
    else:
        print(f"Error: {fileName} not found!")
        return None

#initialize
pygame.init()

#startup window
screenSizeX = 1000
screenSizeY = 600
screen = pygame.display.set_mode((screenSizeX, screenSizeY))

icon = pygame.image.load(fileSearch("ping-pong.png"))
pygame.display.set_icon(icon)
font = pygame.font.Font(fileSearch("joystix monospace.otf"), 20)
font2 = pygame.font.Font(fileSearch("joystix monospace.otf"), 35)
divider1 = pygame.image.load(fileSearch("road.png"))
divider2 = pygame.image.load(fileSearch("road.png"))
divider3 = pygame.image.load(fileSearch("road.png"))
divider4 = pygame.image.load(fileSearch("road.png"))
divider5 = pygame.image.load(fileSearch("road.png"))
divider6 = pygame.image.load(fileSearch("road.png"))


#Load Sounds
ballImpactSound = pygame.mixer.Sound(fileSearch("impact-sound-effect-8-bit-retro-151796.mp3"))
scoreSound = pygame.mixer.Sound(fileSearch("retro-hurt-1-236672.wav"))
powerHitSound = pygame.mixer.Sound(fileSearch("gameboy-pluck-41265.wav") )
slowDown = pygame.mixer.Sound(fileSearch("slowdown.mp3") )
gameEndSound = pygame.mixer.Sound(fileSearch("8-bit-game-4-188106(1).wav"))
selectSound = pygame.mixer.Sound(fileSearch("retro-coin-3-236679.wav"))

#players
player_1 = pygame.image.load(fileSearch("p1.png"))
player_1_x= 25
player_1_y= 300
player_1_dir = 0
p1Collision = pygame.Rect(player_1_x, player_1_y, 25, 120)

player_2 = pygame.image.load(fileSearch("p2.png"))
player_2_x= 955
player_2_y= 300
player_2_dir = 0
p2Collision = pygame.Rect(player_2_x, player_2_y, 25, 120)
baseSpeed = 0.3
paddleSpeed = baseSpeed + 0.1

winner = ""

#Ball
ball = pygame.image.load(fileSearch("circle.png"))
ballX = screenSizeX / 2
ballY = screenSizeY / 2
ballspeed = baseSpeed
ballXDir = -1
ballYDir = -1
ballcol = pygame.Rect(ballX, ballY, 16, 16)

#walls
wall1 = pygame.Rect(0, 0, 1000, 2)
wall2 = pygame.Rect(0, 598, 1000, 2)

#score
scoreP2 = pygame.Rect(0, -170, 15, 1500)
scoreP1 = pygame.Rect(970, -170, 15, 1500)

#score
P1Score = 0
P2Score = 0

text1 = "P1 Score: " + str(P1Score)
txt_surface = font.render(text1, True, (255, 0, 0))

text2 = "P2 Score: " + str(P2Score)
txt_surface2 = font.render(text2, True, (0, 255, 255))

#setup running variable
running = True

def Movement():
    global player_1_y, player_1_dir, player_2_y, player_2_dir, ballX, ballspeed, ballcol
    global ballXDir, ballY, ballYDir, p1Collision, p2Collision
    

    
    if (player_1_y + (paddleSpeed * player_1_dir)) < (screenSizeY - 120) and (player_1_y + (paddleSpeed * player_1_dir)) > 0:
        player_1_y += (paddleSpeed * player_1_dir)
        p1Collision.y = player_1_y

    if (player_2_y + (paddleSpeed * player_2_dir)) < (screenSizeY - 120) and (player_2_y + (paddleSpeed * player_2_dir)) > 0:
        player_2_y += (paddleSpeed * player_2_dir)
        p2Collision.y = player_2_y


    ballX += (ballspeed * ballXDir)
    ballY += (ballspeed * ballYDir)
    ballcol.x = ballX
    ballcol.y = ballY


def Detect_Event() :
    global player_1_dir
    global player_2_dir
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            global running 
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_1_dir = -1
            elif event.key == pygame.K_s:
                player_1_dir = 1


            if(event.key == pygame.K_UP and Gamemode == "twoPlayer"):
                player_2_dir = -1
            elif(event.key == pygame.K_DOWN and Gamemode == "twoPlayer"):
                player_2_dir = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_1_dir = 0 if (player_1_dir == -1) else player_1_dir
            elif event.key == pygame.K_s:
                player_1_dir = 0 if (player_1_dir == 1) else player_1_dir

            elif (event.key == pygame.K_UP and Gamemode == "twoPlayer") :
                player_2_dir = 0 if (player_2_dir == -1) else player_2_dir
            elif event.key == pygame.K_DOWN and Gamemode == "twoPlayer":
                player_2_dir = 0 if (player_2_dir == 1) else player_2_dir

def resetBall():
    global ballX, ballY, ballspeed, paddleSpeed
    ballX= screenSizeX / 2
    ballY = screenSizeY / 2
    ballspeed = baseSpeed
    paddleSpeed = baseSpeed + 0.1

def DrawObjects():
    screen.blit(divider1, (((screenSizeX / 2) - 25), 30))
    screen.blit(divider2, (((screenSizeX / 2) - 25), 130))
    screen.blit(divider3, (((screenSizeX / 2) - 25), 230))
    screen.blit(divider4, (((screenSizeX / 2) - 25), 330))
    screen.blit(divider5, (((screenSizeX / 2) - 25), 430))
    screen.blit(divider6, (((screenSizeX / 2) - 25), 530))
    screen.blit(player_1, (player_1_x, player_1_y))
    screen.blit(player_2, (player_2_x, player_2_y))
    screen.blit(ball, (ballX, ballY))
    screen.blit(txt_surface, (275, 20))
    screen.blit(txt_surface2, (520, 20))
    
    
    #screen.blit(scoreP2, (0, -70))
    #screen.blit(scoreP1, (970, -70))
    

def check_Collision():
    global wall1, ballcol, ballYDir, wall2, ballXDir, P1Score, P2Score, winner, Gamemode
    global ballY, ballX, text1, txt_surface, txt_surface2, ballspeed, paddleSpeed
    if wall1.colliderect(ballcol):
        ballYDir *= -1
        ballImpactSound.play()
    if wall2.colliderect(ballcol):
        ballYDir *= -1
        ballImpactSound.play()
    if p1Collision.colliderect(ballcol):
        ballXDir *= -1
        ballX += 9
        if (player_1_dir != 0 and random.randint(0, 1) == 1):
            ballImpactSound.play()
            powerHitSound.play()
            ballspeed *= 1.2
            paddleSpeed *= 1.2

        elif (player_1_dir == 0 and random.randint(0, 4) == 3):
            ballspeed = baseSpeed if ((ballspeed)/1.2 <= baseSpeed) else ballspeed/1.2
            paddleSpeed = baseSpeed + 0.1 if ((paddleSpeed)/ 1.2 <= baseSpeed + 0.1) else paddleSpeed/1.2
            slowDown.play()
            ballImpactSound.play()
        else :
            ballImpactSound.play()
    if p2Collision.colliderect(ballcol):
        ballXDir *= -1
        ballX -= 9
        if (player_2_dir != 0 and random.randint(0, 1) == 1):
            ballImpactSound.play()
            powerHitSound.play()
            ballspeed *= 1.2
            paddleSpeed *= 1.2
        elif (player_2_dir == 0 and random.randint(0, 4) == 3):
            ballspeed = baseSpeed if ((ballspeed)/1.2 <= baseSpeed) else ballspeed/1.2
            paddleSpeed = baseSpeed + 0.1 if ((paddleSpeed)/ 1.2 <= baseSpeed + 0.1) else paddleSpeed/1.2
            slowDown.play()
            ballImpactSound.play()
        else:
            ballImpactSound.play()
        
    if scoreP1.colliderect(ballcol):
        P1Score += 1
        text1 = "P1 Score: " + str(P1Score)
        txt_surface = font.render(text1, True, (255, 0, 0))
        scoreSound.play()
        if(P1Score == 5) :
            winner = "Player 1"
            gameEndSound.play()
            Gamemode = "GameEnd"
        resetBall()
    if scoreP2.colliderect(ballcol):
        P2Score += 1
        text2 = "P2 Score: " + str(P2Score)
        txt_surface2 = font.render(text2, True, (0, 255, 255))
        scoreSound.play()
        if(P2Score == 5) :
            winner = "Player 2"
            gameEndSound.play()
            Gamemode = "GameEnd"
        resetBall()

def PongTwoPlayer():
    
    screen.fill((0, 0, 0))
    DrawObjects()
    Movement()
    #pygame.draw.rect(screen, (255, 0, 0), scoreP1) 
    #pygame.draw.rect(screen, (0, 0, 255), scoreP2)
    check_Collision()

    pygame.display.update()
    Detect_Event()

def ComputerPlayer():
    global ballY, player_2_dir
    if player_2_y < ballY:
        player_2_dir = 1
    elif player_2_y > ballY:
        player_2_dir = -1
    else:
        player_2_dir = 0

def PongUb():
    
    screen.fill((0, 0, 0))
    DrawObjects()
    Movement()
    check_Collision()
    ComputerPlayer()
    pygame.display.update()
    Detect_Event()

    
Gamemode = "Menu"
pygame.display.set_caption("Main Menu")
textQ = font.render('Quit', True, (255, 0, 0))
text_rectQ = textQ.get_rect(center=(970, 550)).inflate(100, 10)
text7 = font.render("Instructions?" , True, (255, 0, 0))
text_rect7 = text7.get_rect(center=(1, 1)).inflate(220, 70)
running = True

while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if text_rect4.collidepoint(event.pos): 
                P1Score = 0
                P2Score = 0
                text1 = "P1 Score: " + str(P1Score)
                text2 = "P2 Score: " + str(P2Score)
                txt_surface = font.render(text1, True, (255, 0, 0))
                txt_surface2 = font.render(text2, True, (0, 255, 255))
                player_1_y= 300
                player_2_y= 300
                player_1_dir = 0
                player_2_dir = 0
                selectSound.play()
                Gamemode = "twoPlayer"
                pygame.display.set_caption("Two_Player")
            elif text_rect5.collidepoint(event.pos): 
                P1Score = 0
                P2Score = 0
                text1 = "P1 Score: " + str(P1Score)
                text2 = "P2 Score: " + str(P2Score)
                txt_surface = font.render(text1, True, (255, 0, 0))
                txt_surface2 = font.render(text2, True, (0, 255, 255))
                player_1_y= 300
                player_2_y= 300
                player_1_dir = 0
                player_2_dir = 0
                selectSound.play()
                Gamemode = "Unbeatable"
                pygame.display.set_caption("Unbeatable")
            elif text_rectQ.collidepoint(event.pos): 
                pygame.quit()
            elif text_rect7.collidepoint(event.pos): 
                selectSound.play()
                subprocess.run(["Python", fileSearch("Instructions.py")])
            
                


              

    
    if Gamemode == "Menu":
        screen.fill((0, 0, 0))
        text3 = font2.render('PONG', True, (255, 255, 255))
        text4 = font2.render('Two Player Mode', True, (255, 255, 0))
        text5 = font2.render('Unbeatable Mode', True, (255, 255, 0))
        screen.blit(text3, (400, 20))
        screen.blit(text4, (250, 200))
        screen.blit(text5, (250, 400))
        screen.blit(text7, (5, 5))
        text_rect4 = text4.get_rect(center=(470, 230)).inflate(25, 10)
        text_rect5 = text5.get_rect(center=(470, 425)).inflate(25, 10)
        text_rect7 = text7.get_rect(center=(1, 1)).inflate(220, 70)
        #pygame.draw.rect(screen, (0, 0, 200), text_rect7) 
        pygame.display.update()

    elif Gamemode == "twoPlayer":
        PongTwoPlayer()
    elif Gamemode == "Unbeatable" :
        PongUb()

    elif Gamemode == "GameEnd" :
        screen.fill((0, 0, 0))
        victor = winner + " Won "
        text6 = font2.render((victor + 'TRY AGAIN?'), True, (255, 0, 0)) if (winner == "Player 1") else font2.render((victor + 'TRY AGAIN?'), True, (0, 255, 255))
        text4 = font2.render('Two Player Mode', True, (255, 255, 0))
        text5 = font2.render('Unbeatable Mode', True, (255, 255, 0))
        textQ = font.render('Quit', True, (255, 0, 0))
        screen.blit(text6, (200, 20))
        screen.blit(text4, (250, 200))
        screen.blit(textQ, (900, 540))
        screen.blit(text5, (250, 400))
        text_rect4 = text4.get_rect(center=(470, 230)).inflate(25, 10)
        text_rect5 = text5.get_rect(center=(470, 425)).inflate(25, 10)
        text_rectQ = textQ.get_rect(center=(970, 550)).inflate(100, 10)
        #pygame.draw.rect(screen, (255, 0, 0), text_rectQ) 
        pygame.display.update()