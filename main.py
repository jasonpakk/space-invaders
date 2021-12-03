# Space Invaders Game
# By Jason Pak

import pygame
import gamebox
import random

camera = gamebox.Camera(800, 600)

# importing images
player = gamebox.from_image(20, 500, "images/player.jpg")
player.size = [40, 40]

missile = gamebox.from_image(20, 480, "images/missile.jfif")
missile.size = [20, 20]

big_enemy = gamebox.from_image(30, 25, "images/big_invader.jpg")
big_enemy.size = [60, 60]

bullet = gamebox.from_image(20, 500, "images/bullet.jpg")
bullet.size = [5, 10]

big_bullet = gamebox.from_image(20, 500, "images/bullet.jpg")
big_bullet.size = [10, 15]

star = gamebox.from_image(0, -100, "images/star.png")
star.size = [25, 25]

# declaring variables
enemies = [] # stores all the enemies that will be created
shooting = False
hasBullet = False
hasBigBullet = False
end_screen = False
star_moving = False
star_count = 0
enemy_count = 0
score = 0
game_play = False
forward = True
forward_enemy = True

# creating health bar
health_bar = gamebox.from_color(700, 550, "green", 150, 20)
health_damage = gamebox.from_color(700, 550, "gray", 150, 20)
health_bg = gamebox.from_color(550, 550, "black", 200, 20)


def game_screen():
    """Initializes game screen and resets all variables for gameplay"""
    global star_count

    camera.clear("black")
    camera.draw(player)

    # reset parameters
    star_count = 0
    big_enemy.y = 25
    player.x = 20
    health_bar.x = 700
    health_bar.color = "green"
    make_enemy() # draw the enemies


def make_enemy():
    """Draws all enemies onto the game screen"""
    global enemies
    enemies = []

    # create blue colored enemies in row 1
    blue_enemy = gamebox.from_image(20, 400, "images/blue.jpg")
    blue_enemy.size = [40, 40]
    for i in range(1, 13):
        blue_enemy = gamebox.from_image(60*i, 300, "images/blue.jpg")
        blue_enemy.size = [40, 40]
        enemies.append(blue_enemy)

    # create green colored enemies in row 2
    green_enemy = gamebox.from_image(20, 250, "images/green.jpg")
    green_enemy.size = [40, 40]
    for i in range(1, 13):
        green_enemy = gamebox.from_image(60*i, 200, "images/green.jpg")
        green_enemy.size = [40, 40]
        enemies.append(green_enemy)

    # create yellow colored enemies in row 3
    yellow_enemy = gamebox.from_image(20, 100, "images/yellow.jpg")
    yellow_enemy.size = [40, 40]
    for i in range(1, 13):
        yellow_enemy = gamebox.from_image(60*i, 100, "images/yellow.jpg")
        yellow_enemy.size = [40, 40]
        enemies.append(yellow_enemy)


def move_player(keys):
    """Interprets keyboard press to determine player movement
    :param keys: key that user has pressed
    """
    if pygame.K_LEFT in keys: # moving player left
        player.x -= 5
    if pygame.K_RIGHT in keys: # moving player right
        player.x += 5
    if player.x < 10:  # prevent out of bounds (left)
        player.x = 10
    if player.x > 790:
        player.x = 790  # prevent out of bounds (right)
    camera.draw(player)


def shooting_star():
    """Handles displaying a random shooting star for players to catch"""
    global star_moving
    global star_count

    # determine whether or not to send down star
    send_star = random.randint(1, 100)

    # handle movement of star
    if not star_moving and send_star == 1: # 1/100 probability of star coming down
        star_moving = True
        star.x = random.randint(50, 750)
        star.y = 0
        star.speedy = 20
        star.speedx = random.randint(-5, 5)
    if star_moving and star.y < 600:
        star.move_speed()
        camera.draw(star)
    else:
        star_moving = False

    # full health if player catches star
    if star.touches(player):
        health_bar.x = 700
        health_bar.color = "green"
        star_count += 1
        star.y = -100

    # display total count
    camera.draw("Total Stars:", 26, "white", 100, 550)
    camera.draw(str(star_count), 26, "yellow", 170, 550)


def missile_shoot(keys):
    """Shoots a missile if user presses x
    :param keys: key that user has pressed
    """
    global shooting

    # player shoots missile by pressing x
    if pygame.K_x in keys and not shooting:
        missile.x = player.x
        missile.y = 480
        missile.speedy = -30
        shooting = True

    # draw user missile
    if shooting and missile.y > 0:
        camera.draw(missile)
        missile.move_speed()
    else:
        shooting = False

    check_missile_hit() # check for hits


def check_missile_hit():
    """Checks if user's missile has hit the enemy"""
    global enemy_count
    global score

    # check if missile hit any of the small enemies
    for en in enemies:
        if en.bottom_touches(missile):
            missile.y = -100
            en.y = 1000
            enemy_count += 1
            score += 10

    # check if missile hit the big enemy
    if big_enemy.bottom_touches(missile):
        big_enemy.y = 1000
        enemy_count += 1
        score += 1000

    # if all enemies have been killed, regenerate new ones
    if enemy_count > 0 and enemy_count % 37 == 0:
        enemy_count = 0
        make_enemy()
        big_enemy.y = 25


def bullet_shoot():
    """Handles enemies randomly shooting a bullet to attack the player"""
    global hasBullet
    global hasBigBullet

    # handle enemy shooting a bullet
    if hasBullet and bullet.y < 600:
        bullet.move_speed()
        camera.draw(bullet)
    elif hasBullet:
        hasBullet = False
    else:
        hasBullet = True
        # randomly select an enemy to shoot a bullet
        random_enemy = random.randint(0, 35)
        bullet.x = enemies[random_enemy].x
        bullet.y = enemies[random_enemy].y + 10
        bullet.speedy = 10

    # handle big enemy shooting a bullet
    if hasBigBullet and big_bullet.y < 600:
        big_bullet.move_speed()
        camera.draw(big_bullet)
    elif hasBigBullet:
        hasBigBullet = False
    else:
        hasBigBullet = True
        big_bullet.x = big_enemy.x
        big_bullet.y = big_enemy.y + 10
        big_bullet.speedy = 10

    display_score()
    display_health()


def display_score():
    """Displays current score to user"""
    global score
    camera.draw("Score:", 26, "white", 320, 550)
    camera.draw(str(score), 26, "gray", 380, 550)


def display_health():
    """Displays current health to user"""
    global end_screen

    # handle user getting hit by bullet
    if bullet.touches(player):
        health_bar.x -= 10
        bullet.y = 1000
    if big_bullet.touches(player):
        health_bar.x -= 35
        big_bullet.y = 1000

    # display proper color for health bar
    if health_bar.x < 575:
        end_screen = True
    elif health_bar.x < 610:
        health_bar.color = "red"
    elif health_bar.x < 655:
        health_bar.color = "yellow"

    # display health bar
    camera.draw(health_damage)
    camera.draw(health_bar)
    camera.draw(health_bg)
    camera.draw("Health:", 26, "white", 600, 550)


def move_enemies():
    """Handles movement of enemies"""
    global forward_enemy

    # update forward_enemy variable depending on location
    if enemies[35].x > 780: # prevent out of bounds (right)
        forward_enemy = False
    elif enemies[24].x < 20: # prevent out of bounds (left)
        forward_enemy = True

    # move all small enemies
    for i in range(36):
        move_small_enemy(i, forward_enemy)

    # move big enemy
    move_big_enemy()
    camera.display()


def move_small_enemy(number, move_forward):
    """Handles moving a small enemy in the right direction
  
    :param number: index of the enemy in the list
    :type number: int
    :param move_forward: whether enemies are currently moving forward
    :type move_forward: boolean
    """

    # set speed in x direction depending on which row the enemy is in
    if move_forward:
        if 0 <= number <= 11:
            enemies[number].speedx = 1
        elif 12 <= number <= 23:
            enemies[number].speedx = -2
        else:
            enemies[number].speedx = 3
    else:
        if 0 <= number <= 11:
            enemies[number].speedx = -1
        elif 12 <= number <= 23:
            enemies[number].speedx = 2
        else:
            enemies[number].speedx = -3

    # move and draw screen
    enemies[number].move_speed()
    camera.draw(enemies[number])


def move_big_enemy():
    """Handles movement of the big enemy"""
    global forward

    # update direction appropriately
    if big_enemy.x == 770: # check out of bounds (right)
        forward = False
    elif big_enemy.x == 30: # check out of bounds (left)
        forward = True

    if forward:
        big_enemy.speedx = 5
    else:
        big_enemy.speedx = -5
    big_enemy.move_speed()
    camera.draw(big_enemy)


def tick(keys):
    """Updates gameplay every 30ms
    :param keys: key that user has pressed
    """
    camera.clear('black')
    global game_play
    global end_screen
    global score

    if end_screen: # game over screen
        camera.clear("black")
        camera.draw("GAME OVER", 60, "red", 400, 200)
        camera.draw("Final Score ", 30, "white", 400, 280)
        camera.draw(str(score), 30, "white", 400, 320)
        camera.draw("Hold SPACE to play again", 30, "blue", 400, 400)
        game_play = False
    elif not game_play:  # start screen
        camera.draw("SPACE INVADERS", 60, "red", 400, 200)
        camera.draw("Created by Jason Pak", 36, "blue", 400, 300)
        camera.draw("To start, press SPACE", 30, "white", 400, 350)
        camera.draw("Press LEFT or RIGHT to move player", 30, "white", 400, 400)
        camera.draw("Press X to shoot", 30, "white", 400, 450)
        camera.draw("Catch a STAR to regain health", 30, "white", 400, 500)

    # handle if user pushes space bar to start new game
    if pygame.K_SPACE in keys and not game_play:
        game_screen()
        end_screen = False
        game_play = True  # switch to game screen

    # while game is running
    if game_play and not end_screen:
        move_player(keys)
        shooting_star()
        move_enemies()
        missile_shoot(keys)
        bullet_shoot()

    camera.display()


gamebox.timer_loop(30, tick)
