#https://drive.google.com/drive/u/0/folders/1dMUddLYr8bHZOsPhEw9NJZh-AonB9GNZ
from pygame import * 
from pygame.sprite import Group
from random import randint 
#звук 
mixer.init() 
mixer.music.load("space.ogg") 
mixer.music.play(-1) 
fire = mixer.Sound("fire.ogg") 
score_f = 0
score = 0 
lost = 0 
class GameSprite(sprite.Sprite): 
 
    def __init__(self, player_image , player_x , player_y, size_x, size_y, player_speed): 
        sprite.Sprite.__init__(self) 
        self.image = transform.scale(image.load(player_image),(size_x, size_y))  
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
    def reset (self): 
        window.blit(self.image,(self.rect.x , self.rect.y)) 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        #зникає дійдучи до краю екрану
        if self.rect.y < 0:
            self.kill() 
class Player(GameSprite): 
    def update(self): 
        keys_pressed = key.get_pressed() 
        if keys_pressed [K_LEFT] and self.rect.x > 5 : 
            self.rect.x -= self.speed   
 
            keys_pressed = key.get_pressed() 
        if keys_pressed [K_RIGHT] and self.rect.x < win_width - 80 : 
            self.rect.x += self.speed 
 
 
    def fire(self): 
        pass
        
        bullet = Bullet(ammo, self.rect.x, self.rect.y, 15, 20, -15)
        bullets.add(bullet)
#лічильник збитих і пропущених кораблів 

class Enemy(GameSprite): 
    def update(self): 
        self.rect.y += self.speed 
        global lost  
 
        if self.rect.y > win_height: 
            self.rect.x = randint(80, win_width - 80) 
            self.rect.y = 0 
            lost = lost + 1 


class Friend():
    def __init__(self, player_image , player_x , player_y, size_x, size_y, player_speed): 
        sprite.Sprite.__init__(self) 
        self.image = transform.scale(image.load(player_image),(size_x, size_y))  
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
    def update(self):
        self.rect.y += self.speed
        global score_f
        if sprite.spritecollide(bullets, rockets_f, False):
            score_f = score_f + 1
        

#ігрова сцена 
win_width = 700 
win_height = 500 
window = display.set_mode((win_width, win_height)) 
display.set_caption("Shooter Game") 
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height)) 
#шрифти ы написи 
font.init() 
font3 = font.Font(None, 36)
font2 = font.Font(None, 36) 
font1 = font.Font(None,100)
#зображення 
asteroid_img = 'asteroid.png' 
ammo = 'bullet.png' 
rocket_img = 'rocket.png' 
ufo = 'ufo.png' 
rocket_f = 'rocket-friend.jpg'
#спайти 
rocket = Player(rocket_img, 5, win_height - 100, 80, 100, 20) 

monsters = sprite.Group() 
for i in range(1, 5): 
    monster = Enemy(ufo, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) 
    monsters.add(monster)  
asteroids = sprite.Group()
for i in range(1, 2):
    asteroid = Enemy( asteroid_img, randint(80, win_height - 80), -30,  80, 50, randint(1, 5))
    asteroids.add(asteroid)

rockets_f = sprite.Group()
for i in range(1, 3):
    rocket_f = Enemy( rocket_f, randint(80, win_height - 80), -30,  80, 50, randint(1, 5))
    rockets_f.add(rocket_f)
#змінна гра закінчилась 
bullets = sprite.Group()

finish = False 


#Основний цикл гри 
run = True 
lose = font1.render("YOU lose", True, (182,21,21))
win = font1.render("YOU win", True, (34,139,34))
while run: 
 
    #подія натискання на кнопку закрити 
     
    for e in event.get(): 
        if e.type == QUIT: 
            run = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                rocket.fire()
                
    if not finish: 

        window.blit(background, (0, 0)) 
        rocket.reset()
        rocket.update()

        asteroids.draw(window)
        bullets.draw(window)
        monsters.draw(window)
        rockets_f.draw(window)

        rockets_f.update()
        bullets.update()
        asteroids.update()
        monsters.update()

        text = font2.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_friendkill = font3.render("Своїх вбито:" + str(lost), 1, (255, 255, 255))
        window.blit(text_friendkill, (10, 50))

        if lost >= 5:
            finish = True
            window.blit(lose, (200, 200))
        if score >= 10:
            finish = True
            window.blit(win, (200, 200)) 
        if sprite.spritecollide(rocket,monsters, False):
            window.blit(lose, (200, 200))
            finish = True
        if sprite.spritecollide(rocket,asteroids, False):
            window.blit(lose, (200, 200))
            finish = True

        if sprite.spritecollide(rocket,rocket_f, False):
            window.blit(lose, (200, 200))
            finish = True

        collides = sprite.groupcollide(monsters,bullets, True, True)
        
        for c in collides:
            monster = Enemy(ufo, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) 
            monsters.add(monster) 
            score = score + 1
        collidesds = sprite.groupcollide(asteroids,bullets, True, True)
        for s in collidesds:
            asteroid = Enemy( asteroid_img, randint(80, win_height - 80), -30,  80, 50, randint(1, 5))
            asteroids.add(asteroid)
            score = score + 1

        for f in collides:
            rocket_f = Enemy( rocket_f, randint(80, win_height - 80), -30, 80, 50, randint(1, 5))
            rockets_f.add(rocket_f)
            score_f = score_f + 1


        display.update()
    

    time.delay(50)