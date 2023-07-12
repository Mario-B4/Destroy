import pygame
import os
pygame.font.init()
pygame.mixer.init()

#window values
WIDTH, HEIGHT = 900, 500
WIN =  pygame.display.set_mode((WIDTH, HEIGHT))
#display.set_caption titles the window of the game
pygame.display.set_caption("Destroy!")

#setting value (gree, blue, red), used for background
WHITE = (255, 255, 255)
#setting value, used for border
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255,255,0)
#setting value of where the border will be placed
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Boom.wav'))
BULLET_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun.mp3'))
GAME_OVER = pygame.mixer.Sound(os.path.join('Assets', 'Game-over.wav'))

#limiting the refresh of the program to 60 fps to ensure all machines are on the same or close to the same level
FPS = 60
#adding font for health display and winning
HEALTH_FONT = pygame.font.SysFont ('comicsans', 40)
WINNER_FONT = pygame.font.SysFont ('Comicsans', 60)
#Setting sprite/character movement left (velocity = 5), this can be changed to any value. Setting this value also allows for future use without manual math each time
VEL = 5
#Bullet speed
BULLET_VEL = 7
#Number of bullets
MAX_BULLETS = 3
#ship size (width,height or x,y)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

#creating player/user events for bullets interaction
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#this loads the image of your 'sprite' or character
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
#The transform.scale will allow you to adjust size of the image inside the game window
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

#Draw window adds to the game window (fill = color), blit = adding layers (text, images, etc) - Order matters, put background in, then images/text
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)

    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))
    
    for bullet in red_bullets:
          pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
          pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()

#defining value for yellow key movement
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed [pygame.K_a] and yellow.x - VEL > 0: #Left
            yellow.x -= VEL
    if keys_pressed [pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
            yellow.x += VEL
    if keys_pressed [pygame.K_w] and yellow.y - VEL > 0: #UP 
            yellow.y -= VEL
    if keys_pressed [pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #DOWN
            yellow.y += VEL

#defining value for red movement arrows
def red_handle_movement(keys_pressed, red):
    if keys_pressed [pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #Left
            red.x -= VEL
    if keys_pressed [pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
            red.x += VEL
    if keys_pressed [pygame.K_UP] and red.y - VEL > 0: #UP
            red.y -= VEL
    if keys_pressed [pygame.K_DOWN]and red.y + VEL + red.height < HEIGHT - 15: #DOWN
            red.y += VEL

#defining handle_bullet collision
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)  

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
          
def draw_winner (text):
     draw_text = WINNER_FONT.render(text, 1, WHITE)
     WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()))
     pygame.display.update()
     pygame.time.delay(3000)

#this is the value for the game to run - it will fun infiniately until it is ended of proven false
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

#this is defining the number of bullets allowed to each ship
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock ()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
#this is preparing the event for left and right control to allow each ship to fire.
            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        BULLET_SOUND.play()
                  
                  if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append(bullet)
                        BULLET_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "GAME OVER - YELLOW WINS!"
            GAME_OVER.play()
            
        if yellow_health <= 0:
            winner_text = "GAME OVER - RED WINS!"
            GAME_OVER.play()

        if winner_text != "":
            draw_winner (winner_text)
            break
                         
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement (keys_pressed, yellow)
        red_handle_movement (keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

#this ensures that thte program is running on its own and is not a part of another function or algorithm
if __name__ == "__main__":
    main()