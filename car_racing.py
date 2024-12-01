import pygame
import random

pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

try:
    background = pygame.image.load("road.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))
except pygame.error as e:
    print(f"Error loading road.jpg: {e}")
    exit()

try:
    car_image = pygame.image.load("car.png")
    car_image = pygame.transform.scale(car_image, (50, 80))
    car_width = car_image.get_width()
    car_height = car_image.get_height()
except pygame.error as e:
    print(f"Error loading car.png: {e}")
    exit()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)

clock = pygame.time.Clock()

score_font = pygame.font.SysFont("Arial-Bold", 40)

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > screen_width - car_width:
            self.x = screen_width - car_width

    def draw(self):
        screen.blit(car_image, (self.x, self.y))

try:
    obstacle_car_image = pygame.image.load("obstacle_car.png")
    obstacle_car_image = pygame.transform.scale(obstacle_car_image, (50, 80))
except pygame.error as e:
    print(f"Error loading obstacle_car.png: {e}")
    exit()

class Obstacle:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(obstacle_car_image, (self.x, self.y))

def display_score(score):
    value = score_font.render("Score: " + str(score), True, (255, 255, 0))
    screen.blit(value, [10, 10])

try:
    logo_image = pygame.image.load("logocar.png")
    logo_image = pygame.transform.scale(logo_image, (100, 100))
except pygame.error as e:
    print(f"Error loading logocar.png: {e}")
    exit()

def welcome_page():
    screen.fill((254, 216, 1))  
    title_font = pygame.font.SysFont("Arial-Bold", 40)
    instruction_font = pygame.font.SysFont("Arial-Bold", 30)
    
    title_text = title_font.render("Car Racing Game", True, BLACK)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)

    start_text = instruction_font.render("Press any key to Start", True, BLACK)
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(start_text, start_rect)

    screen.blit(logo_image, [screen_width // 2 - 50, screen_height // 2 + 50])
    pygame.display.update()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False

def gameLoop():
    start_ticks = pygame.time.get_ticks()
    time_limit = 60  
    game_over = False
    welcome_page()

    car = Car(screen_width // 2 - car_width // 2, screen_height - car_height - 10)
    obstacles = []
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.move_left()
        if keys[pygame.K_RIGHT]:
            car.move_right()

        if random.randint(1, 50) == 1:
            obstacle_x = random.randint(0, screen_width - car_width)
            new_obstacle = Obstacle(obstacle_x, -car_height, random.randint(5, 10))
            obstacles.append(new_obstacle)

        for obstacle in obstacles:
            obstacle.move()
            if obstacle.y > screen_height:
                obstacles.remove(obstacle)
                score += 1

        for obstacle in obstacles:
            if car.x < obstacle.x + car_width and car.x + car_width > obstacle.x:
                if car.y < obstacle.y + car_height and car.y + car_height > obstacle.y:
                    game_over = True

        screen.blit(background, (0, 0))
        car.draw()
        for obstacle in obstacles:
            obstacle.draw()
        display_score(score)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    gameLoop()
