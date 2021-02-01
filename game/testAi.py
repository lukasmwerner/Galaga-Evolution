from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from characters import *
import NeuralNet as nn
import random

pygame.init()

def nearestEnemy(enemies, player):
    closest = enemies[0]
    for i in range(1, len(enemies)-1):
        current = enemies[i]
        if current.y > closest.y and not current.y > player.y:
            closest = current
    return closest

def run(player):

    displayWidth = displayHeight = 500

    screen = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption("Galaga Evolution Testing...")

    running = True
    clock = pygame.time.Clock()

    enemies = [
        Enemy( (0, 10), 'a' ),
        Enemy( (100, 20), 'a' ),
        Enemy( (200, 10), 'b' ),
        Enemy( (300, 20), 'a' ),
        Enemy( (400, 10), 'a' )
]
    #enemies = [Enemy((10,10))]

    black = (0,0,0)
    white = (255,255,255)

    score = 0
    level = 0


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if len(enemies) == 0:
            level +=1
            enemies = [Enemy( (x, random.choice(range(10,50)) ), 'a') for x in range(0,500, 30)]
            enemies[0] = Enemy( (20,0), 'b')
            for i in range(0, level):
                enemies.append(Enemy( (random.choice(range(0,500-32)), random.choice(range(10,50))), 'b'))
            score += 200
            
        screen.fill(black)
        player.update(nearestEnemy(enemies, player))
        player.show(screen)
        for enemy in enemies:
            if enemy.x in range(player.x-16, player.x+32):
                if enemy.y in range(player.y, player.y+32):
                    running = False
            for proj in player.projectiles:
                xposes = [x for x in range(enemy.x, enemy.x+34)]
                yposes = [x for x in range(enemy.y, enemy.y+34)]
                if proj.x in xposes:
                    if proj.y in yposes:
                        try:
                            enemies.remove(enemy)
                            score += 20
                        except Exception as e:
                            pass
            enemy.show(screen)
            enemy.update(player)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(2000)

    pygame.quit()
    return {'score': score, 'player': player}

if __name__ == "__main__":
    import sys
    import pickle
    args = sys.argv
    with open(args[1], 'rb') as f:
        player = pickle.load(f)
    run(player)