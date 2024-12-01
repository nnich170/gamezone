import pygame
import random
import sqlite3

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 102)

snake_block = 30  
snake_speed = 8

font_style = pygame.font.SysFont("Arial-Bold", 35)
score_font = pygame.font.SysFont("Arial-Bold", 40)
small_font = pygame.font.SysFont("Arial-Bold", 35)
welcome_font = pygame.font.SysFont("Arial-Bold", 50)

background = pygame.image.load('grass22.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))
logo = pygame.image.load('snake.png')
logo = pygame.transform.scale(logo, (100, 100))

def create_db():
    conn = sqlite3.connect('snake_game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores (username TEXT, score INTEGER)''')
    conn.commit()
    conn.close()

def add_score(username, score):
    conn = sqlite3.connect('snake_game.db')
    c = conn.cursor()
    c.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()

def get_high_score():
    conn = sqlite3.connect('snake_game.db')
    c = conn.cursor()
    c.execute("SELECT MAX(score) FROM scores")
    high_score = c.fetchone()[0]
    conn.close()
    return high_score if high_score else 0

def your_score(score):
    value = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(value, [20, 20])

def display_high_score(high_score):
    value = score_font.render("High Score: " + str(high_score), True, YELLOW)
    screen.blit(value, [screen_width - 250, 20])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, DARK_BLUE, [x[0], x[1], snake_block, snake_block])

def message(msg, color, font, y_offset=0):
    mesg = font.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3 + y_offset])

def welcome_screen():
    screen.blit(background, (0, 0))

    logo_x = (screen_width - logo.get_width()) / 2
    logo_y = screen_height / 4 - logo.get_height() / 2
    screen.blit(logo, (logo_x, logo_y))

    message("Welcome to Snake Game!", WHITE, welcome_font)
    message("Use Arrow Keys to Move the Snake", WHITE, small_font, 100)
    message("Press any key to Start", WHITE, small_font, 150)

    pygame.display.update()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False

def gameLoop():
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block

    while not game_over:

        while game_close:
            screen.blit(background, (0, 0))
            message("You Lost! Press Q-Quit or C-Play Again", RED, small_font)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        screen.blit(background, (0, 0))

        burger_image = pygame.image.load('meat.png')
        burger_image = pygame.transform.scale(burger_image, (snake_block, snake_block))

        screen.blit(burger_image, (foodx, foody))

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        high_score = get_high_score()
        display_high_score(high_score)

        pygame.display.update()

        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()

if __name__ == "__main__":
    create_db()
    welcome_screen()
    gameLoop()
