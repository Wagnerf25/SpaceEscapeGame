import pygame
import random
import os
import math


pygame.init()

# ----------------------------------------------------------
# CONFIGURAÇÕES GERAIS
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape - 3 Fases")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# ----------------------------------------------------------
# ASSETS (nomes fornecidos)
# ----------------------------------------------------------
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

# Cores de fallback
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
DARK = (20, 20, 20)

# Funções utilitárias para carregar imagens e sons com fallback
def load_image(filename, fallback_color, size=None):
    if filename and os.path.exists(filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except Exception:
            pass
    surf = pygame.Surface(size or (50, 50), pygame.SRCALPHA)
    surf.fill(fallback_color)
    return surf


def load_sound(filename):
    if filename and os.path.exists(filename):
        try:
            return pygame.mixer.Sound(filename)
        except Exception:
            return None
    return None


def try_play_music(filename, volume=0.3):
    try:
        if filename and os.path.exists(filename):
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            return True
    except Exception:
        pass
    return False

# ----------------------------------------------------------
# CARREGAMENTO INICIAL (tamanhos padrão)
# ----------------------------------------------------------
background_imgs = {
    1: load_image(ASSETS["background1"], (10, 10, 30), (WIDTH, HEIGHT)),
    2: load_image(ASSETS["background2"], (8, 8, 25), (WIDTH, HEIGHT)),
    3: load_image(ASSETS["background3"], (6, 6, 20), (WIDTH, HEIGHT))
}

player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

# ----------------------------------------------------------
# CLASSES: Player e Meteor
# ----------------------------------------------------------
class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 7
        self.lives = 3

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Meteor:
    def __init__(self, x, y, w, h, speed, behavior=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.behavior = behavior  # None, 'zigzag', 'accelerate'
        # propriedades para zigzag
        self._phase = random.uniform(0, math.pi * 2)
        self._amp = random.randint(30, 80)
        self._hz = random.uniform(0.01, 0.04)

    def update(self):
        # comportamento padrão: cai verticalmente
        if self.behavior == 'zigzag':
            self._phase += self._hz
            self.rect.x += int(math.sin(self._phase) * 3)
        elif self.behavior == 'accelerate':
            self.speed += 0.02

        self.rect.y += int(self.speed)

    def reset(self):
        self.rect.y = random.randint(-500, -40)
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        # randomizar comportamento ao reset para fases mais avançadas
        self._phase = random.uniform(0, math.pi * 2)

    def draw(self, surf):
        # desenha a imagem escalada para o tamanho do rect
        try:
            img = pygame.transform.scale(meteor_img, (self.rect.width, self.rect.height))
            surf.blit(img, self.rect)
        except Exception:
            pygame.draw.rect(surf, RED, self.rect)

# ----------------------------------------------------------
# SISTEMA DE FASES
# ----------------------------------------------------------
class PhaseConfig:
    def __init__(self, id, bg, music, meteor_count, meteor_speed, meteor_size, required_score, behaviors=None):
        self.id = id
        self.bg = bg
        self.music = music
        self.meteor_count = meteor_count
        self.meteor_speed = meteor_speed
        self.meteor_size = meteor_size
        self.required_score = required_score
        self.behaviors = behaviors or []  # lista de comportamentos que podem aparecer


PHASES = {
    1: PhaseConfig(
        id=1,
        bg=background_imgs[1],
        music=ASSETS["music1"],
        meteor_count=5,
        meteor_speed=5,
        meteor_size=(40, 40),
        required_score=30,
        behaviors=[]
    ),
    2: PhaseConfig(
        id=2,
        bg=background_imgs[2],
        music=ASSETS["music2"],
        meteor_count=7,
        meteor_speed=7,
        meteor_size=(50, 50),
        required_score=70,
        behaviors=['accelerate']
    ),
    3: PhaseConfig(
        id=3,
        bg=background_imgs[3],
        music=ASSETS["music3"],
        meteor_count=10,
        meteor_speed=9,
        meteor_size=(60, 60),
        required_score=None,  # é a fase final
        behaviors=['accelerate', 'zigzag']
    )
}

# ----------------------------------------------------------
# FUNÇÃO PARA CRIAR LISTA DE METEOROS PARA A FASE
# ----------------------------------------------------------

def create_meteors_for_phase(phase_cfg):
    meteors = []
    for _ in range(phase_cfg.meteor_count):
        w, h = phase_cfg.meteor_size
        x = random.randint(0, WIDTH - w)
        y = random.randint(-500, -40)
        behavior = None
        if phase_cfg.behaviors:
            # aleatoriza comportamento dependendo da fase
            if random.random() < 0.35:
                behavior = random.choice(phase_cfg.behaviors)
        meteor = Meteor(x, y, w, h, phase_cfg.meteor_speed, behavior)
        meteors.append(meteor)
    return meteors

# ----------------------------------------------------------
# INICIALIZAÇÃO DO JOGO
# ----------------------------------------------------------
player = Player()
current_phase = 1
score = 0
state = 'playing'  # 'playing', 'transition', 'gameover'

# carrega primeira fase
phase_cfg = PHASES[current_phase]
meteors = create_meteors_for_phase(phase_cfg)
try_play_music(phase_cfg.music)

# pequeno timer para transições
transition_timer = 0
transition_duration = 90  # frames

# ----------------------------------------------------------
# LOOP PRINCIPAL
# ----------------------------------------------------------
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and state == 'gameover':
            running = False

    # lógica por estado
    if state == 'playing':
        # atualiza jogador
        player.update(keys)

        # atualiza meteoros
        for m in meteors:
            m.update()

            # saiu da tela
            if m.rect.y > HEIGHT:
                m.reset()
                score += 1
                if sound_point:
                    try:
                        sound_point.play()
                    except Exception:
                        pass

            # colisão
            if m.rect.colliderect(player.rect):
                # reduz vida e reseta meteoro
                player.lives -= 1
                m.reset()
                if sound_hit:
                    try:
                        sound_hit.play()
                    except Exception:
                        pass

                if player.lives <= 0:
                    state = 'gameover'
                    pygame.mixer.music.stop()

        # checa subida de fase
        next_phase = current_phase + 1
        if current_phase in PHASES and PHASES[current_phase].required_score:
            if score >= PHASES[current_phase].required_score:
                # iniciar transição
                state = 'transition'
                transition_timer = 0

    elif state == 'transition':
        # toca uma pequena animação/efeito de transição (poderia ser expandida)
        transition_timer += 1
        if transition_timer == 1:
            pygame.mixer.music.fadeout(500)

        if transition_timer >= transition_duration:
            # avança para próxima fase
            current_phase += 1
            if current_phase > max(PHASES.keys()):
                # se passou da última fase — volta à final
                current_phase = max(PHASES.keys())
            phase_cfg = PHASES[current_phase]
            meteors = create_meteors_for_phase(phase_cfg)
            try_play_music(phase_cfg.music)
            state = 'playing'

    # --- Desenho ---
    # desenha fundo da fase atual
    screen.blit(PHASES[current_phase].bg, (0, 0))

    # desenha jogador e meteoros
    player.draw(screen)
    for m in meteors:
        m.draw(screen)

    # HUD — pontuação / vida / fase
    hud = font.render(f"Pontos: {score}   Vidas: {player.lives}   Fase: {current_phase}", True, WHITE)
    screen.blit(hud, (10, 10))

    # se estiver em transição, mostra texto de "Fase X"
    if state == 'transition':
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        big = pygame.font.Font(None, 72)
        txt = big.render(f"Fase {current_phase + 1}", True, WHITE)
        txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(txt, txt_rect)

    pygame.display.flip()

# ----------------------------------------------------------
# TELA DE FIM DE JOGO
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill(DARK)
end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)
final_score = font.render(f"Pontuação final: {score}", True, WHITE)
hint = font.render("Obrigado por jogar Space Escape - pressione qualquer tecla.", True, WHITE)
screen.blit(end_text, (80, 240))
screen.blit(final_score, (300, 290))
screen.blit(hint, (80, 330))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
