import pygame
from config import *



class SceneBase:
    def __init__(self):
        self.next_scene = self
        self.background = None

    def process_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_scene = None

    def update(self, dt): pass
    def render(self, screen): pass

class SceneArea(SceneBase):
    pass

class SceneCombat(SceneBase):
    pass

class SceneMain(SceneBase):
    def render(self, screen):
        screen.fill((255, 0, 0))

class SceneMenu(SceneBase):
    def __init__(self):
        super().__init__()

        #Start button always in center
        self.button_start_game = pygame.rect.Rect(BUTTON_START_X, BUTTON_START_Y, BUTTON_START_WIDTH, BUTTON_START_HEIGHT)

    def process_input(self, events):
        super().process_input(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.button_start_game.collidepoint(x, y):
                    self.next_scene = SceneMain()

    def render(self, screen):
        screen.fill((0, 0, 255))
        pygame.draw.rect(screen, (0, 255, 0), self.button_start_game)