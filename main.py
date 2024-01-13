import pygame 


image_path = "/data/data/com.Manasyan.myapp/files/app/"

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("Ghost Surviver")


#Characters' images
icon = pygame.image.load("images/icon.png").convert_alpha()
bg = pygame.image.load("images/bg1.jpg").convert()
ghost = pygame.image.load("images/enemy.png").convert_alpha()
bullet = pygame.image.load("images/bullet.png").convert_alpha()
bonus = pygame.image.load("images/bonus.png").convert_alpha()

pygame.display.set_icon(icon)

#Configs for Ghost character
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)
ghost_list_in_game = []
killed_ghost = 0

#Configs for Bullet character
bullets_left = 5
bullets = []

#Configs for Bonus-Bullet character
bonus_timer = pygame.USEREVENT + 2
bonus_list_in_game = []
pygame.time.set_timer(bonus_timer, 5500)

#Player images for moving left
walk_left = [
    pygame.image.load("images/player_left/l2.png").convert_alpha(),
    pygame.image.load("images/player_left/l3.png").convert_alpha(),
    pygame.image.load("images/player_left/l1.png").convert_alpha(),
    pygame.image.load("images/player_left/l4.png").convert_alpha()
]

#Player images for moving right
walk_right = [
    pygame.image.load("images/player_right/r2.png").convert_alpha(),
    pygame.image.load("images/player_right/r3.png").convert_alpha(),
    pygame.image.load("images/player_right/r1.png").convert_alpha(),
    pygame.image.load("images/player_right/r4.png").convert_alpha()
]

#Configs for Player character
player_anim_count = 0
bg_x = 0
player_speed = 7
player_x = 150
player_y = 250
is_jump = False
jump_count = 8

#Some fonts in game
label = pygame.font.Font("fonts/IndieFlower-Regular.ttf", 80)
label2 = pygame.font.Font("fonts/Oswald-Light.ttf", 20)
label3 = pygame.font.Font("fonts/Oswald-Light.ttf", 40)

#Labels for some texts and direction-text in game
main_label = label.render("Back to Main!", False, (252, 11, 3))
lose_label = label.render("You Lose!", False, (252, 11, 3))
win_label = label.render("You Win!", False, (252, 11, 3))
restart_label = label.render("Try Again", False, (19, 0, 232))
play_label = label.render("Start Game", False, (19, 0, 232))
about_label = label.render("About Game", False, (100, 0, 210))
about_game_label = label3.render("This is my first Python game", False, (255, 255, 255))
about_game_label1 = label3.render("Your aim is to kill 13 ghosts and survive", False, (255, 255, 255))
about_game_label2 = label3.render("Enjoy it!", False, (255, 255, 255))
restart_label_rect = restart_label.get_rect(topleft=(180, 180))
play_label_rect = play_label.get_rect(topleft=(160, 70))
play_label_rect1 = play_label.get_rect(topleft=(160, 230))
about_label_rect = about_label.get_rect(topleft=(150, 160))
main_label_rect = main_label.get_rect(topleft=(120, 240))

#Sound in game
bg_sound = pygame.mixer.Sound ("sounds/bg.wav")
shot_sound = pygame.mixer.Sound ("sounds/shot.wav")
again_sound = pygame.mixer.Sound ("sounds/again.wav")
lose_sound = pygame.mixer.Sound ("sounds/lose.wav")
jump_sound = pygame.mixer.Sound ("sounds/jump.wav")
hit_sound = pygame.mixer.Sound ("sounds/hit.wav")
start_sound = pygame.mixer.Sound ("sounds/start.wav")
bonus_sound = pygame.mixer.Sound ("sounds/bonus.wav")
tab_sound = pygame.mixer.Sound ("sounds/tab.wav")
win_sound = pygame.mixer.Sound ("sounds/win.wav")



start = True
gameplay = True
about = False
win = False

bg_sound.play()

running = True
while running:

    bullets_count_label = label2.render("You have " + str(bullets_left) + " bullets to survive!", False, (255, 255, 255))
    ghosts_count_label = label2.render("You killed " + str(killed_ghost) + "/13 ghosts",  False, (255, 255, 255))

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 700, 0))
    screen.blit(bullets_count_label, (10, 0))
    screen.blit(ghosts_count_label, (10, 30))

    #Win window
    if win:
        gameplay = False
        start = False
        screen.fill((227, 132, 0))
        screen.blit(win_label, (210, 100))
        screen.blit(main_label, main_label_rect)

        mouse = pygame.mouse.get_pos()
        if main_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            tab_sound.play()
            start = True
            win = False
            player_x = 150
            ghost_list_in_game.clear()
            bonus_list_in_game.clear()
            bullets_left = 5
            killed_ghost = 0

    #Start window
    if start:
        gameplay = False
        screen.fill((227, 132, 0))
        screen.blit(play_label, play_label_rect)
        screen.blit(about_label, about_label_rect)

        mouse = pygame.mouse.get_pos()
        if play_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            start = False
            win = False
            killed_ghost = 0
            bullets_left = 5
            start_sound.play()
        
        if about_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            tab_sound.play()
            about = True
            start = False
    
    #About Window
    elif about:
        win = False
        killed_ghost = 0
        start = False
        screen.fill((227, 132, 0))
        screen.blit(about_game_label, (160, 80))
        screen.blit(about_game_label1, (90, 130))
        screen.blit(about_game_label2, (295, 180))
        screen.blit(play_label, play_label_rect1)

        mouse = pygame.mouse.get_pos()
        if play_label_rect1.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            about = False
            killed_ghost = 0
            bullets_left = 5
            win = False
            start_sound.play()

    #Gamplay
    elif gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if bonus_list_in_game:
            for (index, g) in enumerate(bonus_list_in_game):
                if player_rect.colliderect(g):
                    bonus_list_in_game.pop(index)
                    bullets_left += 1
                    bonus_sound.play()
    
        if ghost_list_in_game:
            for (j, i) in enumerate(ghost_list_in_game):
                screen.blit(ghost, i)
                i.x -= 10

                if i.x < -10:
                    ghost_list_in_game.pop(j)

                if player_rect.colliderect(i):
                    gameplay = False
                    win = False
                    lose_sound.play()

        if bonus_list_in_game:
            for (j, i) in enumerate(bonus_list_in_game):
                screen.blit(bonus, i)
                i.x -= 10

                if i.x < -10:
                    bonus_list_in_game.pop(j)

                if player_rect.colliderect(i):
                    bonus_sound.play()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))


        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 650:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
                jump_sound.play()
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1


        bg_x -= 5
        if bg_x == -700:
            bg_x = 0

        
        if bullets:
            for(j, i) in enumerate(bullets):
                screen.blit(bullet, (i.x, i.y))
                i.x += 4

                if i.x > 720:
                    bullets.pop(j)

                if ghost_list_in_game:
                    for (index, g) in enumerate(ghost_list_in_game):
                        if i.colliderect(g):
                            hit_sound.play()
                            ghost_list_in_game.pop(index)
                            bullets.pop(j)
                            killed_ghost += 1

        if killed_ghost == 13:
            win = True
            win_sound.play()
            
            
    elif gameplay == False and win == False:
        screen.fill((227, 132, 0))
        screen.blit(lose_label, (180, 70))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            again_sound.play()
            player_x = 150
            ghost_list_in_game.clear()
            bonus_list_in_game.clear()
            bullets.clear()
            bullets_left = 5
            killed_ghost = 0

    pygame.display.update()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(720, 260)))
        if event.type == bonus_timer:
            bonus_list_in_game.append(bonus.get_rect(topleft=(750, 200)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left != 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -=1
            shot_sound.play()



    clock.tick(10)



#---------------------------- For Application ---------------------------------------

# import pygame 


# image_path = "/data/data/com.Manasyan.myapp/files/app/"

# clock = pygame.time.Clock()
# pygame.init()
# screen = pygame.display.set_mode((700, 400))
# pygame.display.set_caption("Ghost Surviver")


# #Characters' images
# icon = pygame.image.load(image_path + "images/icon.png").convert_alpha()
# bg = pygame.image.load(image_path + "images/bg1.jpg").convert()
# ghost = pygame.image.load(image_path + "images/enemy.png").convert_alpha()
# bullet = pygame.image.load(image_path + "images/bullet.png").convert_alpha()
# bonus = pygame.image.load(image_path + "images/bonus.png").convert_alpha()

# pygame.display.set_icon(icon)

# #Configs for Ghost character
# ghost_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(ghost_timer, 2500)
# ghost_list_in_game = []
# killed_ghost = 0

# #Configs for Bullet character
# bullets_left = 5
# bullets = []

# #Configs for Bonus-Bullet character
# bonus_timer = pygame.USEREVENT + 2
# bonus_list_in_game = []
# pygame.time.set_timer(bonus_timer, 5500)

# #Player images for moving left
# walk_left = [
#     pygame.image.load(image_path + "images/player_left/l2.png").convert_alpha(),
#     pygame.image.load(image_path + "images/player_left/l3.png").convert_alpha(),
#     pygame.image.load(image_path + "images/player_left/l1.png").convert_alpha(),
#     pygame.image.load(image_path + "images/player_left/l4.png").convert_alpha()
# ]

# #Player images for moving right
# walk_right = [
#     pygame.image.load(image_path + "images/player_right/r2.png").convert_alpha(),
#     pygame.image.load(image_path + "images/player_right/r3.png").convert_alpha(),
#     pygame.image.load(image_path + "images/player_right/r1.png").convert_alpha(),
#     pygame.image.load(image_path + "images/player_right/r4.png").convert_alpha()
# ]

# #Configs for Player character
# player_anim_count = 0
# bg_x = 0
# player_speed = 7
# player_x = 150
# player_y = 250
# is_jump = False
# jump_count = 8

# #Some fonts in game
# label = pygame.font.Font(image_path + "fonts/IndieFlower-Regular.ttf", 80)
# label2 = pygame.font.Font(image_path + "fonts/Oswald-Light.ttf", 20)
# label3 = pygame.font.Font(image_path + "fonts/Oswald-Light.ttf", 40)

# #Labels for some texts and direction-text in game
# main_label = label.render("Back to Main!", False, (252, 11, 3))
# lose_label = label.render("You Lose!", False, (252, 11, 3))
# win_label = label.render("You Win!", False, (252, 11, 3))
# restart_label = label.render("Try Again", False, (19, 0, 232))
# play_label = label.render("Start Game", False, (19, 0, 232))
# about_label = label.render("About Game", False, (100, 0, 210))
# about_game_label = label3.render("This is my first Python game", False, (255, 255, 255))
# about_game_label1 = label3.render("Your aim is to kill 13 ghosts and survive", False, (255, 255, 255))
# about_game_label2 = label3.render("Enjoy it!", False, (255, 255, 255))
# restart_label_rect = restart_label.get_rect(topleft=(180, 180))
# play_label_rect = play_label.get_rect(topleft=(160, 70))
# play_label_rect1 = play_label.get_rect(topleft=(160, 230))
# about_label_rect = about_label.get_rect(topleft=(150, 160))
# main_label_rect = main_label.get_rect(topleft=(120, 240))

# #Sound in game
# bg_sound = pygame.mixer.Sound (image_path + "sounds/bg.wav")
# shot_sound = pygame.mixer.Sound (image_path + "sounds/shot.wav")
# again_sound = pygame.mixer.Sound (image_path + "sounds/again.wav")
# lose_sound = pygame.mixer.Sound (image_path + "sounds/lose.wav")
# jump_sound = pygame.mixer.Sound (image_path + "sounds/jump.wav")
# hit_sound = pygame.mixer.Sound (image_path + "sounds/hit.wav")
# start_sound = pygame.mixer.Sound (image_path + "sounds/start.wav")
# bonus_sound = pygame.mixer.Sound (image_path + "sounds/bonus.wav")
# tab_sound = pygame.mixer.Sound (image_path + "sounds/tab.wav")
# win_sound = pygame.mixer.Sound (image_path + "sounds/win.wav")



# start = True
# gameplay = True
# about = False
# win = False

# bg_sound.play()

# running = True
# while running:

#     bullets_count_label = label2.render("You have " + str(bullets_left) + " bullets to survive!", False, (255, 255, 255))
#     ghosts_count_label = label2.render("You killed " + str(killed_ghost) + "/13 ghosts",  False, (255, 255, 255))

#     screen.blit(bg, (bg_x, 0))
#     screen.blit(bg, (bg_x + 700, 0))
#     screen.blit(bullets_count_label, (10, 0))
#     screen.blit(ghosts_count_label, (10, 30))

#     #Win window
#     if win:
#         gameplay = False
#         start = False
#         screen.fill((227, 132, 0))
#         screen.blit(win_label, (210, 100))
#         screen.blit(main_label, main_label_rect)

#         mouse = pygame.mouse.get_pos()
#         if main_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
#             tab_sound.play()
#             start = True
#             win = False
#             player_x = 150
#             ghost_list_in_game.clear()
#             bonus_list_in_game.clear()
#             bullets_left = 5
#             killed_ghost = 0

#     #Start window
#     if start:
#         gameplay = False
#         screen.fill((227, 132, 0))
#         screen.blit(play_label, play_label_rect)
#         screen.blit(about_label, about_label_rect)

#         mouse = pygame.mouse.get_pos()
#         if play_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
#             gameplay = True
#             start = False
#             win = False
#             killed_ghost = 0
#             bullets_left = 5
#             start_sound.play()
        
#         if about_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
#             tab_sound.play()
#             about = True
#             start = False
    
#     #About Window
#     elif about:
#         win = False
#         killed_ghost = 0
#         start = False
#         screen.fill((227, 132, 0))
#         screen.blit(about_game_label, (160, 80))
#         screen.blit(about_game_label1, (90, 130))
#         screen.blit(about_game_label2, (295, 180))
#         screen.blit(play_label, play_label_rect1)

#         mouse = pygame.mouse.get_pos()
#         if play_label_rect1.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
#             gameplay = True
#             about = False
#             killed_ghost = 0
#             bullets_left = 5
#             win = False
#             start_sound.play()

#     #Gamplay
#     elif gameplay:
#         player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

#         if bonus_list_in_game:
#             for (index, g) in enumerate(bonus_list_in_game):
#                 if player_rect.colliderect(g):
#                     bonus_list_in_game.pop(index)
#                     bullets_left += 1
#                     bonus_sound.play()
    
#         if ghost_list_in_game:
#             for (j, i) in enumerate(ghost_list_in_game):
#                 screen.blit(ghost, i)
#                 i.x -= 10

#                 if i.x < -10:
#                     ghost_list_in_game.pop(j)

#                 if player_rect.colliderect(i):
#                     gameplay = False
#                     win = False
#                     lose_sound.play()

#         if bonus_list_in_game:
#             for (j, i) in enumerate(bonus_list_in_game):
#                 screen.blit(bonus, i)
#                 i.x -= 10

#                 if i.x < -10:
#                     bonus_list_in_game.pop(j)

#                 if player_rect.colliderect(i):
#                     bonus_sound.play()

#         keys = pygame.key.get_pressed()

#         if keys[pygame.K_LEFT]:
#             screen.blit(walk_left[player_anim_count], (player_x, player_y))
#         else:
#             screen.blit(walk_right[player_anim_count], (player_x, player_y))


#         if keys[pygame.K_LEFT] and player_x > 50:
#             player_x -= player_speed
#         elif keys[pygame.K_RIGHT] and player_x < 650:
#             player_x += player_speed

#         if not is_jump:
#             if keys[pygame.K_UP]:
#                 is_jump = True
#                 jump_sound.play()
#         else:
#             if jump_count >= -8:
#                 if jump_count > 0:
#                     player_y -= (jump_count ** 2) / 2
#                 else:
#                     player_y += (jump_count ** 2) / 2
#                 jump_count -= 1
#             else:
#                 is_jump = False
#                 jump_count = 8

#         if player_anim_count == 3:
#             player_anim_count = 0
#         else:
#             player_anim_count += 1


#         bg_x -= 5
#         if bg_x == -700:
#             bg_x = 0

        
#         if bullets:
#             for(j, i) in enumerate(bullets):
#                 screen.blit(bullet, (i.x, i.y))
#                 i.x += 4

#                 if i.x > 720:
#                     bullets.pop(j)

#                 if ghost_list_in_game:
#                     for (index, g) in enumerate(ghost_list_in_game):
#                         if i.colliderect(g):
#                             hit_sound.play()
#                             ghost_list_in_game.pop(index)
#                             bullets.pop(j)
#                             killed_ghost += 1

#         if killed_ghost == 13:
#             win = True
#             win_sound.play()
            
            
#     elif gameplay == False and win == False:
#         screen.fill((227, 132, 0))
#         screen.blit(lose_label, (180, 70))
#         screen.blit(restart_label, restart_label_rect)

#         mouse = pygame.mouse.get_pos()
#         if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
#             gameplay = True
#             again_sound.play()
#             player_x = 150
#             ghost_list_in_game.clear()
#             bonus_list_in_game.clear()
#             bullets.clear()
#             bullets_left = 5
#             killed_ghost = 0

#     pygame.display.update()



#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit()
#         if event.type == ghost_timer:
#             ghost_list_in_game.append(ghost.get_rect(topleft=(720, 260)))
#         if event.type == bonus_timer:
#             bonus_list_in_game.append(bonus.get_rect(topleft=(750, 200)))
#         if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left != 0:
#             bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
#             bullets_left -=1
#             shot_sound.play()



#     clock.tick(10)