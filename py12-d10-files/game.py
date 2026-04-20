import pygame
import random

from PIL import Image, ImageDraw, ImageFont

def load_image(path):
  pil_img = Image.open(path).convert("RGBA")
  return pygame.image.fromstring(pil_img.tobytes(), pil_img.size, "RGBA")

def render_text(text, size, color, bold=False):
  font = ImageFont.load_default(size)
  bbox = font.getbbox(text)
  w = bbox[2] - bbox[0] + 4
  h = bbox[3] - bbox[1] + 4
  img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)
  draw.text((-bbox[0] + 2, -bbox[1] + 2), text, fill=color, font=font)
  return pygame.image.fromstring(img.tobytes(), img.size, "RGBA")


class Entity:
  def __init__(self, state, asset, x, y, w, h, frame_delay=None):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.asset = asset
    self.state = state
    margin_x = int(w * 0.3)
    margin_y = int(h * 0.3)
    self.hitbox_margin_x = margin_x
    self.hitbox_margin_y = margin_y
    self.rect = pygame.Rect(
      x + margin_x, y + margin_y,
      w - 2 * margin_x, h - 2 * margin_y
    )
    self.frame_time = 0.0
    self.frame_delay = frame_delay
    self.is_anim = type(asset) is list

  def update_rect(self):
    self.rect.x = self.x + self.hitbox_margin_x
    self.rect.y = self.y + self.hitbox_margin_y

  def draw(self, dst, dt):
    if self.is_anim:
      self.frame_time += dt
      frame = (
         int(self.frame_time / self.frame_delay) %
         len(self.asset)
      )
      dst.blit(self.asset[frame], (self.x, self.y))
    else:
      dst.blit(self.asset, (self.x, self.y))

  def logic(self):
    return True

class Mob(Entity):
  def __init__(
      self, state, asset, x, y, w, h, vx, vy,
      frame_delay=None
    ):
    super().__init__(
      state, asset, x, y, w, h, frame_delay=frame_delay
    )
    self.vx = vx
    self.vy = vy

  def logic(self, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt

    if self.y > self.state.screen.get_height():
      return False

    self.update_rect()
    return True

class Bullet:
  def __init__(self, x, y, asset):
    self.x = x
    self.y = y
    self.speed = -600
    self.asset = asset
    self.w = asset.get_width()
    self.h = asset.get_height()
    self.rect = pygame.Rect(x, y, self.w, self.h)

  def logic(self, dt):
    self.y += self.speed * dt
    if self.y < -self.h:
      return False
    self.rect.x = self.x
    self.rect.y = self.y
    return True

  def draw(self, dst):
    dst.blit(self.asset, (self.x, self.y))

class Player(Entity):
  def __init__(self, state, asset, x, y, w, h):
    super().__init__(state, asset, x, y, w, h)
    self.move_speed = 800

  def move_left(self, dt):
    self.x -= self.move_speed * dt
    if self.x < 0:
      self.x = 0

  def move_right(self, dt):
    self.x += self.move_speed * dt
    screen_edge = (
      self.state.screen.get_width() - self.asset.get_width()
    )
    if self.x >= screen_edge:
      self.x = screen_edge - 1

  def logic(self):
    self.update_rect()
    return True

class GameState:
  def __init__(self, assets, screen):
    self.assets = assets
    self.screen = screen
    self._init_state()

  def _init_state(self):
    self.player = Player(self, self.assets.spaceship, 600, 600, 65, 92)
    self.asteroids = []
    self.bullets = []
    self.time_to_add_asteroid = 1.5
    self.time_left_to_add_asteroid = self.time_to_add_asteroid
    self.max_asteroid_count = 500
    self.game_over = False
    self.score = 0
    self.elapsed_time = 0.0
    self.bg_offset = 0.0
    self.difficulty_level = 0
    self.shoot_cooldown = 0.0

  def _update_difficulty(self):
    level = int(self.elapsed_time // 10)
    if level != self.difficulty_level:
      self.difficulty_level = level
      self.time_to_add_asteroid = max(0.3, 1.5 - level * 0.12)

  def _get_spawn_params(self):
    level = self.difficulty_level
    if level < 2:
      weights = (0.7, 0.3, 0.0)
    elif level < 5:
      weights = (0.4, 0.4, 0.2)
    else:
      weights = (0.2, 0.4, 0.4)
    min_speed = 50 + level * 20
    max_speed = 250 + level * 30
    return min_speed, max_speed, weights

  def _spawn_asteroid(self):
    min_speed, max_speed, weights = self._get_spawn_params()

    roll = random.random()
    if roll < weights[0]:
      size = "small"
    elif roll < weights[0] + weights[1]:
      size = "medium"
    else:
      size = "large"

    if size == "small":
      asset = random.choice(self.assets.asteroid_small)
      w, h = 35, 35
    elif size == "medium":
      asset = random.choice(self.assets.asteroid_medium)
      w, h = 70, 70
    else:
      asset = random.choice(self.assets.asteroid_large)
      w, h = 120, 120

    self.asteroids.append(Mob(
      self, asset,
      random.randint(-150, self.screen.get_width() + 150),
      -max(w, h),
      w, h,
      random.randint(-100, 100),
      random.randint(min_speed, max_speed),
      frame_delay=0.05 + random.random() * 0.30
    ))

  def _shoot(self):
    px = self.player.x + self.player.w // 2 - self.assets.bullet.get_width() // 2
    py = self.player.y
    self.bullets.append(Bullet(px, py, self.assets.bullet))
    self.shoot_cooldown = 0.2

  def logic(self, dt):
    shoot_pressed = False
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return False
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        shoot_pressed = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      return False

    if self.game_over:
      if shoot_pressed:
        self._init_state()
      return True

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      self.player.move_left(dt)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.player.move_right(dt)

    self.shoot_cooldown -= dt
    if shoot_pressed and self.shoot_cooldown <= 0:
      self._shoot()

    self.player.logic()

    self.elapsed_time += dt
    self.score = int(self.elapsed_time)
    self._update_difficulty()

    self.bg_offset = (self.bg_offset + 30 * dt) % self.assets.bg.get_height()

    if len(self.asteroids) < self.max_asteroid_count:
      self.time_left_to_add_asteroid -= dt
      if self.time_left_to_add_asteroid <= 0:
        self._spawn_asteroid()
        self.time_left_to_add_asteroid = self.time_to_add_asteroid

    self.asteroids = [
      mob for mob in self.asteroids if mob.logic(dt)
    ]

    self.bullets = [
      b for b in self.bullets if b.logic(dt)
    ]

    # Bullet-asteroid collisions
    hit_asteroids = set()
    hit_bullets = set()
    for bi, bullet in enumerate(self.bullets):
      for ai, asteroid in enumerate(self.asteroids):
        if ai not in hit_asteroids and bullet.rect.colliderect(asteroid.rect):
          hit_asteroids.add(ai)
          hit_bullets.add(bi)
          if asteroid.w <= 35:
            self.score += 5
          elif asteroid.w <= 70:
            self.score += 10
          else:
            self.score += 20
    if hit_asteroids:
      self.asteroids = [a for i, a in enumerate(self.asteroids) if i not in hit_asteroids]
      self.bullets = [b for i, b in enumerate(self.bullets) if i not in hit_bullets]

    # Player-asteroid collision
    hit_list = self.player.rect.collidelistall(self.asteroids)
    if hit_list:
      self.game_over = True

    return True

  def draw(self, dt):
    self._draw_scrolling_bg()
    self.player.draw(self.screen, dt)

    for mob in self.asteroids:
      mob.draw(self.screen, dt)

    for bullet in self.bullets:
      bullet.draw(self.screen)

    self._draw_score()

    if self.game_over:
      self._draw_game_over()

  def _draw_scrolling_bg(self):
    bg = self.assets.bg
    y = int(self.bg_offset)
    self.screen.blit(bg, (0, y - bg.get_height()))
    self.screen.blit(bg, (0, y))

  def _draw_score(self):
    text = render_text(f"Score: {self.score}", self.assets.font_size, (255, 255, 255))
    self.screen.blit(text, (10, 10))

  def _draw_game_over(self):
    overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    self.screen.blit(overlay, (0, 0))

    go_text = render_text("GAME OVER", self.assets.font_big_size, (255, 50, 50))
    score_text = render_text(f"Score: {self.score}", self.assets.font_size, (255, 255, 255))
    restart_text = render_text("Press SPACE to play again", self.assets.font_size, (200, 200, 200))
    esc_text = render_text("Press ESC to quit", self.assets.font_size, (150, 150, 150))

    cx = self.screen.get_width() // 2
    cy = self.screen.get_height() // 2

    self.screen.blit(go_text, (cx - go_text.get_width() // 2, cy - 80))
    self.screen.blit(score_text, (cx - score_text.get_width() // 2, cy - 10))
    self.screen.blit(restart_text, (cx - restart_text.get_width() // 2, cy + 40))
    self.screen.blit(esc_text, (cx - esc_text.get_width() // 2, cy + 80))

class Assets:
  def __init__(self):
    self.bg = load_image("art/bg5.jpg")
    self.spaceship = load_image("art/spaceship.png")

    self.asteroid_medium = self._load_variants("medium", ["a1", "a3"])
    self.asteroid_small = self._load_variants(
      "small", ["a1", "a3", "a4", "b1", "b3", "b4"]
    )
    self.asteroid_large = self._load_variants(
      "large", ["a1", "a3", "b1", "b3", "c1", "c3", "c4"]
    )

    self.bullet = pygame.Surface((4, 14), pygame.SRCALPHA)
    self.bullet.fill((0, 255, 255))

    self.font_size = 28
    self.font_big_size = 64

  def _load_variants(self, size, types):
    variants = []
    for t in types:
      frames = [
        load_image(f"art/{size}/{t}{i:04}.png")
        for i in range(16)
      ]
      variants.append(frames)
    return variants


def main():
  pygame.init()
  screen = pygame.display.set_mode((1280, 720))
  pygame.display.set_caption("Asteroid Dodge")
  assets = Assets()

  clock = pygame.time.Clock()

  state = GameState(assets, screen)
  dt = 0
  while True:
    if not state.logic(dt):
      break

    state.draw(dt)
    pygame.display.flip()
    dt = clock.tick(60) / 1000

  pygame.quit()

if __name__ == "__main__":
  main()
