#!/usr/bin/python3

import pygame
import random

# initial configuration
pygame.init()   # starts pygame
pygame.display.set_caption("Snake Game")    # sets the title
width, height = 1000, 600
window = pygame.display.set_mode((width, height))    # sets the dimensions of the window
clock = pygame.time.Clock()   # creates the clock of the game (the loop must run, check conditions etc. based on this)

# colors (RGB)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# snake parameters
square_size = 20    # 20 by 20 pixels
game_speed = 15


def food_positions():
    """
    This function randomly chooses the positions of the food, considering that the food must be inside the window
    :return: (x_position, y_position)
    """
    x_food = round(random.randrange(0, width - square_size) / square_size) * square_size
    y_food = round(random.randrange(0, height - square_size) / square_size) * square_size
    return x_food, y_food


def draw_food(square_size, x_food, y_food):
    # format to draw: (window_created, color, [x_pos, y_pos, x_size, y_size])
    pygame.draw.rect(window, green, [x_food, y_food, square_size, square_size]) # draws the food


def draw_snake(size, pixel_list):
    for pixel in pixel_list:
        pygame.draw.rect(window, white, [pixel[0], pixel[1], size, size])


def draw_points(points):
    font = pygame.font.SysFont("Helvetica", 25) # defines the font and size
    text = font.render(f"Points: {points}", True, red)
    window.blit(text, [1, 1])   # writes the text


def select_speed(key):
    global x_speed
    global y_speed

    if key == pygame.K_DOWN and y_speed == 0:
        x_speed = 0
        y_speed = square_size
    elif key == pygame.K_UP and y_speed == 0:
        x_speed = 0
        y_speed = -square_size
    elif key == pygame.K_RIGHT and x_speed == 0:
        x_speed = square_size
        y_speed = 0
    elif key == pygame.K_LEFT and x_speed == 0:
        x_speed = -square_size
        y_speed = 0

    return x_speed, y_speed


def run_game():
    global x_speed
    global y_speed
    end = False
    # start variables
    x = width / 2
    y = height / 2
    x_speed = 0
    y_speed = 0
    snake_size = 1
    pixels = []
    x_food, y_food = food_positions()

    while not end:
        window.fill(black)

        for event in pygame.event.get():    # gets the user interaction (clicks)
            if event.type == pygame.QUIT:   # occurs if the user closes the game
                end = True
            elif event.type == pygame.KEYDOWN:  # when any key is pressed
                x_speed, y_speed = select_speed(event.key)

        draw_food(square_size, x_food, y_food)

        # update snake's position
        x += x_speed
        y += y_speed

        # borders
        if x < 0 or x >= width or y < 0 or y >= height:
            end = True

        # draw snake
        pixels.append([x, y])
        if len(pixels) > snake_size:    # if the snake is bigger, but no food was consumed, delete the tail pixel (move)
            del pixels[0]

        for pixel in pixels[:-1]:
            if pixel == [x, y]: # verifies if the current position is in the list (snake ate itself, except the head)
                end = True

        draw_snake(square_size, pixels)

        draw_points(snake_size - 1)

        pygame.display.update()  # updates the screen

        # new food
        if x == x_food and y == y_food: # if the head of the snake is in the food's position
            snake_size += 1
            x_food, y_food = food_positions()

        clock.tick(game_speed)  # applies the clock speed


run_game()
