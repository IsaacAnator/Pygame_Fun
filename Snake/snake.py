import pygame
import random
import os

# pygame setup
pygame.init()

food_color = (0,150,150)
snake_color = (255,0,255)
speed = 4
snake_grow_rate = 5
screen = pygame.display.set_mode((800, 400))
font1 = pygame.font.SysFont('Times New Roman', 25)

file_name = 'high_score.txt'

snake_length = 0
clock = pygame.time.Clock()
snake_buffer = 0

#defining game_over text window and text
def game_over():
    global snake_length 
    global font
    global file_name

    highscore = 0

    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(current_dir, file_name), 'r+') as file:
        highscore = int(file.readline())
        if int(highscore) < int(snake_length):
            file.seek(0)
            file.write(str(snake_length))

    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    snake_length = 0
                    game_start()

        y = 50
        score_text = "Final Score: " +  str(snake_length) + ", Highscore: " + str(highscore)
        restart_text = "Press SPACE to restart"
        score_text_surface = font1.render(score_text, True, (255,0,255))
        restart_text_surface = font1.render(restart_text, True, ('red'))
        overlay_surface = pygame.Surface((400,200))
        overlay_surface.fill((90, 90, 90)) 

        overlay_center = (overlay_surface.get_width() // 2) - (score_text_surface.get_width() // 2)
        restart_text_center = (overlay_surface.get_width() // 2) - (restart_text_surface.get_width() // 2)
        screen_center = (screen.get_width() // 2) - (overlay_surface.get_width() // 2)

        overlay_surface.blit(score_text_surface, (overlay_center, y))
        y += score_text_surface.get_height() + 5
        overlay_surface.blit(restart_text_surface, (restart_text_center, y))
        screen.blit(overlay_surface, (screen_center,y))      
        
        pygame.display.flip()

    pygame.quit()

   

def game_start():
    global snake_length 
    global speed
    global snake_color
    global food_color
    global snake_grow_rate
    global snake_buffer

    wait = 0
    
    up = False
    down = False
    left = False
    right = False
    
    size_x,size_y = screen.get_width()/40 , screen.get_height()/20
    snake_speed = size_x
    pos_x = 0
    pos_y = 0
    snake = [(pos_x, pos_y)]
    
    food_location = (random.randint(1,39)*size_x, random.randint(1,19)*size_y)
    
    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
                    left = False
                    up = False
                    down = False
                if event.key == pygame.K_LEFT:
                    right = False
                    left = True
                    up = False
                    down = False
                if event.key == pygame.K_UP:
                    right = False
                    left = False
                    up = True
                    down = False
                if event.key == pygame.K_DOWN:
                    right = False
                    left = False
                    up = False
                    down = True
    
        #set speed of the game
        wait += 1
        if wait == speed:
            wait = 0
    
            #fill the screen with a color to wipe away anything from last frame
            screen.fill("black")
    
            #set direction of snake
            if down:
                pos_y += snake_speed
            elif up:
                pos_y -= snake_speed
            elif left: 
                pos_x -= snake_speed
            elif right:
                pos_x += snake_speed
    
            #check to see if snake has eaten an apple
            snake_location = (pos_x, pos_y)
            if snake_location == food_location:
                snake_length += snake_grow_rate
                snake_buffer += snake_grow_rate
                food_location = (random.randint(1,39)*size_x, random.randint(1,19)*size_y)

            if len(snake) <= snake_length:
                snake.append((0,0))
                snake_buffer -= 1
            
            #check to see if snake has died
            if snake_location[0] < 0 or snake_location[0] - 1 > screen.get_width() or snake_location[1] < 0 or snake_location[1] - 1 > screen.get_height():
                game_over() 
    
            if snake_length > 0:
                for tail in snake:
                    if snake_location == tail:
                        game_over()    

            #update position of snake and tail
            for i in range(snake_length - snake_buffer):
                snake[(snake_length - snake_buffer)-i] = (snake[(snake_length - snake_buffer)-i-1])
            snake[0] = (pos_x, pos_y)
    
    
    
        # RENDER YOUR GAME HERE
        pygame.draw.rect(screen, food_color, (*food_location, size_x, size_y))
    
        for element in snake:
            pygame.draw.rect(screen, snake_color, (element[0]+1,element[1]+1, size_x-2, size_y-2))
    
        # flip() the display to put your work on screen
        pygame.display.flip()
    
        clock.tick(60)  # limits FPS to 60

    pygame.quit()

# main program start
game_start()
