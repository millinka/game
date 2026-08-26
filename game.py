import pygame
import random

pygame.init()
pygame.mixer.init()

# вікно гри
screen = pygame.display.set_mode((1280, 640))

# налаштування вікна

icon = pygame.image.load("images/mushroom.png")
pygame.display.set_icon(icon)

pygame.display.set_caption("Platformer")

# фоновий звук
bg_sound = pygame.mixer.Sound("sounds/2.mp3")
bg_sound.play()


# написи
label = pygame.font.Font("fonts/pixel.ttf", 40)
label_los = label.render("Game over", False, (255, 0, 0))
label_restart = label.render("Restart game", False, (3, 252, 252))
label_restart_rect = label_restart.get_rect(topleft = (180,200))

# фон
bg = pygame.image.load("images/bg.png").convert_alpha()


# персонажі
player = pygame.image.load("images/r1.png").convert_alpha()

anim_count = 0  # 4

# списки для анімації
walk_right = [
    pygame.image.load("images/r1.png").convert_alpha(),
    pygame.image.load("images/r2.png").convert_alpha(),
    pygame.image.load("images/r3.png").convert_alpha(),
    pygame.image.load("images/r4.png").convert_alpha()
              ]

walk_left = [
    pygame.image.load("images/l1.png").convert_alpha(),
    pygame.image.load("images/l2.png").convert_alpha(),
    pygame.image.load("images/l3.png").convert_alpha(),
    pygame.image.load("images/l4.png").convert_alpha()

]


for i in range(4):
    walk_right[i] = pygame.transform.scale(walk_right[i], (80,90))
    walk_left[i] = pygame.transform.scale(walk_left[i], (80,90))

enemy1 = pygame.image.load("images/ghost.png").convert_alpha()
enemy1 = pygame.transform.scale(enemy1, (80,90))
enemy1.set_alpha(128)
is_enemy1 = True

enemy2 = pygame.image.load("images/en1.png").convert_alpha()
enemy2 = pygame.transform.scale(enemy2, (80,90))
enemy2_list = []
is_enemy2 = True

# куля

bullet = pygame.image.load("images/bullet.png").convert_alpha()
bullets = []
bullets_count = 5

# початкові координати рухомих персонажів

player_x = 10
player_y = 475

enemy1_x = 3000
enemy1_y = 450

enemy2_x = 1300
enemy2_y = 475

bg_x = 0

# швидкість гравця 

player_speed = 10

enemy1_speed = 3


# стрибок

is_jump = False
jump_count = 9


# таймер гри

enemy2_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy2_timer, 5000)


# життя персонажа

hp = 3
# score = 0

# гра вкл/викл

running = True

# гра активна чи ні

gamePlay = True

while running:

        
    if gamePlay:
        # обмежуємо швидкість гри
        pygame.time.Clock().tick(20)



        keys = pygame.key.get_pressed()  # Отримуємо список нажатих клавіш

        screen.blit(bg, (bg_x,0))
        screen.blit(bg, (bg_x + 1280,0))

        bg_x -= 2
        
        if bg_x <= -1280:
            bg_x = 0

        if hp == 0:
            gamePlay = False

        label_hp = label.render(f"HP: {hp}", False, (245,245,15))
        screen.blit(label_hp, (20,20))

        # Доступ до колайдерів персонажів
        player_rect = walk_right[0].get_rect(topleft=(player_x,player_y))
    
    
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[anim_count], (player_x, player_y))
    
        anim_count += 1
        if anim_count == 3:
            anim_count = 0

        # ворог-привид 2
        if enemy2_list:   # якщо список ворогів не порожній
            for element in enemy2_list[:] :
                screen.blit(enemy2, element)
                element.x -= 10
                if player_rect.colliderect(element):
                    print("Ох")
                    hp -= 1
                    print(hp)
                    enemy2_list.remove(element)
                elif element.x <= -10:
                    
                    enemy2_list.remove(element)

        # кульки

        if bullets:    
            for element in bullets[:] :
                screen.blit(bullet, element)
                element.x += 10

                if element.x > 1250:
                    bullets.remove(element)

                if enemy2_list:
                    for enemy in enemy2_list[:] :
                        if element.colliderect(enemy):
                            bullets.remove(element)
                            enemy2_list.remove(enemy)


                
        


        # Ворог 1
        if is_enemy1:
            enemy1_rect = enemy1.get_rect(topleft=(enemy1_x,enemy1_y))
            screen.blit(enemy1, (enemy1_x, enemy1_y))
            # рух ворога
            enemy1_x -= enemy1_speed
            if player_rect.colliderect(enemy1_rect):
                print("Упс")
                is_enemy1 = False
                gamePlay = False


        
        

        # рух персонажа

        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        

        
        # обмеження ворога

        if enemy1_x < -20:
            enemy1_x = 1100

        # обмеження гравця

        if player_x < -20:  # Якщо герой вийшов за ліву межу
            player_x = 0  # Повертаємо його на межу
    
        if player_x > 1200:  # Якщо герой вийшов за праву межу
            player_x = 1160  # Повертаємо його на межу

        # стрибок

        if not is_jump:  # якщо стан спокою
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:  # стан стрибка
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

    else:
        screen.fill((0,0,0))


        screen.blit(label_los, (180, 100))
        screen.blit(label_restart, (180, 200))

        mouse = pygame.mouse.get_pos()

        if label_restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gamePlay = True
            hp = 3
            player_x = 100
            enemy2_list.clear()
            is_enemy1 = True
            enemy1_x = 3000
            enemy2_x = 1300
            bullets.clear()
            bullets_count = 5




      


    
    



    

    pygame.display.update()

    # перебір подій

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == enemy2_timer:
            enemy2_list.append(enemy2.get_rect(topleft=(enemy2_x, enemy2_y)))
        if event.type == pygame.KEYUP and event.key == pygame.K_q and gamePlay and bullets_count > 0:
            bullets.append(bullet.get_rect(topleft = (player_x + 47, player_y + 19)))
            bullets_count -= 1
