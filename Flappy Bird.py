import pygame
import sys
import os
import random

pygame.init()
WIDTH, HEIGHT = (500, 750)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
game_font = pygame.font.SysFont('04b_19.TTF', 50, True, False)
gravity = 0.5
bird_movement = 0
game_active = True
score = 0
high_score = 0
bird_death = 0


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(800, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(800, random_pipe_pos - 300))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 7
    return pipes


def draw_floor():
    WIN.blit(floor_surface, (floor_x_pos, 650))
    WIN.blit(floor_surface, (floor_x_pos + 500, 650))


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 750:
            WIN.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            WIN.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= 100 or bird_rect.bottom >= 650:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 100))
        WIN.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"SCORE: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 270))
        WIN.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score : {int(score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(250, 230))
        WIN.blit(high_score_surface, high_score_rect)


bg_surface = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-day.png")), (WIDTH, HEIGHT))
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png")).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png")).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png")).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 500))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_height = [550, 575, 600, 675, 650, 700]

flap_sound = pygame.mixer.Sound("assets/sfx_wing.wav")
death_sound = pygame.mixer.Sound("assets/sfx_hit.wav")
score_sound = pygame.mixer.Sound("assets/sfx_point.wav")
a_sound = pygame.mixer.Sound("assets/sfx_swooshing.wav")
score_sound_countdown = 50

game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(250, 375))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_b and game_active:
                bird_movement = 0
                bird_movement += 6
                a_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (100, 500)
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    WIN.blit(bg_surface, (0, 0))

    if game_active:

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        WIN.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        WIN.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")
        pipe_list = []

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -50:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(70)

