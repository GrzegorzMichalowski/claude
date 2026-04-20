import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

"""
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
"""

line_pos = [
  pygame.Vector2(
    random.randint(0, screen.get_width() - 1),
    random.randint(0, screen.get_height() - 1)
  ),
  pygame.Vector2(
    random.randint(0, screen.get_width() - 1),
    random.randint(0, screen.get_height() - 1)
  )
]
line_mov = [
  pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])),
  pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
]


SPEED = 3
it = 0

def clamp(a, v, b):
  if v < a:
    return a
  if v > b:
    return b
  return v


while running:
  it += 0.01
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  line_pos[0] += line_mov[0] * SPEED
  line_pos[1] += line_mov[1] * SPEED

  for i in range(2):
    if line_pos[i].x < 0:
      line_pos[i].x = 0
      line_mov[i].x = 1
    if line_pos[i].x >= screen.get_width():
      line_pos[i].x = screen.get_width() - 1
      line_mov[i].x = -1
    if line_pos[i].y < 0:
      line_pos[i].y = 0
      line_mov[i].y = 1
    if line_pos[i].y >= screen.get_height():
      line_pos[i].y = screen.get_height() - 1
      line_mov[i].y = -1

  x = clamp(0, int(127 + math.sin(it) * 100), 255)
  color = ( x, x, x )
  # clamp(0, int(127 + math.sin(it * 0.7 + 1.0) * 100), 255),
  # clamp(0, int(127 + math.sin(it * 0.9 + 1.2) * 100), 255),

  pygame.draw.line(screen, color, line_pos[0], line_pos[1], width=2)


  """
  screen.fill("purple")
  pygame.draw.circle(screen, "red", player_pos, 40)

  keys = pygame.key.get_pressed()
  if keys[pygame.K_w]:
    player_pos.y -= 300 * dt
  if keys[pygame.K_s]:
    player_pos.y += 300 * dt
  if keys[pygame.K_a]:
    player_pos.x -= 300 * dt
  if keys[pygame.K_d]:
    player_pos.x += 300 * dt
  """


  pygame.display.flip()

  dt = clock.tick(60) / 1000

pygame.quit()
