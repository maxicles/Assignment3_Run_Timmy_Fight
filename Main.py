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

# defining grid variables
tile_size = 50  # tile size will be 50x50 on the grid


# drawing a grid to help with the placement of the tiles and images
# def draw_grid():
#     for line in range(0, 20):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#         pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class Player():
    def __init__(self, x, y):
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
        self.image = self.anim_right[self.index]

        self.rect = self.image.get_rect()
        # iving the image an coordinate
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity_y = 0
        self.jump = False
        self.direction = 0  # usin the variable to determine whether the player is pressing left or riht

    def update(self):
        dx = 0
        dy = 0
        anim_cooldown = 20  # 20 iterations need to pass before the next index
        # adding in controls for the player
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jump == False:
            self.velocity_y = -15
            self.jump = True
        if key[pygame.K_SPACE]:
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
                # updating the animation with the next imae
                self.image = self.anim_right[self.index]
            if self.direction == -1:
                # updating the animation with the next imae
                self.image = self.anim_left[self.index]

        # adding in some gravity when jumping
        self.velocity_y += 1
        if self.velocity_y > 10:
            self.velocity_y = 10
        dy += self.velocity_y

        # check for collision
        for tile in world.tile_list:  # lookin for collison in the world tile list from the y direction
            # checking for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,
                                   self.height):  # creatin a new collision detection box which wil act as a temporary collision box, in orde to make adjustmenst before the actual collision
                # checkin if the player is below the ground. if the player is jumping
                if self.velocity_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.velocity_y = 0
                # checking if the player is above the ground and is fallin
                elif self.velocity_y >= 0:
                    dy = tile[1].top - self.rect.bottom

        # updating player coordinates

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        screen.blit(self.image, self.rect)  # drawing the player on the screen
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


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
        if abs(self.move_counter) > 50: # changing it to an absolutin so that even if the its neative it going to convert it to a positive value
            self.move_direction *= -1
            self.move_counter *= -1




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
blob_group = pygame.sprite.Group()
world = World(world_data)

GameIsRunning = True
while GameIsRunning:
    clock.tick(fps)

    # drawing the background image onto the screen
    screen.blit(background_image, (0, 0))
    screen.blit(sun_image, (100, 100))

    world.draw()
    blob_group.update()
    blob_group.draw(screen)
    player.update()
    # calling the grid
    # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameIsRunning = False

    pygame.display.update()  # updating the display window with the background image and sun

pygame.quit()
