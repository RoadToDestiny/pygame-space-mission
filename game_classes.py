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
        self.controls = controls 
        self.color = color
        
        # Simulator attributes
        self.fuel = 100.0
        self.hull = 100.0
        self.current_speed = 0
        self.crew = [CrewMember("Alice", "Pilot"), CrewMember("Bob", "Engineer")]

    def update(self, keys_pressed):
        # Check fuel and hull before allowing movement
        if self.fuel > 0 and self.hull > 0:
            moved = False
            if keys_pressed[self.controls['left']] and self.rect.left > 0:
                self.rect.x -= self.speed
                self.fuel -= 0.1 # Consume fuel
                moved = True
            if keys_pressed[self.controls['right']] and self.rect.right < self.screen_width:
                self.rect.x += self.speed
                self.fuel -= 0.1 # Consume fuel
                moved = True
            
            # Ensure fuel doesn't go below 0
            if self.fuel < 0: self.fuel = 0
        
    def draw(self, surface):
        if self.hull > 0:
            pygame.draw.rect(surface, self.color, self.rect)
            # Draw Hull bar (Red)
            pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, 50 * (self.hull/100), 4))
            # Draw Fuel bar (Yellow) below hull
            pygame.draw.rect(surface, (255, 165, 0), (self.rect.x, self.rect.y - 5, 50 * (self.fuel/100), 4))

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
