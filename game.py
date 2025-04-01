## python Program to create a basic game using pygame.
import pygame
import random
import os
pygame.init()
pygame.mixer.init() 
WIDTH, HEIGHT = 800, 400  
BALL_SIZE = 30
SPIKE_SIZE = 45
STAR_SIZE = 25
METEOR_SIZE = 40 
GRAVITY = 0.8
JUMP_STRENGTH = -17
OBSTACLE_SPEED = 3  
LIVES = 3
FPS = 60  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BOUNCE BUDDY")
def load_image(path, size):
    if os.path.exists(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    else:
        print(f"Warning: Missing asset {path}")
        return pygame.Surface(size) 
background_img = load_image("assets/bg.jpg", (WIDTH * 2, HEIGHT)) 
ball_img = load_image("assets/ball.png", (BALL_SIZE, BALL_SIZE))
spike_img = load_image("assets/spike.png", (SPIKE_SIZE, SPIKE_SIZE))
star_img = load_image("assets/star.png", (STAR_SIZE, STAR_SIZE))
meteor_img = load_image("assets/meteor.png", (METEOR_SIZE, METEOR_SIZE))
heart_img = load_image("assets/heart.png", (30, 30)) 
# Fonts
title_font = pygame.font.Font("assets/font.ttf", 40)
score_font = pygame.font.Font("assets/font.ttf", 15)
game_over_font = pygame.font.Font("assets/font.ttf", 35)
button_font = pygame.font.Font("assets/font.ttf", 26)
# Load Sounds
bg_music = "assets/bg.mp3"
jump_sound = pygame.mixer.Sound("assets/jump.mpeg")
hit_sound = pygame.mixer.Sound("assets/hit.mp3")
score_sound = pygame.mixer.Sound("assets/score.mp3")
# Adjust Volume Levels
pygame.mixer.music.load(bg_music)
pygame.mixer.music.set_volume(0.1)  
pygame.mixer.music.play(-1) 
jump_sound.set_volume(0.4) 
hit_sound.set_volume(0.4)   
score_sound.set_volume(0.3) 
# Ball Properties
ball_x = WIDTH // 4
ball_y = HEIGHT - BALL_SIZE
ball_vel_y = 0
on_ground = True
bg_x = 0
bg_speed = 2
spikes = []
stars = []
score = 0
high_score = 0
lives = LIVES
def save_high_score():
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))
def load_high_score():
    global high_score
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())
    else:
        high_score = 0
load_high_score()
def generate_obstacle():
    spike_x = WIDTH
    spike_y = HEIGHT - SPIKE_SIZE
    spikes.append(pygame.Rect(spike_x, spike_y, SPIKE_SIZE, SPIKE_SIZE))

    # 30% chance to spawn a second spike
    if random.random() < 0.3:
        spikes.append(pygame.Rect(spike_x + SPIKE_SIZE + 10, spike_y, SPIKE_SIZE, SPIKE_SIZE))

    star_x = WIDTH + random.randint(100, 300)
    star_y = HEIGHT - STAR_SIZE - 60
    stars.append(pygame.Rect(star_x, star_y, STAR_SIZE, STAR_SIZE))

def generate_falling_meteor():
    meteor_x = random.randint(100, WIDTH - 100)
    meteor_y = -METEOR_SIZE
    meteors.append(pygame.Rect(meteor_x, meteor_y, METEOR_SIZE, METEOR_SIZE))

generate_obstacle()

def reset_game():
    global lives, score, spikes, stars, ball_y, ball_vel_y, bg_x
    lives = LIVES
    score = 0
    spikes.clear()
    stars.clear()
    ball_y = HEIGHT - BALL_SIZE
    ball_vel_y = 0
    bg_x = 0
    generate_obstacle()
    pygame.mixer.music.play(-1)  
running = True
clock = pygame.time.Clock()
game_over = False
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0
    screen.blit(background_img, (bg_x, 0))
    screen.blit(background_img, (bg_x + WIDTH, 0))
 # Display Game Name
    title_text = title_font.render("Bounce Buddy", True, BLACK)
    screen.blit(title_text, (WIDTH // 3, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_RETURN:
                game_over = False
                reset_game()
            elif event.key == pygame.K_SPACE and on_ground:
                ball_vel_y = JUMP_STRENGTH
                on_ground = False
                jump_sound.play()
    if not game_over:
        ball_vel_y += GRAVITY
        ball_y += ball_vel_y
        
        if ball_y >= HEIGHT - BALL_SIZE:
            ball_y = HEIGHT - BALL_SIZE
            ball_vel_y = 0
            on_ground = True
        for spike in spikes:
            spike.x -= OBSTACLE_SPEED
        for star in stars:
            star.x -= OBSTACLE_SPEED
        spikes = [spike for spike in spikes if spike.x > -SPIKE_SIZE]
        stars = [star for star in stars if star.x > -STAR_SIZE]
        if not spikes or spikes[-1].x < WIDTH - random.randint(400, 800):
            generate_obstacle()
        for spike in spikes:
            if pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE).colliderect(spike):
                lives -= 1
                hit_sound.play()
                if lives == 0:
                    if score > high_score:
                        high_score = score
                        save_high_score()
                    game_over = True
                    pygame.mixer.music.stop()
                ball_y = HEIGHT - BALL_SIZE
                ball_vel_y = 0
                spikes.clear()
                stars.clear()
                generate_obstacle()
        new_stars = []
        for star in stars:
            if pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE).colliderect(star):
                score += 1
                score_sound.play()
            else:
                new_stars.append(star)
        stars = new_stars
    screen.blit(ball_img, (ball_x, ball_y))
    for spike in spikes:
        screen.blit(spike_img, (spike.x, spike.y))
    for star in stars:
        screen.blit(star_img, (star.x, star.y))
    score_text = score_font.render(f"Score: {score}", True, BLACK)
    high_score_text = score_font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 40))
    screen.blit(high_score_text, (10, 70))
    for i in range(lives):
        screen.blit(heart_img, (WIDTH - (i + 1) * 35, 10))
    if game_over:
        game_over_text = game_over_font.render("Game Over!", True, BLACK)
        restart_text = button_font.render("Press Enter to Restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 3 + 10, HEIGHT // 2 + 10))
    pygame.display.flip()
pygame.quit()