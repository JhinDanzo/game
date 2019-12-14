import pygame
import datetime
import math
import random

pygame.init()
window_height = 500
window_width = 500
win = pygame.display.set_mode((window_height, window_width))
pygame.display.set_caption('Cosmic Odyssey')
clock = pygame.time.Clock()

#Player
player_image = pygame.image.load('spaceship.png')
x = 225
y = 440
widht = 50
height = 50
speed = 8
left = False
right = False

#Enemy
enemy_speed = 5
enemy_image = pygame.image.load('enemy1.png')
enemy_width = 50
enemy_heiht = 50
enemy_x = random.randint(50, 450)
enemy_y = -60

#Background
back = pygame.image.load('Back.jpg')

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 14)
text_x = 5
text_y = 20

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 40)
#Start text
start_font = pygame.font.Font('freesansbold.ttf', 10)

def show_score(text_x, text_y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 0))
    win.blit(score, (text_x, text_y))

def hello():
    first_msg = start_font.render('You must score 20 points', True, (255, 255, 0))
    win.blit(first_msg, (5, 10))

# Bullets
class Projectile():

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 15

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def creation_of_objects():

    win.fill((0, 0, 0))

    #Background
    win.blit(back, (0, 0))

    #Player
    win.blit(player_image, (x, y))

    #Enemy
    win.blit(enemy_image, (enemy_x, enemy_y))

    for bullet in bullets:  # Bullet creation
        bullet.draw(win)


# Main game cycle
start_time = datetime.datetime.now()
run = True
bullets = []
while run:
    clock.tick(30) # fps

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
    # Bullet destruction
    for bullet in bullets:
        if bullet.y < 500 and bullet.y > 0:
            bullet.y -= bullet.vel # bullet speed

        else:
            bullets.pop(bullets.index(bullet))
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > speed:
        x -= speed
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 500 - widht - speed:
        x += speed
        left = False
        right = True
    else:
        left = False
        right = False
    # Collision creation
    enemy_image = pygame.image.load('enemy1.png')

    for bullet in bullets:
        distance = math.sqrt(math.pow(enemy_x - bullet.x, 2) + math.pow(enemy_y - bullet.y, 2))
        if distance < 35:
            enemy_image = pygame.image.load('explosion.png')
            bullets.pop(1)
            score_value += 1
            enemy_x = random.randint(50, 450)
            enemy_y = 5

    # Creation of delay between shots
    shooting = True
    if enemy_y > 440 or score_value == 20: # if game over stop shooting
        shooting = False

    current_time = datetime.datetime.now()
    if shooting is True and (current_time - start_time) > datetime.timedelta(milliseconds=200):
        start_time = datetime.datetime.now()
        bullets.append(Projectile(round(x + widht // 2), round(y - height // 5), 2, (255, 0, 0)))

    # Enemy movement
    '''enemy_x += enemy_speed
    if enemy_x <= 0:
        enemy_speed = 4
    elif enemy_x >= 500 - enemy_width:
        enemy_speed = -4'''
    enemy_y += 9

    creation_of_objects()
    show_score(text_x, text_y)
    hello()

    # Game over
    if enemy_y > 440:
        enemy_y = 600
        game_over = over_font.render('Game Over!', True, (255, 255, 0))
        win.blit(game_over, (127, 250))
        player_image = pygame.image.load('explosion.png')

    # Victory
    if score_value == 20:
        enemy_y = -1000
        enemy_speed = 0
        victory = over_font.render('Winner!!!', True, (255, 255, 0))
        win.blit(victory, (160, 250))

    pygame.display.update()

pygame.quit()

