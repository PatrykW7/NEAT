import pygame
import os 
import math
import sys
import neat
import matplotlib.pyplot as plt
import keyboard
import time
import neat

screen_width = 1244
screen_height = 1016

# OKRESLENIE OKNA GRY W PYGAME
screen = pygame.display.set_mode((screen_width, screen_height))

# WYSWIETLENIE OKNA TORU
track = pygame.image.load(r"C:\\DeepLearning\\NEAT\\new_track2.png")

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(r"C:\\DeepLearning\\NEAT\\automobile.png")
        self.image = self.original_image
        # UMIESZCZENIE SAMOCHODZIKU NA MAPIE
        self.rect  = self.image.get_rect(center = (490,820))
        self.is_driveing = False
        self.vel_vector = pygame.math.Vector2(0.8,0)
        self.angle = 0
        # ZMIENNE ODPOWIADAJACE ZA SKRECANIE
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []

    def update(self):
        self.drive()
        self.rotate()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()
     

    def drive(self):
        if self.is_driveing:
            # PRZESUNIECIE PROSTOKATU O WEKTOR - JAZDA DO PRZODU
            self.rect.center += self.vel_vector * 6


    def rotate(self):
        # SKRET W PRAWO - OBROT OBIEKTU W STOPNIACH O OKRESLONY WEKTOR 
        if self.direction == 1:
            self.angle -= self.rotation_vel
            # OBROCENIE Z KONKRETNA PREDKOSCIA
            self.vel_vector.rotate_ip(self.rotation_vel)

        # SKRET W LEWO
        if self.direction == -1:
            self.angle += self.rotation_vel
            # OBROCENIE Z KONKRETNA PREDKOSCIA
            self.vel_vector.rotate_ip(-self.rotation_vel)
            
        # OBRACANIE I SKALOWANIE PRZESTRZENI GRAFICZNEJ
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1) 
        # OKRESLENIE NOWEJ POZYCJI SAMOCHODZIKA
        self.rect = self.image.get_rect(center = self.rect.center)



    def radar(self, radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        while not screen.get_at((x,y)) == pygame.Color(92,178,84) and length < 200:
            length +=1
            x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)

        # DRAWING RADARS
        # screen - obszar na ktorym jest rysowanie, 255, 255... - kolor, self.rect.center - punkt poczatkowy rysowania, (x,y) - punkt koncowy rysowania, 1 - grubosc linii
        pygame.draw.line(screen, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(screen, (0, 255, 0, 0), (x, y), 3)

        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2)
                   + math.pow(self.rect.center[1] - y,2 )))

        self.radars.append([radar_angle, dist])


        #for i, radar in enumerate(self.radars):
            # INPUT ZAWIERA WTEDY WARTOSCI DYSTANSU MIEDZY SRODKIEM SAMOCHODU A KRAWEDZIA TORU
        #    input[i] = int(radar[1])



    def collision(self):
        length = 40
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * length)]
        collision_point_left  = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle - 18)) * length)]

        # SET ALIVE = FALSE ON HITTING BORDER
        if screen.get_at(collision_point_right) == pygame.Color(2, 105, 31, 255) or \
            screen.get_at(collision_point_left) == pygame.Color(2, 105, 31, 255):
                self.alive = False
                print("stop exist")

# TWORZENIE KONTENERA, KTORY PRZECHOWUJE POJEDYNCZY SPRITE, INSTANCJI KLASY CAR
car = pygame.sprite.GroupSingle(Car())


def eval_genomes():
    run = True
    pygame.font.init()
    while run:
        
        print()
        myfont = pygame.font.SysFont(None, 30) 

        
        # ZAMYKANIE OKNA
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        # KOPIOWANIE POWIERZCHNI NA INNA POWIERZCHNIE, W OKIENKU KOPIUJE SIE TOR NA WSPOLRZEDNE 0, 0
        screen.blit(track, (0,0))

        
        # STEROWANIE SAMOCHODZIKIEM

        if sum(pygame.key.get_pressed()) <=1:
            # TRZEBA ODNOSIC SIE DO KLASY Z KTOREJ SIE DZIEDZICZY
            car.sprite.is_driveing = False
            car.sprite.direction = 0 

        if keyboard.is_pressed('up'):
            car.sprite.is_driveing = True

        if keyboard.is_pressed("left"):
            car.sprite.direction = -1
        
        if keyboard.is_pressed("right"):
            car.sprite.direction = 1

        
            
        # AKTUALIZACJE OBRAZU i OBIEKTOW
        # NA POWIERZCHNI SCREEN ZOSTAJE NARYSOWANY OBIEKT CAR
        car.draw(screen)
        car.update()

        # ODSWIEZANIE OKNA GRY
        pygame.display.update()
eval_genomes()


