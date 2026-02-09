#Alien Defence (game with spaceship defending bottom of the screen
#2/5/26
__author__ = "jackson del Gaizo"
__version__ = "2/5/26"


import pygame
from pygame import Surface
import random
import time



def addAliens(aliens):
    global speed

    while len(aliens)<5:
        temp = pygame.Rect(random.randint(0,580), -40, 20, 20)
        speed = random.randint(1, 5)
        aliens.append((temp, speed))
    #ad ten boxes


def main():
    global speed
    pygame.init()
    pygame.mixer.init()
    score_font = pygame.font.SysFont("Bold", 30)
    size = (800, 600)
    window = pygame.display.set_mode((600, 600))
    BLACK = (7, 7, 7)
    RED = (255, 0, 0)
    white = (255, 255, 255)
    pygame.display.set_caption("Alien Defence")
    sound1 = pygame.mixer.Sound("sound/laser.wav")
    sound2 = pygame.mixer.Sound("sound/boom.wav")
    sound3 = pygame.mixer.Sound("sound/explode.wav")
    sound4 = pygame.mixer.Sound("sound/big_explosion.wav")
    image: Surface = pygame.image.load("img/spaceship2.png")
    cat_image = pygame.image.load("img/alien2.png")
    clock = pygame.time.Clock()
    speed_multiplier = 1
    running = True
    elapsed = 0
    ship = image.get_rect()
    aliens = []
    addAliens(aliens)
    ship_width = ship.width
    ship.y=window.get_height()-120
    ship.x=window.get_width()//2
    lasers=[]
    big_lasers=[]
    big_laser_queue = []
    while running:

        while running:
            # 1. Handle events (keyboard input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        sound1.play()
                        laser = pygame.Rect(ship.centerx, ship.top, 500, 15)
                        lasers.append(laser)
                    if event.key == pygame.K_c:
                        sound2.play()
                        big_laser_queue.append(elapsed + 36)

            # 2. Handle continuous key presses (ship movement)
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                ship.move_ip(-5, 0)
            if key[pygame.K_RIGHT]:
                ship.move_ip(5, 0)
            ship.clamp_ip(window.get_rect())

            # 3. Move lasers
            for laser in lasers:
                laser.move_ip(0, -10)

            for fire_time in big_laser_queue[:]:
                if elapsed >= fire_time:
                    laser = pygame.Rect(ship.centerx, ship.top, 40, 20)
                    big_lasers.append(laser)
                    big_laser_queue.remove(fire_time)

            for laser in big_lasers:
                laser.move_ip(0, -20)
                print('debug', laser.x, laser.y)

            # 4. Move aliens
            for i in range(len(aliens)):
                alien_rect, alien_speed = aliens[i]
                speed_multiplier = 1 + elapsed / 7000
                alien_speed = int(alien_speed)
                alien_speed = alien_speed * speed_multiplier
                alien_rect.move_ip(0, alien_speed)
                aliens[i] = (alien_rect, alien_speed)

            # 5. Check collisions
            i = 0
            while i < len(aliens):
                alien_rect, alien_speed = aliens[i]
                hit = False
                for laser in lasers[:]:
                    if laser.colliderect(alien_rect):
                        print("hit")
                        sound3.play()
                        lasers.remove(laser)
                        aliens.pop(i)
                        hit = True
                        break
                for laser in big_lasers[:]:
                    if laser.colliderect(alien_rect):
                        print("big hit")
                        sound4.play()
                        big_lasers.remove(laser)
                        aliens.pop(i)
                        hit = True
                        break
                if not hit:
                    i += 1

            # 6. Remove lasers that are off screen
            for laser in lasers[:]:
                if laser.y < 0:
                    lasers.remove(laser)
                    print('debug laser deleted')
            for laser in big_lasers[:]:
                if laser.y < 0:
                    big_lasers.remove(laser)

            # 7. Spawn new aliens if needed
            if len(aliens) == 0:
                addAliens(aliens)

            # 8. Check if player lost
            for alien in aliens:
                alien_rect, alien_speed = alien
                if alien_rect.y > ship.top:
                    print("you lose")
                    sound4.play()
                    aliens.remove(alien)
                    running = False
                    break

            # 9. Draw everything
            window.fill(BLACK)
            window.blit(image, ship)

            for laser in lasers:
                pygame.draw.rect(window, (255, 0, 0), laser)

            for laser in big_lasers:
                pygame.draw.rect(window, (0, 255, 0), laser)

            for alien_rect, alien_speed in aliens:
                alien_angle = elapsed * 3
                rotated_alien = pygame.transform.rotate(cat_image, alien_angle)
                window.blit(rotated_alien, alien_rect)

            # 10. Display score
            score_text = score_font.render(f"Score: {elapsed}", True, white)
            score_rect = score_text.get_rect()
            score_rect.topright = (window.get_width() - 10, 10)
            window.blit(score_text, score_rect)

            # 11. Update display and tick clock
            pygame.display.flip()
            clock.tick(60)
            elapsed += 1
    running = True
    font = pygame.font.SysFont("Bold", 20)  # 20=size
    text_surface = font.render(f"Gameover, click to quit, score:{elapsed}", True, RED)

    text_rect = text_surface.get_rect(centerx=size[0] / 2, centery=size[1] / 2)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        window.fill(BLACK)
        window.blit(text_surface, text_rect)
        pygame.display.flip()


    pygame.quit()




if __name__ == "__main__":
    main()


