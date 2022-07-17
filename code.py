
from re import T
import pygame
from pygame import mixer
import os
import random
import csv


pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 262144)
mixer.init()
pygame.init()
pygame.font.init()


screen_width = 800
screen_height = int(screen_width*0.8)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ninja vs robots')


# set framerate
clock = pygame.time.Clock()
fps = 60

# define game variables
gravity = 0.75
scroll_thresh = 200
rows = 16
tile_size = screen_height//rows
TILE_TYPES = 109
max_levels = 4
screen_scroll = 0
bg_scroll = 0
game_over = 0
score = 0
cols = 145
level = 1
start_game = False
start_intro = False
time = 0


# define player action variables
moving_left = False
moving_right = False
attack = False
enemy_attack = False

scale = 2.1
scale2 = 2.6
scale3 = 1.8

# load music and sounds
pygame.mixer.music.load('audio/bg1.mp3')
pygame.mixer.music.set_volume(0.4)  # to reduce it
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump2.wav')
jump_fx.set_volume(0.7)
plyattack_fx = pygame.mixer.Sound('audio/playeratt.wav')
plyattack_fx.set_volume(0.3)
zomattack_fx = pygame.mixer.Sound('audio/zombie-6851.wav')
zomattack_fx.set_volume(0.06)
coin_fx = pygame.mixer.Sound('audio/coin.wav.wav')
coin_fx.set_volume(0.35)
heal_fx = pygame.mixer.Sound('audio/heal.wav')
heal_fx.set_volume(0.18)
zomdeath_fx = pygame.mixer.Sound('audio/zomdeath.wav')
zomdeath_fx.set_volume(0.1)
plydeath_fx = pygame.mixer.Sound('audio/playerded.wav')
plydeath_fx.set_volume(0.1)
gamew_fx = pygame.mixer.Sound('audio/won.wav')
gamew_fx.set_volume(1.0)

# load images
# store tiles in a list
img_list = []
for x in range(1, TILE_TYPES+1):
    img = pygame.image.load(f'images/tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)
# coin related images
coin = pygame.image.load('images/windows/Windows_32.png').convert_alpha()
coin_bar = pygame.image.load('images/windows/Windows_36.png').convert_alpha()
coin_bar = pygame.transform.scale(
    coin_bar, (int(coin_bar.get_width()/scale), int(coin_bar.get_height()/scale)))
# health related images
full_healthbar = pygame.image.load(
    'images/windows/Windows_46.png').convert_alpha()
full_healthbar = pygame.transform.scale(
    full_healthbar, (int(full_healthbar.get_width()/scale), int(full_healthbar.get_height()/scale2)))
empty_healthbar = pygame.image.load(
    'images/windows/Windows_52.png').convert_alpha()
empty_healthbar = pygame.transform.scale(
    empty_healthbar, (int(empty_healthbar.get_width()/scale2), int(empty_healthbar.get_height()/scale2)))
var_healthbar = pygame.image.load(
    'images/windows/Windows_52.png').convert_alpha()
var_healthbar = pygame.transform.scale(
    var_healthbar, (int(var_healthbar.get_width()/scale2), int(var_healthbar.get_height()/scale2)))
# box related images
healthbox1 = pygame.image.load(
    'images/windows/Windows_56.png').convert_alpha()
health1 = pygame.transform.scale(
    healthbox1, (int(healthbox1.get_width()/scale3), int(healthbox1.get_height()/scale3)))
healthbox2 = pygame.image.load(
    'images/windows/Windows_57.png').convert_alpha()
health2 = pygame.transform.scale(
    healthbox2, (int(healthbox2.get_width()/scale3), int(healthbox2.get_height()/scale3)))
healthbox3 = pygame.image.load(
    'images/windows/Windows_58.png').convert_alpha()
health3 = pygame.transform.scale(
    healthbox3, (int(healthbox3.get_width()/scale3), int(healthbox3.get_height()/scale3)))
healthbox4 = pygame.image.load(
    'images/windows/Windows_59.png').convert_alpha()
health4 = pygame.transform.scale(
    healthbox4, (int(healthbox4.get_width()/scale3), int(healthbox4.get_height()/scale3)))
list_ofboxes = [health1, health2, health3, health4]
# bg related images
pine1_img = pygame.image.load('images/tiles/pine1.png').convert_alpha()
pine2_img = pygame.image.load('images/tiles/pine2.png').convert_alpha()
mountain_img = pygame.image.load('images/tiles/mountain.png').convert_alpha()
sky_img = pygame.image.load('images/tiles/sky_cloud.png').convert_alpha()
bg_img = pygame.image.load('images/tiles/bg1.png').convert_alpha()
win = pygame.image.load('images/windows/win1.png').convert_alpha()
# button images
start_img = pygame.image.load('images/windows/start_btn.png').convert_alpha()
start_img=pygame.transform.scale(
    start_img, (int(start_img.get_width()/1.3), int(start_img.get_height()/1.3)))
exit_img = pygame.image.load('images/windows/exit_btn.png').convert_alpha()
exit_img=pygame.transform.scale(
   exit_img, (int(exit_img.get_width()/1.3), int(exit_img.get_height()/1.3)))
restart_img = pygame.image.load('images/windows/restart_btn.png').convert_alpha()
restart_img = pygame.transform.scale(
    restart_img, (int(restart_img.get_width()*2), int(restart_img.get_height()*2)))
text_img = pygame.image.load('images/windows/text.png').convert_alpha()
banner_img=pygame.image.load('images/windows/banner.png').convert_alpha()


# define colours
bg = (144, 201, 120)
red = (255, 48, 48)
pink = (255, 62, 150)
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
pink2 = (235, 65, 54)
purple = (191, 62, 255)
green2 = (144, 201, 120)
hover_col = (75, 225, 255)

# define font
#font = pygame.font.Font('freesansbold.ttf', 10)
#font3 = pygame.freetype.Font('ALBA____.ttf', 30)


# def draw_text(text, font, text_col, x, y):
#    img = font.render(text, True, text_col)
#    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(bg)
    width = bg_img.get_width()
    for x in range(5):
        screen.blit(bg_img, ((x*width)-bg_scroll*0.5,
                             screen_height-bg_img.get_height()))


def reset_level():
    enemy_group.empty()
    coin_group.empty()
    liquid_group.empty()
    decoration_group.empty()
    exit_group.empty()
    item_box_group.empty()

    # create empty tile list
    data = []
    for row in range(rows):
        r = [-1]*cols
        data.append(r)

    return data


class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, sound):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.health = 4000
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.attack_sound = sound
        self.action = 0
        self.coins = 0
        self.update_time = pygame.time.get_ticks()
        self.time = 0
        # ai specific varaiables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 10, 20)
        self.idling = False
        self.idle_counter = 0
        self.enemy_attack = False
        if self.char_type == 'player':
            # load all images for the players
            animation_types = ['Idle', 'Run', 'Jump', 'Dead', 'Attack']
            for animation in animation_types:
                # reset temporary list of images
                temp_list = []
                # count number of files in the folder
                num_of_frames = len(os.listdir(
                    f'images/{self.char_type}/png/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(
                        f'images/{self.char_type}/png/{animation}/{animation}__00{i}.png').convert_alpha()
                    img = pygame.transform.scale(
                        img, (int(img.get_width()/scale), int(img.get_height()/scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

        if self.char_type == 'enemy':
            # load all images for the players
            animation_types = ['Idle', 'Run', 'Attack', 'Dead', 'Jump']
            for animation in animation_types:
                # reset temporary list of images
                temp_list = []
                # count number of files in the folder
                num_of_frames = len(os.listdir(
                    f'images/{self.char_type}/png/{animation}'))
                for i in range(1, num_of_frames+1):
                    img = pygame.image.load(
                        f'images/{self.char_type}/png/{animation}/{animation} ({i}).png').convert_alpha()
                    img = pygame.transform.scale(
                        img, (int(img.get_width()/scale), int(img.get_height()/scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left, moving_right):
        # reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -12
            self.jump = False
            self.in_air = True
        # apply gravity
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check for collision
        for tile in world.obstacle_list:
            # check collision in x direction
            if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                dx = 0
                # if the ai has hit a wall make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            # check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):
                # check if below ground i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom-self.rect.top
                # check if above ground i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top-self.rect.bottom

        # check for collision with liquid
        if pygame.sprite.spritecollide(self, liquid_group, False):
            self.health = 0

        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False) and len(enemy_group) == 0:
            level_complete = True
        elif pygame.sprite.spritecollide(self, exit_group, False):
            screen.blit(text_img, (130, 200))
            # font3.render_to(screen, (100, 200), 'Defeat all the enemies to proceed to next level', red)
            level_complete = False

        # check if fallen off map
        if self.rect.bottom > screen_height:
            self.health = 0

        # check if going off the edges of screen
        if self.char_type == 'player':
            if self.rect.left+dx < 0 or self.rect.right+dx > screen_width:
                dx = 0

        # update rectangular position
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > screen_width-scroll_thresh and bg_scroll < (world.level_length*tile_size)-screen_width) or (self.rect.left < scroll_thresh and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def ai(self):
        global time
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 350) == 1:
                self.update_action(0)  # 0:idle
                self.idling = True
                self.idle_counter = 50

            # check if the ai is near the player
            if self.rect.colliderect(player.rect):
                self.attack_sound.play()
                self.enemy_attack = True
                if self.direction == player.direction:
                    self.direction *= -1
                    self.move_counter = 0
                if self.enemy_attack:
                    # attack
                    self.update_action(2)
                    player.health -= 15
                    self.time += 1
                if self.rect.colliderect(player.rect) and self.time > 100:
                    self.attack_sound.stop()
                    self.time = self.update_time

            if self.rect.colliderect(player.rect) == False:
                self.enemy_attack = False

            if attack and self.rect.colliderect(player.rect):
                enemy.health -= 29

            else:
                if self.idling == False and self.enemy_attack == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1: walk
                    self.move_counter += 1
                    if self.move_counter > tile_size:
                        self.direction *= -1
                        self.move_counter *= -1
                    # update ai vision as the enemy moves
                    self.vision.center = (
                        self.rect.centerx + 40 * self.direction, self.rect.centery)

                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False

        # scroll

        self.rect.x += screen_scroll

    def update_animation(self):
        # update animation
        animation_cooldown = 50
        # updating img depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action])-1
                self.kill()
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings (so the new animation starts from initial img)
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            if self.char_type == 'enemy':
                self.attack_sound.stop()
                self.update_action(3)
            elif self.char_type == 'player':
                self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x*tile_size
                    img_rect.y = y*tile_size
                    tile_data = (img, img_rect)
                if tile >= 0 and tile <= 63:  # building tiles of game
                    self.obstacle_list.append(tile_data)
                elif tile >= 64 and tile <= 96:  # decor
                    decor = Decoration(img, x*tile_size, y*tile_size)
                    decoration_group.add(decor)
                elif tile == 97:  # coin
                    coin = Coin(img, x*tile_size, y*tile_size)
                    coin_group.add(coin)
                elif tile == 98 and tile <= 101:  # item boxes
                    item_box = Item_box(0, x*tile_size, y*tile_size)
                    item_box_group.add(item_box)
                elif tile == 99:
                    item_box = Item_box(1, x*tile_size, y*tile_size)
                    item_box_group.add(item_box)
                elif tile == 100:
                    item_box = Item_box(2, x*tile_size, y*tile_size)
                    item_box_group.add(item_box)
                elif tile == 101:
                    item_box = Item_box(3, x*tile_size, y*tile_size)
                    item_box_group.add(item_box)
                elif tile in [102, 103]:  # create enemy
                    enemy = Character('enemy', x*tile_size,
                                      y*tile_size, 6, 2, zomattack_fx)
                    enemy_group.add(enemy)
                elif tile == 104:  # exit
                    exit = Exit(img, x*tile_size, y*tile_size)
                    exit_group.add(exit)
                elif tile >= 105 and tile <= 107:  # killing liquid(water)
                    liquid = Liquid(img, x*tile_size, y*tile_size)
                    liquid_group.add(liquid)
                elif tile == 108:  # player and health bar
                    player = Character(
                        'player', x*tile_size, y*tile_size, 6.6, 4, plyattack_fx)
                    health_bar = Healthbar(
                        10, 10, player.health, player.max_health)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            # 0 accesses the x coordinate of rect of tile
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])  # from tile data


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+tile_size//2, y +
                            (tile_size-self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Liquid(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y +
                            (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Coin(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+tile_size//2, y +
                            (tile_size-self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        # check if the player has picked up the coin
        collision = pygame.sprite.collide_rect(player, self)
        # pygame.draw.rect(screen, red, self, 1)
        if collision:
            player.coins += 1
            coin_fx.play()
            self.kill()


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+tile_size//2, y +
                            (tile_size-self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Item_box(pygame.sprite.Sprite):
    def __init__(self, item_index, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_index = item_index
        self.image = list_ofboxes[self.item_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size//2, y +
                            (tile_size-self.image.get_height()))

    def update(self):
        # scroll
        self.rect.x += screen_scroll

        # check if the player has picked up the box
        collision = pygame.sprite.collide_rect(player, self)
        if collision and player.health != player.max_health:
            heal_fx.play()
            player.health += 1500
            if player.health > player.max_health:
                player.health = player.max_health
            # delete the item box
            self.kill()


class Healthbar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health/self.max_health
        screen.blit(empty_healthbar, (self.x-2, self.y-4))
        pygame.draw.rect(screen, pink, (self.x+47, self.y+9, 130*ratio, 20))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Screenfade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(screen, self.colour,
                             (0-self.fade_counter, 0, screen_width//2, screen_height))
            pygame.draw.rect(screen, self.colour,
                             (screen_width//2+self.fade_counter, 0, screen_width, screen_height))
            pygame.draw.rect(screen, self.colour,
                             (0, 0-self.fade_counter, screen_width, screen_height//2))
            pygame.draw.rect(screen, self.colour,
                             (0, screen_height//2+self.fade_counter, screen_width, screen_height))
        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.colour,
                             (0, 0, screen_width, 0+self.fade_counter))
        if self.fade_counter >= screen_width:
            fade_complete = True

        return fade_complete


# create screen fade
death_fade = Screenfade(2, pink2, 4)
intro_fade = Screenfade(1, black, 4)


# create buttons
start_button = Button(
    screen_width//2-95, screen_height//2-50, start_img)
exit_button = Button(screen_width//2-80, screen_height//2+60, exit_img)
restart_button = Button(screen_width//2-100, screen_height//2-50, restart_img)

# create sprite groups
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
liquid_group = pygame.sprite.Group()


# creating empty tile list
world_data = []
for row in range(rows):
    r = [-1]*cols
    world_data.append(r)
# load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)


run = True

while run:
    clock.tick(fps)

    if start_game == False:
        screen.blit(banner_img,(0,0))
        # add buttons
        if start_button.draw():
            start_game = True
            start_intro = True
        if exit_button.draw():
            run = False
    else:
        # update bg
        draw_bg()
        # draw world map
        world.draw()
        # show player health
        health_bar.draw(player.health)
        # show coins
        screen.blit(coin_bar, (650, 5))
        number_img = pygame.image.load(
            f'images/no/Number{player.coins}.png').convert_alpha()
        number_img = pygame.transform.scale(
            number_img, (int(number_img.get_width()*1.75), int(number_img.get_height()*1.75)))

        screen.blit(number_img, (710, 19))
        #draw_text(f'{player.coins}', font, white, 712, 18)
        # font3.render_to(screen, (712, 18), f'{player.coins}', white)

        player.check_alive()
        player.update_animation()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.check_alive()
            enemy.draw()
            enemy.update_animation()
            if enemy.alive == False:
                zomdeath_fx.play()

        # update and draw groups
        item_box_group.update()
        coin_group.update()
        exit_group.update()
        decoration_group.update()
        liquid_group.update()

        item_box_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
        decoration_group.draw(screen)
        liquid_group.draw(screen)

        # play intro transition
        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # update player actions
        if player.alive:
            if player.in_air:
                player.update_action(2)  # 2 : Jump
            elif moving_left or moving_right and attack:
                player.update_action(1)
            elif attack:
                player.update_action(4)  # 3:Attack
            elif moving_left or moving_right:
                player.update_action(1)  # 1:run
            else:
                player.update_action(0)  # 0:idle
            screen_scroll, level_complete = player.move(
                moving_left, moving_right)
            bg_scroll -= screen_scroll
            # check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= max_levels:
                    # load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
                    bg_img = pygame.image.load(
                        f'images/tiles/bg{level}.png').convert_alpha()
        else:
            pygame.mixer.music.stop()
            screen_scroll = 0
            plydeath_fx.play()
            if death_fade.fade():
                plydeath_fx.stop()
                if restart_button.draw():
                    pygame.mixer.music.play(-1, 0.0, 5000)
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    # load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
        if player.alive == True and level > max_levels:
            screen.blit(win, (0, 0))
            pygame.mixer.music.stop()
            gamew_fx.play()

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_SPACE and player.alive:
                attack = True
                player.attack_sound.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        # Keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                attack = False

    pygame.display.update()


pygame.quit()
