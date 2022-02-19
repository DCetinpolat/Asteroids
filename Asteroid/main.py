import pygame
from pygame.version import PygameVersion
import os
from random import randint
import sys

#Einstellungen von PyGame
class settings:
    window_width =1000
    window_height = 800
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image= os.path.join(path_file,"images")
    fps=60
    caption = "Meteoritenschauer"
    nof_meteors = 3

#Background Klasse
class background:
    def __init__(self,filename="background.png"):
        super().__init__()
        self.image = pygame.image.load(os.path.join(settings.path_image,filename)).convert()
        self.image = pygame.transform.scale(self.image,(settings.window_width,settings.window_height))


    def draw(self,screen):
        screen.blit(self.image,(0,0))

#Alien sprite klasse
class alien(pygame.sprite.Sprite):
    def __init__(self,picturefile) -> object:
        super().__init__()
        self.image=pygame.image.load(os.path.join(settings.path_image,picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect=self.image.get_rect()
        #Alien spawn
        self.rect.left=400
        self.rect.top=600
        self.speed_h = 0
        self.speed_v = 0

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.rect.top >= settings.window_height:
            self.rect.centery = 2
        if self.rect.centery <= 0:
            self.rect.centery = settings.window_height 
            
        if self.rect.left >= settings.window_width:
            self.rect.centerx = 2
        if self.rect.centerx <= 0:
            self.rect.centerx = settings.window_width 

        self.rect.move_ip((self.speed_h, self.speed_v))

    def stop(self):
        self.speed_v = self.speed_h = 0

    def down(self):
        self.speed_v = 6

    def up(self):
        self.speed_v = -6

    def left(self):
        self.speed_h = -6

    def right(self):
        self.speed_h = 6

#Meteorit sprite klasse
class meteorit(pygame.sprite.Sprite):
    def __init__(self,filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(settings.path_image,filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,150))
        self.rect=self.image.get_rect()
        self.speed_h = randint(1,5)
        self.speed_v = randint(1,5)
        scale_ratio = randint(2, 6) / 4
        self.image = pygame.transform.scale(self.image, ( int(self.image.get_rect().width * scale_ratio),int(self.image.get_rect().height * scale_ratio)))
        self.randompos()

    def randompos(self):

        self.rect.left = randint(0, settings.window_width - self.rect.width)

    def draw(self,screen):
        screen.blit(self.image_1,self.rect)

    def update(self):
        self.rect.move_ip(self.speed_h,self.speed_v)

        if self.rect.top >= settings.window_height:
            self.rect.centery = 2
        if self.rect.centery <= 0:
            self.rect.centery = settings.window_height 
            
        if self.rect.left >= settings.window_width:
            self.rect.centerx = 2
        if self.rect.centerx <= 0:
            self.rect.centerx = settings.window_width 




#Game Klasse
#Diese Klasse verwaltet alle Komponenten und Logiken des Spiels.
class Game(object):
    def __init__(self,)-> None:
        super().__init__()
        #Fenster größe
        os.environ['SDL_VIDEO_WINDOW_POS'] = "380,100"
        pygame.init()
        pygame.display.set_caption(settings.caption)
        self.screen=pygame.display.set_mode((settings.window_width,settings.window_height))
        self.clock=pygame.time.Clock()
        self.background= background()
        self.meteorit=meteorit("meteorit.png")
        self.alien=alien("0.png")
        self.all_meteor=pygame.sprite.Group()
        self.all_meteor.add(self.meteorit)



        self.running= False

#Spielstart
    def run(self):
        self.start()
        self.running = True
        while self.running:
            self.clock.tick(settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
            self.check_for_collision()


        pygame.quit()

    #Tastatur event und andere events
    def watch_for_events(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.alien.down()
                elif event.key == pygame.K_UP:
                    self.alien.up()
                elif event.key == pygame.K_LEFT:
                    self.alien.left()
                elif event.key == pygame.K_RIGHT:
                    self.alien.right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.alien.stop()
                elif event.key == pygame.K_UP:
                    self.alien.stop()
                elif event.key == pygame.K_LEFT:
                    self.alien.stop()
                elif event.key == pygame.K_RIGHT:
                    self.alien.stop()

#Aktualisiert die Sprites und  andere Spielkomponenten.
    def update(self):
        self.check_for_collision()
        self.alien.update()
        self.all_meteor.update()

        


    
    def start(self):
        self.background= background()

        for a in range(settings.nof_meteors):
           self.all_meteor.add(meteorit ("meteorit.png"))



    

#Kollisions kontrolle
    def check_for_collision(self):
        self.alien.hit = False
        for s in self.all_meteor:
            if pygame.sprite.collide_mask(s,self.alien):
                self.alien.hit = True
                if self.alien.hit == True:
                   self.running = False


#Zeichnet alle Bitmaps auf dem Bildschirm.
    def draw(self):
        self.background.draw(self.screen)
        self.all_meteor.draw(self.screen)
        self.alien.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':

    game = Game()
    game.run()

        
