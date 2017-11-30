import pygame
from math import sqrt
from sys import argv
import numpy as np
from data import *

current_grid_number = -1

def getGridNum():
  global current_grid_number
  return current_grid_number

def setGridNum(grid_num):
  global current_grid_number
  current_grid_number = grid_num

def run(length=330):
  """
   Example program to show using an array to back a grid on-screen.
   
   Sample Python/Pygame Programs
   Simpson College Computer Science
   http://programarcadegames.com/
   http://simpson.edu/computer-science/
   
   Explanation video: http://youtu.be/mdTeqiWyFnc
  """
   
  # Define some colors
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  GREEN = (0, 255, 0)
  RED = (255, 0, 0)
   

  # This sets the WIDTH and HEIGHT of each grid location
  display_width = 1366
  display_height = 768

  #total_screen_area = display_height*display_width
  #area_of_grid = total_screen_area/num_grids

  #WIDTH = sqrt(area_of_grid)
  #HEIGHT = sqrt(area_of_grid)
  WIDTH = length
  HEIGHT = length

  num_rows = int(display_height/HEIGHT)
  num_cols = int(display_width/WIDTH) 

  #print "total_screen_area ", total_screen_area
  #print "area_of_grid ", area_of_grid
  #print "display_height/HEIGHT ", display_height/HEIGHT
  #print "display_width/WIDTH", display_width/WIDTH

  #print WIDTH, HEIGHT
  #print num_rows, num_cols 

   
  # This sets the margin between each cell
  MARGIN = 1
   
  # Create a 2 dimensional array. A two dimensional
  # array is simply a list of lists.
  grid = np.zeros([num_rows,num_cols])

  # Set row 1, cell 5 to one. (Remember rows and
  # column numbers start at zero.)
  #grid[1][1] = 1
   
  # Initialize pygame
  pygame.init()
   
  # Set the HEIGHT and WIDTH of the screen
  WINDOW_SIZE = [1366,768]
  screen = pygame.display.set_mode(WINDOW_SIZE)
   
  # Set title of screen
  pygame.display.set_caption("Array Backed Grid")
   
  # Loop until the user clicks the close button.
  done = False
   
  # Used to manage how fast the screen updates
  clock = pygame.time.Clock()
  
  # -------- Main Program Loop -----------
  while not done:
      for event in pygame.event.get():  # User did something
          if event.type == pygame.QUIT:  # If user clicked close
              done = True  # Flag that we are done so we exit this loop

          '''
          elif event.type == pygame.MOUSEBUTTONDOWN:
              # User clicks the mouse. Get the position
              pos = pygame.mouse.get_pos()
              # Change the x/y screen coordinates to grid coordinates
              column = pos[0] // (WIDTH + MARGIN)
              row = pos[1] // (HEIGHT + MARGIN)
              # Set that location to one
              grid[row][column] = 1
              print("Click ", pos, "Grid coordinates: ", row, column)
          '''
      pos = pygame.mouse.get_pos()
      # Change the x/y screen coordinates to grid coordinates
      column = pos[0] // (WIDTH + MARGIN)
      row = pos[1] // (HEIGHT + MARGIN)
      # Set that location to one
      grid = np.zeros([num_rows,num_cols])

      if column > (num_cols - 1): column = num_cols - 1
      if row > (num_rows - 1): row = num_rows - 1

      grid[row][column] = 1
      grid_number = row*num_cols+column
      setGridNum(grid_number)

      #print "pos ", pos, " grid ", getGridNum()
         
      # Set the screen background
      screen.fill(BLACK)
   
      # Draw the grid
      for row in range(num_rows):
          for column in range(num_cols):
              color = WHITE
              if grid[row][column] == 1:
                  color = GREEN
              pygame.draw.rect(screen,
                               color,
                               [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
   
      # Limit to 60 frames per second
      clock.tick(10)

      # Go ahead and update the screen with what we've drawn.
      pygame.display.flip()
      with open("current_grid", "w") as text_file:
        text_file.write("%d" % getGridNum())
   
  # Be IDLE friendly. If you forget this line, the program will 'hang'
  # on exit.
  pygame.quit()


if __name__ == '__main__':
  if len(argv)>1:
    run(int(argv[1]))
  else:
    run(330)