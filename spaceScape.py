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
    "meteor1": "meteoro001.png",
    "meteor2": "meteoro002.png",
    "meteor3": "meteoro003.png",
    "meteor_special": "meteoroespecial.png",
    "meteor_invincibility": "meteorovermelho.png",
    "laserbeam": "laserbeam.png",
    "gameover": "Game-over.png",
    "insertcoin": "insertcoin.png",
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

def create_engine_frames():
    """Criar frames de animação do motor da nave"""
    frames = []
    colors = [
        (255, 200, 0),    # Amarelo
        (255, 150, 0),    # Laranja
        (255, 80, 0),     # Laranja-vermelho
        (200, 40, 0)      # Vermelho escuro
    ]
    alpha_values = [100, 150, 200, 255]

    for frame_idx in range(4):
        engine_frame = pygame.Surface((40, 40), pygame.SRCALPHA)
        engine_frame.fill((0, 0, 0, 0))

        # Desenhar chamas em 3 camadas
        for layer in range(3):
            y_pos = 12 + (layer * 7)
            width = int(20 - (layer * 3))
            x_pos = (40 - width) // 2

            color_with_alpha = (*colors[frame_idx], alpha_values[frame_idx])
            pygame.draw.rect(engine_frame, color_with_alpha, (x_pos, y_pos, width, 6))

        frames.append(engine_frame)

    return frames

background_imgs = {
    1: load_image(ASSETS["background1"], (10, 10, 30), (WIDTH, HEIGHT)),
    2: load_image(ASSETS["background2"], (8, 8, 25), (WIDTH, HEIGHT)),
    3: load_image(ASSETS["background3"], (6, 6, 20), (WIDTH, HEIGHT))
}

player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_imgs = [
    load_image(ASSETS["meteor1"], RED, (40, 40)),
    load_image(ASSETS["meteor2"], RED, (40, 40)),
    load_image(ASSETS["meteor3"], RED, (40, 40))
]
meteor_special_img = load_image(ASSETS["meteor_special"], (255, 100, 0), (50, 50))
meteor_invincibility_img = load_image(ASSETS["meteor_invincibility"], (255, 0, 0), (45, 45))
laserbeam_img = load_image(ASSETS["laserbeam"], (0, 255, 0), (10, 30))
gameover_img = load_image(ASSETS["gameover"], (0, 0, 0), (WIDTH, HEIGHT))
insertcoin_img = load_image(ASSETS["insertcoin"], (0, 0, 0), (WIDTH, HEIGHT))

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

# Criar frames de animação do motor
engine_frames = create_engine_frames()

class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 7
        self.lasers = []
        self.shoot_cooldown = 0
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 300  # 5 segundos a 60 FPS
        # Animação do motor
        self.engine_frame_index = 0
        self.engine_frame_counter = 0
        self.engine_animation_speed = 2  # Velocidade de animação do motor

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

        # Disparar com SPACE ou clique do mouse
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot()
            self.shoot_cooldown = 10

        self.shoot_cooldown -= 1

        # Atualizar invencibilidade
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Atualizar animação do motor
        self.engine_frame_counter += 1
        if self.engine_frame_counter >= self.engine_animation_speed:
            self.engine_frame_index = (self.engine_frame_index + 1) % len(engine_frames)
            self.engine_frame_counter = 0

        # Atualizar lasers
        for laser in self.lasers[:]:
            laser.update()
            if laser.rect.y < 0:
                self.lasers.remove(laser)

    def shoot(self):
        laser = Laser(self.rect.centerx - 5, self.rect.top)
        self.lasers.append(laser)

    def activate_invincibility(self):
        self.invincible = True
        self.invincible_timer = self.invincible_duration

    def draw(self, surf):
        # Desenhar nave com efeito piscante se invencível
        if self.invincible and (self.invincible_timer // 10) % 2 == 0:
            img = self.image.copy()
            img.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
            surf.blit(img, self.rect)
        else:
            surf.blit(self.image, self.rect)

        # Desenhar animação do motor abaixo da nave
        engine_img = engine_frames[self.engine_frame_index]
        engine_rect = engine_img.get_rect(centerx=self.rect.centerx, top=self.rect.bottom - 5)
        surf.blit(engine_img, engine_rect)

        for laser in self.lasers:
            laser.draw(surf)

class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 30)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

    def draw(self, surf):
        img = pygame.transform.scale(laserbeam_img, (self.rect.width, self.rect.height))
        surf.blit(img, self.rect)

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 255), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_color = (150, 150, 255)
        self.is_hovered = False

    def draw(self, surf):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surf, color, self.rect)
        pygame.draw.rect(surf, WHITE, self.rect, 3)  # Bordas

        font_btn = pygame.font.Font(None, 32)
        txt = font_btn.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

class Meteor:
    def __init__(self, x, y, w, h, speed, behavior=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.behavior = behavior
        self._phase = random.uniform(0, math.pi * 2)
        self._amp = random.randint(30, 80)
        self._hz = random.uniform(0.01, 0.04)
        # Animação do sprite
        self.frame_index = 0
        self.frame_counter = 0
        self.animation_speed = 5  # Número de updates antes de trocar frame

    def update(self):
        if self.behavior == 'zigzag':
            self._phase += self._hz
            self.rect.x += int(math.sin(self._phase) * 3)
        elif self.behavior == 'accelerate':
            self.speed += 0.02
        self.rect.y += int(self.speed)

        # Atualizar animação
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(meteor_imgs)
            self.frame_counter = 0

    def reset(self):
        self.rect.y = random.randint(-500, -40)
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self._phase = random.uniform(0, math.pi * 2)
        self.frame_index = 0
        self.frame_counter = 0

    def draw(self, surf):
        img = pygame.transform.scale(meteor_imgs[self.frame_index], (self.rect.width, self.rect.height))
        surf.blit(img, self.rect)

class MeteorSpecial:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.active = False
        self.spawn_timer = 0
        self.spawn_interval = 180  # 3 segundos a 60 FPS
        self.is_falling = False

    def update(self):
        if not self.is_falling:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self.is_falling = True
                self.rect.y = -self.rect.height
                self.rect.x = random.randint(0, WIDTH - self.rect.width)
        else:
            self.rect.y += int(self.speed)
            if self.rect.y > HEIGHT:
                self.is_falling = False

    def reset(self):
        self.is_falling = False
        self.spawn_timer = 0

    def draw(self, surf):
        if self.is_falling:
            img = pygame.transform.scale(meteor_special_img, (self.rect.width, self.rect.height))
            surf.blit(img, self.rect)

class MeteorInvincibility:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.spawn_timer = 0
        self.spawn_interval = 300  # 5 segundos a 60 FPS
        self.is_falling = False

    def update(self):
        if not self.is_falling:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self.is_falling = True
                self.rect.y = -self.rect.height
                self.rect.x = random.randint(0, WIDTH - self.rect.width)
        else:
            self.rect.y += int(self.speed)
            if self.rect.y > HEIGHT:
                self.is_falling = False

    def reset(self):
        self.is_falling = False
        self.spawn_timer = 0

    def draw(self, surf):
        if self.is_falling:
            img = pygame.transform.scale(meteor_invincibility_img, (self.rect.width, self.rect.height))
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
    2: PhaseConfig(2, background_imgs[2], ASSETS["music2"], 7, 7, (50, 50), 150, ['accelerate']),
    3: PhaseConfig(3, background_imgs[3], ASSETS["music3"], 10, 9, (60, 60), 999, ['accelerate', 'zigzag'])
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
state = 'menu'  # Mudar para 'menu' como estado inicial
phase_cfg = PHASES[current_phase]
meteors = create_meteors_for_phase(phase_cfg)
meteor_special = MeteorSpecial(0, 0, 50, 50, 6)
meteor_invincibility = MeteorInvincibility(0, 0, 45, 45, 4)
try_play_music(phase_cfg.music)
transition_timer = 0
transition_duration = 90

# Botões de game over
btn_restart = Button(WIDTH//2 - 150, HEIGHT - 120, 140, 50, "REINICIAR")
btn_exit = Button(WIDTH//2 + 10, HEIGHT - 120, 140, 50, "SAIR")

# Botão de insert coin
btn_insert_coin = Button(WIDTH//2 - 80, HEIGHT - 100, 160, 60, "INSERT COIN", (255, 100, 0), (255, 255, 255))

running = True

while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == 'menu':
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Iniciar o jogo
                    state = 'playing'
                    pygame.mixer.music.stop()
                    try_play_music(phase_cfg.music)
            elif state == 'gameover':
                if event.key == pygame.K_SPACE:
                    # Reiniciar o jogo
                    player = Player()
                    current_phase = 1
                    score = 0
                    lives = 3
                    phase_cfg = PHASES[current_phase]
                    meteors = create_meteors_for_phase(phase_cfg)
                    meteor_special.reset()
                    meteor_invincibility.reset()
                    try_play_music(phase_cfg.music)
                    state = 'playing'
                elif event.key == pygame.K_ESCAPE:
                    running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'menu':
                if btn_insert_coin.is_clicked(mouse_pos):
                    # Iniciar o jogo
                    state = 'playing'
                    pygame.mixer.music.stop()
                    try_play_music(phase_cfg.music)
            elif state == 'gameover':
                if btn_restart.is_clicked(mouse_pos):
                    # Reiniciar o jogo
                    player = Player()
                    current_phase = 1
                    score = 0
                    lives = 3
                    phase_cfg = PHASES[current_phase]
                    meteors = create_meteors_for_phase(phase_cfg)
                    meteor_special.reset()
                    meteor_invincibility.reset()
                    try_play_music(phase_cfg.music)
                    state = 'playing'
                elif btn_exit.is_clicked(mouse_pos):
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
                if not player.invincible:
                    lives -= 1
                    m.reset()
                    if sound_hit:
                        sound_hit.play()
                    if lives <= 0:
                        state = 'gameover'
                        pygame.mixer.music.stop()
                else:
                    m.reset()

            # Colisão entre laser e meteoro
            for laser in player.lasers[:]:
                if laser.rect.colliderect(m.rect):
                    player.lasers.remove(laser)
                    m.reset()
                    score += 5
                    if sound_point:
                        sound_point.play()
                    break

        # Atualizar meteoro especial
        meteor_special.update()
        if meteor_special.is_falling and meteor_special.rect.colliderect(player.rect):
            # Meteoro especial causa morte instantânea
            lives = 0
            state = 'gameover'
            pygame.mixer.music.stop()
            if sound_hit:
                sound_hit.play()

        # Atualizar meteoro de invencibilidade
        meteor_invincibility.update()
        if meteor_invincibility.is_falling and meteor_invincibility.rect.colliderect(player.rect) and not player.invincible:
            # Ativar invencibilidade por 5 segundos
            player.activate_invincibility()
            meteor_invincibility.reset()
            if sound_point:
                sound_point.play()

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
            meteor_special.reset()
            meteor_invincibility.reset()
            try_play_music(phase_cfg.music)
            state = 'playing'

    # Renderização da tela de menu
    if state == 'menu':
        screen.blit(insertcoin_img, (0, 0))

        # Atualizar e desenhar botão INSERT COIN
        btn_insert_coin.update_hover(mouse_pos)
        btn_insert_coin.draw(screen)

        # Mensagem adicional
        txt_info = pygame.font.Font(None, 28).render("ou pressione SPACE para começar", True, WHITE)
        screen.blit(txt_info, (WIDTH//2 - txt_info.get_width()//2, HEIGHT - 40))

    # Renderização do jogo
    elif state in ['playing', 'transition', 'gameover']:
        screen.blit(PHASES[current_phase].bg, (0, 0))
        player.draw(screen)
        for m in meteors:
            m.draw(screen)
        meteor_special.draw(screen)
        meteor_invincibility.draw(screen)

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
        # Exibir imagem de game over
        screen.blit(gameover_img, (0, 0))

        # Adicionar informações finais
        big = pygame.font.Font(None, 48)
        txt_score = big.render(f"Pontuação Final: {score}", True, WHITE)
        txt_phase = big.render(f"Fase Alcançada: {current_phase}", True, WHITE)

        # Posicionar textos no centro da tela
        screen.blit(txt_score, (WIDTH//2 - txt_score.get_width()//2, HEIGHT//2 - 80))
        screen.blit(txt_phase, (WIDTH//2 - txt_phase.get_width()//2, HEIGHT//2 - 20))

        # Atualizar e desenhar botões
        btn_restart.update_hover(mouse_pos)
        btn_exit.update_hover(mouse_pos)
        btn_restart.draw(screen)
        btn_exit.draw(screen)

        # Mensagem adicional
        txt_info = pygame.font.Font(None, 28).render("ou pressione SPACE/ESC", True, WHITE)
        screen.blit(txt_info, (WIDTH//2 - txt_info.get_width()//2, HEIGHT - 30))

    pygame.display.flip()

pygame.quit()
