import pygame
import random
import math
from pygame import mixer

# Initialization of the module
pygame.init()

# Create a play window 800 px width, 600px of height
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# BGM(Background Music)
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
# This image is 64 x 64 px big
# Initial x and y coordinates of the playerImg
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_alien = 6

for i in range(num_of_alien):
    alienImg.append(pygame.image.load('alien.png'))
    # This image is 64 x 64 px big
    # Initial x and y coordinates of the alienImg
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(0, 50))
    alienX_change.append(0.2)
    alienY_change.append(0.2)

# Bullet
bulletImg = pygame.image.load('bullet.png')
# This image is 32 x 32 px big
# Initial x and y coordinates of the bulletImg
bulletX = playerX
bulletY = playerY
bulletY_change = 0.6
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)
global over
over = False


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    # Draw the playerImg on the game window screen at x,y point
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    # Draw the alienImg on the game window screen at x,y point
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    # Need access bullet_state variable within the function
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulX, bulY):
    distance = math.sqrt(math.pow(enemyX - bulX, 2) + math.pow(enemyY - bulY, 2))
    if distance < 27:
        return True
    else:
        return False;


def show_score(x, y):
    display = font.render("Score: " + str(score), True, (0, 255, 0))
    screen.blit(display, (x, y))


# Game Loop
running = True
while running:
    # Fill the screen color with RGB value
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    # Update the current x&y coordinate for the bullet according to the spaceship
    if bullet_state == "ready":
        bulletY = playerY
        bulletX = playerX

    # Check all the event to see what the user's input/move is
    for event in pygame.event.get():
        # When close button is pressed, close the window
        if event.type == pygame.QUIT:
            running = False
        # If keystroke is pressed check whether its right ot left
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    fire_bullet(bulletX, bulletY)
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Update the x and y coordinate of the spaceship
    playerX += playerX_change
    playerY += playerY_change
    # Checking boundaries for the spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Alien Movement
    for i in range(num_of_alien):
        # Game Over
        if isCollision(alienX[i], alienY[i], playerX, playerY):
            over = True

        if over:
            for j in range(num_of_alien):
                alienY[j] = 1000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        alienY[i] += alienY_change[i]
        # Checking boundaries for the alien
        if alienX[i] <= 0:
            alienX_change[i] = -alienX_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -alienX_change[i]
        if alienY[i] < 0:
            alienY_change[i] = -alienY_change[i]
        elif alienY[i] > 536:
            alienY_change[i] = -alienY_change[i]

        # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bullet_state = "ready"
            score += 1
            print(score)
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(0, 50)

        alien(alienX[i], alienY[i], i)

    # Bullet Movement
    if (bulletY + 32) <= 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    # Constantly update the game window if there is any change during the game
    pygame.display.update()
