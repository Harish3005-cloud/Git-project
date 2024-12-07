import pygame
import time
import random
import sys

# Initialize Pygame
pygame.init()

# Window size
window_x = 720
window_y = 480

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Initialize game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS controller
fps = pygame.time.Clock()

# Default snake position and body
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True

# Set default direction
direction = 'RIGHT'
change_to = direction

# Initial score
score = 0

# Function to display score
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect(topleft=(10, 10))
    game_window.blit(score_surface, score_rect)

# Game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(f'Your Score is : {score}', True, red)
    game_over_rect = game_over_surface.get_rect(midtop=(window_x / 2, window_y / 4))
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # Update direction
    direction = change_to

    # Update snake position
    if direction == 'UP':
        snake_position[1] -= 10
    elif direction == 'DOWN':
        snake_position[1] += 10
    elif direction == 'LEFT':
        snake_position[0] -= 10
    elif direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))

    # Fruit consumption check
    if snake_position == fruit_position:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        while True:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]
            if fruit_position not in snake_body:
                break
    fruit_spawn = True

    # Refresh game window
    game_window.fill(black)

    # Draw snake and fruit
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Check for game over conditions
    if (snake_position[0] < 0 or snake_position[0] >= window_x or
        snake_position[1] < 0 or snake_position[1] >= window_y):
        game_over()

    # Check for self-collision
    if snake_position in snake_body[1:]:
        game_over()

    # Display score
    show_score(white, 'times new roman', 20)

    # Refresh display
    pygame.display.update()

    # Frame rate control
    fps.tick(15)
