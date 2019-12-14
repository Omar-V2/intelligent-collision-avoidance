import pygame

def display_text(screen, text, y):
    """
    A function that displays text to the screen for debugging 
    purposes.
    """
    font = pygame.font.Font('freesansbold.ttf', 10) 
    text = font.render(text, True, (255, 255, 255), (0, 0, 0)) 
    text_rect = text.get_rect()
    text_rect.center = (800, y)
    screen.blit(text, text_rect)
