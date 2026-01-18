import pygame
import sys
import random
from game_classes import SpaceShip, Bullet, Meteor, Mission

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

class GameState:
    MENU = 0
    PLAYING = 1
    GAMEOVER = 2

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.midtop = (x, y)
    surface.blit(text_surface, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Mission Simulator - Multiplayer")
    clock = pygame.time.Clock()

    state = GameState.MENU
    mode = "SINGLE" 
    
    # Game State Objects
    ships = []
    bullets = []
    meteors = []
    mission = Mission()
    stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)] for _ in range(100)]

    def reset_game(game_mode):
        nonlocal ships, bullets, meteors, mission
        ships = []
        bullets = []
        meteors = []
        mission = Mission()
        
        # Player 1 (Arrow keys, Space to shoot)
        p1_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'fire': pygame.K_UP}
        ships.append(SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, SCREEN_WIDTH // 3, p1_controls))
        
        if game_mode == "MULTI":
            # Player 2 (A/D keys, Left Shift to shoot)
            p2_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'fire': pygame.K_w}
            ships.append(SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, 2 * SCREEN_WIDTH // 3, p2_controls))
        else:
            ships[0].rect.centerx = SCREEN_WIDTH // 2

    meteor_timer = 0

    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if state == GameState.MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        mode = "SINGLE"
                        reset_game(mode)
                        state = GameState.PLAYING
                    elif event.key == pygame.K_2:
                        mode = "MULTI"
                        reset_game(mode)
                        state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            elif state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    for ship in ships:
                        if ship.hull > 0 and event.key == ship.controls['fire']:
                            bullets.append(Bullet(ship.rect.centerx, ship.rect.top))
                                
            elif state == GameState.GAMEOVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state = GameState.MENU

        # --- Drawing & Logic ---
        screen.fill(BLACK)
        
        # Background Stars
        for star in stars:
            star[1] += 2
            if star[1] > SCREEN_HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, SCREEN_WIDTH)
            pygame.draw.circle(screen, WHITE, star, 1)

        if state == GameState.MENU:
            draw_text(screen, "SPACE MISSION", 64, SCREEN_WIDTH // 2, 100)
            draw_text(screen, "1. Single Player", 32, SCREEN_WIDTH // 2, 250)
            draw_text(screen, "2. Two Players", 32, SCREEN_WIDTH // 2, 300)
            draw_text(screen, "Q. Quit", 32, SCREEN_WIDTH // 2, 350)
            
            draw_text(screen, "P1: Arrows + Space | P2: A/D + L-Shift", 24, SCREEN_WIDTH // 2, 500)

        elif state == GameState.PLAYING:
            active_ships = [s for s in ships if s.hull > 0]
            if not active_ships:
                state = GameState.GAMEOVER

            for ship in ships:
                ship.update(keys)
                ship.draw(screen)

            # Update Bullets
            for bullet in bullets[:]:
                bullet.update()
                bullet.draw(screen)
                if bullet.rect.bottom < 0:
                    bullets.remove(bullet)

            # Update Meteors
            meteor_timer += 1
            if meteor_timer > 30:
                meteors.append(Meteor(SCREEN_WIDTH))
                meteor_timer = 0
            
            for meteor in meteors[:]:
                meteor.update()
                meteor.draw(screen)
                if meteor.rect.top > SCREEN_HEIGHT:
                    meteors.remove(meteor)
                
                # Collisions
                for ship in active_ships:
                    if meteor.rect.colliderect(ship.rect):
                        ship.hull -= 20
                        if meteor in meteors: meteors.remove(meteor)
                
                for bullet in bullets[:]:
                    if meteor in meteors and bullet.rect.colliderect(meteor.rect):
                        bullets.remove(bullet)
                        meteors.remove(meteor)
                        mission.score += 10
                        break

            # UI HUD
            draw_text(screen, f"Score: {mission.score}", 30, SCREEN_WIDTH // 2, 10)
            
            # P1 Stats (Left)
            draw_text(screen, f"P1 Hull: {int(ships[0].hull)}%", 20, 70, 20)
            draw_text(screen, f"P1 Fuel: {int(ships[0].fuel)}%", 20, 70, 40, ORANGE)
            
            # P2 Stats (Right)
            if mode == "MULTI" and len(ships) > 1:
                draw_text(screen, f"P2 Hull: {int(ships[1].hull)}%", 20, SCREEN_WIDTH - 70, 20)
                draw_text(screen, f"P2 Fuel: {int(ships[1].fuel)}%", 20, SCREEN_WIDTH - 70, 40, ORANGE)

        elif state == GameState.GAMEOVER:
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, 200)
            draw_text(screen, f"Score: {mission.score}", 32, SCREEN_WIDTH // 2, 300)
            draw_text(screen, "Press R to Restart", 24, SCREEN_WIDTH // 2, 400)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
