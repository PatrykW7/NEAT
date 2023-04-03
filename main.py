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
screen = pygame.display.set_mode((screen_width, screen_height))
# OKRESLENIE OKNA GRY W PYGAME

# WYSWIETLENIE OKNA TORU
track = pygame.image.load("new_track2.png")
from samochodzik import Car


def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)



def eval_genomes(genomes, config):

    global cars, ge, nets

    cars = []
    ge = []
    nets = []
   

    # TWORZENIE INSTANCJI KLASY I SIECI NEURONOWYCH
    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    run = True
    pygame.font.init()
    while run:
        # ZAMYKANIE OKNA
        myfont = pygame.font.SysFont(None, 30) 
        mytext = myfont.render(str(pop.generation), 1, (255, 100, 100)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # KOPIOWANIE POWIERZCHNI NA INNA POWIERZCHNIE, W OKIENKU KOPIUJE SIE TOR NA WSPOLRZEDNE 0, 0
        screen.blit(track, (0,0))
        screen.blit(mytext, (600, 300))
        if len(cars) == 0:
            break
        
        for i, car in enumerate(cars):
            # INKREMENTOWANIE DOPASOWANIA WSZYSTKICH SAMOCHODOW NA TORZE
            ge[i].fitness += 1
            if not car.sprite.alive:
                remove(i)
        
        # OKRESLENIE KIEDY POJEDYNCZA INSTANCJA KLASY MA JECHAC
        for i, car in enumerate(cars):
            output = nets[i].activate(car.sprite.data())
            if output[0] > 0.7:
                car.sprite.direction = 1
            if output[1] > 0.7:
                car.sprite.direction = -1
            if output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0
            #print(output)
        # AKTUALIZACJE OBRAZU i OBIEKTOW
        # NA POWIERZCHNI SCREEN ZOSTAJE NARYSOWANY OBIEKT CAR
        for car in cars:
            car.draw(screen)
            car.update()

        # ODSWIEZANIE OKNA GRY
        pygame.display.update()


# SETUP NEAT NEURAL NETWORK

def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)

    # STATISTICS REPORTER

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, 10)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)