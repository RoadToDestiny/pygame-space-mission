import pygame
import random

class CrewMember:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.health = 100
        self.skills = {"piloting": 10, "engineering": 10}

class SpaceShip:
    def __init__(self, screen_width, screen_height, image_surface, start_x, controls, label):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = image_surface
        self.rect = self.image.get_rect()
        self.rect.centerx = start_x
        self.rect.bottom = screen_height - 30 # Moved up slightly for label space
        self.speed = 5
        self.controls = controls 
        self.label = label
        self.font = pygame.font.Font(None, 24)
        
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
                self.fuel -= 0.1
                moved = True
            if keys_pressed[self.controls['right']] and self.rect.right < self.screen_width:
                self.rect.x += self.speed
                self.fuel -= 0.1
                moved = True
            
            # Ensure fuel doesn't go below 0
            if self.fuel < 0: self.fuel = 0
        
    def draw(self, surface):
        if self.hull > 0:
            surface.blit(self.image, self.rect)
            
            # Bar configuration
            bar_max_width = 80 # Match the ship width (80px)
            bar_height = 5
            
            # Calculate centered X position for bars
            # self.rect.centerx is the center of the ship
            # Start drawing from center - half_width
            bar_x = self.rect.centerx - (bar_max_width // 2)
            
            # Draw Hull bar (Red) - Top bar
            pygame.draw.rect(surface, (255, 0, 0), (bar_x, self.rect.y - 15, bar_max_width * (self.hull/100), bar_height))
            
            # Draw Fuel bar (Orange) - Bottom bar
            pygame.draw.rect(surface, (255, 165, 0), (bar_x, self.rect.y - 8, bar_max_width * (self.fuel/100), bar_height))
            
            # Draw Player Label (P1/P2) below the ship
            text_surf = self.font.render(self.label, True, (255, 255, 255))
            text_rect = text_surf.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 5))
            surface.blit(text_surf, text_rect)

class Bullet:
    def __init__(self, x, y, owner):
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -7
        self.owner = owner 

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)

class Meteor:
    def __init__(self, screen_width, image_surface):
        self.image = image_surface
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 60)
        self.rect.y = -60
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Mission:
    def __init__(self):
        self.goals = "Survive and destroy asteroids"
        self.status = "Active"
        self.score = 0
