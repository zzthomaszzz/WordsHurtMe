import pygame

from config import *
import sys



class SceneBase:
    def __init__(self):
        self.next_scene = self
        self.image_background = None

    def process_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_scene = None

    def update(self, dt): pass
    def render(self, screen): pass

class SceneArea(SceneBase):
    def __init__(self, image_background = None, class_next_scene = None):
        super().__init__()
        self.image_background = image_background
        self.class_next_scene = class_next_scene

        self.button_width = 150
        self.button_height = 100

        self.button_go_back = pygame.rect.Rect(0, WINDOW_HEIGHT - self.button_height, self.button_width, self.button_height)
        self.button_go_to_combat = pygame.rect.Rect(WINDOW_WIDTH - self.button_width, WINDOW_HEIGHT - self.button_height, self.button_width, self.button_height)

    def process_input(self, events):
        super().process_input(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.button_go_back.collidepoint(x, y):
                    self.next_scene = SceneMain()

    def render(self, screen):
        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (0, 255, 0), self.button_go_back)
        pygame.draw.rect(screen, (0, 255, 0), self.button_go_to_combat)


class SceneCombat(SceneBase):
    def __init__(self):
        super().__init__()

        self.player_hp = 100
        self.player_stamina = 100

        self.font = pygame.font.SysFont(None, 30)
        self.user_text = ""
        self.input_box = pygame.rect.Rect(BUTTON_INPUT_BOX_X, BUTTON_INPUT_BOX_Y, BUTTON_INPUT_BOX_WIDTH, BUTTON_INPUT_BOX_HEIGHT)

        self.enemy_text = "Hello There"
        self.enemy_text_box = pygame.rect.Rect(BUTTON_ENEMY_TEXT_BOX_X, BUTTON_ENEMY_TEXT_BOX_Y, BUTTON_ENEMY_TEXT_BOX_WIDTH, BUTTON_ENEMY_TEXT_BOX_HEIGHT)

    def generate_new_text(self, enemy):
        pass

    def isStringEqual(self):
        return self.user_text == self.enemy_text

    def process_input(self, events):
        super().process_input(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.isStringEqual():
                        self.enemy_text = "Good job"
                    else:
                        self.player_hp -= 30
                    self.user_text = ""
                else:
                    self.user_text += event.unicode

    def render(self, screen):
        screen.fill((0, 0, 255))
        pygame.draw.rect(screen, (0, 255, 0 ), self.input_box, 2)
        pygame.draw.rect(screen, (0, 255, 0), self.enemy_text_box, 2)

        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 10))

        enemy_text_surface = self.font.render(self.enemy_text, True, (255, 255, 255))
        screen.blit(enemy_text_surface, (self.enemy_text_box.x + 5, self.enemy_text_box.y + 10))

        player_hp_text = self.font.render("Health: " + str(self.player_hp), True, (255, 255, 255))
        screen.blit(player_hp_text, (50, WINDOW_HEIGHT/2))





class SceneMain(SceneBase):
    def __init__(self):
        super().__init__()
        self.button_house = pygame.rect.Rect(BUTTON_HOUSE_X, BUTTON_HOUSE_Y, BUTTON_HOUSE_WIDTH, BUTTON_HOUSE_HEIGHT)
        self.image_house = pygame.transform.smoothscale(pygame.image.load(HOUSE_IMAGE_PATH).convert_alpha(), (BUTTON_HOUSE_WIDTH, BUTTON_HOUSE_HEIGHT))

        self.button_murkey_water = pygame.rect.Rect(BUTTON_MURKEY_WATER_X, BUTTON_MURKEY_WATER_Y, BUTTON_MURKEY_WATER_WIDTH, BUTTON_MURKEY_WATER_HEIGHT)
        self.image_murkey_water = pygame.transform.smoothscale(pygame.image.load(MURKEY_WATER_IMAGE_PATH).convert_alpha(), (BUTTON_MURKEY_WATER_WIDTH, BUTTON_MURKEY_WATER_HEIGHT))

        self.button_boat_house = pygame.rect.Rect(BUTTON_BOAT_HOUSE_X, BUTTON_BOAT_HOUSE_Y, BUTTON_BOAT_HOUSE_WIDTH, BUTTON_BOAT_HOUSE_HEIGHT)
        self.image_boat_house = pygame.transform.smoothscale(pygame.image.load(BOAT_HOUSE_IMAGE_PATH).convert_alpha(), (BUTTON_BOAT_HOUSE_WIDTH, BUTTON_BOAT_HOUSE_HEIGHT))

        self.button_chapel = pygame.rect.Rect(BUTTON_CHAPEL_X, BUTTON_CHAPEL_Y, BUTTON_CHAPEL_WIDTH, BUTTON_CHAPEL_HEIGHT)
        self.image_chapel = pygame.transform.smoothscale(pygame.image.load(CHAPEL_IMAGE_PATH).convert_alpha(), (BUTTON_CHAPEL_WIDTH, BUTTON_CHAPEL_HEIGHT))

        self.button_lighthouse = pygame.rect.Rect(BUTTON_LIGHTHOUSE_X, BUTTON_LIGHTHOUSE_Y, BUTTON_LIGHTHOUSE_WIDTH, BUTTON_LIGHTHOUSE_HEIGHT)
        self.image_lighthouse = pygame.transform.smoothscale(pygame.image.load(LIGHTHOUSE_IMAGE_PATH).convert_alpha(), (BUTTON_LIGHTHOUSE_WIDTH, BUTTON_LIGHTHOUSE_HEIGHT))

        self.image_background = pygame.transform.smoothscale(pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))

    def process_input(self, events):
        super().process_input(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.button_house.collidepoint(x, y):
                    self.next_scene = SceneArea()
                if self.button_murkey_water.collidepoint(x, y):
                    self.next_scene = SceneArea()
                if self.button_boat_house.collidepoint(x, y):
                    self.next_scene = SceneArea()
                if self.button_chapel.collidepoint(x, y):
                    self.next_scene = SceneArea()
                if self.button_lighthouse.collidepoint(x, y):
                    self.next_scene = SceneArea()

    def render(self, screen):
        screen.fill((0, 0, 0))

        screen.blit(self.image_background, (0,0))

        screen.blit(self.image_boat_house, self.button_boat_house.topleft)
        screen.blit(self.image_murkey_water, self.button_murkey_water.topleft)
        screen.blit(self.image_lighthouse, self.button_lighthouse.topleft)
        screen.blit(self.image_house, self.button_house.topleft)
        screen.blit(self.image_chapel, self.button_chapel.topleft)

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