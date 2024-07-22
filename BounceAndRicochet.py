import pygame
from random import randrange

pygame.init()

# Game Variables
pressed_btn = "N/A"
font = pygame.font.Font(None, 40)

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))

fps = 60
clock = pygame.time.Clock()

GRAVITY = 0.5
GROUND_SMOOTHNESS = 0.99

mouse_trajectory: list = []


class Ball:
    ball_list: list = []

    def __init__(self, pos, color, radius, retention) -> None:
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.color = color
        self.radius = radius
        self.retention = retention
        self.max_speed = 40
        self.xspeed = 0
        self.yspeed = 0
        self.circle = None
        self.selected = False

        Ball.ball_list.append(self)

    def deploy(self, mouse_pos):
        self.circle = pygame.draw.circle(
            surface=screen,
            color=self.color,
            center=(self.x_pos, self.y_pos),
            radius=self.radius,
        )
        self.yspeed += GRAVITY
        self.y_pos += self.yspeed
        self.x_pos += self.xspeed
        if self.xspeed > self.max_speed:
            self.xspeed = self.max_speed
        if self.yspeed > self.max_speed:
            self.yspeed = self.max_speed

        if not self.selected:
            # Bottom border
            if self.y_pos + self.radius >= HEIGHT:
                self.yspeed *= -self.retention

                self.y_pos = HEIGHT - self.radius

                self.xspeed *= GROUND_SMOOTHNESS

            # Left and Right border
            if self.x_pos - self.radius < 0 or self.x_pos + self.radius > WIDTH:
                self.xspeed *= -self.retention

                self.x_pos = (
                    0 + self.radius
                    if self.x_pos - self.radius < 0
                    else WIDTH - self.radius
                )

            # # Top border
            if self.y_pos - self.radius < 0:
                self.y_pos = 0 + self.radius
                self.yspeed *= -self.retention
        else:
            self.x_pos, self.y_pos = mouse_pos
            self.yspeed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / 10
            self.xspeed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / 10


# Make balls
BALL_COUNT = 100
BALL_MIN_SIZE = 20
BALL_IN_ORDER = False
for i in range(BALL_COUNT + BALL_MIN_SIZE, BALL_MIN_SIZE, -1):
    Ball(
        (randrange(WIDTH), 0),
        (
            randrange(50, 255),
            randrange(50, 255),
            randrange(50, 255),
        ),
        i if BALL_IN_ORDER else randrange(BALL_MIN_SIZE, BALL_COUNT + BALL_MIN_SIZE),
        randrange(65, 95) / 100,
    )

# Game loop
running = True
while running:
    clock.tick(fps)
    screen.fill((255, 255, 255))

    text_surface = font.render(f"MOUSE BUTTON : {pressed_btn}", False, (0, 0, 0))
    text_surface2 = font.render(f"BALL COUNT : {BALL_COUNT}", False, (0, 0, 0))
    screen.blit(text_surface, (5, 5))
    screen.blit(text_surface2, (5, 35))

    mouse_pos = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_pos)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)

    # Event loop
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pressed_btn = "BUTTON_LEFT"
                for ball in Ball.ball_list:
                    if ball.circle.collidepoint(event.pos):
                        ball.selected = True
            if event.button == pygame.BUTTON_RIGHT:
                pressed_btn = "BUTTON_RIGHT"
                for ball in Ball.ball_list:
                    ball.selected = True
            if event.button == pygame.BUTTON_MIDDLE:
                pressed_btn = "BUTTON_MIDDLE"
                for ball in Ball.ball_list:
                    ball.selected = False
                    ball.xspeed = randrange(-50, 50)
                    ball.yspeed = randrange(-50, 50)
        if event.type == pygame.MOUSEBUTTONUP:
            pressed_btn = "N/A"
            for ball in Ball.ball_list:
                ball.selected = False

    for ball in Ball.ball_list:
        ball.deploy(mouse_pos)

    pygame.display.flip()
