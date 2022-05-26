from pygame import*
import pygame
from random import randint
import sys
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
pygame.init()
w_width = 700
w_height = 500
score= 0
lost = 0
font.init()
font2=font.SysFont('Arial',36)
#=-=-=-=-=-=-=-=-=-
display.set_caption("Shooter")
window = display.set_mode((w_width,w_height))
background = transform.scale(image.load("background.jpg"),(w_width,w_height))
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y)) #перемалювати гру з новим положенням спрайта
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Player(GameSprite):
    def control(self):
        keys = key.get_pressed()
        #=-=-=-=-=-=-=-=-=-керування-=-=-=-=-=-=-=-=-
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<550:
            self.rect.x+=self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx, self.rect.top, 20,20, 20) #вирівнювання кулі
        bullets.add(bullet)
bullets = sprite.Group()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > w_height:
            self.rect.x = randint(80,600)
            self.rect.y = 50
            lost += 1
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Bullet(GameSprite): #клас куля
    def update(self):
        self.rect.y = self.rect.y - self.speed #куля летить вертикально вгору
        if self.rect.y<0: # коли куля дістається кінця вона знищується
            self.kill()
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
finish = False
game = True
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
hero = Player("player.png",10,400,60,60,16)
#-=-=-=-
monsters = sprite.Group() #монстри - група спрайтів
for i in range(1,7):
    monster = Enemy("enemy.png",randint(80,400),-40,60,60,2)
    monsters.add(monster)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
lose = font2.render("ВИ ПРОГРАЛИ!", True, (250,250,250))
victory = font2.render("ВИ ВИГРАЛИ!", True, (250,250,250))
while game:
    for event1 in event.get():
        if event1.type == pygame.QUIT:
            sys.exit()
            game = False
        elif event1.type == KEYDOWN: #зажимання кнопки вниз
            if event1.key == K_SPACE:
                hero.fire()
    if not finish:
        window.blit(background,(0,0))
        text1=font2.render("РАХУНОК: "+str(score),1,(250,250,250))
        window.blit(text1,(25,25))
        text2=font2.render("ПРОПУЩЕНО:"+str(lost),1,(250,250,250))
        window.blit(text2,(25,50))
        hero.control()
        bullets.update()
        monsters.update()
        #=-=-=-=-=-=-=-=-=-=-=-=-=-=
        hero.reset()
        monsters.draw(window)
        bullets.draw(window)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        collides=sprite.groupcollide(bullets,monsters,True,True)
        for c in collides:
            score=score+1
            monster = Enemy("enemy.png",randint(80,400),-40,60,60,2)
            monsters.add(monster)
        if sprite.spritecollide(hero,monsters,True) or lost>=3:
            finish=True
            window.blit(lose,(200,200))
        if score>=10:
            finish=True


        display.update()
    time.delay(50)