
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

        self.font = pygame.font.SysFont(None, 26)
        self.font_header = pygame.font.SysFont(None, 32)
        self.font_title = pygame.font.SysFont(None, 52)

        self.button_width = 150
        self.button_height = 60

        self.button_go_back = pygame.rect.Rect(0, WINDOW_HEIGHT - self.button_height, self.button_width, self.button_height)
        self.button_go_to_combat = pygame.rect.Rect(WINDOW_WIDTH - self.button_width, WINDOW_HEIGHT - self.button_height, self.button_width, self.button_height)

        # Build preview data from area class so changing the class updates this screen
        self.area_name = ""
        self.area_time = 0
        self.area_dmg = 0
        self.enemy_previews = []  # list of (enemy_name, [(Item, pct), ...])
        if class_next_scene:
            temp = class_next_scene()
            self.area_name = temp.name
            self.area_time = temp.time_per_prompt
            self.area_dmg = temp.damage_wrong_letter
            seen = set()
            for cls in temp.enemies:
                if cls in seen:
                    continue
                seen.add(cls)
                e = cls()
                total_w = sum(e.weights)
                drops = [
                    (item, round(w / total_w * 100))
                    for item, w in zip(e.loots, e.weights)
                    if item is not None
                ]
                self.enemy_previews.append((e.name, drops))

        # Pre-compute panel height to match render exactly:
        # header section ends at y-offset 76, then 28px name + 22px*drops + 10px gap per enemy
        PAD = 10
        self.panel_w = 450
        self.panel_h = 76 + sum(28 + max(1, len(drops)) * 22 + 10 for _, drops in self.enemy_previews) + PAD

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

        # Info panel
        PAD = 10
        panel_x, panel_y = 20, 20

        overlay = pygame.Surface((self.panel_w, self.panel_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (panel_x, panel_y))
        pygame.draw.rect(screen, (0, 255, 0), (panel_x, panel_y, self.panel_w, self.panel_h), 2)

        title_surf = self.font_title.render(self.area_name, True, (255, 255, 255))
        screen.blit(title_surf, (panel_x + PAD, panel_y + PAD))

        stats_surf = self.font.render(
            f"Timer: {self.area_time}s     Typo damage: {self.area_dmg} HP",
            True, (160, 160, 160)
        )
        screen.blit(stats_surf, (panel_x + PAD, panel_y + 48))

        y = panel_y + 76
        for enemy_name, drops in self.enemy_previews:
            name_surf = self.font_header.render(enemy_name, True, (255, 215, 0))
            screen.blit(name_surf, (panel_x + PAD, y))
            y += 28
            if drops:
                for item, pct in drops:
                    if item.stat in ("damage_reduction", "stamina_regen"):
                        val_str = f"+{item.value}% {item.stat.replace('_', ' ')}"
                    else:
                        val_str = f"+{item.value} {item.stat.replace('_', ' ')}"
                    drop_text = f"  • {item.name}  {val_str}  ({pct}%)"
                    drop_surf = self.font.render(drop_text, True, (200, 200, 200))
                    screen.blit(drop_surf, (panel_x + PAD, y))
                    y += 22
            else:
                no_drop = self.font.render("  • No loot", True, (80, 80, 80))
                screen.blit(no_drop, (panel_x + PAD, y))
                y += 22
            y += 10

        # Buttons with labels
        pygame.draw.rect(screen, (0, 255, 0), self.button_go_back)
        back_lbl = self.font.render("Go Back", True, (0, 0, 0))
        screen.blit(back_lbl, (
            self.button_go_back.x + self.button_go_back.width // 2 - back_lbl.get_width() // 2,
            self.button_go_back.y + self.button_go_back.height // 2 - back_lbl.get_height() // 2
        ))

        pygame.draw.rect(screen, (0, 255, 0), self.button_go_to_combat)
        start_lbl = self.font.render("Start", True, (0, 0, 0))
        screen.blit(start_lbl, (
            self.button_go_to_combat.x + self.button_go_to_combat.width // 2 - start_lbl.get_width() // 2,
            self.button_go_to_combat.y + self.button_go_to_combat.height // 2 - start_lbl.get_height() // 2
        ))

class SceneVictory(SceneBase):
    def __init__(self, loot_collected):
        super().__init__()
        self.font = pygame.font.SysFont(None, 30)
        self.font_title = pygame.font.SysFont(None, 60)
        self.loot_collected = loot_collected
        self.button_back = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 80, 200, 50)

    def process_input(self, events):
        super().process_input(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_back.collidepoint(event.pos):
                    self.next_scene = SceneMain()

    def render(self, screen):
        screen.fill((0, 0, 0))
        title = self.font_title.render("YOU WIN", True, (255, 255, 255))
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 60))

        if self.loot_collected:
            header = self.font.render("Loot collected:", True, (255, 215, 0))
            screen.blit(header, (WINDOW_WIDTH // 2 - header.get_width() // 2, 160))
            for i, item in enumerate(self.loot_collected):
                text = self.font.render(
                    f"- {item.name}  (+{item.value} {item.stat.replace('_', ' ')})",
                    True, (200, 200, 200)
                )
                screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 200 + i * 35))
        else:
            nothing = self.font.render("No loot this run.", True, (150, 150, 150))
            screen.blit(nothing, (WINDOW_WIDTH // 2 - nothing.get_width() // 2, 200))

        pygame.draw.rect(screen, (0, 200, 0), self.button_back)
        label = self.font.render("Back to Map", True, (0, 0, 0))
        screen.blit(label, (self.button_back.x + self.button_back.width // 2 - label.get_width() // 2,
                             self.button_back.y + self.button_back.height // 2 - label.get_height() // 2))

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

        equipped = [item for item in player_equipment.values() if item is not None]
        bonus_hp = sum(i.value for i in equipped if i.stat == "health")
        bonus_stamina = sum(i.value for i in equipped if i.stat == "stamina")
        self.damage_reduction = sum(i.value for i in equipped if i.stat == "damage_reduction")

        self.player_hp = PLAYER_BASE_HP + bonus_hp
        self.player_max_hp = self.player_hp
        self.player_stamina = PLAYER_BASE_STAMINA + bonus_stamina
        self.player_max_stamina = self.player_stamina

        total_regen_pct = sum(i.value for i in equipped if i.stat == "stamina_regen")
        self.stamina_regen = PLAYER_BASE_STAMINA_REGEN + (total_regen_pct / 100) * self.player_max_stamina
        self.player_is_submitted = False

        self.is_contemplating = False
        self.contemplation_timer = 0.0

        self.is_delirium = False
        self.delirium_timer = 0.0

        self.is_acceptance = False
        self.acceptance_timer = 0.0

        self.is_damage_flash = False
        self.damage_flash_timer = 0.0

        self.is_paused = False
        self.pause_timer = 0.0

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
        reduced = round(amount * (1 - self.damage_reduction / 100))
        self.player_hp -= reduced
        self.is_damage_flash = True
        self.damage_flash_timer = DAMAGE_FLASH_DURATION
        self.is_paused = True
        self.pause_timer = DAMAGE_PAUSE_DURATION
        if self.player_hp <= 0:
            self.next_scene = SceneLost()
        self.time = self.time_per_prompt

    def handle_submission(self):
        if self.isStringEqual():
            self.handle_correct_answer()
        else:
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
        loot = self.enemy.get_loot()
        if loot:
            self.loot_collected.append(loot)
            player_inventory.append(loot)
        del self.area.enemies_list[0]
        if len(self.area.enemies_list) > 0:
            self.enemy = self.area.enemies_list[0]
            self.time = self.time_per_prompt
        else:
            self.next_scene = SceneVictory(self.loot_collected)

    def update_timer(self, dt):
        if self.is_damage_flash:
            self.damage_flash_timer -= dt
            if self.damage_flash_timer <= 0:
                self.is_damage_flash = False

        if self.is_paused:
            self.pause_timer -= dt
            if self.pause_timer <= 0:
                self.is_paused = False
            return

        self.player_stamina = min(self.player_max_stamina, self.player_stamina + self.stamina_regen * dt)

        if self.is_delirium:
            self.delirium_timer -= dt
            if self.delirium_timer <= 0:
                self.is_delirium = False

        if self.is_acceptance:
            self.acceptance_timer -= dt
            if self.acceptance_timer <= 0:
                self.is_acceptance = False

        if self.is_contemplating:
            self.contemplation_timer -= dt
            if self.contemplation_timer <= 0:
                self.is_contemplating = False
            return
        self.time -= dt
        if self.time <= 0:
            self.time = self.time_per_prompt
            self.user_text = ""
            timer_damage = self.damage_wrong_letter // 2 if self.is_acceptance else self.damage_wrong_letter
            self.take_damage(timer_damage)

    def draw_player_health_bar(self, screen):
        ratio = max(0.0, self.player_hp / self.player_max_hp)
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
        ratio = max(0.0, self.player_stamina / self.player_max_stamina)

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
            border_color = (180, 0, 255) if i == 1 and self.is_delirium else \
                           (255, 165, 0) if i == 4 and self.is_acceptance else \
                           (140, 140, 140)
            pygame.draw.rect(screen, border_color, rect, 2)

            label = self.font.render(str(i + 1), True, (180, 180, 180))
            screen.blit(label, (square_x + SKILL_SLOT_SIZE // 2 - label.get_width() // 2,
                                SKILL_SLOT_Y + SKILL_SLOT_SIZE // 2 - label.get_height() // 2))

    def handle_skill_input(self, key):
        match key:
            case pygame.K_1:
                self.activate_contemplation()
            case pygame.K_2:
                self.activate_delirium()
            case pygame.K_3:
                self.activate_concentration()
            case pygame.K_4:
                self.activate_denial()
            case pygame.K_5:
                self.activate_acceptance()

    def activate_contemplation(self):
        if not self.is_contemplating and self.player_stamina >= SKILL_CONTEMPLATION_COST:
            self.is_contemplating = True
            self.contemplation_timer = SKILL_CONTEMPLATION_DURATION
            self.player_stamina -= SKILL_CONTEMPLATION_COST

    def activate_delirium(self):
        if not self.is_delirium and self.player_stamina >= SKILL_DELIRIUM_COST:
            self.is_delirium = True
            self.delirium_timer = SKILL_DELIRIUM_DURATION
            self.player_stamina -= SKILL_DELIRIUM_COST

    def activate_concentration(self):
        if self.player_stamina >= SKILL_CONCENTRATION_COST:
            self.time = min(self.time + SKILL_CONCENTRATION_TIME_BONUS, self.time_per_prompt)
            self.player_stamina -= SKILL_CONCENTRATION_COST

    def activate_denial(self):
        if not self.enemy.is_boss and self.player_stamina >= SKILL_DENIAL_COST:
            self.enemy.set_new_prompt()
            self.time = self.time_per_prompt
            self.user_text = ""
            self.player_stamina -= SKILL_DENIAL_COST

    def activate_acceptance(self):
        if not self.is_acceptance and self.player_stamina >= SKILL_ACCEPTANCE_COST:
            self.is_acceptance = True
            self.acceptance_timer = SKILL_ACCEPTANCE_DURATION
            self.player_stamina -= SKILL_ACCEPTANCE_COST

    def process_input(self, events):
        super().process_input(events)

        for event in events:
            if event.type == pygame.KEYDOWN and self.is_done_buffer and not self.is_paused:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    self.handle_skill_input(event.key)
                elif not self.is_contemplating:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.player_is_submitted = True
                    elif event.unicode:
                        expected_len = len(self.user_text)
                        if expected_len < len(self.enemy.current_prompt) and event.unicode == self.enemy.current_prompt[expected_len]:
                            self.user_text += event.unicode
                        else:
                            self.user_text = ""
                            if not self.is_delirium:
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
        self.button_inventory = pygame.Rect(BUTTON_INVENTORY_X, BUTTON_INVENTORY_Y, BUTTON_INVENTORY_WIDTH, BUTTON_INVENTORY_HEIGHT)

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
                if self.button_inventory.collidepoint(x, y):
                    self.next_scene = SceneInventory()

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
        self.draw_area_label(screen, self.button_murkey_water, "Murky Water")
        self.draw_area_label(screen, self.button_boat_house, "Boat House")
        self.draw_area_label(screen, self.button_chapel, "Chapel")
        self.draw_area_label(screen, self.button_lighthouse, "Lighthouse")
        self.draw_area_label(screen, self.button_old_chapel, "Old Chapel")

        pygame.draw.rect(screen, (0, 255, 0), self.button_inventory)
        inv_label = self.font.render("Inventory", True, (0, 0, 0))
        screen.blit(inv_label, (
            self.button_inventory.x + self.button_inventory.width // 2 - inv_label.get_width() // 2,
            self.button_inventory.y + self.button_inventory.height // 2 - inv_label.get_height() // 2
        ))

class SceneInventory(SceneBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(None, 25)
        self.font_header = pygame.font.SysFont(None, 30)
        self.font_title = pygame.font.SysFont(None, 50)
        self.font_small = pygame.font.SysFont(None, 22)
        self.button_back = pygame.Rect(30, WINDOW_HEIGHT - 55, 150, 40)
        self.item_rects = []
        self.slot_rects = {}

        self.selected_item = None

        self.skill_data = [
            ("Ctrl+1", "Contemplation", "Freeze the timer",  f"{int(SKILL_CONTEMPLATION_DURATION)}s  |  {SKILL_CONTEMPLATION_COST} SP"),
            ("Ctrl+2", "Delirium",      "No typo damage",    f"{int(SKILL_DELIRIUM_DURATION)}s  |  {SKILL_DELIRIUM_COST} SP"),
            ("Ctrl+3", "Concentration", "+5s to timer",      f"Instant  |  {SKILL_CONCENTRATION_COST} SP"),
            ("Ctrl+4", "Denial",        "Skip prompt",       f"No bosses  |  {SKILL_DENIAL_COST} SP"),
            ("Ctrl+5", "Acceptance",    "Half timer damage", f"{int(SKILL_ACCEPTANCE_DURATION)}s  |  {SKILL_ACCEPTANCE_COST} SP"),
        ]

    def process_input(self, events):
        super().process_input(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_back.collidepoint(event.pos):
                    self.next_scene = SceneMain()
                for i, rect in enumerate(self.item_rects):
                    if rect.collidepoint(event.pos) and i < len(player_inventory):
                        item = player_inventory[i]
                        self.selected_item = item
                        if item.equip_slot:
                            if player_equipment[item.equip_slot] == item:
                                player_equipment[item.equip_slot] = None
                            else:
                                player_equipment[item.equip_slot] = item
                for slot_name, rect in self.slot_rects.items():
                    if rect.collidepoint(event.pos):
                        player_equipment[slot_name] = None

    def draw_bar(self, screen, x, y, w, h, ratio, color):
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(x, y, w, h))
        fill_w = int(w * max(0.0, min(1.0, ratio)))
        if fill_w > 0:
            pygame.draw.rect(screen, color, pygame.Rect(x, y, fill_w, h))

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines, line = [], ""
        for word in words:
            test = (line + " " + word).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.item_rects = []
        self.slot_rects = {}

        PAD = 10
        BOX_Y = 68
        PANEL_H = 400
        ITEMS_X, ITEMS_W = 30, 390
        EQUIP_X, EQUIP_W = 440, 370
        STATS_X, STATS_W = 830, WINDOW_WIDTH - 830 - 30
        SKILL_Y = BOX_Y + PANEL_H + 12

        # Title
        title = self.font_title.render("INVENTORY", True, (255, 255, 255))
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 16))

        # --- Items panel ---
        items_rect = pygame.Rect(ITEMS_X, BOX_Y, ITEMS_W, PANEL_H)
        pygame.draw.rect(screen, (0, 255, 0), items_rect, 2)

        hdr = self.font_header.render("Items", True, (255, 215, 0))
        screen.blit(hdr, (ITEMS_X + PAD, BOX_Y + PAD))
        pygame.draw.line(screen, (0, 255, 0), (ITEMS_X + PAD, BOX_Y + 36), (ITEMS_X + ITEMS_W - PAD, BOX_Y + 36), 1)

        desc_sep_y = BOX_Y + PANEL_H - 110
        row_h = 26
        max_rows = (desc_sep_y - (BOX_Y + 44)) // row_h
        if player_inventory:
            for i, item in enumerate(player_inventory[:max_rows]):
                row_y = BOX_Y + 44 + i * row_h
                row_rect = pygame.Rect(ITEMS_X + PAD, row_y, ITEMS_W - PAD * 2, row_h)
                self.item_rects.append(row_rect)

                is_equipped = item.equip_slot and player_equipment.get(item.equip_slot) == item
                if item.equip_slot is None:
                    text_color = (90, 90, 90)
                elif is_equipped:
                    text_color = (255, 215, 0)
                else:
                    text_color = (255, 255, 255)

                if item.stat in ("damage_reduction", "stamina_regen"):
                    stat_str = f"+{item.value}% {item.stat.replace('_', ' ')}"
                else:
                    stat_str = f"+{item.value} {item.stat.replace('_', ' ')}"
                line = self.font.render(f"{item.name}   {stat_str}", True, text_color)
                screen.blit(line, (ITEMS_X + PAD, row_y + 3))

                if is_equipped:
                    tag = self.font_small.render("[E]", True, (0, 255, 0))
                    screen.blit(tag, (ITEMS_X + ITEMS_W - PAD - tag.get_width(), row_y + 5))
        else:
            empty = self.font.render("No items collected yet.", True, (80, 80, 80))
            screen.blit(empty, (ITEMS_X + PAD, BOX_Y + 44))

        # --- Description panel (bottom of items box) ---
        pygame.draw.line(screen, (0, 255, 0), (ITEMS_X + PAD, desc_sep_y), (ITEMS_X + ITEMS_W - PAD, desc_sep_y), 1)
        desc_x = ITEMS_X + PAD
        desc_w = ITEMS_W - PAD * 2
        if self.selected_item and self.selected_item.description:
            lines = self.wrap_text(self.selected_item.description, self.font_small, desc_w)
            for j, text_line in enumerate(lines[:4]):
                surf = self.font_small.render(text_line, True, (200, 200, 200))
                screen.blit(surf, (desc_x, desc_sep_y + 6 + j * 22))
        else:
            hint = self.font_small.render("Click an item for details.", True, (70, 70, 70))
            screen.blit(hint, (desc_x, desc_sep_y + 6))

        # --- Equipment panel ---
        equip_rect = pygame.Rect(EQUIP_X, BOX_Y, EQUIP_W, PANEL_H)
        pygame.draw.rect(screen, (0, 255, 0), equip_rect, 2)

        hdr2 = self.font_header.render("Equipment", True, (255, 215, 0))
        screen.blit(hdr2, (EQUIP_X + PAD, BOX_Y + PAD))
        pygame.draw.line(screen, (0, 255, 0), (EQUIP_X + PAD, BOX_Y + 36), (EQUIP_X + EQUIP_W - PAD, BOX_Y + 36), 1)

        slot_h = 72
        slot_gap = 10
        for i, (slot_name, slot_label) in enumerate([("head", "Head"), ("body", "Body"), ("legs", "Legs"), ("weapon", "Weapon")]):
            sy = BOX_Y + 44 + i * (slot_h + slot_gap)
            s_rect = pygame.Rect(EQUIP_X + PAD, sy, EQUIP_W - PAD * 2, slot_h)
            self.slot_rects[slot_name] = s_rect

            equipped_item = player_equipment.get(slot_name)
            pygame.draw.rect(screen, (0, 255, 0), s_rect, 2)

            slot_lbl = self.font_small.render(slot_label, True, (180, 180, 180))
            screen.blit(slot_lbl, (s_rect.x + 8, s_rect.y + 8))

            if equipped_item:
                name_surf = self.font.render(equipped_item.name, True, (255, 255, 255))
                screen.blit(name_surf, (s_rect.x + 8, s_rect.y + 28))
                if equipped_item.stat in ("damage_reduction", "stamina_regen"):
                    eq_stat_str = f"+{equipped_item.value}% {equipped_item.stat.replace('_', ' ')}"
                else:
                    eq_stat_str = f"+{equipped_item.value} {equipped_item.stat.replace('_', ' ')}"
                stat_surf = self.font_small.render(eq_stat_str, True, (255, 215, 0))
                screen.blit(stat_surf, (s_rect.x + 8, s_rect.y + 50))
            else:
                empty_surf = self.font.render("— empty —", True, (60, 60, 60))
                screen.blit(empty_surf, (s_rect.x + 8, s_rect.y + 28))

        # --- Stats panel ---
        stats_rect = pygame.Rect(STATS_X, BOX_Y, STATS_W, PANEL_H)
        pygame.draw.rect(screen, (0, 255, 0), stats_rect, 2)

        hdr3 = self.font_header.render("Player Stats", True, (255, 215, 0))
        screen.blit(hdr3, (STATS_X + PAD, BOX_Y + PAD))
        pygame.draw.line(screen, (0, 255, 0), (STATS_X + PAD, BOX_Y + 36), (STATS_X + STATS_W - PAD, BOX_Y + 36), 1)

        equipped = [item for item in player_equipment.values() if item is not None]
        bonus_hp = sum(i.value for i in equipped if i.stat == "health")
        bonus_sp = sum(i.value for i in equipped if i.stat == "stamina")
        bonus_dr = sum(i.value for i in equipped if i.stat == "damage_reduction")
        bonus_regen = sum(i.value for i in equipped if i.stat == "stamina_regen")
        total_hp = PLAYER_BASE_HP + bonus_hp
        total_sp = PLAYER_BASE_STAMINA + bonus_sp
        total_regen = PLAYER_BASE_STAMINA_REGEN + (bonus_regen / 100) * total_sp

        bar_x = STATS_X + PAD
        bar_w = STATS_W - PAD * 2
        bar_h = 14

        stat_rows = [
            ("HP",            f"{total_hp}  (base {PLAYER_BASE_HP} + {bonus_hp})", min(1.0, total_hp / 200), (80, 200, 80)),
            ("Stamina",       f"{total_sp}  (base {PLAYER_BASE_STAMINA} + {bonus_sp})", min(1.0, total_sp / 200), (255, 215, 0)),
            ("Dmg Reduction", f"{bonus_dr}%",                                           min(1.0, bonus_dr / 100), (0, 180, 255)),
            ("SP Regen",      f"{total_regen:.1f}/s  (base {PLAYER_BASE_STAMINA_REGEN} + {bonus_regen}% of SP)", min(1.0, total_regen / 20), (0, 200, 160)),
        ]
        for i, (label, value_text, ratio, color) in enumerate(stat_rows):
            ry = BOX_Y + 44 + i * 82
            lbl_surf = self.font_small.render(label, True, (180, 180, 180))
            screen.blit(lbl_surf, (bar_x, ry))
            val_surf = self.font.render(value_text, True, (255, 255, 255))
            screen.blit(val_surf, (bar_x, ry + 20))
            self.draw_bar(screen, bar_x, ry + 48, bar_w, bar_h, ratio, color)

        # --- Skills panel ---
        skill_panel_h = WINDOW_HEIGHT - SKILL_Y - 60
        skill_rect = pygame.Rect(30, SKILL_Y, WINDOW_WIDTH - 60, skill_panel_h)
        pygame.draw.rect(screen, (0, 255, 0), skill_rect, 2)

        hdr4 = self.font_header.render("Skills  (use Ctrl + number during combat)", True, (255, 215, 0))
        screen.blit(hdr4, (30 + PAD, SKILL_Y + PAD))
        pygame.draw.line(screen, (0, 255, 0), (30 + PAD, SKILL_Y + 36), (WINDOW_WIDTH - 30 - PAD, SKILL_Y + 36), 1)

        card_area_w = WINDOW_WIDTH - 60 - PAD * 2
        card_w = card_area_w // 5
        card_x0 = 30 + PAD
        card_y = SKILL_Y + 42
        card_h = skill_panel_h - 50

        for i, (key, name, desc, cost) in enumerate(self.skill_data):
            cx = card_x0 + i * card_w
            card_rect = pygame.Rect(cx, card_y, card_w - 6, card_h)
            pygame.draw.rect(screen, (0, 255, 0), card_rect, 2)

            mid = cx + (card_w - 6) // 2
            key_surf = self.font_small.render(key, True, (0, 255, 255))
            screen.blit(key_surf, (mid - key_surf.get_width() // 2, card_y + 8))
            name_surf = self.font.render(name, True, (255, 255, 255))
            screen.blit(name_surf, (mid - name_surf.get_width() // 2, card_y + 28))
            desc_surf = self.font_small.render(desc, True, (200, 200, 200))
            screen.blit(desc_surf, (mid - desc_surf.get_width() // 2, card_y + 52))
            cost_surf = self.font_small.render(cost, True, (255, 215, 0))
            screen.blit(cost_surf, (mid - cost_surf.get_width() // 2, card_y + 72))

        # Back button
        pygame.draw.rect(screen, (0, 255, 0), self.button_back)
        lbl = self.font.render("Back", True, (0, 0, 0))
        screen.blit(lbl, (
            self.button_back.x + self.button_back.width // 2 - lbl.get_width() // 2,
            self.button_back.y + self.button_back.height // 2 - lbl.get_height() // 2
        ))

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