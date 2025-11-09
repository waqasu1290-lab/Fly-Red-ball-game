import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floppy Bird 🐥")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Game variables
gravity = 0.5
bird_movement = 0
game_active = True
score = 0

# Load bird
bird = pygame.Rect(50, HEIGHT // 2, 30, 30)

# Pipe list
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

# Font
game_font = pygame.font.Font(None, 50)

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [p for p in pipes if p.right > -50]
    return visible_pipes

def check_collision(pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return False
    if bird.top <= -100 or bird.bottom >= HEIGHT:
        return False
    return True

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and not game_active:
                # Reset game
                game_active = True
                pipe_list.clear()
                bird.center = (50, HEIGHT // 2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            random_pipe_pos = random.choice(pipe_height)
            bottom_pipe = pygame.Rect(WIDTH, random_pipe_pos, 50, HEIGHT - random_pipe_pos)
            top_pipe = pygame.Rect(WIDTH, random_pipe_pos - 150 - HEIGHT, 50, HEIGHT)
            pipe_list.extend([bottom_pipe, top_pipe])

    # Background
    screen.fill(BLUE)

    if game_active:
        # Bird
        bird_movement += gravity
        bird.centery += bird_movement
        pygame.draw.ellipse(screen, RED, bird)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Collision
        game_active = check_collision(pipe_list)

        # Score
        score += 0.01
        score_surface = game_font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_surface, (10, 10))

    else:
        game_over_surface = game_font.render("Game Over! Press SPACE", True, WHITE)
        screen.blit(game_over_surface, (20, HEIGHT // 2 - 20))

    pygame.display.update()
    clock.tick(60)
