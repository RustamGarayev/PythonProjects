# Toadie
# Code Angel

# Classes: Toad

import pygame

import toadie
import world

# Define constants
TOAD_START_X = 6
TOAD_START_Y = world.PAVEMENT_LANE_1

TOAD_DEATH_TIME = 2


class Toad:

    def __init__(self):
        self.image = toadie.load_media('image', 'toad')
        self.dead_image = toadie.load_media('image', 'dead_toad')
        
        self.hop_sound = toadie.load_media('audio', 'hop')
        self.death_sound = toadie.load_media('audio', 'death')
        self.home_sound = toadie.load_media('audio', 'home')

        self.rect = self.image.get_rect()
        self.padding_width = (world.BLOCK_SIZE - self.image.get_width()) / 2
        self.padding_height = (world.BLOCK_SIZE - self.image.get_height()) / 2
        
        self.rect.x = TOAD_START_X * world.BLOCK_SIZE + self.padding_width
        self.rect.y = TOAD_START_Y * world.BLOCK_SIZE + self.padding_height

        self.lives = 3
        self.points = 0
        self.home_count = 0
        self.alive = True
        self.death_pause_timer = 0
        self.furthest_forward = self.rect.y
    
    # Drawing toad either dead or alive
    def draw(self, game_screen):
        if self.alive is True:
            game_screen.blit(self.image, [self.rect.x, self.rect.y])
        else:
            game_screen.blit(self.dead_image, [self.rect.x, self.rect.y])
    
    # Moving toad one block ahead if alive and not at the edge of screen
    def move(self, direction):

        if self.alive is True:
            
            # Right
            if direction == 'R':
                if self.rect.x + world.BLOCK_SIZE < toadie.SCREEN_WIDTH:
                    self.rect.x += world.BLOCK_SIZE
                    self.hop_sound.play()
            
            elif direction == 'L':
                if self.rect.x - world.BLOCK_SIZE > 0:
                    self.rect.x -= world.BLOCK_SIZE
                    self.hop_sound.play()
            
            elif direction == 'U':
                self.rect.y -= world.BLOCK_SIZE
                self.hop_sound.play()

                # Adding 10 points for each step toadie takes towards home
                # If he moves down and up again, no points are added
                if self.rect.y < self.furthest_forward:
                    self.furthest_forward = self.rect.y
                    self.points += 10
            
            elif direction == 'D':
                if self.rect.y + 3 * world.BLOCK_SIZE < toadie.SCREEN_HEIGHT:
                    self.rect.y += world.BLOCK_SIZE
                    self.hop_sound.play()
    
    # Checking for collision
    def check_collision(self, vehicle_list):
        for vehicle in vehicle_list:
            if self.rect.colliderect(vehicle.rect):
                self.die()
    
    # Checking if toadie drawn down
    def check_water(self, river_list):

        toad_top = self.calc_toad_top()
        river_bottom_edge = world.PAVEMENT_LANE_2 * world.BLOCK_SIZE
        river_top_edge = world.HOME_LANE * world.BLOCK_SIZE

        # if toadie is between the middle pavement and home -- thats the river
        if river_top_edge < toad_top < river_bottom_edge:

            floating_toad = False

            for river_item in river_list:
                if self.rect.colliderect(river_item):
                    if self.rect.left > river_item.rect.left and self.rect.right < river_item.rect.right:
                        floating_toad = True
                        self.rect.x += river_item.speed
                    
            if floating_toad is False:
                self.die()
            
            if floating_toad is True and self.rect.right >= toadie.SCREEN_WIDTH:
                self.die()
            
            if floating_toad is True and self.rect.left <= 0:
                self.die()
        
    def check_home(self, home_pads, game_timer):

        toad_top = self.calc_toad_top()
        home_loc = world.HOME_LANE * world.BLOCK_SIZE

        if toad_top <= home_loc:

            found_home = False

            for pad in home_pads:

                if pad.rect.left <= self.rect.centerx <= pad.rect.right:

                    if pad.occupied is False:
                        found_home = True

                        pad.occupied = True
                        self.home_sound.play()
                        
                        self.points += 50
                        self.home_count += 1
                        
                        if self.home_count == 5:
                            self.points += 1000
                        
                        secs_left = game_timer.get_seconds_left()
                        self.points += 10 * secs_left
                        self.rect.x = TOAD_START_X * world.BLOCK_SIZE + self.padding_width
                        self.rect.y = TOAD_START_Y * world.BLOCK_SIZE + self.padding_height

                        self.furthest_forward = self.rect.y
                        game_timer.reset()
                    
                    else:
                        self.die()
            
            if found_home is False:
                self.die()
    
    def die(self):
        if self.alive is True:
            self.alive = False

            self.lives -= 1
            self.death_sound.play()

            if self.lives > 0:
                self.death_pause_timer = pygame.time.get_ticks()
    
    def check_death_pause(self, game_timer):

        elapsed_time = pygame.time.get_ticks() - self.death_pause_timer

        if elapsed_time > TOAD_DEATH_TIME * world.MILLISECONDS:

            self.alive = True
            self.rect.x = TOAD_START_X * world.BLOCK_SIZE + self.padding_width
            self.rect.y = TOAD_START_Y * world.BLOCK_SIZE + self.padding_height
            self.furthest_forward = self.rect.y
            game_timer.reset()
    
    def collect_points(self):
        collected_points = self.points
        self.points = 0
        
        return collected_points
    
    def calc_toad_top(self):
        return self.rect.y - self.padding_height













