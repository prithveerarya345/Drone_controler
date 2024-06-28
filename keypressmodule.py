# This code is based on the tutorial by Murtaza's Workshop - Robotics and AI
# Tutorial: https://youtu.be/LmEcyQnfpDA

import pygame

def init():
    """Initialize Pygame and create a window"""
    pygame.init()
    win = pygame.display.set_mode((400, 400))
     
def getKey(keyName):
    """Check if a specific key is pressed"""
    ans = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans

def main():
    """Main function for testing key presses"""
    if getKey("LEFT"):
        print("Left key pressed")
    if getKey("RIGHT"):
        print("Right key pressed")
    
if __name__ == '__main__':
    init()
    while True:
        main()