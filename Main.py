import pygame
from pygame.locals import *
import pickle
from os import path
from pygame import mixer

# Initializing pygame
pygame.init()

mixer.init()

clock = pygame.time.Clock()
fps = 60

# Creating the game window
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Run Timmy, Fight Platformer")

# defining the text fonts
fontScore = pygame.font.SysFont('ComicSans', 70)
font = pygame.font.SysFont('Bauhaus', 80)


# font colors
black = (0, 0, 0)
green = (0, 255, 0)

# defining grid variables
tile_size = 50  # tile size will be 50x50 on the grid
game_over = 0
# creating a variable to determine whether your in the main game or at the main menu so the start and exit buttons will appear
main_menu = True
level = 1
maxLevel = 2
score = 0
lives = 3
Lost = False


# Loading some images into the game to store them
sun_image = pygame.image.load('assets/sun.png')
background_image = pygame.image.load('assets/Sky_dark.png')
restart_image = pygame.image.load('assets/restart_Buttom.png')
start_image = pygame.image.load('assets/start Button.png')
exit_image = pygame.image.load('assets/exit_button.png')

# drawing a grid to help with the placement of the tiles and images
# def draw_grid():
#     for line in range(0, 20):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#         pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

# loading the music and sound effects
coinSound = pygame.mixer.Sound('assets/coinSound.wav')
coinSound.set_volume(0.5)  # reducing the sound voulume of the coin by half
jumpSound = pygame.mixer.Sound('assets/jumpSound.wav')
jumpSound.set_volume(0.5)
gameoverSound = pygame.mixer.Sound('assets/gameoverSound.wav')
gameoverSound.set_volume(0.5)
# pygame.mixer.music.load('assets/Worldmap Theme.mp3')
# pygame.mixer.music.play()


# drawing the text of the score and how many coins collected
def draw_text(text, font, text_column, x, y):
    text_image = font.render(text, True, text_column)
    screen.blit(text_image, (x, y))

    # lives_font = font.render(f"LIVES: {lives}", 1, black)  # using the f string to embedd variables inside the brackets
    # screen.blit(lives_font, (600, 5))  # top level hand corner of the screen


#
def reset_level(level):  # creatin a function for the level to reset when the player has died
    player.reset(100, screen_height - 130)  # resetting the player back to the start of the game
    enemy_group.empty()  # emptying the sprite Groups so that the ones that were there on the previous level disappear
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()

    # # if the player dies the the below fuction will reset the level data creating the world again.#
    # if path.exists(f'level{level}'):
    #     pickle_in = open(f'level{level}', 'r')
    #     world_data = pickle_in.load(pickle_in)
    world = World(world_data)
    return world  # loading all the levels again and returnin the ame world back into the game loop


class Button():  # creatin the class for the load, restart and save buttons
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False  # whatever the mosue button does
        # checking to see if the button is being pressed throuh the mouse position
        position = pygame.mouse.get_pos()

        # checking to see if the mouse button has been pressed
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[
                0] == 1 and self.clicked == False:  # the index 0 is referred to the left mosue button
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[
            0] == 0:  # if you've released the mouse button its not pressed and nothing with happen
            self.clicked = False

        # drawing the vutton images on the screen
        screen.blit(self.image, self.rect)

        return action


class Player():
    def __init__(self, x, y):
        self.reset(x,
                   y)  # calling the reset method, so when the player dies, The character will be respawned at the beginning

    def update(self, game_over, lives):
        dx = 0
        dy = 0
        anim_cooldown = 5  # 20 iterations need to pass before the next index
        collision_threshold = 20

        if game_over == 0:
            # adding in controls for the player
            key = pygame.key.get_pressed()
            if key[
                pygame.K_SPACE] and self.jump == False and self.in_air == False:  # the player will only be able to jump if he is on the round
                jumpSound.play()
                self.velocity_y = -18
                self.jump = True
            if key[pygame.K_SPACE] == False:
                self.jump = False

            # calculating the new player position. Checking the collision of that new positiom and the adjustin the position when collinding with an object
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[
                pygame.K_RIGHT] == False:  # resetting the counter and index when you not holding dow left or right buttoons
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    # updating the animation with the next imae
                    self.image = self.anim_right[self.index]
                if self.direction == -1:
                    # updating the animation with the next imae
                    self.image = self.anim_left[self.index]

            # addin in the animation for the character
            self.counter += 1
            if self.counter > anim_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.anim_right):
                    self.index = 0
                if self.direction == 1:
                    # updating the animation with the next image
                    self.image = self.anim_right[self.index]
                if self.direction == -1:
                    # updating the animation with the next image
                    self.image = self.anim_left[self.index]

            # adding in some gravity when jumping
            self.velocity_y += 1
            if self.velocity_y > 10:
                self.velocity_y = 10
            dy += self.velocity_y

            # check for collision with the enemies
            self.in_air = True  # checkin if the player is in the air, assuming he is..
            for tile in world.tile_list:  # lookin for collison in the world tile list from the y direction
                # checking for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    # checking for collison in the y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,
                                       self.height):  # creatin a new collision detection box which wil act as a temporary collision box, in orde to make adjustmenst before the actual collision
                    # checkin if the player is below the ground. if the player is jumping
                    if self.velocity_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.velocity_y = 0
                    # checking if the player is above the ground and is fallin
                    elif self.velocity_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.velocity_y = 0
                        self.in_air = False

            # checking if the character collides with the enemies
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
                gameoverSound.play()

            # checking if the player collides with the lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1  # if the player hits the lava, they die
                gameoverSound.play()

            # checkin if the player collides with the exit door and if you do, you proceed to the next level
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # collison with the platforms
            #moving through each of the platforms individually and checkin if the player has collided with it
            for platform in platform_Group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):  #checkin for collision in the x direction
                    dx = 0
                if platform.rect.colliderect(self.rect.x + dy, self.rect.y, self.width,
                                             self.height):  # checkin for collision in the y direction
                # checking if the player is below the platform
                    if ((self.rect.top + dy) - platform.rect.bottom) < collision_threshold:
                        self.velocity_y = 0
                        dy = platform.rect.bottom - self.rect.top

                    #checkin if player is above the platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) <collision_threshold:
                        self.rect.bottom = platform.rect.top - 1# lands the the player on top of the platform and making sure you're able to still move on the platform
                        dy = 0
                        self.in_air = False #while on top of the platform the player is able to jump
                    # moving with the platform in the x direction
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction





            # updating player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.player_died
            draw_text('GAMEOVER!', font, black, screen_width // 2 - 200, screen_height // 2)
            if self.rect.y > 250:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)  # drawing the player on the screen
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        self.anim_right = []
        self.anim_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 9):
            player_image_right = pygame.image.load(f'assets/player{num}.png')
            player_image_right = pygame.transform.scale(player_image_right,
                                                        (35, 70))  # loading in the player image and scaling in to size
            player_image_left = pygame.transform.flip(player_image_right, True,
                                                      False)  # using the right image thats loaded and flipping it to the left
            self.anim_right.append(player_image_right)
            self.anim_left.append(player_image_left)
        self.player_died = pygame.image.load('assets/ghost.png')
        self.image = self.anim_right[self.index]

        self.rect = self.image.get_rect()
        # iving the image an coordinate
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity_y = 0
        self.jump = False
        self.direction = 0
        self.in_air = True


# creating a class to display all the world data from the lsit below
class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_image = pygame.image.load('assets/tiles_brown.png')  # loading the images
        grass_image = pygame.image.load('assets/tiles_Green.png')
        row_count = 0

        # below i want to be able to apply the dirt image to each of the rows one by one
        for row in data:
            column_count = 0
            for tile in row:  # if the tile in the row is 1 the create dirt
                if tile == 1:
                    image = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    # ivin the image an x and y coordinate
                    image_rect.x = column_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 2:  # creating the grass
                    image = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    # ivin the image an x and y coordinate
                    image_rect.x = column_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 3:  # in the level data each number 3 will represent the enemies
                    blob = Enemy(column_count * tile_size, row_count * tile_size + 15)
                    enemy_group.add(blob)
                if tile == 4:
                    platform = Platform(column_count * tile_size, row_count * tile_size, 0, 1)
                    platform_Group.add(platform)
                if tile == 5:
                    platform = Platform(column_count * tile_size, row_count * tile_size, 1, 0)
                    platform_Group.add(platform)
                if tile == 6:  # in the level data each number 6 will represent where the lava is placed
                    lava = Lava(column_count * tile_size, row_count * tile_size + (
                            tile_size // 2))  # the lava image is half the size of the tile. Scalin it up by 2 to fit
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coins(column_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:  # the number 8 will represent the level completion door
                    exit = ExitDoor(column_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)

                column_count += 1  # increasing the tiles in the rows by 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:  # going throuh each of the tiles in the list and drawin them on the screen
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2),
            # checking for a collision between the player and the background tiles


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # the enemy class is a child of the sprite clasas
        self.image = pygame.image.load('assets/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(
                self.move_counter) > 50:  # changing it to an absolutin so that even if the its negative its going to convert it to a positive value
            self.move_direction *= -1
            self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y


    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # the enemy class is a child of the sprite class
        lava_image = pygame.image.load('assets/lava.png')
        self.image = pygame.transform.scale(lava_image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # the enemy class is a child of the sprite clasas
        lava_image = pygame.image.load('assets/coin.png')
        self.image = pygame.transform.scale(lava_image, (
            tile_size // 2,
            tile_size // 2))  # divinding the witdh and height by 2 to make the coins smaller than the tiles
        self.rect = self.image.get_rect()
        # positioning the coins based on the center point of the image
        self.rect.center = (x, y)


class ExitDoor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/Door.png')
        self.image = pygame.transform.scale(image, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# the world data is just a list of numbers tha represent the grass, dirt and moving platforms
world_data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               # this is the same data that is created and stored in the level_data files. This one is level 2
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 8, 1],
               [1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 2, 2, 1],
               [1, 0, 0, 0, 0, 3, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
               [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
               [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
               [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1]]  # the first row is going to be the dirt in the 20x20 grid. Defining where all the elements in the game will sit on the grid
# # The bottom row will be for the grass images
#
# world_data2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1],
#                [1, 8, 0, 0, 0, 7, 4, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                [1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1],
#                [1, 1, 1, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 2, 2, 2, 0, 0, 0, 1],
#                [1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 0, 0, 0, 1],
#                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
#                [1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1],
#                [1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
#                [1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1],
#                [1, 0, 0, 0, 2, 1, 1, 2, 0, 3, 0, 1, 1, 0, 0, 0, 3, 0, 0, 1],
#                [1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1]]

# instances created to be able to run it in the game
player = Player(100, screen_height - 130)

enemy_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
platform_Group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# creating a coin image at the top to display the score
coinScore = Coins(tile_size // 2, tile_size // 2)
coin_group.add(coinScore)

# loadin in the level data to create the world
# if path.exists(f'level{level}'):  # checkin to see if the level data files exits in the directory
#     pickle_in = open(f'level{level}', 'r')  # if it exists used the pickle module to load the data in
#     world_data = pickle.load(pickle_in)
world = World(world_data)



# creating buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_image)
# loading in the menu start button and exit button
start_button = Button(screen_width // 2 - 350, screen_height // 2,
                      start_image)  # the start iumage will be on the left hand side just offset from the center of the screen
exit_button = Button(screen_width // 2 + 150, screen_height // 2,
                     exit_image)  # the exit buttom will be on the right hand side, next to the start button

GameIsRunning = True
while GameIsRunning:
    clock.tick(fps)

    # drawing the background image onto the screen
    screen.blit(background_image, (0, 0))
    screen.blit(sun_image, (100, 100))

    if main_menu == True:
        # drawing the buttons on the screen
        if exit_button.draw():  # if the main main is showing then hide the exit button a
            GameIsRunning = False
        if start_button.draw():
            main_menu = False

    else:  # if the main menu is not true, the game will begin and the below code will run
        world.draw()

        if game_over == 0:  # if the player dies, reset the enemies
            enemy_group.update()
            platform_Group.update()
            # updatin the score and checkin if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coinSound.play()
            draw_text(' SCORE: ' + str(score), fontScore, black, tile_size - 10, 5)


        enemy_group.draw(screen)
        platform_Group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over, lives)

        # if player has died the the restart button will appear on the screen
        if game_over == -1:
            if restart_button.draw():
                player.reset(100, screen_height - 130)  # resetting the player back to the start of the game
                game_over = 0
                # reseetin the score back to 0 when the player dies
                score = 0


        if game_over == 1:
            # resettin the game and the proceed to the next level
              # increasing the level by one when the player completes a level
            if level <= maxLevel:
                # reset all the levels and go back to level 1
                world_data = []  # clearin the current level data that exists
                world = reset_level(
                    level)  # passin the reset function that clears the level and creates the new level based on the level data files and returnin it
                world2 = reset_level(level)
                game_over = 0  # resetting everyhting
            else:
                draw_text('YOU WON!!', font, green, (screen_width // 2) - 140, screen_height // 2)
            if restart_button.draw():
                level = 1
                # reset from level 1
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

    # calling the grid
    # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameIsRunning = False

    pygame.display.update()  # updating the display window with the background image and sun

pygame.quit()
