#Создай собственный Шутер!
from pygame import *
from random import randint
from time import sleep
from time import time as timer 

window = display.set_mode((700,500))
display.set_caption("a")
clock = time.Clock()
FPS = 60
scoreInt = 0
fatalInt = 0
font.init()


class GameSprite(sprite.Sprite):
    def __init__(self, img, ximg, yimg, x, y, s):
        super().__init__()
        self.image = transform.scale(image.load(img), (ximg, yimg))
        self.s = s
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.s
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.s
    def tapiy(self):
        pyla = Pylka("bullet.png", 30,40, self.rect.centerx, self.rect.y, 3)
        pyli.add(pyla)
        #zvyk_tapiva.play()
class Enemy(GameSprite):
    def update(self):
        global fatalInt
        self.rect.y += self.s
        if self.rect.y >= 460:
            fatalInt = fatalInt + 1
            self.rect.y = 0
            self.rect.x = randint(0, 700)
            self.s = randint(1, 3)
            if self.s == 3:
                self.s /=2
class Asteroid(GameSprite):
    def update(self):
        global fatalInt
        self.rect.y += self.s
        if self.rect.y >= 460:
            self.rect.y = 0
            self.rect.x = randint(0, 700)
            self.s = randint(1, 3)*0.7
            if self.s == 1.5:
                self.s =0.7
class Pylka(GameSprite):
    def update(self):
        self.rect.y -= self.s
        if self.rect.y <= 50:
            self.kill()
#totalPyl = 0
cosmolet = Player("rocket.png", 65, 100, 300, 405, 10)
pyli = sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()
asteroids.add(Asteroid("asteroid.png", 100, 75, 450, 450, 1))
x = 50
y = 75
s = 1
for i in range(5):
    e = Enemy("ufo.png", 100, 65, x, y, s)
    enemies.add(e)
    x = randint(0, 400)
    y = randint(0, 200)
    s = randint(1, 3)/2
    if s == 1.5:
        s /=2
background = transform.scale(image.load("galaxy.jpg"), (700,500))

game = True
finish = False
font = font.SysFont("Arial", 72)
#mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()
#zvyk_tapiva = mixer.Sound("fire.ogg")
win = font.render("Pabeda!!!", True, (50, 255, 75))
lose = font.render("Ne pabeda(((", True, (255, 50, 75))
reb = False
totalPyl = 0
last = timer()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if not reb and totalPyl <= 5:
                    cosmolet.tapiy()
                    totalPyl += 1
                if not reb and totalPyl >5:
                    reb = True
                    last = timer()
    if finish==False: 
        window.blit(background, (0,0))
        enemiesCollided = sprite.groupcollide(enemies, pyli, True, True)
        for e in enemiesCollided:
            scoreInt += 1
            newEnemy = Enemy("ufo.png", 100, 65, x, y, s)    
            x = randint(0, 400)
            y = randint(0, 200)
            s = randint(10, 30)/10
            enemies.add(newEnemy)
        if sprite.spritecollide(cosmolet, enemies, False) or fatalInt >=3:
            window.blit(lose, (200,250))
            display.update()
            finish = True
        if reb: 
            now = timer()
            if now - last <= 3:
                window.blit(font.render(("Перезардка..." + str(round(now - last, 2))), True, (150, 50, 255)), (200, 420)) 
            else:
                totalPyl = 0
                reb = False
        enemies.update()
        enemies.draw(window)
        cosmolet.update()
        cosmolet.reset()
        asteroids.update()
        asteroids.draw(window)
        window.blit(font.render(("Score:" + str(scoreInt)), True, (150, 50, 255)), (0, 0))
        window.blit(font.render(("Fatal:" + str(fatalInt)), True, (150, 50, 255)), (0, 60))
        
        pyli.update()
        pyli.draw(window)
        display.update()
        clock.tick(FPS)
    if scoreInt == 15:
        window.blit(win, (250,250))
        display.update()
        finish = True
    if finish == True:
        sleep(3)
        finish = False
        scoreInt = 0
        fatalInt = 0
        for pyla in pyli:
            pyla.kill()
        for enemy in enemies:
            enemy.kill()
        for i in range(5):
            e = Enemy("ufo.png", 100, 65, x, y, s)
            enemies.add(e)
            x = randint(0, 400)
            y = randint(0, 200)
            s = randint(1, 3)
            if s == 3:
                s /=2