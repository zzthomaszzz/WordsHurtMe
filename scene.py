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
    def __init__(self):
        super().__init__()
        self.button_house = pygame.rect.Rect(BUTTON_HOUSE_X, BUTTON_HOUSE_Y, BUTTON_HOUSE_WIDTH, BUTTON_HOUSE_HEIGHT)

        self.button_murkey_water = pygame.rect.Rect(BUTTON_MURKEY_WATER_X, BUTTON_MURKEY_WATER_Y, BUTTON_MURKEY_WATER_WIDTH, BUTTON_MURKEY_WATER_HEIGHT)
        self.image_murkey_water = pygame.transform.smoothscale(pygame.image.load(MURKEY_WATER_IMAGE_PATH).convert_alpha(), (BUTTON_MURKEY_WATER_WIDTH, BUTTON_MURKEY_WATER_HEIGHT))

        self.button_boat_house = pygame.rect.Rect(BUTTON_BOAT_HOUSE_X, BUTTON_BOAT_HOUSE_Y, BUTTON_BOAT_HOUSE_WIDTH, BUTTON_BOAT_HOUSE_HEIGHT)
        self.image_boat_house = pygame.transform.smoothscale(pygame.image.load(BOAT_HOUSE_IMAGE_PATH).convert_alpha(), (BUTTON_BOAT_HOUSE_WIDTH, BUTTON_BOAT_HOUSE_HEIGHT))

        self.button_chapel = pygame.rect.Rect(BUTTON_CHAPEL_X, BUTTON_CHAPEL_Y, BUTTON_CHAPEL_WIDTH, BUTTON_CHAPEL_HEIGHT)

        self.button_lighthouse = pygame.rect.Rect(BUTTON_LIGHTHOUSE_X, BUTTON_LIGHTHOUSE_Y, BUTTON_LIGHTHOUSE_WIDTH, BUTTON_LIGHTHOUSE_HEIGHT)
        self.image_lighthouse = pygame.transform.smoothscale(pygame.image.load(LIGHTHOUSE_IMAGE_PATH).convert_alpha(), (BUTTON_LIGHTHOUSE_WIDTH, BUTTON_LIGHTHOUSE_HEIGHT))


    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.image_boat_house, self.button_boat_house.topleft)
        screen.blit(self.image_murkey_water, self.button_murkey_water.topleft)
        screen.blit(self.image_lighthouse, self.button_lighthouse.topleft)
        pygame.draw.rect(screen, (0, 255, 0), self.button_house, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_murkey_water, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_boat_house, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_chapel, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_lighthouse, 1)

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