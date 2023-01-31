import pygame

clock = pygame.time.Clock() #функція часу

pygame.init()

screen = pygame.display.set_mode((1200,675)) #flags=pygame.NOFRAME якщо добавить не буде рамки віндовса
pygame.display.set_caption("Game Sedimat")
icon = pygame.image.load('images/315.png').convert_alpha()
pygame.display.set_icon(icon)




square = pygame.Surface((50,170)) # прямокутник
square.fill('Blue')

myfont = pygame.font.Font('fonts/Kanit.ttf', 40) #текст з вибором шрифта
text_surface = myfont.render('SeDimat', True, 'Red') #розміри тексту

bg = pygame.image.load('images/1624.png').convert() # конвертує не прозорі зображення
walk_left = [
    pygame.image.load('images/Player_left/l1.png').convert_alpha(),
    pygame.image.load('images/Player_left/l2.png').convert_alpha(),
    pygame.image.load('images/Player_left/l3.png').convert_alpha(),
    pygame.image.load('images/Player_left/l4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/Player_right/r1.png').convert_alpha(),
    pygame.image.load('images/Player_right/r2.png').convert_alpha(),
    pygame.image.load('images/Player_right/r3.png').convert_alpha(),
    pygame.image.load('images/Player_right/r4.png').convert_alpha(),
]


ghost = pygame.image.load('images/32.png').convert_alpha() # конвертує прозорі зображення
ghost_list_in_game =[] #список де з'являються монстри


player_anim_count = 0
bg_x = 0 # робить зміну заднього зображення

player_speed = 5 # швидкість та координати гравця
player_x = 150
player_y = 485

is_jump = False
jump_count = 8

gh = pygame.mixer.Sound('sound/amb16.ogg') #фоновий звук
gh.play()

ghost_timer = pygame.USEREVENT + 1  # задаємо таймер противнику коли той буде з'являться
pygame.time.set_timer(ghost_timer, 2300)


label = pygame.font.Font('fonts/Kanit.ttf', 40)
lose_label = label.render('Game over', False,(193, 196, 199)) #Текст кінця гри
restart_label = label.render('Continue', False,(115, 132, 148)) #текст растарту гри
restart_label_rect = restart_label.get_rect(topleft=(500, 350))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha() # пуля
bullets = []

gameplay = True


running = True
while running:


    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1200, 0))
    #screen.blit(ghost, (ghost_x,  500))
    
    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y)) # задаємо розміри гравця (хітбокси)
        #ghost_rect = ghost.get_rect(topleft=(ghost_x, 500)) # тут був один противник # задаємо розміри противника
        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el) # el ознаечає що привид буде виводиться в кординатах які вказані в функції
                el.x -= 10 #зменшуем координати привида

                if el.x < -10:
                    ghost_list_in_game.pop(i) # видаляємо привида за екраном після гравця.

                if player_rect.colliderect(el): # задаємо умови коли гравець зіткнувся з противником el і є противник
                    gameplay = False
        
        #screen.blit(square,(10,0)) #прямокутник
        #screen.blit(text_surface,(250,100)) # де знаходиться текст

        keys = pygame.key.get_pressed() # клавіши на які нажимає користувач
        if keys[pygame.K_LEFT]:
            screen.blit(walk_right[player_anim_count],(player_x,player_y)) #гравець
        else:
            screen.blit(walk_left[player_anim_count],(player_x,player_y))

        
        if keys[pygame.K_LEFT] and player_x > 50: #привязка клавіш куда двигаеться гравець
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 500:
            player_x += player_speed

        if not is_jump:    #функція стрибка, перевіряем чи включений прижок.
            if keys[pygame.K_SPACE]: 
                is_jump = True # постійно перевярє чи виконаний прижок
        else:
            if jump_count >= -8: 
                if jump_count > 0:
                    player_y -= (jump_count **2) / 2 # множителі для сильнішого прижку
                else:
                    player_y += (jump_count **2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 5
        if bg_x == -1200: # робить зміну заднього зображення
            bg_x = 0

        

        if bullets:
            for (i, el) in enumerate(bullets): # перебираем i щоб видалити кулю за екраном
                screen.blit(bullet, (el.x, el.y)) #місце де зявляеться куля шляхом перебору
                el.x += 5 #швидкість кулі

                if el.x > 1230:
                    bullets.pop(i)

                if ghost_list_in_game: # перебираем список з привидами
                    for(index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):  # якщо куля зіткнулась з привидом то видаляємо обох
                            ghost_list_in_game.pop(index) #індекс це привид
                            bullets.pop(i)


        pygame.draw.circle(screen, 'Red', (10,15), 5) # обєкт шар

        #screen.fill((5, 0, 0))

    else:
        screen.fill((87,88,89))
        screen.blit(lose_label, (500, 300))
        screen.blit(restart_label, restart_label_rect) # виведення текстів в кінці гри

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]: # 0 означає нажату ліву кнопку 1 права
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()

    pygame.display.update()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == ghost_timer:
                ghost_list_in_game.append(ghost.get_rect(topleft=(1230, 500)))  # спрацьовує таймер противника

            if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0: #цей код спрацьовує тільки тоді коли кнопка після натиску відпущена, щоб спрацювало 1 раз
                bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y))) #задаємо розміри кулі та координати спамлення.
                bullets_left -= 1

    clock.tick(30) #кадри які задали




            #elif event.type == pygame.KEYDOWN: #перевіряем на яку клавішу натиснули
                #if event.key == pygame.K_a:
                    #screen.fill((70, 44, 133))
