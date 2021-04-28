import pygame
from pygame.locals import *

# Initializing pygame
pygame.init()

# Creating the game window
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Run Timmy, Fight Platformer")

# Loading some images into the game to store them
sun_image = pygame.image.load('assets/sun.png')
background_image = pygame.image.load('assets/sky.png')

# defining grid variables
tile_size = 50  # tile size will be 50x50 on the grid


# drawing a grid to help with the placement of the tiles and images
# def draw_grid():
#     for line in range(0, 20):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#         pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class Player():
    def __init__(self, x, y):
        player_image = pygame.image.load('assets/guy1.png')
        self.image = pygame.transform.scale(player_image, (40, 80))
        self.rect = self.image.get_rect()
        # iving the image an coordinate
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.jump = False

    def update(self):
        dx = 0
        dy = 0
        # addin in controls for the player
        key = pygame.key.get_pressed()
        if key [pygame.K_SPACE] and self.jump == False:
            self.velocity_y = -15
            self.jump = True
        if key[pygame.K_SPACE]:
            self.jump = False

        # calculating the new player position. Checking the collision of that new positiom and the adjustin the position when collinding with an object
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5

        # adding in some ravity when jumping
        self.velocity_y += 1
        if self.velocity_y > 10:
            self.velocity_y = 10
        dy += self.velocity_y


        #check for collision
        #updating player coordinates

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0




        screen.blit(self.image, self.rect)  # drawing the player on the screen





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
            for tile in row:  # if the tile in the row is 1
                if tile == 1:
                    image = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    # ivin the image an x and y coordinate
                    image_rect.x = column_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    image = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    # ivin the image an x and y coordinate
                    image_rect.x = column_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                column_count += 1  # increasing the tiles in the rows by 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:  # going throuh each of the tiles in the list and drawin them on the screen
            screen.blit(tile[0], tile[1])


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


player = Player(100, screen_height - 130)
world = World(world_data)

GameIsRunning = True
while GameIsRunning:

    # drawing the background image onto the screen
    screen.blit(background_image, (0, 0))
    screen.blit(sun_image, (100, 100))

    world.draw()
    player.update()
    # calling the grid
    # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameIsRunning = False

    pygame.display.update()  # updating the display window with the background image and sun

pygame.quit()
