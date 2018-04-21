from gamelib import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Two Worlds')

background = pygame.image.load('game_resource/background.jpg')
background = pygame.transform.scale(background, (480, 800))

game_over = pygame.image.load('game_resource/gameover.jpg')
game_over = pygame.transform.scale(game_over, (480, 800))

bullet_img = pygame.image.load('game_resource/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (21, 32))

boss_bullet_img = pygame.image.load('game_resource/bomb.png')
boss_bullet_img = pygame.transform.scale(boss_bullet_img, (21, 32))

plane_img = pygame.image.load('game_resource/shoot.png')

friend_img = pygame.image.load('game_resource/friend.png')
friend_img = pygame.transform.scale(friend_img, (64, 82))

boss_img = pygame.image.load('game_resource/pie.png')
boss_img = pygame.transform.scale(boss_img, (128, 246))

plane_pos = [200, 600]

plane_rect = []
plane_rect.append(pygame.Rect(0, 99, 102, 126))
plane_rect.append(pygame.Rect(165, 360, 102, 126))
plane_rect.append(pygame.Rect(165, 234, 102, 126))
plane_rect.append(pygame.Rect(330, 624, 102, 126))
plane_rect.append(pygame.Rect(330, 498, 102, 126))
plane_rect.append(pygame.Rect(432, 624, 102, 126))

plane = Plane(plane_img, plane_rect, plane_pos)

boss_pos = [random.randint(0, SCREEN_WIDTH - 128), 0]
boss = Boss(boss_img, boss_img, boss_pos)

enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies_plane = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()

friends_starboy = pygame.sprite.Group()
friends_down = pygame.sprite.Group()

shoot_frequency = 0
boss_shoot_frequency = 0
enemy_frequency = 0
friend_frequency = 0

plane_down_index = 16

score = 0

clock = pygame.time.Clock()

running = True

while running:
    clock.tick(50)

    if not plane.is_hit:
        if shoot_frequency % 15 == 0:
            plane.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    if (boss.is_hit == False) and (boss.show == True):
        if boss_shoot_frequency % 70 == 0:
            boss.shoot(boss_bullet_img)
        boss_shoot_frequency += 1
        if boss_shoot_frequency >= 71:
            boss_shoot_frequency = 0

    if score >= 30000:
        boss.show = True

    if boss.show == True:
        boss.move_parallel()

    for bullet in boss.bullets:
        bullet.boss_bullet_move()
        if bullet.image.get_rect().bottom >= SCREEN_HEIGHT:
            boss.bullets.remove(bullet)

    if pygame.sprite.collide_circle(boss, plane):
        plane.is_hit = True
        break

    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width),
                      random.randint(0, SCREEN_HEIGHT / 2.0)]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies_plane.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    friend_rect = friend_img.get_rect()
    if friend_frequency % 200 == 0:
        friend1_pos = [random.randint(0, SCREEN_WIDTH - friend_rect.width), 0]
        friend1 = Friend(friend_img, friend_img,friend1_pos)
        friends_starboy.add(friend1)
    friend_frequency += 1
    if friend_frequency >= 200:
        friend_frequency = 0

    for bullet in plane.bullets:
        bullet.move()
        if bullet.image.get_rect().bottom < 0:
            plane.bullets.remove(bullet)

    for bullet in plane.bullets:
        if pygame.sprite.collide_circle(bullet, boss):
            boss.got_shot()
            plane.bullets.remove(bullet)

    if boss.hp <= 0:
        break

    for enemy in enemies_plane:
        enemy.move_vertical()
        enemy.move_parallel()
        if pygame.sprite.collide_circle(enemy, plane):
            enemies_down.add(enemy)
            enemies_plane.remove(enemy)
            plane.is_hit = True
            break
        if enemy.rect.top < 0:
            enemies_plane.remove(enemy)

    for friend in friends_starboy:
        friend.move_vertical()
        friend.move_parallel()
        if pygame.sprite.collide_circle(friend, plane):
            friends_down.add(friend)
            friends_starboy.remove(friend)
        if friend.rect.top < 0:
            friends_starboy.remove(friend)

    for bomb in boss.bullets:
        if pygame.sprite.collide_circle(bomb, plane):
            plane.is_hit = True
            break

    enemies_plane_down = pygame.sprite.groupcollide(enemies_plane, plane.bullets, 1, 1)
    for enemy_down in enemies_plane_down:
        enemies_down.add(enemy_down)

    screen.fill(0)
    screen.blit(background, (0, 0))

    if not plane.is_hit:
        screen.blit(plane.image[plane.img_index], plane.rect)
        plane.img_index = shoot_frequency // 8
    else:
        plane.img_index = plane_down_index // 8
        screen.blit(plane.image[plane.img_index], plane.rect)
        plane_down_index += 1
        if plane_down_index > 47:
            running = False

    if boss.show == True:
        if not boss.is_hit:
            screen.blit(boss.image, boss.rect)
            boss.bullets.draw(screen)

        else:
            pass

    for friend_down in friends_down:
        if friend_down.down_index == 0:
            pass
        if friend_down.down_index > 7:
            friends_down.remove(friend_down)
            score += 2000
            continue
        friend_down.down_index += 1

    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            pass
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    boss.bullets.draw(screen)
    plane.bullets.draw(screen)
    enemies_plane.draw(screen)
    friends_starboy.draw(screen)

    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_pressed = pygame.key.get_pressed()

    if key_pressed[K_w] or key_pressed[K_UP]:
        plane.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        plane.moveDown()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        plane.moveLeft()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        plane.moveRight()

screen.blit(game_over, (0, 0))

font = pygame.font.Font(None, 48)

text = font.render('Score: ' + str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery - 60

text2 = font.render('go back to', True, (255, 0, 0))
text_rect2 = text2.get_rect()
text_rect2.centerx = screen.get_rect().centerx
text_rect2.centery = screen.get_rect().centery

font3 = pygame.font.Font(None, 72)
text3 = font3.render('CODING!', True, (255, 0, 0))
text_rect3 = text3.get_rect()
text_rect3.centerx = screen.get_rect().centerx
text_rect3.centery = screen.get_rect().centery + 60

screen.blit(text, text_rect)
screen.blit(text2, text_rect2)
screen.blit(text3, text_rect3)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()



