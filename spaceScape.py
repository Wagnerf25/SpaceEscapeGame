import pygame
import random
import os
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape - 3 Fases")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

ASSETS = {
    "background1": "fundo_espacial.png",
    "background2": "fundo_espacial2.png",
    "background3": "fundo_espacial3.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "music1": "distorted-future-363866.mp3",
    "music2": "ThemeSpace2.mp3",
    "music3": "ThemeSpace3.mp3"
}

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)

def load_image(filename, fallback_color, size=None):
    if filename and os.path.exists(filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except:
            pass
    surf = pygame.Surface(size or (50, 50), pygame.SRCALPHA)
    surf.fill(fallback_color)
    return surf

def load_sound(filename):
    if filename and os.path.exists(filename):
        try:
            return pygame.mixer.Sound(filename)
        except:
            return None
    return None

def try_play_music(filename, volume=0.3):
    try:
        if filename and os.path.exists(filename):
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            return True
    except:
        pass
    return False

background_imgs = {
    1: load_image(ASSETS["background1"], (10, 10, 30), (WIDTH, HEIGHT)),
    2: load_image(ASSETS["background2"], (8, 8, 25), (WIDTH, HEIGHT)),
    3: load_image(ASSETS["background3"], (6, 6, 20), (WIDTH, HEIGHT))
}

player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 7

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        mx, _ = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            self.rect.centerx = mx
        elif abs(self.rect.centerx - mx) > 4:
            if self.rect.centerx < mx:
                self.rect.centerx += self.speed
            elif self.rect.centerx > mx:
                self.rect.centerx -= self.speed

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class Meteor:
    def __init__(self, x, y, w, h, speed, behavior=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.behavior = behavior
        self._phase = random.uniform(0, math.pi * 2)
        self._amp = random.randint(30, 80)
        self._hz = random.uniform(0.01, 0.04)

    def update(self):
        if self.behavior == 'zigzag':
            self._phase += self._hz
            self.rect.x += int(math.sin(self._phase) * 3)
        elif self.behavior == 'accelerate':
            self.speed += 0.02
        self.rect.y += int(self.speed)

    def reset(self):
        self.rect.y = random.randint(-500, -40)
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self._phase = random.uniform(0, math.pi * 2)

    def draw(self, surf):
        img = pygame.transform.scale(meteor_img, (self.rect.width, self.rect.height))
        surf.blit(img, self.rect)

class PhaseConfig:
    def __init__(self, id, bg, music, meteor_count, meteor_speed, meteor_size, required_score, behaviors=None):
        self.id = id
        self.bg = bg
        self.music = music
        self.meteor_count = meteor_count
        self.meteor_speed = meteor_speed
        self.meteor_size = meteor_size
        self.required_score = required_score
        self.behaviors = behaviors or []

PHASES = {
    1: PhaseConfig(1, background_imgs[1], ASSETS["music1"], 5, 5, (40, 40), 30, []),
    2: PhaseConfig(2, background_imgs[2], ASSETS["music2"], 7, 7, (50, 50), 70, ['accelerate']),
    3: PhaseConfig(3, background_imgs[3], ASSETS["music3"], 10, 9, (60, 60), None, ['accelerate', 'zigzag'])
}

def create_meteors_for_phase(cfg):
    lst = []
    for _ in range(cfg.meteor_count):
        w, h = cfg.meteor_size
        x = random.randint(0, WIDTH - w)
        y = random.randint(-500, -40)
        behavior = None
        if cfg.behaviors and random.random() < 0.35:
            behavior = random.choice(cfg.behaviors)
        lst.append(Meteor(x, y, w, h, cfg.meteor_speed, behavior))
    return lst

player = Player()
current_phase = 1
score = 0
lives = 3
state = 'playing'
phase_cfg = PHASES[current_phase]
meteors = create_meteors_for_phase(phase_cfg)
try_play_music(phase_cfg.music)
transition_timer = 0
transition_duration = 90
running = True

while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if state == 'playing':
        player.update(keys)

        for m in meteors:
            m.update()
            if m.rect.y > HEIGHT:
                m.reset()
                score += 1
                if sound_point:
                    sound_point.play()
            if m.rect.colliderect(player.rect):
                lives -= 1
                m.reset()
                if sound_hit:
                    sound_hit.play()
                if lives <= 0:
                    state = 'gameover'
                    pygame.mixer.music.stop()

        if PHASES[current_phase].required_score and score >= PHASES[current_phase].required_score:
            state = 'transition'
            transition_timer = 0

    elif state == 'transition':
        transition_timer += 1
        if transition_timer == 1:
            pygame.mixer.music.fadeout(500)
        if transition_timer >= transition_duration:
            current_phase += 1
            if current_phase > 3:
                current_phase = 3
            phase_cfg = PHASES[current_phase]
            meteors = create_meteors_for_phase(phase_cfg)
            try_play_music(phase_cfg.music)
            state = 'playing'

    screen.blit(PHASES[current_phase].bg, (0, 0))
    player.draw(screen)
    for m in meteors:
        m.draw(screen)

    hud = font.render(f"Pontos: {score}   Vidas: {lives}   Fase: {current_phase}", True, WHITE)
    screen.blit(hud, (10, 10))

    if state == 'transition':
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        big = pygame.font.Font(None, 72)
        txt = big.render(f"Fase {current_phase + 1}", True, WHITE)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))

    if state == 'gameover':
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        big = pygame.font.Font(None, 72)
        txt = big.render("GAME OVER", True, RED)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))

    pygame.display.flip()

pygame.quit()
