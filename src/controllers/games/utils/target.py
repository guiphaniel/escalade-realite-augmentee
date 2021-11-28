import math
import random

import pygame.image


class Target(pygame.sprite.Sprite):

    def __init__(self,screen):
        super().__init__()
        self.screen=screen
        self.image=pygame.transform.scale(pygame.image.load("controllers/games/sprites/target.png"),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen.get_rect().width - self.rect.width)
        self.rect.y = random.randint(0, self.screen.get_rect().height - self.rect.height)
        self.center = [self.rect.x + self.rect.width/2.0, self.rect.y + self.rect.height/2.0]
        self.radius = self.rect.height/2.0
        self.ticks = pygame.time.get_ticks()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def collide(self,x,y):
        if math.sqrt((x - self.center[0]) ** 2 + (y - self.center[1]) ** 2)<=self.radius:
            self.image=pygame.transform.scale(pygame.image.load("controllers/games/sprites/success.png"),(50,50))
            return True
        return False

    def failed(self):
        self.image=pygame.transform.scale(pygame.image.load("controllers/games/sprites/fail.png"), (50, 50))