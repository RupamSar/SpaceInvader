import math
import pygame
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
background = pygame.image.load("background.png")

mixer.music.load("backgroung.mp3")
mixer.music.play(-1)

playerImg = pygame.image.load("ship.png")
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (250, 250))  # Display "GAME OVER" at the center

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    return distance < 27

running = True
game_over = False  # Track game over state

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.mp3")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not game_over:
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(no_of_enemies):
            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

            if enemyY[i] > 440:  # Enemy reaches bottom = Game Over
                game_over = True
                break

            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletY = 480
                bullet_state = "ready"
                explosion_sound = mixer.Sound("explosion.mp3")
                explosion_sound.play()
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            if isCollision(enemyX[i], enemyY[i], playerX, playerY):  # Player hit
                game_over = True
                break

            enemy(enemyX[i], enemyY[i], i)

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        player(playerX, playerY)
        show_score(textX, textY)
    else:
        game_over_text()

    pygame.display.update()
