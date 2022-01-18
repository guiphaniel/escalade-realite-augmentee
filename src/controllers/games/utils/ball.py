import math
import random

import pygame.image


class Ball(pygame.sprite.Sprite):
    """Une balle qui se déplace sur lécran
    Retourne: objet ball
    Fonctions: update, calcnewpos
    Attributs: area, vector"""

    def __init__(self,manager, x,y , vector):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = pygame.transform.scale(pygame.image.load("controllers/games/sprites/target.png"),(50,50))
        self.area = manager.screen.get_rect()
        self.vector = vector
        self.hit = 0

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if tr and tl or (br and bl):
                angle = -angle
            if tl and bl:
                # self.offcourt()
                angle = math.pi - angle
            if tr and br:
                angle = math.pi - angle
                # self.offcourt()
        else:
            # Réduire les rectangles pour ne pas frapper la balle derrière les raquettes
            player1.rect.inflate(-3, -3)
            player2.rect.inflate(-3, -3)
            # Est-ce que la raquette et la balle entre en collision ?
            # Notez que je mets dans une règle à part qui définit self.hit à 1 quand ils entrent en collision
            # et à 0 à la prochaine itération. C'est pour stopper un comportement étrange de la balle
            # lorsqu'il trouve une collision *à l'intérieur* de la raquette, la balle s'inverse, et est
            # toujours à l'intérieur de la raquette et donc rebondit à l'intérieur.
            # De cette façon, la balle peut toujours s'échapper et rebondir correctement
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit
        self.vector = (angle, z)

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)

