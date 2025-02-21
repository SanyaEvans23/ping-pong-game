from pygame import *
from random import randint


window = display.set_mode((1920,1080))
display.set_caption('Ping-Pong')

bg = transform.scale(image.load('sprites/bg.png'), (1920, 1080))


#23

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_size_y = player_size_y
        self.player_size_x = player_size_x
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_s] and self.rect.y <= 1080 - self.player_size_y - self.speed and K_block == False:
            self.rect.y += self.speed
        if keys[K_w] and self.rect.y >= self.speed and K_block == False:
            self.rect.y -= self.speed
    def update_right(self):
        keys = key.get_pressed()
        if keys[K_DOWN] and self.rect.y <= 1080 - self.player_size_y - self.speed and K_block == False:
            self.rect.y += self.speed
        if keys[K_UP] and self.rect.y >= self.speed and K_block == False:
            self.rect.y -= self.speed

class Ball(GameSprite):
    def update(self):
        global speed_x, speed_y
        self.rect.x += speed_x
        self.rect.y += speed_y
        if self.rect.y >= 1080 - self.player_size_y or self.rect.y <= 0:
            speed_y *= -1
            self.speed_boost(0.5)
    def speed_boost(self, speed_up):
        global speed_x, speed_y
        if speed_x >= 0:
            speed_x += speed_up
        else:
            speed_x -= speed_up
        if speed_y >= 0:
            speed_y += speed_up
        else:
            speed_y -= speed_up





L_rocket = Player('sprites/rocketka.png', 0, 340, 10, 240,400)
R_rocket = Player('sprites/rocketka.png', 1680, 340, 10, 240,400)

ball = Ball('sprites/ball.png', 860, 440, 20, 200,200)

font.init()
font1 = font.Font(None, 100)
lose1 = font1.render('Player 1 lose!', True, (180,0,0))
lose2 = font1.render('Player 2 lose!', True, (180,0,0))

Game = True
Finish = False
K_block = False
clock = time.Clock()
FPS = 60

speed_x = randint(-5, 5)
if speed_x >= 0:
    speed_y = 5 - speed_x
else:
    speed_y = 5 + speed_x



while Game:
    for e in event.get():
        if e.type == QUIT:
            Game = False
    if not Finish:
        window.blit(bg, (0, 0))

        L_rocket.update_left()
        L_rocket.reset()

        R_rocket.update_right()
        R_rocket.reset()

        ball.update()
        ball.reset()
    if ball.rect.x >= 1920:
        Finish = True
        window.blit(lose2, (700, 200))
    if ball.rect.x <= 0 - ball.player_size_x:
        Finish = True
        window.blit(lose1, (700, 200))
    if sprite.collide_rect(ball, L_rocket):
        if ball.rect.y + ball.player_size_y > L_rocket.rect.y and ball.rect.y < L_rocket.rect.y + L_rocket.player_size_y and L_rocket.rect.x + L_rocket.player_size_x <= ball.rect.x - speed_x:
            ball.speed_boost(0.5)
            speed_x *= -1
        else:
            if ball.rect.y > L_rocket.rect.y + L_rocket.player_size_y/2:
                if speed_y < 0:
                    speed_y *= -1
                else:
                    ball.rect.y = L_rocket.rect.y + L_rocket.player_size_y
            else:
                if speed_y >= 0:
                    speed_y *= -1
                else:
                    ball.rect.y = L_rocket.rect.y - ball.player_size_y

    if sprite.collide_rect(ball, R_rocket):
        if ball.rect.y + ball.player_size_y > R_rocket.rect.y and ball.rect.y < R_rocket.rect.y + R_rocket.player_size_y and R_rocket.rect.x >= ball.rect.x + ball.player_size_x - speed_x:
            ball.speed_boost(0.5)
            speed_x *= -1
        else:
            if ball.rect.y > R_rocket.rect.y + R_rocket.player_size_y / 2:
                if speed_y < 0:
                    speed_y *= -1
                else:
                    ball.rect.y = R_rocket.rect.y + R_rocket.player_size_y
            else:
                if speed_y >= 0:
                    speed_y *= -1
                else:
                    ball.rect.y = R_rocket.rect.y - ball.player_size_y




    display.update()
    clock.tick(FPS)

