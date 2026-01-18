import pygame
import random
import sys
from game_classes import SpaceShip, Bullet, Meteor, Mission

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Mission Simulator")
clock = pygame.time.Clock()

# Stars background (Extended functionality)
stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)] for _ in range(100)]

def draw_stars(surface):
    for star in stars:
        star[1] += 2 # speed
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)
        pygame.draw.circle(surface, WHITE, star, 1)

def main():
    mission = Mission()
    ship = SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT)
    bullets = []
    meteors = []
    
    running = True
    moving_left = False
    moving_right = False
    
    meteor_timer = 0
    
    font = pygame.font.Font(None, 36)

    while running:
        clock.tick(FPS)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(ship.rect.centerx, ship.rect.top))
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False

        # Update
        ship.update(moving_left, moving_right)
        
        # Bullets
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
        
        # Meteors
        meteor_timer += 1
        if meteor_timer > 30: # Spawn rate
            meteors.append(Meteor(SCREEN_WIDTH))
            meteor_timer = 0
            
        for meteor in meteors[:]:
            meteor.update()
            if meteor.rect.top > SCREEN_HEIGHT:
                meteors.remove(meteor)
                mission.score += 1 # Avoided
            
            # Collision Ship
            if meteor.rect.colliderect(ship.rect):
                ship.hull -= 20
                meteors.remove(meteor)
                if ship.hull <= 0:
                    print("Game Over")
                    running = False

            # Collision Bullet
            for bullet in bullets[:]:
                if bullet.rect.colliderect(meteor.rect):
                    if bullet in bullets: bullets.remove(bullet)
                    if meteor in meteors: meteors.remove(meteor)
                    mission.score += 10
                    break

        # Draw
        screen.fill(BLACK)
        draw_stars(screen) # Extended func
        
        ship.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for meteor in meteors:
            meteor.draw(screen)
            
        # UI
        score_text = font.render(f"Score: {mission.score}", True, WHITE)
        fuel_text = font.render(f"Fuel: {int(ship.fuel)}%", True, WHITE)
        hull_text = font.render(f"Hull: {int(ship.hull)}%", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(fuel_text, (10, 50))
        screen.blit(hull_text, (10, 90))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
