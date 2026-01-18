import pygame
import random

class CrewMember:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.health = 100
        self.skills = {"piloting": 10, "engineering": 10}

class SpaceShip:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 255, 0))  # Green ship
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5
        
        # Simulator attributes from requirements
        self.fuel = 100.0
        self.hull = 100.0
        self.current_speed = 0
        self.crew = [CrewMember("Alice", "Pilot"), CrewMember("Bob", "Engineer")]

    def update(self, moving_left, moving_right):
        if self.fuel > 0:
            if moving_left and self.rect.left > 0:
                self.rect.x -= self.speed
                self.fuel -= 0.05
            if moving_right and self.rect.right < self.screen_width:
                self.rect.x += self.speed
                self.fuel -= 0.05
        
    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
        # Draw basic HUD bar for hull/fuel above ship
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, 50 * (self.hull/100), 5))

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -7

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)

class Meteor:
    def __init__(self, screen_width):
        self.image = pygame.Surface((30, 30))
        self.image.fill((139, 69, 19)) # Brown
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 30)
        self.rect.y = -30
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (139, 69, 19), self.rect)

class Mission:
    def __init__(self):
        self.goals = "Survive and destroy asteroids"
        self.status = "Active"
        self.score = 0
