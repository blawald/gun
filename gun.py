import math
from random import choice
from random import randint as rnd

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.g = 0.4
        self.live = 90

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        if self.x + self.vx < self.r:
            self.x = abs(self.x + self.vx) + self.r
            self.vx *= -1
        elif self.x + self.vx > WIDTH - self.r:
            self.x =  WIDTH - abs(WIDTH - (self.x + self.vx)) - self.r
            self.vx *= -1
        elif self.y - self.vy < self.r:
            self.y =  abs(self.y - self.vy) + self.r
            self.vy *= -1
        elif self.y - self.vy > HEIGHT - self.r:
            self.y =  HEIGHT - abs(HEIGHT - (self.y - self.vy)) - self.r
            self.vy *= -1
        else:
            self.x += self.vx
            self.y -= self.vy
        self.vy-=self.g
        self.live -= 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        distase_2 = (self.x-obj.x)*(self.x-obj.x) + (self.y-obj.y)*(self.y-obj.y)
        return distase_2<=(self.r+obj.r)*(self.r+obj.r)


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 0.1
        self.f2_on = 0
        self.color = (0, 0, 0)
        self.x = 50
        self.y = HEIGHT - 50
        self.teta = 0
        self.color_status = 0
        self.grow = 0.02
        self.a = 50
        self.b = 25

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.f2_on = 0
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x + self.a/2 * math.cos(self.teta), self.y + self.a/2 * math.sin(self.teta))
        new_ball.vx = self.f2_power * math.cos(self.teta)*30
        new_ball.vy = - self.f2_power * math.sin(self.teta)*30
        balls.append(new_ball)
        self.f2_power = 0.1

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0]-self.x) != 0:
                if event.pos[0]-self.x>=0:
                    self.teta = math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
                else:
                    self.teta = math.pi + math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
            else:
                self.teta = math.pi/2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def update_color(self):
        return (int(255*self.f2_power), 0, 0)

    def draw(self):
        a = self.a
        b = self.b
        alpha = math.atan(b/a)
        d = 1/2.0 * math.sqrt(a*a + b*b)
        A = [round(self.x + d * math.cos(self.teta+alpha)), round(self.y + d * math.sin(self.teta+alpha))]
        B = [round(self.x + d * math.cos(self.teta-alpha)), round(self.y + d * math.sin(self.teta-alpha))]
        C = [round(self.x - d * math.cos(self.teta+alpha)), round(self.y - d * math.sin(self.teta+alpha))]
        D = [round(self.x - d * math.cos(self.teta-alpha)), round(self.y - d * math.sin(self.teta-alpha))]
        pygame.draw.polygon(self.screen, self.color, 
                   [A, B, 
                     C, D])


    def power_up(self):
        if self.f2_on:
            if self.f2_power + self.grow<=1:
                self.f2_power += self.grow
            else: 
                self.f2_power = 1
            self.color = self.update_color()
        else:
            self.color = (0,0,0)


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color = RED
        self.live = 1

    def __init__(self, screen):
        self.points = 0
        self.live = 0
        self.screen = screen
        self.x=0
        self.y=0
        self.r=0
        self.color = (0, 0, 0)
        self.new_target()

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        if b.live<=0:
            balls.remove(b)
        else:
            b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
