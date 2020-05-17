import pygame
import random
import numpy as np

pygame.font.init()
font = pygame.font.SysFont('Arial', 10)

CONFIDENCE = 0.7

class Enemy(object):
    def __init__(self, home, type=random.choice(['a', 'b'])):
        self.type = type
        if self.type == 'a':
            self.image = pygame.image.load("enemyA.png")
        else: 
            self.image = pygame.image.load("enemyB.png")
        self.image = pygame.transform.scale(self.image, (32,32))
        self.size = 32
        self.home = home
        self.x = home[0]
        self.y = home[1]
        self.mode = 0
        self.step = 1
        self.t = 0

    def show(self, screen: pygame.display, debug=False):
        screen.blit(self.image, (self.x, self.y))
        if debug:
            screen.blit(font.render(self.__str__(), False, (255,255,255)), (self.x+32, self.y))

    def move(self, target):
        if self.type == 'a':
            if self.y < target[1]:
                self.y += self.step
            elif self.y > target[1]:
                self.y -= self.step
            else:
                pass

            if self.x > target[0]:
                self.x -= self.step
            elif self.x < target[0]:
                self.x += self.step
        else:
            if self.t % 4 == 0:
                if not self.y in range(target[1], target[1]+55):
                    self.y += self.step
                else:
                    if self.x > target[0]:
                        self.x -= self.step
                    elif self.x < target[0]:
                        self.x += self.step


    def update(self, player):
        self.target = (player.x, player.y)
        if self.mode == 0:
            if self.t % 40 == 0:
                self.randomModeSwitch()
            if self.x == self.home[0] and self.y == self.home[1]:
                self.mode = 1
            else:
                self.move(self.home)
        elif self.mode == 1:
            if self.x == self.target[0] and self.y == self.target[1]:
                self.mode = 0
            else:
                self.move(self.target)
        self.t +=1

    def randomModeSwitch(self):
        if random.choice([0,1]) == 1:
            self.mode = 0

    def __str__(self):
        return f"Enemy < X:{self.x} Y:{self.y} Mode:{self.mode}>"

class Player(object):
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (32,32))
        self.size = 32
        self.x = 100
        self.y = 350
        self.projectiles = []

    def move(self, xAmt, yAmt):
        newX = self.x + xAmt
        newY = self.y + yAmt
        self.x = max(0, min(newX, 500-32)) # you handle where to store screen width
        self.y = max(0, min(newY, 500-32))


    def show(self, screen: pygame.display):
        screen.blit(self.image, (self.x, self.y))
        for projectile in self.projectiles:
            projectile.show(screen)

    def shoot(self):
        self.projectiles.append(
            Projectile(self.x+16, self.y, 3)
        )

    def update(self):
        for projectile in self.projectiles:
            if projectile.x < 0 or projectile.y < 0:
                self.projectiles.remove(projectile)
            else:
                projectile.update()
pyrImage = pygame.transform.scale(pygame.image.load('player.png'), (32,32))

class AiPlayer(object):
    def __init__(self, brain):
        self.brain = brain
        self.size = 32
        self.x = 100
        self.y = 400
        self.projectiles = []
        self.actions = np.asarray([0,0,0], dtype=np.float32)
        self.t = 0

    def move(self, xAmt, yAmt):
        newX = self.x + xAmt
        newY = self.y + yAmt
        self.x = max(0, min(newX, 500-32)) # you handle where to store screen width
        self.y = max(0, min(newY, 500-32))

    def show(self, screen: pygame.display):
        screen.blit(pyrImage, (self.x, self.y))
        #screen.blit(font.render(self.actions.__str__(), False, (255,255,255)), (0, 0))
        for projectile in self.projectiles:
            projectile.show(screen)

    def shoot(self):
        if self.t % 10 == 0:
            self.projectiles.append(
                Projectile(self.x+16, self.y-10, 3)
            )

    def update(self, nearestEnemy):
        for projectile in self.projectiles:
            if projectile.x < 0 or projectile.y < 0:
                self.projectiles.remove(projectile)
            else:
                projectile.update()
        enemyXnorm = nearestEnemy.x / 500
        enemyYnorm = nearestEnemy.y / 500
        currentXnorm = self.x / 500
        self.actions = self.brain.predict(nearestEnemyX= enemyXnorm, nearestEnemyY=enemyYnorm, currentX=currentXnorm)
        if self.actions[0] >= CONFIDENCE:
            self.shoot()
        if self.actions[1] >= CONFIDENCE:
            self.move(-1, 0)
        elif self.actions[2] >= CONFIDENCE:
            self.move(1,0)
        self.t += 1

    def mutate(self, amt):
        self.brain.mutate(amt)


class Projectile(object):
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.velocity = v

    def show(self, screen, debug=False):
        rect = pygame.Rect(self.x, self.y, 5, 10)
        pygame.draw.rect(screen, (255,255,255), rect)
        if debug:
            screen.blit(font.render(self.__str__(), False, (255,255,255)), (self.x, self.y))

    def update(self):
        self.y -= self.velocity

    def __str__(self):
        return f"Projectile <X:{self.x} Y:{self.y}>"