
import math
from config import *
from area import *



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
    def __init__(self, image_background = BACKGROUND_IMAGE_PATH, class_next_scene = None):
        super().__init__()
        self.image_background = pygame.transform.smoothscale(pygame.image.load(image_background).convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))
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
                if self.button_go_to_combat.collidepoint(x, y):
                    if self.class_next_scene:
                        self.next_scene = SceneCombat(self.class_next_scene())

    def render(self, screen):
        if self.image_background:
            screen.blit(self.image_background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (0, 255, 0), self.button_go_back)
        pygame.draw.rect(screen, (0, 255, 0), self.button_go_to_combat)

class SceneVictory(SceneBase):
    def __init__(self, loot_collected):
        super().__init__()

        self.font = pygame.font.SysFont(None, 30)
        self.loot_collected = loot_collected

        self.timer = 3.0

    def update(self, dt):
        self.timer -= dt
        if self.timer < 0:
            self.next_scene = SceneMain()

    def render(self, screen):
        screen.fill((0, 0, 0))
        text_surface = self.font.render("YOU WIN", True, (255, 255, 255))
        screen.blit(text_surface, ((WINDOW_WIDTH/2) - (text_surface.get_width()/2), (WINDOW_HEIGHT/2) - (text_surface.get_height()/2)))

class SceneLost(SceneBase):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.SysFont(None, 30)
        self.timer = 3

    def update(self, dt):
        self.timer -= dt
        if self.timer < 0:
            self.next_scene = SceneMenu()

    def render(self, screen):
        screen.fill((0, 0, 0))
        text_surface = self.font.render("YOU LOST", True, (255, 255, 255))
        screen.blit(text_surface, ((WINDOW_WIDTH/2) - (text_surface.get_width()/2), (WINDOW_HEIGHT/2) - (text_surface.get_height()/2)))

class SceneCombat(SceneBase):
    def __init__(self, area):
        super().__init__()

        self.loot_collected = []

        self.counter = 0.0
        self.time = BUFFER_TIME
        self.is_done_buffer = False
        self.time_per_prompt = area.time_per_prompt
        self.damage_wrong_letter = area.damage_wrong_letter

        self.player_hp = 100
        self.player_stamina = 100
        self.player_is_submitted = False

        self.is_contemplating = False
        self.contemplation_timer = 0.0

        self.is_damage_flash = False
        self.damage_flash_timer = 0.0

        self.font = pygame.font.SysFont(None, 25)
        self.font_large = pygame.font.SysFont(None, 150)
        self.user_text = ""
        self.input_box = pygame.rect.Rect(BUTTON_INPUT_BOX_X, BUTTON_INPUT_BOX_Y, BUTTON_INPUT_BOX_WIDTH, BUTTON_INPUT_BOX_HEIGHT)

        self.area = area

        self.enemy_text_box = pygame.rect.Rect(BUTTON_ENEMY_TEXT_BOX_X, BUTTON_ENEMY_TEXT_BOX_Y, BUTTON_ENEMY_TEXT_BOX_WIDTH, BUTTON_ENEMY_TEXT_BOX_HEIGHT)
        self.enemy = self.area.current_enemy

    def isStringEqual(self):
        return self.user_text == self.enemy.current_prompt

    def update(self, dt):
        if not self.is_done_buffer:
            self.update_buffer(dt)
        else:
            if self.player_is_submitted:
                self.handle_submission()
            self.update_timer(dt)

    def update_buffer(self, dt):
        self.time -= dt
        if self.time <= 0:
            self.is_done_buffer = True
            self.time = self.time_per_prompt

    def take_damage(self, amount):
        self.player_hp -= amount
        self.is_damage_flash = True
        self.damage_flash_timer = DAMAGE_FLASH_DURATION
        if self.player_hp <= 0:
            self.next_scene = SceneLost()
        self.time = self.time_per_prompt

    def handle_submission(self):
        if self.isStringEqual():
            self.handle_correct_answer()
        self.take_damage(self.damage_wrong_letter)
        self.user_text = ""
        self.player_is_submitted = False

    def handle_correct_answer(self):
        self.enemy.health -= 30
        self.time = self.time_per_prompt
        if self.enemy.health <= 0:
            self.handle_enemy_death()
        else:
            self.enemy.set_new_prompt()

    def handle_enemy_death(self):
        self.loot_collected.append(self.enemy.get_loot())
        del self.area.enemies_list[0]
        if len(self.area.enemies_list) > 0:
            self.enemy = self.area.enemies_list[0]
            self.enemy.set_new_prompt()
            self.time = self.time_per_prompt
        else:
            self.next_scene = SceneVictory(self.loot_collected)

    def update_timer(self, dt):
        if self.is_damage_flash:
            self.damage_flash_timer -= dt
            if self.damage_flash_timer <= 0:
                self.is_damage_flash = False

        if self.is_contemplating:
            self.contemplation_timer -= dt
            if self.contemplation_timer <= 0:
                self.is_contemplating = False
            return
        self.time -= dt
        if self.time <= 0:
            self.time = self.time_per_prompt
            self.user_text = ""
            self.take_damage(30)

    def draw_enemy_health_bar(self, screen):
        ratio = max(0.0, self.enemy.health / self.enemy.max_health)
        r = min(255, int((1 - ratio) * 2 * 255))
        g = min(255, int(ratio * 2 * 255))

        bg_rect = pygame.Rect(ENEMY_HP_BAR_X, ENEMY_HP_BAR_Y, ENEMY_HP_BAR_W, ENEMY_HP_BAR_H)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)

        fill_h = int(ENEMY_HP_BAR_H * ratio)
        fill_rect = pygame.Rect(ENEMY_HP_BAR_X, ENEMY_HP_BAR_Y + ENEMY_HP_BAR_H - fill_h, ENEMY_HP_BAR_W, fill_h)
        pygame.draw.rect(screen, (r, g, 0), fill_rect)

        name_surface = self.font.render(self.enemy.name, True, (255, 255, 255))
        screen.blit(name_surface, (ENEMY_HP_BAR_X + ENEMY_HP_BAR_W // 2 - name_surface.get_width() // 2, ENEMY_HP_BAR_Y - 20))

    def draw_player_health_bar(self, screen):
        ratio = max(0.0, self.player_hp / 100)
        r = min(255, int((1 - ratio) * 2 * 255))
        g = min(255, int(ratio * 2 * 255))

        bg_rect = pygame.Rect(PLAYER_HP_BAR_X, PLAYER_HP_BAR_Y, PLAYER_HP_BAR_W, PLAYER_HP_BAR_H)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)

        fill_h = int(PLAYER_HP_BAR_H * ratio)
        fill_rect = pygame.Rect(PLAYER_HP_BAR_X, PLAYER_HP_BAR_Y + PLAYER_HP_BAR_H - fill_h, PLAYER_HP_BAR_W, fill_h)
        pygame.draw.rect(screen, (r, g, 0), fill_rect)

        label_surface = self.font.render("HP", True, (255, 255, 255))
        screen.blit(label_surface, (PLAYER_HP_BAR_X + PLAYER_HP_BAR_W // 2 - label_surface.get_width() // 2, PLAYER_HP_BAR_Y - 20))

    def draw_player_stamina_bar(self, screen):
        ratio = max(0.0, self.player_stamina / 100)

        bg_rect = pygame.Rect(PLAYER_STAMINA_BAR_X, PLAYER_STAMINA_BAR_Y, PLAYER_STAMINA_BAR_W, PLAYER_STAMINA_BAR_H)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)

        fill_h = int(PLAYER_STAMINA_BAR_H * ratio)
        fill_rect = pygame.Rect(PLAYER_STAMINA_BAR_X, PLAYER_STAMINA_BAR_Y + PLAYER_STAMINA_BAR_H - fill_h, PLAYER_STAMINA_BAR_W, fill_h)
        pygame.draw.rect(screen, (255, 215, 0), fill_rect)

        label_surface = self.font.render("SP", True, (255, 255, 255))
        screen.blit(label_surface, (PLAYER_STAMINA_BAR_X + PLAYER_STAMINA_BAR_W // 2 - label_surface.get_width() // 2, PLAYER_STAMINA_BAR_Y - 20))

    def draw_buffer_countdown(self, screen):
        number = math.ceil(self.time)
        countdown_surface = self.font_large.render(str(number), True, (255, 255, 255))
        x = WINDOW_WIDTH // 2 - countdown_surface.get_width() // 2
        y = WINDOW_HEIGHT // 2 - countdown_surface.get_height() // 2
        screen.blit(countdown_surface, (x, y))

    def draw_timer_bar(self, screen):
        ratio = max(0.0, self.time / self.time_per_prompt)
        r = min(255, int((1 - ratio) * 2 * 255))
        g = min(255, int(ratio * 2 * 255))

        bg_rect = pygame.Rect(TIMER_BAR_X, TIMER_BAR_Y, TIMER_BAR_W, TIMER_BAR_H)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)

        fill_rect = pygame.Rect(TIMER_BAR_X, TIMER_BAR_Y, int(TIMER_BAR_W * ratio), TIMER_BAR_H)
        color = (0, 150, 255) if self.is_contemplating else (r, g, 0)
        pygame.draw.rect(screen, color, fill_rect)

    def draw_skill_slots(self, screen):
        slot_width = TIMER_BAR_W // SKILL_SLOT_COUNT
        for i in range(SKILL_SLOT_COUNT):
            square_x = TIMER_BAR_X + i * slot_width + (slot_width - SKILL_SLOT_SIZE) // 2
            rect = pygame.Rect(square_x, SKILL_SLOT_Y, SKILL_SLOT_SIZE, SKILL_SLOT_SIZE)
            pygame.draw.rect(screen, (60, 60, 60), rect)
            pygame.draw.rect(screen, (140, 140, 140), rect, 2)

            label = self.font.render(str(i + 1), True, (180, 180, 180))
            screen.blit(label, (square_x + SKILL_SLOT_SIZE // 2 - label.get_width() // 2,
                                SKILL_SLOT_Y + SKILL_SLOT_SIZE // 2 - label.get_height() // 2))

    def handle_skill_input(self, key):
        match key:
            case pygame.K_1:
                self.activate_contemplation()

    def activate_contemplation(self):
        if not self.is_contemplating and self.player_stamina >= SKILL_CONTEMPLATION_COST:
            self.is_contemplating = True
            self.contemplation_timer = SKILL_CONTEMPLATION_DURATION
            self.player_stamina -= SKILL_CONTEMPLATION_COST

    def process_input(self, events):
        super().process_input(events)

        for event in events:
            if event.type == pygame.KEYDOWN and self.is_done_buffer:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    self.handle_skill_input(event.key)
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.player_is_submitted = True
                elif event.unicode:
                    expected_len = len(self.user_text)
                    if expected_len < len(self.enemy.current_prompt) and event.unicode == self.enemy.current_prompt[expected_len]:
                        self.user_text += event.unicode
                    else:
                        self.user_text = ""
                        self.take_damage(self.damage_wrong_letter)

    def render(self, screen):
        if not self.is_done_buffer:
            screen.fill((0, 125, 125))
        else:
            screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (0, 255, 0 ), self.input_box, 2)
        pygame.draw.rect(screen, (0, 255, 0), self.enemy_text_box, 2)

        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 10))

        enemy_text_surface = self.font.render(self.enemy.current_prompt, True, (255, 255, 255))
        screen.blit(enemy_text_surface, (self.enemy_text_box.x + 5, self.enemy_text_box.y + 10))

        self.draw_enemy_health_bar(screen)

        enemy_left_text = self.font.render(f"Enemies left: {len(self.area.enemies_list)}", True, (255, 255, 255))
        screen.blit(enemy_left_text, (1000, 100))

        self.draw_player_health_bar(screen)
        self.draw_player_stamina_bar(screen)

        self.draw_skill_slots(screen)

        if self.is_done_buffer:
            self.draw_timer_bar(screen)
        else:
            self.draw_buffer_countdown(screen)

        if self.is_damage_flash:
            flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 0, 0, 60))
            screen.blit(flash_surface, (0, 0))

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

        self.button_old_chapel = pygame.rect.Rect(BUTTON_OLD_CHAPEL_X, BUTTON_OLD_CHAPEL_Y, BUTTON_OLD_CHAPEL_WIDTH, BUTTON_OLD_CHAPEL_HEIGHT)
        self.image_old_chapel = pygame.transform.smoothscale(pygame.image.load(OLD_CHAPEL_IMAGE_PATH).convert_alpha(), (BUTTON_OLD_CHAPEL_WIDTH, BUTTON_OLD_CHAPEL_HEIGHT))

        self.image_background = pygame.transform.smoothscale(pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.font = pygame.font.SysFont(None, 22)

    def draw_area_label(self, screen, button, name):
        label = self.font.render(name, True, (0, 255, 255))
        x = button.x + button.width // 2 - label.get_width() // 2
        y = button.y + button.height + 5
        screen.blit(label, (x, y))

    def process_input(self, events):
        super().process_input(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.button_house.collidepoint(x, y):
                    self.next_scene = SceneArea(class_next_scene=AreaHouse)
                if self.button_murkey_water.collidepoint(x, y):
                    self.next_scene = SceneArea(class_next_scene=AreaMurkeyWater)
                if self.button_boat_house.collidepoint(x, y):
                    self.next_scene = SceneArea(class_next_scene=AreaBoatHouse)
                if self.button_chapel.collidepoint(x, y):
                    self.next_scene = SceneArea(class_next_scene=AreaChapel)
                if self.button_lighthouse.collidepoint(x, y):
                    self.next_scene = SceneArea(class_next_scene=AreaLighthouse)
                if self.button_old_chapel.collidepoint(x, y):
                    self.next_scene = SceneArea(class_next_scene=AreaOldChapel)

    def render(self, screen):
        screen.fill((0, 0, 0))

        screen.blit(self.image_background, (0,0))

        screen.blit(self.image_boat_house, self.button_boat_house.topleft)
        screen.blit(self.image_murkey_water, self.button_murkey_water.topleft)
        screen.blit(self.image_lighthouse, self.button_lighthouse.topleft)
        screen.blit(self.image_house, self.button_house.topleft)
        screen.blit(self.image_chapel, self.button_chapel.topleft)
        screen.blit(self.image_old_chapel, self.button_old_chapel.topleft)

        pygame.draw.rect(screen, (0, 255, 0), self.button_house, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_murkey_water, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_boat_house, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_chapel, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_lighthouse, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.button_old_chapel, 1)

        self.draw_area_label(screen, self.button_house, "House")
        self.draw_area_label(screen, self.button_murkey_water, "Murkey Water")
        self.draw_area_label(screen, self.button_boat_house, "Boat House")
        self.draw_area_label(screen, self.button_chapel, "Chapel")
        self.draw_area_label(screen, self.button_lighthouse, "Lighthouse")
        self.draw_area_label(screen, self.button_old_chapel, "Old Chapel")

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