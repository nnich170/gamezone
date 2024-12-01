import pygame, sys, random, sqlite3

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

def create_db():
    conn = sqlite3.connect('pong_scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            player1_score INTEGER,
            player2_score INTEGER,
            game_time INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def reset_database():
    conn = sqlite3.connect('pong_scores.db')
    c = conn.cursor()
    c.execute('DELETE FROM scores')
    conn.commit()
    conn.close()

def save_score(player1_score, player2_score, game_time):
    conn = sqlite3.connect('pong_scores.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO scores (player1_score, player2_score, game_time)
        VALUES (?, ?, ?)
    ''', (player1_score, player2_score, game_time))
    conn.commit()
    conn.close()

def get_high_score():
    conn = sqlite3.connect('pong_scores.db')
    c = conn.cursor()
    c.execute('SELECT MAX(player1_score), MAX(player2_score) FROM scores')
    high_scores = c.fetchone()
    conn.close()
    return high_scores if high_scores else (0, 0)

logo_path = "logo.png"  
try:
    logo = pygame.image.load(logo_path)
    logo_width = int(screen_width * 0.2)  
    logo_height = int(logo_width * logo.get_height() / logo.get_width())  
    logo = pygame.transform.scale(logo, (logo_width, logo_height))
except pygame.error:
    print("Logo file not found. Please ensure 'logo.png' is in the same directory.")
    logo = None

def get_player_names():
    screen.fill(bg_color)
    font = pygame.font.Font(None, 50)
    input_box = pygame.Rect(screen_width / 2 - 150, screen_height / 2 - 25, 300, 50)
    text = ""
    player_names = ["", ""]
    player_index = 0

    welcome_message = "Welcome to Ping Pong!"
    instructions = "Use UP and DOWN arrows to move."
    message = f"Enter Player {player_index + 1} Name:"

    show_welcome = True
    welcome_display_duration = 3000  
    welcome_start_time = pygame.time.get_ticks()

    while player_index < 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not show_welcome:
                    if text.strip():
                        player_names[player_index] = text.strip()
                        player_index += 1
                        text = ""
                        if player_index < 2:
                            message = f"Enter Player {player_index + 1} Name:"
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif not show_welcome:
                    text += event.unicode

        screen.fill(bg_color)
        
        if logo:
            screen.blit(logo, (screen_width / 2 - logo.get_width() / 2, 50))

        if show_welcome:
            if pygame.time.get_ticks() - welcome_start_time < welcome_display_duration:
                welcome_label = font.render(welcome_message, True, score_color)
                screen.blit(welcome_label, (screen_width / 2 - welcome_label.get_width() / 2, screen_height / 2 - 100))
                instructions_label = font.render(instructions, True, score_color)
                screen.blit(instructions_label, (screen_width / 2 - instructions_label.get_width() / 2, screen_height / 2 + 20))
            else:
                show_welcome = False
        else:
            label = font.render(message, True, score_color)
            pygame.draw.rect(screen, score_color, input_box, 2)
            screen.blit(label, (screen_width / 2 - label.get_width() / 2, screen_height / 2 - 100))
            text_surface = font.render(text, True, score_color)
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        pygame.display.flip()

    return player_names

def ball_animation():
    global ball_speed_x, ball_speed_y, player1_score, player2_score, speed_increased

    elapsed_time = pygame.time.get_ticks() - start_time

    if elapsed_time >= 20000 and not speed_increased:
        ball_speed_x *= 1.5
        ball_speed_y *= 1.5
        speed_increased = True

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        player2_score += 1
        ball_restart()
    if ball.right >= screen_width:
        player1_score += 1
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, speed_increased
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x = 3 * random.choice((1, -1))  
    ball_speed_y = 3 * random.choice((1, -1))  
    speed_increased = False  

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

bg_color = (0, 128, 0)
player_color = (0, 0, 255)
opponent_color = (255, 0, 0)
score_color = (255, 255, 255)
timer_color = (255, 215, 0)

font = pygame.font.Font(None, 50)

create_db()
reset_database()
player_names = get_player_names()

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = 4 * random.choice((1, -1))
player_speed = 0
opponent_speed = 6

player1_score = 0
player2_score = 0
start_time = pygame.time.get_ticks()
game_duration = 60 * 1000
game_active = True
speed_increased = False  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 6
                if event.key == pygame.K_UP:
                    player_speed -= 6

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 6
                if event.key == pygame.K_UP:
                    player_speed += 6

    if game_active:
        ball_animation()
        player_animation()
        opponent_ai()

        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= game_duration:
            game_active = False

        screen.fill(bg_color)
        pygame.draw.rect(screen, player_color, player)
        pygame.draw.rect(screen, opponent_color, opponent)
        pygame.draw.ellipse(screen, score_color, ball)
        pygame.draw.aaline(screen, score_color, (screen_width / 2, 0), (screen_width / 2, screen_height))

        if (game_duration - elapsed_time) <= 10000:
            timer_color = (255, 0, 0)
        else:
            timer_color = (255, 215, 0)

        player1_text = font.render(f"{player_names[0]}: {player1_score}", True, score_color)
        player2_text = font.render(f"{player_names[1]}: {player2_score}", True, score_color)
        timer_text = font.render(f"Time: {max(0, (game_duration - elapsed_time) // 1000)}s", True, timer_color)
        screen.blit(player1_text, (40, 20))
        screen.blit(player2_text, (screen_width - player2_text.get_width() - 40, 20))
        screen.blit(timer_text, (screen_width / 2 - timer_text.get_width() / 2, 20))
    else:
        winner = f"{player_names[0]} Wins!" if player1_score > player2_score else f"{player_names[1]} Wins!" if player2_score > player1_score else "It's a Tie!"
        save_score(player1_score, player2_score, elapsed_time)

        screen.fill(bg_color)
        winner_text = font.render(winner, True, timer_color)
        restart_text = font.render("Press R to Restart", True, score_color)
        screen.blit(winner_text, (screen_width / 2 - winner_text.get_width() / 2, screen_height / 2 - 50))
        screen.blit(restart_text, (screen_width / 2 - restart_text.get_width() / 2, screen_height / 2 + 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player1_score = 0
            player2_score = 0
            start_time = pygame.time.get_ticks()
            game_active = True
            ball_restart()

    high_scores = get_high_score()
    high_score_text = font.render(f"High Score: {player_names[0]}: {high_scores[0]} / {player_names[1]}: {high_scores[1]}", True, score_color)
    screen.blit(high_score_text, (screen_width / 2 - high_score_text.get_width() / 2, screen_height - 50))

    pygame.display.flip()
    clock.tick(60)
