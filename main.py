import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load("funky.mp3")
pygame.mixer.music.set_volume(0.018)
intro_sound = pygame.mixer.Sound('mixkit-sweet-kitty-meow-93.wav')
intro_sound.set_volume(0.1)
level_sound = pygame.mixer.Sound('level_up.mp3')
level_sound.set_volume(0.05)
final_boss = pygame.mixer.Sound('boss_trimmed.mp3')
final_boss.set_volume(0.10)
game_over_sound = pygame.mixer.Sound('mixkit-cartoon-little-cat-meow-91.wav')
game_over_sound.set_volume(0.1)
win_sound = pygame.mixer.Sound('magpie_purr-37132.mp3')
win_sound.set_volume(1)


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kitty Dash")

BG = pygame.transform.scale(pygame.image.load('outer_space.jpeg'), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load('city.jpg'), (WIDTH, HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load('pyramid.jpg'), (WIDTH, HEIGHT))
BG4 = pygame.transform.scale(pygame.image.load('rave2jpg.jpg'), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont('arial', 30)




def draw(player, elapsed_time, stars, level1_triggered):
    if elapsed_time  < 15:
        WIN.blit(BG, (0, 0))
    elif elapsed_time  < 30:
        WIN.blit(BG3, (0, 0))
    elif elapsed_time  < 45:
        WIN.blit(BG2, (0, 0))
    else:
        WIN.blit(BG4, (0, 0))


    if level1_triggered is False and elapsed_time > 15 and elapsed_time < 16:
        pygame.mixer.Sound.play(level_sound)
        level1_triggered = True
    
    if level1_triggered is False and elapsed_time > 30 and elapsed_time < 31:
        pygame.mixer.Sound.play(level_sound)
        level1_triggered = True

    if level1_triggered is False and elapsed_time > 45 and elapsed_time < 46:
        pygame.mixer.Sound.play(level_sound)
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(final_boss)
        level1_triggered = True




    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'plum')
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, (49, 50, 51), player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()



def main():
    run = True

    pygame.mixer.music.play(1)

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False
    level1_triggered = False

    
    pygame.mixer.Sound.play(intro_sound)
    while run:

        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP]:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN]:
            player.y += PLAYER_VEL
        if keys[pygame.K_SPACE]:
            pygame.mixer.Sound.play(intro_sound)




        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break


        if hit:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(game_over_sound)
            lost_text = FONT.render("GAME OVER!", 1, 'red')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)

            break
                
                    

        if elapsed_time > 60:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(win_sound)
            win_text = FONT.render("WINNER!", 1, 'green')
            WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break


        draw(player, elapsed_time, stars, level1_triggered)

    pygame.quit()




if __name__ == "__main__":
    main()