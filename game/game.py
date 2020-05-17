import pygame
from characters import *
import random

pygame.init()

displayWidth = displayHeight = 500

screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Galaga Evolution")

running = True
clock = pygame.time.Clock()

player = Player('player.png')

enemies = [Enemy( (x, random.choice(range(10,50)) )) for x in range(0,500, 100)]
#enemies = [Enemy((10,10))]

black = (0,0,0)
white = (255,255,255)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-3, 0)
    elif keys[pygame.K_RIGHT]:
        player.move(3, 0)
    screen.fill(black)
    player.update()
    player.show(screen)
    if len(enemies) == 0:
        enemies = [Enemy( (x, random.choice(range(10,50)) )) for x in range(0,500, 30)]
    for enemy in enemies:
        if enemy.x in range(player.x, player.x+32):
            if enemy.y in range(player.y, player.y+32):
                running = False
                

        for proj in player.projectiles:
            xposes = [x for x in range(enemy.x, enemy.x+32)]
            yposes = [x for x in range(enemy.y, enemy.y+32)]
            if proj.x in xposes:
                if proj.y in yposes:
                    try:
                        enemies.remove(enemy)
                    except Exception as e:
                        pass
        enemy.show(screen)
        enemy.update(player)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
