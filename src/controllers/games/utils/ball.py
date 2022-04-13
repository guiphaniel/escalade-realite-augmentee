import math
import threading

import pygame.image

from src.view.items.drawable import Drawable


class Ball(Drawable):
    def __init__(self):
        Drawable.__init__(self)
        self.area = self.win.get_rect()
        self.radius = 25
        self.rect = pygame.rect.Rect(self.area.w / 2 - self.radius, self.area.h / 2 - self.radius, self.radius * 2, self.radius * 2)
        self.image= pygame.transform.scale(pygame.image.load("src/view/images/sprites/ball.png"), (self.rect.w, self.rect.h))

        self.vector = []
        self.velocity = None
        self.intangible = False
        self.spawn()

    def collideBorder(self):
        if self.rect.y <= 0:
            self.vector[1] = abs(self.vector[1])

        elif self.rect.y + self.rect.height >= self.area.height:
            self.vector[1] = abs(self.vector[1]) * -1

    def collidePlayer(self, point,radius):
        if (radius+(self.rect.width / 2)) < math.sqrt((point[0]-self.rect.centerx)**2 + (point[1]-self.rect.centery)**2)  or self.intangible:
            return
        if self.rect.centerx > self.area.width / 2:  # joueur gauche touche la balle
            self.vector = [abs(self.rect.centerx - point[0]) * -1, self.rect.centery - point[1]]
        elif self.rect.centerx < self.area.width / 2:
            self.vector = [abs(self.rect.centerx - point[0]), self.rect.centery - point[1]]
        else:
            self.vector = [self.rect.centerx - point[0], self.rect.centery - point[1]]

        th = threading.Thread(target=self.startTimerIntangible)
        th.start()

    def spawn(self):
        self.velocity = 0.25
        self.vector = [0, 0]
        self.rect.x = self.area.width / 2 - self.rect.width / 2
        self.rect.y = self.area.height / 2 - self.rect.height / 2

    def update(self,frames):
        if self.vector[0] == 0 and self.vector[1] == 0:
            return
        angle = math.acos(self.vector[0] / (math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2)))

        if self.vector[0] < 0:
            self.rect.x += math.floor(math.cos(angle) * self.velocity * frames)
        else:
            self.rect.x += math.ceil(math.cos(angle) * self.velocity * frames)
        if self.vector[1] < 0:
            self.rect.y += math.floor(math.sin(angle) * self.velocity * -1 * frames)
        else:
            self.rect.y += math.ceil(math.sin(angle) * self.velocity * frames)

    def draw(self):
        self.win.blit(self.image, self.rect)

    def startTimerIntangible(self):
        self.intangible = True
        time = pygame.time.get_ticks()
        while pygame.time.get_ticks() < time + 500:
            continue
        self.intangible = False

    def goalLeft(self):
        return self.rect.x <= 0

    def goalRight(self):
        return self.rect.x + self.rect.width >= self.area.width
