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
        if keys[K_s] and self.rect.y <= 1080 - self.player_size_y - self.speed:
            self.rect.y += self.speed
        if keys[K_w] and self.rect.y >= self.speed:
            self.rect.y -= self.speed
    def update_right(self):
        keys = key.get_pressed()
        if keys[K_DOWN] and self.rect.y <= 1080 - self.player_size_y - self.speed:
            self.rect.y += self.speed
        if keys[K_UP] and self.rect.y >= self.speed:
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


L_Lifes = 3
R_Lifes = 3

font.init()
font1 = font.Font(None, 100)
font2 = font.Font(None, 50)
Win1 = font1.render('Player 1 Win!', True, (0,240,0))
Win2 = font1.render('Player 2 Win!', True, (0,240,0))

Game = True
Finish = False
clock = time.Clock()
FPS = 60
speed_x = 0
speed_y = 0

def start():
    global speed_x, speed_y
    speed_x = randint(-5, 5)
    if speed_x >= 0:
        speed_y = 5 - speed_x
    else:
        speed_y = 5 + speed_x

start()


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
        if R_Lifes > 1:
            R_Lifes -= 1
            ball.rect.x = 860
            ball.rect.y = 440
            L_rocket.rect.x = 0
            L_rocket.rect.y = 340
            R_rocket.rect.x = 1680
            R_rocket.rect.y = 340
            start()
        else:
            Finish = True
            window.blit(Win1, (700, 200))
    if ball.rect.x <= 0 - ball.player_size_x:
        if L_Lifes > 1:
            L_Lifes -= 1
            ball.rect.x = 860
            ball.rect.y = 440
            L_rocket.rect.x = 0
            L_rocket.rect.y = 340
            R_rocket.rect.x = 1680
            R_rocket.rect.y = 340
            start()
        else:
            Finish = True
            window.blit(Win2, (700, 200))
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
    L_Counter = font1.render('P1 Lifes: ' + str(L_Lifes), True, (255, 255, 255))
    R_Counter = font1.render('P2 Lifes: ' + str(R_Lifes), True, (255, 255, 255))
    window.blit(L_Counter, (100, 100))
    window.blit(R_Counter, (1470, 100))



    display.update()
    clock.tick(FPS)

