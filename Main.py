import pygame
from pygame.locals import *

# Initializing pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

# Creating the game window
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Run Timmy, Fight Platformer")

# Loading some images into the game to store them
sun_image = pygame.image.load('assets/sun.png')
background_image = pygame.image.load('assets/sky.png')
restart_image = pygame.image.load('assets/restart_btn.png')
start_image = pygame.image.load('assets/start_btn.png')
exit_image = pygame.image.load('assets/exit_btn.png')


# defining grid variables
tile_size = 50  # tile size will be 50x50 on the grid
game_over = 0
# creating a variable to determine whether your in the main game or at the main menu so the start and exit buttons will appear
main_menu = True


# drawing a grid to help with the placement of the tiles and images
# def draw_grid():
#     for line in range(0, 20):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#         pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

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
        self.reset(x,y)  # calling the reset method, so when the player dies, The character will be respawned at the beginning

    def update(self, game_over):
        dx = 0
        dy = 0
        anim_cooldown = 20  # 20 iterations need to pass before the next index

        if game_over == 0:
            # adding in controls for the player
            key = pygame.key.get_pressed()
            if key[
                pygame.K_SPACE] and self.jump == False and self.in_air == False:  # the player will only be able to jump if he is on the round
                self.velocity_y = -15
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

            # check for collision
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
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1

            # checking if the player collides with the lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            # updating player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.player_died
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

        for num in range(1, 5):
            player_image_right = pygame.image.load(f'assets/guy{num}.png')
            player_image_right = pygame.transform.scale(player_image_right,
                                                        (40, 80))  # loading in the player image and scaling in to size
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
        dirt_image = pygame.image.load('assets/dirt.png')  # loading the images
        grass_image = pygame.image.load('assets/grass.png')
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
                if tile == 3:
                    blob = Enemy(column_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 6:
                    lava = Lava(column_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)

                column_count += 1  # increasing the tiles in the rows by 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:  # going throuh each of the tiles in the list and drawin them on the screen
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1],
                             2)  # checking for a collision between the player and the background tiles


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
                self.move_counter) > 50:  # changing it to an absolutin so that even if the its neative it going to convert it to a positive value
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # the enemy class is a child of the sprite clasas
        lava_image = pygame.image.load('assets/lava.png')
        self.image = pygame.transform.scale(lava_image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


world_data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
              [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
              [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
              [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
              [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1]]  # the first row is going to be the dirt in the 5x5 grid. Defining where all the elements in the game will sit on the grid
# The bottom row will be for the grass images

# instances created to be able to run it in the game
player = Player(100, screen_height - 130)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
world = World(world_data)

# creatin buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_image)
# loading in the menu start button and exit button
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_image) # the start iumage will be on the left hand side just offset from the center of the screen
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_image) # the exit buttom will be on the right hand side, next to the start button

GameIsRunning = True
while GameIsRunning:
    clock.tick(fps)

    # drawing the background image onto the screen
    screen.blit(background_image, (0, 0))
    screen.blit(sun_image, (100, 100))

    if main_menu == True:
        # drawing the buttons on the screen
        if exit_button.draw():
            GameIsRunning = False
        if start_button.draw():
            main_menu = False

    else: # if the main menu is not tru, the game will begin and the below code will run
        world.draw()

        if game_over == 0:
            blob_group.update()

        blob_group.draw(screen)
        lava_group.draw(screen)

        game_over = player.update(game_over)

        # if player has died calling the restart button
        if game_over == - 1:
            if restart_button.draw():
                player.reset(100, screen_height - 130)
                game_over = 0

    # calling the grid
    # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameIsRunning = False

    pygame.display.update()  # updating the display window with the background image and sun

pygame.quit()
