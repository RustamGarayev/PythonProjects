# Toadie

# Classes: MovingObject, Digger, Truck, Car, Turtle, Log, Pavement, Pad, Timer

import pygame

import toadie

# Define constants
BLOCK_SIZE = 32

PAVEMENT_LANE_1 = 13
CAR_LANE_1 = 12
DIGGER_LANE = 11
CAR_LANE_2 = 10
CAR_LANE_3 = 9
TRUCK_LANE = 8
PAVEMENT_LANE_2 = 7
TURTLE_LANE_1 = 6
LOG_LANE_1 = 5
LOG_LANE_2 = 4
TURTLE_LANE_2 = 3
LOG_LANE_3 = 2
HOME_LANE = 1

TOAD_TIME = 45
MILLISECONDS = 1000

# Moving objects class
class MovingObjects:

    # All moving objects have and image, rectangle and speed
    def __init__(self, speed, location, object_image):
        self.image = toadie.load_media('image', object_image)
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * BLOCK_SIZE
        self.rect.y = location[1] * BLOCK_SIZE
        self.padding_height = (BLOCK_SIZE - self.image.get_height()) / 2
        self.speed = speed
    
    # All moving objects move using the same principles
    def move(self, game_screen):
        # Add speed on to x coordinate
        self.rect.x = self.rect.x + self.speed

        # Checking if the object passed the left of the screen
        if self.rect.right < 0:
            self.rect.x = toadie.SCREEN_WIDTH
        
        # When object goes off the screen on the right and start again on the left side
        if self.rect.left > toadie.SCREEN_WIDTH:
            self.rect.x = 0 - self.rect.width
        
        game_screen.blit(self.image, [self.rect.x, self.rect.y + self.padding_height])


# Land objects classes
class Digger(MovingObjects):
    def __init__(self, start_x):
        location = [start_x, DIGGER_LANE]
        MovingObjects.__init__(self, speed=2, location=location, object_image='digger')


class Truck(MovingObjects):
    def __init__(self, start_x):
        location = [start_x, TRUCK_LANE]
        MovingObjects.__init__(self, speed=-3, location=location, object_image='truck')


class RedCar(MovingObjects):
    def __init__(self, start_x):
        location = [start_x, CAR_LANE_1]
        MovingObjects.__init__(self, speed=-2, location=location, object_image='car_red')


class PurpleCar(MovingObjects):
    def __init__(self, start_x):
        location = [start_x, CAR_LANE_2]
        MovingObjects.__init__(self, speed=-3, location=location, object_image='car_purple')


class PinkCar(MovingObjects):
    def __init__(self, start_x):
        location = [start_x, CAR_LANE_3]
        MovingObjects.__init__(self, speed=-2, location=location, object_image='car_pink')


# Water objects classes, Turtle has either the size of 2 or 3
class Turtle(MovingObjects):
    def __init__(self, start_x, size):
        if size == 3:
            MovingObjects.__init__(self, speed=-3, location=[start_x, TURTLE_LANE_1], object_image='turtle3')
        else:
            MovingObjects.__init__(self, speed=-3, location=[start_x, TURTLE_LANE_2], object_image='turtle2')


# Log has the either the size of 1, 2 or 3
class Log(MovingObjects):
    def __init__(self, start_x, size):
        if size == 1:
            MovingObjects.__init__(self, 2, [start_x, LOG_LANE_1], 'log')
        elif size == 2:
            MovingObjects.__init__(self, 3, [start_x, LOG_LANE_3], 'log2')
        elif size == 3:
            MovingObjects.__init__(self, 4, [start_x, LOG_LANE_2], 'log3')


class Pavement:

    def __init__(self, location):
        self.x = location[0]
        self.y = location[1]
        self.image = toadie.load_media('image', 'pavement')
        self.rect = pygame.Rect(
            self.x * BLOCK_SIZE,
            self.y * BLOCK_SIZE,
            BLOCK_SIZE,
            BLOCK_SIZE
        )
    
    def draw(self, game_screen):
        game_screen.blit(self.image, [self.rect.x, self.rect.y])


# CLass for the last spot of toadie
class Pad:

    def __init__(self, x_coord):
        self.x = x_coord
        self.image = toadie.load_media('image', 'pad')
        self.occupied_image = toadie.load_media('image', 'occupied_pad')
        self.padding_width = (BLOCK_SIZE - self.image.get_width()) / 2 + self.image.get_width()
        self.padding_height = (BLOCK_SIZE - self.image.get_height()) / 2
        self.rect = pygame.Rect(
            self.x * BLOCK_SIZE + self.padding_width,
            HOME_LANE * BLOCK_SIZE + self.padding_height,
            BLOCK_SIZE,
            BLOCK_SIZE
        )
        self.occupied = False
    
    def draw(self, game_screen):
        if self.occupied is False:
            game_screen.blit(self.image, [self.rect.x, self.rect.y])
        else:
            game_screen.blit(self.occupied_image, [self.rect.x, self.rect.y])


# Timer class to keep the track of game time
class Timer:
    
    def __init__(self):
        self.duration = TOAD_TIME * MILLISECONDS
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = self.duration
    
    def update_time(self):
        new_time = pygame.time.get_ticks()
        elapsed_time = new_time - self.start_time
        self.time_remaining = self.duration - elapsed_time
        if self.time_remaining < 0:
            self.time_remaining = 0
    
    def out_of_time(self):
        if self.time_remaining < 0:
            no_time_left = True
        else:
            no_time_left = False
        
        return no_time_left
    
    def get_seconds_left(self):
        return int(self.time_remaining / MILLISECONDS)
    
    def reset(self):
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = self.duration

