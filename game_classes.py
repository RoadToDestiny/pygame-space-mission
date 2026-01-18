import pygame
import random

class CrewMember:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.health = 100
        self.skills = {"piloting": 10, "engineering": 10}

class SpaceShip:
    def __init__(self, screen_width, screen_height, color, start_x, controls):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((50, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = start_x
        self.rect.bottom = screen_height - 10
        self.speed = 5
        self.controls = controls # Expected dict: {'left': K_LEFT, 'right': K_RIGHT, 'fire': K_SPACE}
        self.color = color
        
        # Simulator attributes
        self.fuel = 100.0
        self.hull = 100.0
        self.current_speed = 0
        self.crew = [CrewMember("Alice", "Pilot"), CrewMember("Bob", "Engineer")]

    def update(self, keys_pressed):
        if self.fuel > 0 and self.hull > 0:
            if keys_pressed[self.controls['left']] and self.rect.left > 0:
                self.rect.x -= self.speed
                self.fuel -= 0.05
            if keys_pressed[self.controls['right']] and self.rect.right < self.screen_width:
                self.rect.x += self.speed
                self.fuel -= 0.05
        
    def draw(self, surface):
        if self.hull > 0:
            pygame.draw.rect(surface, self.color, self.rect)
            # Draw HUD bar for hull above ship
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
