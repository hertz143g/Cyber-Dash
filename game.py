
import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Dash")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

player_img = pygame.image.load("assets/player.png")
enemy_img = pygame.image.load("assets/enemy.png")
bg_color = (20, 20, 20)

# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 5
        self.health = 3

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Враг
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), -40))
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

player = Player()
player_group = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()

score = 0
spawn_timer = 0
running = True

while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    win.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    spawn_timer += 1
    if spawn_timer > 30:
        enemies.add(Enemy())
        spawn_timer = 0

    player.update(keys)
    enemies.update()

    player_group.draw(win)
    enemies.draw(win)

    # Столкновения
    if pygame.sprite.spritecollideany(player, enemies):
        player.health -= 1
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                enemy.kill()
        if player.health <= 0:
            running = False

    score += 1
    text = font.render(f"Score: {score}  HP: {player.health}", True, (255, 255, 255))
    win.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
