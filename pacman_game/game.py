import os
import random
import sys
import pygame
from pygame.locals import K_a, K_d, K_s, K_w, MOUSEBUTTONDOWN, QUIT
SCREEN_SIZE = 592
TILE_SIZE = 16
MAX_TILE_ORIGIN = SCREEN_SIZE - TILE_SIZE
WIN_SCORE = 250
window = None
fps_clock = None
wall_image = None
food_image = None
big_food_image = None
player_image = None
ghost_image = None
purple_ghost_image = None
map_xy = []
food_xy = []
bigFood_xy = []
score = 0
timer = 0
font = None
menu_font = None
small_font = None
tiny_font = None
title_font = None
info_font = None
button_font = None
game_over = False
game_over_reason = ""
game_state = "start_menu"
selected_level = None
game_map = None
player = None
ghosts = []
level_1_button = None
level_2_button = None
level_3_button = None
back_button = None
start_button = None
restart_button = None
exit_button = None
level_descriptions = {
    1: [
        "Level 1: One ghost",
        "Red Ghost chases you along the path.",
        "Try to avoid it and eat the food to gain score.",
    ],
    2: [
        "Level 2: Two ghosts",
        "Red Ghost chases you, Purple Ghost teleports to you.",
        "Try to avoid them and eat the food to gain score.",
    ],
    3: [
        "Level 3: Two ghosts, but faster",
        "Red Ghost chases you, Purple Ghost teleports to you faster.",
        "Try to avoid them and eat the food to gain score.",
    ],
}
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
class Map:
    def __init__(self):
        with open(resource_path("map2.txt"), encoding="utf-8") as file_handle:
            self.data = file_handle.readlines()
        map_y = 0
        for map_line in self.data:
            map_x = 0
            for char in map_line:
                if char == "*":
                    map_xy.append((map_x, map_y))
                if char == " ":
                    food_xy.append((map_x, map_y))
                if char == "|":
                    bigFood_xy.append((map_x, map_y))
                map_x += TILE_SIZE
            map_y += TILE_SIZE
    def draw(self):
        for wall_tile in map_xy:
            window.blit(wall_image, wall_tile)
        for food_tile in food_xy:
            window.blit(food_image, food_tile)
        for big_food_tile in bigFood_xy:
            window.blit(big_food_image, big_food_tile)
class Player:
    def __init__(self, image):
        self.x = TILE_SIZE
        self.y = TILE_SIZE
        self.img = image
        self.angle = 90
    def draw(self):
        rotated_image = pygame.transform.rotate(self.img, self.angle)
        window.blit(rotated_image, (self.x, self.y))
    def control(self):
        global score, timer
        press = pygame.key.get_pressed()
        if press[K_w]:
            self.y -= TILE_SIZE
            if self.y < 0 or (self.x, self.y) in map_xy:
                self.y += TILE_SIZE
            self.angle = 90
        elif press[K_s]:
            self.y += TILE_SIZE
            if self.y > MAX_TILE_ORIGIN or (self.x, self.y) in map_xy:
                self.y -= TILE_SIZE
            self.angle = 270
        elif press[K_a]:
            self.x -= TILE_SIZE
            if self.x < 0 or (self.x, self.y) in map_xy:
                self.x += TILE_SIZE
            self.angle = 180
        elif press[K_d]:
            self.x += TILE_SIZE
            if self.x > MAX_TILE_ORIGIN or (self.x, self.y) in map_xy:
                self.x -= TILE_SIZE
            self.angle = 0
        for index, food_tile in enumerate(food_xy):
            if (self.x, self.y) == food_tile:
                food_xy.pop(index)
                score += 1
                break
        if (self.x, self.y) in bigFood_xy:
            bigFood_xy.remove((self.x, self.y))
            timer = 20 * 20
            score += 2
class Ghost:
    def __init__(self, image):
        self.x = SCREEN_SIZE - TILE_SIZE * 2
        self.y = TILE_SIZE
        self.img = image
        self.angle = 180
    def draw(self):
        window.blit(self.img, (self.x, self.y))
    def movement(self, player_x, player_y):
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            possible = []
            distances = {}
            if self.x < SCREEN_SIZE - TILE_SIZE and (self.x + TILE_SIZE, self.y) not in map_xy:
                possible.append(0)
                distances[0] = abs((self.x + TILE_SIZE) - player_x) + abs(self.y - player_y)
            if self.x > 0 and (self.x - TILE_SIZE, self.y) not in map_xy:
                possible.append(180)
                distances[180] = abs((self.x - TILE_SIZE) - player_x) + abs(self.y - player_y)
            if self.y > 0 and (self.x, self.y - TILE_SIZE) not in map_xy:
                possible.append(90)
                distances[90] = abs(self.x - player_x) + abs((self.y - TILE_SIZE) - player_y)
            if self.y < SCREEN_SIZE - TILE_SIZE and (self.x, self.y + TILE_SIZE) not in map_xy:
                possible.append(270)
                distances[270] = abs(self.x - player_x) + abs((self.y + TILE_SIZE) - player_y)
            if self.angle == 0 and 180 in possible:
                possible.remove(180)
            elif self.angle == 180 and 0 in possible:
                possible.remove(0)
            elif self.angle == 90 and 270 in possible:
                possible.remove(270)
            elif self.angle == 270 and 90 in possible:
                possible.remove(90)
            if possible:
                self.angle = min(possible, key=lambda direction: distances[direction])
        if self.angle == 0:
            self.x += 4
            if self.x > MAX_TILE_ORIGIN or (self.x + 12, self.y) in map_xy:
                self.x -= 4
        if self.angle == 180:
            self.x -= 4
            if self.x < 0 or (self.x - 12, self.y) in map_xy:
                self.x += 4
        if self.angle == 90:
            self.y -= 4
            if self.y < 0 or (self.x, self.y - 12) in map_xy:
                self.y += 4
        if self.angle == 270:
            self.y += 4
            if self.y > MAX_TILE_ORIGIN or (self.x, self.y + 12) in map_xy:
                self.y -= 4
class PurpleGhost:
    def __init__(self, image, teleport_interval=5000):
        self.img = image
        self.x = SCREEN_SIZE - TILE_SIZE * 2
        self.y = TILE_SIZE
        self.teleport_interval = teleport_interval
        self.last_teleport_time = pygame.time.get_ticks()
        self.recorded_player_pos = (self.x, self.y)
        self.has_recorded_pos = False
    def draw(self):
        window.blit(self.img, (self.x, self.y))
    def teleport(self):
        walkable_tiles = []
        for row in range(0, SCREEN_SIZE, TILE_SIZE):
            for col in range(0, SCREEN_SIZE, TILE_SIZE):
                if (col, row) not in map_xy:
                    walkable_tiles.append((col, row))
        if walkable_tiles:
            self.x, self.y = random.choice(walkable_tiles)
    def update(self, player_x, player_y):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_teleport_time
        if elapsed >= self.teleport_interval - 1000 and not self.has_recorded_pos:
            self.recorded_player_pos = ((player_x // TILE_SIZE) * TILE_SIZE, (player_y // TILE_SIZE) * TILE_SIZE)
            self.has_recorded_pos = True
        if elapsed >= self.teleport_interval:
            target_x, target_y = self.recorded_player_pos
            if (target_x, target_y) not in map_xy:
                self.x, self.y = target_x, target_y
            self.last_teleport_time = current_time
            self.has_recorded_pos = False
def collide(char1, char2):
    rect1 = char1.img.get_rect(topleft=(char1.x, char1.y))
    rect2 = char2.img.get_rect(topleft=(char2.x, char2.y))
    return rect1.colliderect(rect2)
def init_game_for_level(level):
    global game_map, player, ghosts, score, timer, game_over, game_over_reason
    map_xy.clear()
    food_xy.clear()
    bigFood_xy.clear()
    score = 0
    timer = 0
    game_over = False
    game_over_reason = ""
    game_map = Map()
    player = Player(player_image)
    ghosts = [Ghost(ghost_image)]
    if level == 2:
        ghosts.append(PurpleGhost(purple_ghost_image, 5000))
    elif level == 3:
        ghosts.append(PurpleGhost(purple_ghost_image, 3000))
def start_menu():
    window.fill((20, 24, 60))
    title_text = title_font.render("PACMAN CHASE", True, (255, 232, 120))
    window.blit(title_text, ((SCREEN_SIZE - title_text.get_width()) // 2, 44))
    controls_title = menu_font.render("Controls", True, (255, 255, 255))
    controls_text = small_font.render("Use W A S D to move tile by tile.", True, (235, 235, 235))
    window.blit(controls_title, (70, 130))
    window.blit(controls_text, (70, 166))
    mechanism_title = menu_font.render("General Mechanism", True, (255, 255, 255))
    mechanism_line_1 = tiny_font.render("Eat food to gain score and avoid ghosts.", True, (235, 235, 235))
    mechanism_line_2 = tiny_font.render(f"Reach score {WIN_SCORE} to win.", True, (235, 235, 235))
    window.blit(mechanism_title, (70, 214))
    window.blit(mechanism_line_1, (70, 252))
    window.blit(mechanism_line_2, (70, 278))
    pygame.draw.rect(window, (46, 135, 66), level_1_button, border_radius=8)
    pygame.draw.rect(window, (56, 110, 180), level_2_button, border_radius=8)
    pygame.draw.rect(window, (138, 74, 158), level_3_button, border_radius=8)
    l1_text = small_font.render("Level 1 - One ghost", True, (255, 255, 255))
    l2_text = small_font.render("Level 2 - Two ghosts", True, (255, 255, 255))
    l3_text = small_font.render("Level 3 - Fast teleport", True, (255, 255, 255))
    window.blit(l1_text, (level_1_button.centerx - l1_text.get_width() // 2, level_1_button.centery - l1_text.get_height() // 2))
    window.blit(l2_text, (level_2_button.centerx - l2_text.get_width() // 2, level_2_button.centery - l2_text.get_height() // 2))
    window.blit(l3_text, (level_3_button.centerx - l3_text.get_width() // 2, level_3_button.centery - l3_text.get_height() // 2))
def level_info(level):
    window.fill((18, 18, 48))
    header = title_font.render(f"LEVEL {level}", True, (255, 255, 255))
    window.blit(header, ((SCREEN_SIZE - header.get_width()) // 2, 60))
    for index, text in enumerate(level_descriptions[level]):
        line_text = small_font.render(text, True, (240, 240, 240))
        window.blit(line_text, ((SCREEN_SIZE - line_text.get_width()) // 2, 190 + index * 44))
    pygame.draw.rect(window, (90, 90, 120), back_button, border_radius=8)
    pygame.draw.rect(window, (50, 140, 70), start_button, border_radius=8)
    back_text = button_font.render("Back", True, (255, 255, 255))
    start_text = button_font.render("Start", True, (255, 255, 255))
    window.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - back_text.get_height() // 2))
    window.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
def _load_assets():
    global wall_image, food_image, big_food_image, player_image, ghost_image, purple_ghost_image
    player_surface = pygame.image.load(resource_path("pacman.png"))
    ghost_surface = pygame.image.load(resource_path("ghost.png"))
    wall_image = pygame.image.load(resource_path("wall.png"))
    food_image = pygame.image.load(resource_path("food.png"))
    big_food_surface = pygame.image.load(resource_path("red_ball.jpg"))
    purple_ghost_surface = pygame.image.load(resource_path("ghost(2).jpg"))
    player_image = player_surface
    ghost_image = pygame.transform.scale(ghost_surface, (TILE_SIZE, TILE_SIZE))
    big_food_image = pygame.transform.scale(big_food_surface, (TILE_SIZE, TILE_SIZE))
    purple_ghost_image = pygame.transform.scale(purple_ghost_surface, (TILE_SIZE, TILE_SIZE))
def _init_ui():
    global font, menu_font, small_font, tiny_font, title_font, info_font, button_font
    global level_1_button, level_2_button, level_3_button, back_button, start_button, restart_button, exit_button
    font = pygame.font.Font(None, 36)
    menu_font = pygame.font.Font(None, 44)
    small_font = pygame.font.Font(None, 30)
    tiny_font = pygame.font.Font(None, 26)
    title_font = pygame.font.Font(None, 84)
    info_font = pygame.font.Font(None, 42)
    button_font = pygame.font.Font(None, 40)
    level_1_button = pygame.Rect(166, 320, 260, 52)
    level_2_button = pygame.Rect(166, 386, 260, 52)
    level_3_button = pygame.Rect(166, 452, 260, 52)
    back_button = pygame.Rect(166, 470, 120, 55)
    start_button = pygame.Rect(306, 470, 120, 55)
    restart_button = pygame.Rect(156, 470, 130, 55)
    exit_button = pygame.Rect(306, 470, 130, 55)
def main():
    global window, fps_clock, game_state, selected_level, game_over, game_over_reason
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Pacman - by Norris")
    fps_clock = pygame.time.Clock()
    _load_assets()
    _init_ui()
    game_state = "start_menu"
    selected_level = None
    game_over = False
    game_over_reason = ""
    while True:
        fps_clock.tick(20)
        if game_state == "playing":
            window.fill((0, 0, 100))
            game_map.draw()
            player.control()
            player.draw()
            for enemy in ghosts:
                if isinstance(enemy, Ghost):
                    enemy.movement(player.x, player.y)
                elif isinstance(enemy, PurpleGhost):
                    enemy.update(player.x, player.y)
                enemy.draw()
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            window.blit(score_text, (SCREEN_SIZE - score_text.get_width() - 10, 10))
            if any(collide(player, enemy) for enemy in ghosts):
                game_over = True
                game_over_reason = "You've been touched by a ghost"
            if score >= WIN_SCORE:
                game_over = True
                game_over_reason = "You've eaten enough food"
            if game_over:
                game_state = "game_over"
        elif game_state == "start_menu":
            start_menu()
        elif game_state == "level_info":
            level_info(selected_level)
        elif game_state == "game_over":
            window.fill((15, 15, 35))
            title_text = title_font.render("Game Over", True, (255, 255, 255))
            reason_text = info_font.render(game_over_reason, True, (240, 240, 240))
            final_score_text = info_font.render(f"Score: {score}", True, (255, 230, 120))
            window.blit(title_text, ((SCREEN_SIZE - title_text.get_width()) // 2, 140))
            window.blit(reason_text, ((SCREEN_SIZE - reason_text.get_width()) // 2, 240))
            window.blit(final_score_text, ((SCREEN_SIZE - final_score_text.get_width()) // 2, 295))
            pygame.draw.rect(window, (50, 140, 70), restart_button, border_radius=8)
            pygame.draw.rect(window, (140, 50, 50), exit_button, border_radius=8)
            restart_text = button_font.render("Restart", True, (255, 255, 255))
            exit_text = button_font.render("Exit", True, (255, 255, 255))
            window.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))
            window.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == MOUSEBUTTONDOWN:
                if game_state == "start_menu":
                    if level_1_button.collidepoint(event.pos):
                        selected_level = 1
                        game_state = "level_info"
                    elif level_2_button.collidepoint(event.pos):
                        selected_level = 2
                        game_state = "level_info"
                    elif level_3_button.collidepoint(event.pos):
                        selected_level = 3
                        game_state = "level_info"
                elif game_state == "level_info":
                    if back_button.collidepoint(event.pos):
                        game_state = "start_menu"
                    elif start_button.collidepoint(event.pos):
                        init_game_for_level(selected_level)
                        game_state = "playing"
                elif game_state == "game_over":
                    if restart_button.collidepoint(event.pos):
                        game_state = "start_menu"
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        raise SystemExit
if __name__ == "__main__":
    main()
