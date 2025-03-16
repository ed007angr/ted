import pygame
from random import randrange as rnd, choice
import time
WIDTH, HEIGHT = 1200, 700


def choose_difficulty_screen():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 74)
    text_easy = font.render("1 - Легко", True, (255, 255, 255))
    text_medium = font.render("2 - Средне", True, (255, 255, 255))
    text_hard = font.render("3 - Сложно", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(text_easy, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        screen.blit(text_medium, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(text_hard, (WIDTH // 2 - 100, HEIGHT // 2 + 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 60
                if event.key == pygame.K_2:
                    return 90
                if event.key == pygame.K_3:
                    return 120


def game_over_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 100)
    text = font.render("GAME OVER! Press R ", True, (255, 0, 0))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, (WIDTH // 2 - 300, HEIGHT // 2 - 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True


fps = choose_difficulty_screen()

paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(10) for _ in range(4)]

boosters = []
lives = 3

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
img = pygame.image.load('image.png').convert()
speed_boost_active = False
speed_boost_end_time = 0
BOOST_DURATION = 5

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    sc.blit(img, (0, 0))
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    for booster in boosters:
        pygame.draw.circle(sc, pygame.Color('gold'), booster.center, 10)

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    if ball.centery < ball_radius:
        dy = -dy

    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        fps += 2

        if rnd(0, 10) > 1:
            boosters.append(pygame.Rect(hit_rect.centerx, hit_rect.centery, 20, 20))

    for booster in boosters[:]:
        booster.y += 5
        if booster.colliderect(paddle):
            boosters.remove(booster)
            boost_type = choice(['speed', 'paddle', 'life'])
            if boost_type == 'speed':
                speed_boost_active = True
                speed_boost_end_time = time.time() + BOOST_DURATION
                ball_speed -= 2

            elif boost_type == 'paddle':
                paddle.w += 50
            elif boost_type == 'life':
                lives += 1
        elif booster.y > HEIGHT:
            boosters.remove(booster)
    if speed_boost_active and time.time() > speed_boost_end_time:
        speed_boost_active = False
        ball_speed += 2

    if ball.bottom > HEIGHT:
        lives -= 1
        if lives <= 0:
            if game_over_screen():
                lives = 3
                block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
                color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(10) for _ in range(4)]
                ball.x, ball.y = WIDTH // 2, HEIGHT // 2
                dx, dy = 1, -1
        else:
            ball.x, ball.y = WIDTH // 2, HEIGHT // 2
            dx, dy = 1, -1
    elif not len(block_list):
        print('WIN!!!')
        exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    pygame.display.flip()
    clock.tick(fps)
