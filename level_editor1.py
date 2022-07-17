from json import load
import pygame
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_HEIGHT = 640
SCREEN_WIDTH = 1000
LOWER_MARGIN = 100
SIDE_MARGIN = 400

screen = pygame.display.set_mode((
    SCREEN_WIDTH+SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('Level Editor')


# define game variables
ROWS = 16
MAX_COLS = 145
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPES = 109
level = 1
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


# load images
pine1_img = pygame.image.load('images/tiles/pine1.png').convert_alpha()
pine2_img = pygame.image.load('images/tiles/pine2.png').convert_alpha()
mountain_img = pygame.image.load('images/tiles/mountain.png').convert_alpha()
sky_img = pygame.image.load('images/tiles/sky_cloud.png').convert_alpha()
bg_img = pygame.image.load(f'images/tiles/bg{level}.png').convert_alpha()

# store tiles in a list
img_list = []
scale = 2.1
for x in range(1, TILE_TYPES+1):
    img = pygame.image.load(f'images/tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('images/windows/save_btn.png').convert_alpha()
load_img = pygame.image.load('images/windows/load_btn.png').convert_alpha()


# define colours
GREEN = (144, 201, 120)
RED = (200, 25, 25)
WHITE = (255, 255, 255)

# define font
font = pygame.font.SysFont('Futura', 30)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1]*MAX_COLS
    world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS-1][tile] = 0


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# create function for drawing bg
def draw_bg():
    screen.fill(GREEN)
    width = bg_img.get_width()
    for x in range(4):
        if level == 5:
            screen.blit(sky_img, ((x*width)-scroll*0.5, 0))
            screen.blit(mountain_img, ((x*width)-scroll*0.6, SCREEN_HEIGHT -
                                       mountain_img.get_height()-300))
            screen.blit(pine1_img, ((x*width)-scroll*0.7,
                                    SCREEN_HEIGHT-pine1_img.get_height()-150))
            screen.blit(pine2_img, ((x*width)-scroll*0.8,
                                    SCREEN_HEIGHT-pine2_img.get_height()))
        else:
            screen.blit(bg_img, ((x*width)-scroll*0.5,
                                 SCREEN_HEIGHT-bg_img.get_height()))

# draw grid


def draw_grid():
    # vertical lines
    for c in range(MAX_COLS+1):
        pygame.draw.line(screen, WHITE, (c*TILE_SIZE-scroll, 0),
                         (c*TILE_SIZE-scroll, SCREEN_HEIGHT))
    # horizontal lines
    for c in range(ROWS+1):
        pygame.draw.line(screen, WHITE, (0, c*TILE_SIZE),
                         (SCREEN_WIDTH, c*TILE_SIZE))


def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x*TILE_SIZE-scroll, y*TILE_SIZE))


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


# create buttons
save_button = Button(
    SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img)
load_button = Button(SCREEN_WIDTH // 2 + 200,
                     SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img)
# make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(970+(50*button_col)+60,
                         45 * button_row + 10, img_list[i])
    button_list.append(tile_button)
    button_col += 1
    if button_col == 7:
        button_row += 1
        button_col = 0


run = True
while run:

    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE,
              10, SCREEN_HEIGHT+LOWER_MARGIN-90)
    draw_text('Press UP or DOWN to change level', font,
              WHITE, 10, SCREEN_HEIGHT+LOWER_MARGIN-60)

    #screen.blit(bg_img, (0, 0))

    # Save and load data
    if save_button.draw():
        # save level data
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw():
        # load in data levels
        # reset scroll back to the start of the level
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH,
                                     0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw():  # i.draw() becomes true when a tile is clicked (draw method of button class)
            current_tile = button_count
    # highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 4 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS*TILE_SIZE)-SCREEN_WIDTH-400:
        scroll += 4 * scroll_speed

    # add new tiles to the screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    # position of mouse in grid
    x = (pos[0]+scroll)//TILE_SIZE  # 0:x coordinate of mouse
    y = pos[1]//TILE_SIZE  # 1:y coordinate of mouse

    # check the coordinates are within tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile area
        # 0 indicates that left key of mouse has been clicked
        if pygame.mouse.get_pressed()[0]:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2]:  # 2:right key
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
                bg_img = pygame.image.load(
                    f'images/tiles/bg{level}.png').convert_alpha()
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
                bg_img = pygame.image.load(
                    f'images/tiles/bg{level}.png').convert_alpha()
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 51

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()
