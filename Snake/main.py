import pygame
import random
import os
import sys

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()


def game_start():
    # initialize variables
    text_font = pygame.font.SysFont("Times New Roman", 20)
    snake_speed = 15

    x_pos = 0
    y_pos = 0
    snake_tail = [(x_pos, y_pos)]
    snake_position = (x_pos, y_pos)
    snake_increase = 5
    snake_size = 0
    high_score = 0

    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2

    up = False
    down = False
    left = False
    right = False
    game_over = False
    paused = False
    running = True

    snake_dim = screen.get_width() // 40
    food_position = (
        random.randint(1, 39) * snake_dim,
        random.randint(1, 19) * snake_dim,
    )

    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_DOWN:
                    if up:
                        break
                    up = False
                    down = True
                    left = False
                    right = False
                elif event.key == pygame.K_UP:
                    if down:
                        break
                    up = True
                    down = False
                    left = False
                    right = False
                elif event.key == pygame.K_LEFT:
                    if right:
                        break
                    up = False
                    down = False
                    left = True
                    right = False
                elif event.key == pygame.K_RIGHT:
                    if left:
                        break
                    up = False
                    down = False
                    left = False
                    right = True

        # manage snake movement
        if up:
            y_pos -= snake_dim
        elif down:
            y_pos += snake_dim
        elif left:
            x_pos -= snake_dim
        elif right:
            x_pos += snake_dim

        snake_position = (x_pos, y_pos)
        if snake_position == food_position:
            snake_size += snake_increase
            for _ in range(snake_increase):
                # Append new segments to the tail
                snake_tail.append(snake_tail[-1])
                food_position = (
                    random.randint(1, 39) * snake_dim,
                    random.randint(1, 19) * snake_dim,
                )

        # check if game over
        if snake_size > 1:
            for tail in snake_tail:
                if tail == snake_position:
                    game_over = True

        if (
            x_pos < 0
            or x_pos >= screen.get_width()
            or y_pos < 0
            or y_pos >= screen.get_height()
        ):
            game_over = True

        # draw the snake
        for i in range(len(snake_tail) - 1, 0, -1):
            snake_tail[i] = snake_tail[i - 1]
        snake_tail[0] = snake_position

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # RENDER YOUR GAME HERE
        for element in snake_tail:
            snake_window = pygame.Surface((snake_dim - 1, snake_dim - 1))
            snake_window.fill("red")
            screen.blit(snake_window, element)

        food_window = pygame.Surface((snake_dim, snake_dim))
        food_window.fill("blue")
        screen.blit(food_window, (food_position))

        pygame.display.update()

        # control snake speed
        clock.tick(snake_speed)

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    paused = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

        while game_over:
            # ensure it always opens this file no matter the working directory
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "high_score.txt")
            with open(file_path, "r+") as file:
                high_score = int(file.read())
                if high_score < snake_size:
                    file.seek(0)
                    file.write(str(snake_size))

            # display the game over screen
            game_over_window = pygame.Surface((300, 150), pygame.SRCALPHA)
            game_over_window.fill((150, 150, 150))
            game_over_window_center_x = game_over_window.get_width() // 2
            game_over_window_center_y = game_over_window.get_height() // 2
            game_over_text = (
                "Score: "
                + str(snake_size)
                + "\nHigh Score: "
                + str(high_score)
                + "\n Press SPACE to try again"
            )
            game_over_text = game_over_text.split("\n")
            text_y = 30
            for i in range(len(game_over_text)):
                text_window = text_font.render(game_over_text[i], True, "red")
                text_window_center_x = text_window.get_width() // 2
                text_window_center_y = text_window.get_height() // 2
                game_over_window.blit(
                    text_window,
                    (game_over_window_center_x - text_window_center_x, text_y),
                )
                text_y += text_font.get_height() + 5
            screen.blit(
                game_over_window,
                (
                    screen_center_x - game_over_window_center_x,
                    screen_center_y - game_over_window_center_y,
                ),
            )

            pygame.display.update()

            # event handler for game over screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_start()
    pygame.quit()
    sys.exit()


# function to start the game
game_start()
