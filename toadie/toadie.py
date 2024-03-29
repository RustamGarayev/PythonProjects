#!/usr/bin/python
# Toadie
# Code Angel

import sys
import os
import pygame
from pygame.locals import *

import toad
import world
import scoreboard

# Define the colours
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 121)

# Define constants
SCREEN_WIDTH = 448
SCREEN_HEIGHT = 512

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Toadie')
pygame.key.set_repeat(500, 200)

clock = pygame.time.Clock()

large_font = pygame.font.SysFont('Helvetica', 24)
score_font = pygame.font.SysFont('Helvetica Bold', 24)


def main():
    # Load images
    toad_lives_image = load_media('image', 'toad_lives')
    home_image = load_media('image', 'home')

    screen_blocks_wide = int(SCREEN_WIDTH / world.BLOCK_SIZE)

    # Initialize objects
    toadie = toad.Toad()
    score = 0
    hi_score = 0
    game_timer = world.Timer()

    # Create a list of pavement blocks the width of the screen
    pavement_blocks = []
    for counter in range(screen_blocks_wide):
        pavement_block = world.Pavement([counter, world.PAVEMENT_LANE_1])
        pavement_blocks.append(pavement_block)
        pavement_block = world.Pavement([counter, world.PAVEMENT_LANE_2])
        pavement_blocks.append(pavement_block)
    
    # Create list of landing pads
    landing_pads = []
    for counter in range(5):
        landing_pad = world.Pad(counter * 3)
        landing_pads.append(landing_pad)
    
    # Creating land objects
    traffic = []

    red_car_1 = world.RedCar(4)
    red_car_2 = world.RedCar(9)
    red_car_3 = world.RedCar(14)
    traffic.extend((red_car_1, red_car_2, red_car_3))

    digger_1 = world.Digger(6)
    digger_2 = world.Digger(11)
    digger_3 = world.Digger(16)
    traffic.extend((digger_1, digger_2, digger_3))

    purple_car_1 = world.PurpleCar(2)
    purple_car_2 = world.PurpleCar(7)
    purple_car_3 = world.PurpleCar(12)
    traffic.extend((purple_car_1, purple_car_2, purple_car_3))

    pink_car_1 = world.PinkCar(3)
    pink_car_2 = world.PinkCar(8)
    pink_car_3 = world.PinkCar(13)
    traffic.extend((pink_car_1, pink_car_2, pink_car_3))

    truck_1 = world.Truck(3)
    truck_2 = world.Truck(9)
    traffic.extend((truck_1, truck_2))

    # Creating river objects
    river = []
    turtle_a1 = world.Turtle(1, 3)
    turtle_a2 = world.Turtle(5, 3)
    turtle_a3 = world.Turtle(9, 3)
    turtle_a4 = world.Turtle(13, 3)
    river.extend((turtle_a1, turtle_a2, turtle_a3, turtle_a4))

    turtle_b1 = world.Turtle(2, 2)
    turtle_b2 = world.Turtle(6, 2)
    turtle_b3 = world.Turtle(10, 2)
    turtle_b4 = world.Turtle(14, 2)
    river.extend((turtle_b1, turtle_b2, turtle_b3, turtle_b4))

    log_a1 = world.Log(1, 1)
    log_a2 = world.Log(6, 1)
    log_a3 = world.Log(11, 1)
    river.extend((log_a1, log_a2, log_a3))
    
    log_b1 = world.Log(5, 3)
    log_b2 = world.Log(13, 3)
    river.extend((log_b1, log_b2))

    log_c1 = world.Log(3, 2)
    log_c2 = world.Log(9, 2)
    log_c3 = world.Log(15, 2)
    river.extend((log_c1, log_c2, log_c3))

    # Main game loop
    while True:
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_LEFT]:
                toadie.move('L')
            elif key_pressed[pygame.K_RIGHT]:
                toadie.move('R')
            elif key_pressed[pygame.K_UP]:
                toadie.move('U')
            elif key_pressed[pygame.K_DOWN]:
                toadie.move('D')
            
            elif key_pressed[pygame.K_RETURN] and (toadie.lives == 0 or toadie.home_count == 5):
                toadie = toad.Toad()
                score = 0
                game_timer = world.Timer()

                if new_hi_score > hi_score:
                    hi_score = new_hi_score
                
                del landing_pads[:]
                for counter in range(5):
                    landing_pad = world.Pad(counter * 3)
                    landing_pads.append(landing_pad)
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        game_screen.fill(DARK_BLUE)

        pygame.draw.rect(game_screen, BLACK, (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        game_screen.blit(home_image, [0, 0])

        for pavement in pavement_blocks:
            pavement.draw(game_screen)
        
        for pad in landing_pads:
            pad.draw(game_screen)
        
        for moving_river_object in river:
            moving_river_object.move(game_screen)
        
        for moving_road_object in traffic:
            moving_road_object.move(game_screen)
        
        toadie.draw(game_screen)

        toadie.check_collision(traffic)
        toadie.check_water(river)
        toadie.check_home(landing_pads, game_timer)

        game_timer.update_time()
        scoreboard.display_scores(game_screen, toadie.lives, score, game_timer.time_remaining, toad_lives_image)

        if game_timer.out_of_time() is True:
            toadie.die()
        
        if toadie.alive is False and toadie.lives > 0:
            toadie.check_death_pause(game_timer)
        
        if toadie.lives == 0 or toadie.home_count == 5:
            new_hi_score = check_hi_score(score, hi_score)
            scoreboard.game_over(game_screen, score, hi_score, new_hi_score)
        
        score = score + toadie.collect_points()
        pygame.display.update()
        clock.tick(30)


def check_hi_score(score, hi_score):
    new_hi_score = 0
    if score > hi_score:
        new_hi_score = score
    
    return new_hi_score


def load_media(media_type, filename):
    media = None
    full_path = os.path.dirname(os.path.realpath(__file__))

    if media_type == 'image':
        images_path = os.path.join(full_path, 'images')
        full_filename = os.path.join(images_path, filename + '.png')
        media = pygame.image.load(full_filename).convert_alpha()
    elif media_type == 'audio':
        audio_path = os.path.join(full_path, 'audio')
        full_filename = os.path.join(audio_path, filename + '.ogg')
        media = pygame.mixer.Sound(full_filename)
    
    return media

if __name__ == '__main__':
    main()