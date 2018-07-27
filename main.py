import random

import pygame
import time

pygame.init()

display_width = 800
display_height = 600
car_width = 73
car_height = 100
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
carImg = pygame.image.load('racecar.png')

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')


def draw_car(x, y):
    gameDisplay.blit(carImg, (x, y))


def game_loop():
    crashed = False
    x = (display_width * .45)
    y = (display_height * .8)
    x_change = 0
    score = 0
    time_elapsed = 30
    speed = 5
    obstacles = []
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        if x > display_width - car_width or x < 0:
            message_display("Game Over")
            crashed = True
        x += x_change
        speed += .001
        gameDisplay.fill(white)
        draw_car(x, y)
        draw_score(score)
        for obstacle in obstacles:
            obstacle.draw()
            obstacle.update(speed)
            if obstacle.isTouchingCar(x, y):
                message_display("Game Over")
                crashed = True
        for obstacle in obstacles:
            if obstacle.isOffscreen():
                obstacles.remove(obstacle)
                score += 1
        if time_elapsed > 50:
            obstacles.append(Obstacle(random.randrange(50,200), random.randrange(30, 100), random_color()))
            time_elapsed = 0

        pygame.display.update()
        clock.tick(60)
        time_elapsed += 1

def draw_score(score):
    small_text = pygame.font.Font('freesansbold.ttf', 25)
    text_surf, text_rect = text_objects((str)(score), small_text)
    text_rect.center = ((display_width - 80), (30))
    gameDisplay.blit(text_surf, text_rect)

def random_color():
    return (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    gameDisplay.fill(white)
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

class Obstacle:
    def __init__(self, width, height, color):
        self.x = random.randrange(0, display_width)
        self.y = 0 - height
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])

    def update(self, speed):
        self.y += speed

    def isOffscreen(self):
        if(self.y > display_height):
            return True
        return False

    def isTouchingCar(self, carX, carY):
        yCrossover = carY + car_height > self.y and carY < self.y + self.height
        xCrossover = carX + car_width > self.x and carX < self.x+ self.width
        return yCrossover and xCrossover

game_loop()
pygame.quit()
quit()