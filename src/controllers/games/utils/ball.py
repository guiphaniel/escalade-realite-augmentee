import math
import threading

import pygame.image


class Ball(pygame.sprite.Sprite):
    def __init__(self, manager):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.image = pygame.transform.scale(pygame.image.load("controllers/games/sprites/ball.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.area = manager.screen.get_rect()
        self.vector = []
        self.velocity = None
        self.intangible = False
        self.spawn()

    def collideBorder(self):
        if self.rect.y <= 0:
            self.vector[1] = abs(self.vector[1])

        elif self.rect.y + self.rect.height >= self.area.height:
            self.vector[1] = abs(self.vector[1]) * -1

    def collideGoal(self):
        if self.rect.x <= 0:
            self.vector[0] = abs(self.vector[0])

        elif self.rect.x + self.rect.width >= self.area.width:
            self.vector[0] = abs(self.vector[0]) * -1
        # if self.rect.x<=0 or self.rect.x>=self.area.width:
        # self.spawn()

    def collidePlayer(self, polygon):
        if not polygon.colliderect(self.rect) or self.intangible:
            return
        if self.rect.centerx > self.area.width / 2:  # joueur gauche touche la balle
            self.vector = [abs(self.rect.centerx - polygon.centerx) * -1, self.rect.centery - polygon.centery]
        elif self.rect.centerx < self.area.width / 2:
            self.vector = [abs(self.rect.centerx - polygon.centerx), self.rect.centery - polygon.centery]
        else:
            self.vector = [self.rect.centerx - polygon.centerx, self.rect.centery - polygon.centery]

        th = threading.Thread(target=self.startTimerIntangible)
        th.start()
        self.velocity += 0.0

    def spawn(self):
        self.velocity = 1.0
        self.vector = [0, 0]
        self.rect.x = self.area.width / 2 - self.rect.width / 2
        self.rect.y = self.area.height / 2 - self.rect.height / 2

    def update(self):
        if self.vector[0] == 0 and self.vector[1] == 0:
            return
        angle = math.acos(self.vector[0] / (math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2)))

        if self.vector[0] < 0:
            self.rect.x += math.floor(math.cos(angle) * self.velocity)
        else:
            self.rect.x += math.ceil(math.cos(angle) * self.velocity)
        if self.vector[1] < 0:
            self.rect.y += math.floor(math.sin(angle) * self.velocity * -1)
        else:
            self.rect.y += math.ceil(math.sin(angle) * self.velocity)

    def draw(self):
        self.manager.screen.blit(self.image, self.rect)

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
