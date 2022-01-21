import pygame.event

from src.model.database import Database


class PathManager:

    def __init__(self,manager):
        self.manager=manager
        self.database = Database()
        self.walls = self.database.getWalls()

    def startMenuWalls(self):
        running = True

        

        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    self.manager.running = False
