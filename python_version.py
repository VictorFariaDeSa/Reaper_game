"""
Como será definida a movimentação dos enimigos:
2 - colocar o player 2
4 - colocar npc
6 - aumentar spaw e velocidade dos inimigos com o tempo
7 - fazer um menu
8 - display de pontos
9 - menu de seleção de personagem
10 - scoreboard
11 - animações do movimento
12 - animações de ataque
13 - Novo background
14 - metodologia de pontuação
15 - achar uma fonte melhor
16 - colocar um parametro de dificuldade variando spawn rate and speed

"""

import pygame
import time
import random
import os
pygame.font.init()

# GAME PARAMETERS
FPS = 30
standart_player1_speed = 10
dash_player1_speed = 70

# SCREEN SETUP
WIDTH, HEIGTH = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("THE REAPER")

# GRAPHICS LOAD
def import_and_scale_character(folder,img):
    return pygame.transform.scale(pygame.image.load(os.path.join("graphics",folder,img)),(pygame.image.load(os.path.join("graphics",folder,img)).get_width() * 1.5,pygame.image.load(os.path.join("graphics",folder,img)).get_height() * 1.5))

BG = pygame.transform.scale(pygame.image.load(os.path.join("graphics","backgrounds", 'background.jpg')),(WIDTH, HEIGTH))
blue_reaper = import_and_scale_character("characters","Blue_reaper.png")
blue_reaper2 = import_and_scale_character("characters","Blue_reaper2.0.png")
blue_reaper_attaking = import_and_scale_character("characters","Blue_reaper_attacking.png")

creature = import_and_scale_character("monsters","enemy.png")




# CLASSES DEFINITION
class monster:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.std_image = None
        self.img = None
 
    def draw(self,window):
        window.blit(self.img, (self.x,self.y))

    def get_width(self):
        return self.img.get_width()
    
    def get_height(self):
        return self.img.get_height()
    
    def collision(self,obj):
        return collide(obj,self)

class Player(monster):
    COOLDOWN = 10 
    attacking_time = 2
    def __init__(self,x,y,image,image2,speed,upkey,downkey,leftkey,rightkey,dashkey):
        super().__init__(x,y)
        self.upkey = upkey
        self.downkey = downkey
        self.leftkey = leftkey
        self.rightkey = rightkey
        self.dashkey = dashkey
        self.speed = speed
        self.cooldown_counter = 0
        self.attacking_counter = 0
        self.std_img = image
        self.img = image
        self.mask = pygame.mask.from_surface(self.img)
        self.attacking = False
        self.facing = "right"
        
    def uptade_image(self):
        if self.attacking and self.facing =="right":
            self.img = pygame.transform.flip(blue_reaper_attaking,False,False)
        elif self.attacking and self.facing =="left":
            self.img = pygame.transform.flip(blue_reaper_attaking,True,False)
        else:
            if self.facing == "right":
                self.img = pygame.transform.flip(self.std_img, False,False)
            else:
                self.img = pygame.transform.flip(self.std_img, True,False)
        self.mask = pygame.mask.from_surface(self.img)
            
    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0 :
            self.cooldown_counter += 1

    def attack(self):
        if self.cooldown_counter == 0:
            self.attacking = True 
            self.cooldown_counter  += 1 
            #adicionar um contador de tempo para o tempo de ataque (este será o mesmo para contar o aumento de velocidade)
            
    def attacking_duration(self):
        if self.attacking and self.attacking_counter <= self.attacking_time:
            self.attacking_counter += 1
            self.speed = dash_player1_speed
        else:
            self.attacking = False
            self.speed = standart_player1_speed
            self.attacking_counter = 0
    def move(self,teclas):
        if teclas[self.leftkey]:
            self.x -= self.speed
            self.facing = "left"
        if teclas[self.downkey]:
            self.y += self.speed
        if teclas[self.rightkey]:
            self.x += self.speed
            self.facing = "right"
        if teclas[self.upkey]:
            self.y -= self.speed
        if teclas[self.dashkey]:
            self.attack()


class Enemy(monster):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img = creature
        self.mask = pygame.mask.from_surface(self.img)
        self.direita = True
        self.up = True
        self.x_vel = 30
        self.y_vel = 30

    def move(self):
        if self.x > WIDTH:
            self.direita = False
            self.img = pygame.transform.flip(creature, True,False)
        if self.direita:
            self.x += self.x_vel
        if self.direita == False:
            self.x -= self.x_vel
        if self.x < -200:
            self.direita = True
            self.img = pygame.transform.flip(creature, False,False)

        if self.y > HEIGTH:
            self.up = False
        if self.up:
            self.y += self.y_vel
        if self.up == False:
            self.y -= self.y_vel
        if self.y < -200:
            self.up = True



def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None

def create_enemie(vetor,valor):
    spawn = random.randint(0,valor)
    if spawn == 1: 
        offscrren_side = random.randint(1,4)
        if offscrren_side == 1:
            enimy = Enemy(random.randrange(-200,-150),random.randrange(-200,HEIGTH))
        elif offscrren_side == 2:
            enimy = Enemy(random.randrange(-200,WIDTH),random.randrange(-200,-150))
        elif offscrren_side == 3:
            enimy = Enemy(random.randrange(WIDTH,WIDTH+200),random.randrange(-200,HEIGTH))
        else:
            enimy = Enemy(random.randrange(-200,WIDTH),random.randrange(HEIGTH,HEIGTH+200))
        vetor.append(enimy)


def main():
    run = True
    enemies = []
    lives = 1
    score = 0
    main_font = pygame.font.SysFont("comicsans",50)

    player1 = Player(500,300 ,blue_reaper,blue_reaper2,standart_player1_speed,pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_SPACE)
    player2 = Player(700,300 ,blue_reaper,blue_reaper2,standart_player1_speed,pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,pygame.K_v)

    bot = Enemy(random.randrange(-200,WIDTH),random.randrange(-200,HEIGTH))

    clock = pygame.time.Clock()
    
    def draw_windown():
        WIN.blit(BG,(0,0))
        score_label = main_font.render(f"score:{score}",1,(255,255,255))
        lives_label = main_font.render(f"lives:{lives}",1,(255,255,255))
        for enimy in enemies:
            enimy.draw(WIN)
            enimy.move()

        player1.draw(WIN)
        player2.draw(WIN)
        
        WIN.blit(score_label,(10,10))
        WIN.blit(lives_label,(10,70))


        pygame.display.update()
    
    while run:
        bot.draw(WIN)
        clock.tick(FPS)
        create_enemie(enemies,  50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        player1.move(keys)
        player2.move(keys)
        for enimie in enemies:
            if player1.collision(enimie):
                if player1.attacking:
                    enemies.remove(enimie)
                    score +=1 
                else:
                    run = False
        for enimie in enemies:
            if player2.collision(enimie):
                if player2.attacking:
                    enemies.remove(enimie)
                    score +=1 
                else:
                    run = False



        player1.uptade_image()
        player1.attacking_duration()
        player1.cooldown()
        player2.uptade_image()
        player2.attacking_duration()
        player2.cooldown()
        
        

        draw_windown()

    pygame .quit()  
main()    


 