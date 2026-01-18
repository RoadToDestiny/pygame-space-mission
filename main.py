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
BROWN = (139, 69, 19)

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

def load_images():
    try:
        # Load and scale images with INCREASED sizes
        # 1.png -> Player 1 (was 50x40, now 80x60)
        img_p1 = pygame.image.load("1.png")
        img_p1 = pygame.transform.scale(img_p1, (80, 60))
        
        # 2.png -> Player 2 (was 50x40, now 80x60)
        img_p2 = pygame.image.load("2.png")
        img_p2 = pygame.transform.scale(img_p2, (80, 60))
        
        # meteorit.png -> Meteor (was 30x30, now 60x60)
        img_meteor = pygame.image.load("meteorit.png")
        img_meteor = pygame.transform.scale(img_meteor, (60, 60))
        
        return img_p1, img_p2, img_meteor
    except pygame.error as e:
        print(f"Warning: Could not load images ({e}). Using shapes instead.")
        # Fallback surfaces
        s1 = pygame.Surface((80, 60)); s1.fill(GREEN)
        s2 = pygame.Surface((80, 60)); s2.fill(BLUE)
        sm = pygame.Surface((60, 60)); sm.fill(BROWN)
        return s1, s2, sm

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Mission Simulator - Multiplayer")
    clock = pygame.time.Clock()

    # Load resources
    img_p1, img_p2, img_meteor_base = load_images()

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
        
        # Player 1 (A/D movement, W to shoot)
        p1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'fire': pygame.K_w}
        ships.append(SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT, img_p1, SCREEN_WIDTH // 3, p1_controls))
        
        if game_mode == "MULTI":
            # Player 2 (Arrows movement, UP Arrow to shoot)
            p2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'fire': pygame.K_UP}
            ships.append(SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT, img_p2, 2 * SCREEN_WIDTH // 3, p2_controls))
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
                    if event.key == pygame.K_ESCAPE:
                        state = GameState.MENU
                    
                    for ship in ships:
                        if ship.hull > 0 and event.key == ship.controls['fire']:
                            # DUAL CANNONS: Fire two bullets from the sides
                            # Left cannon (offset +15 from left edge)
                            bullets.append(Bullet(ship.rect.left + 15, ship.rect.top + 20, ship))
                            # Right cannon (offset -15 from right edge)
                            bullets.append(Bullet(ship.rect.right - 15, ship.rect.top + 20, ship))
                                
            elif state == GameState.GAMEOVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state = GameState.MENU

        # --- Drawing & Logic ---
        screen.fill(BLACK)
        
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
            draw_text(screen, "P1: A/D + W | P2: Arrows + UP", 24, SCREEN_WIDTH // 2, 500)

        elif state == GameState.PLAYING:
            active_ships = [s for s in ships if s.hull > 0]
            if not active_ships:
                state = GameState.GAMEOVER

            for ship in ships:
                ship.update(keys)
                ship.draw(screen)

            for bullet in bullets[:]:
                bullet.update()
                bullet.draw(screen)
                if bullet.rect.bottom < 0:
                    bullets.remove(bullet)

            meteor_timer += 1
            if meteor_timer > 30:
                meteors.append(Meteor(SCREEN_WIDTH, img_meteor_base)) # Pass image
                meteor_timer = 0
            
            for meteor in meteors[:]:
                meteor.update()
                meteor.draw(screen)
                if meteor.rect.top > SCREEN_HEIGHT:
                    meteors.remove(meteor)
                
                for ship in active_ships:
                    if meteor.rect.colliderect(ship.rect):
                        ship.hull -= 20
                        if meteor in meteors: meteors.remove(meteor)
                
                for bullet in bullets[:]:
                    if meteor in meteors and bullet.rect.colliderect(meteor.rect):
                        bullets.remove(bullet)
                        meteors.remove(meteor)
                        mission.score += 10
                        if bullet.owner and bullet.owner in ships:
                            bullet.owner.fuel += 15
                            if bullet.owner.fuel > 100:
                                bullet.owner.fuel = 100
                        break

            draw_text(screen, f"Score: {mission.score}", 30, SCREEN_WIDTH // 2, 10)
            draw_text(screen, "ESC: Menu", 20, SCREEN_WIDTH // 2, 40)
            draw_text(screen, f"P1 Hull: {int(ships[0].hull)}%", 20, 70, 20)
            draw_text(screen, f"P1 Fuel: {int(ships[0].fuel)}%", 20, 70, 40, ORANGE)
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
