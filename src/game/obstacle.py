import math as m
import numpy as np
import pygame

class Circle:
    """
    Class for defining obstacles
    """
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour

    def draw(self):
        pygame.draw.circle()


class Rectangle:
    """
    Rectangle class which serves as an obstacle
    """
    def __init__(self, x, y, width, height, colour, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.id = id
    
    def __repr__(self):
        return str(self.id)

    def draw(self, screen):
        """
        Draws the rectangle on to the screen
        """
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), 0)

    def move(self, x_change, y_change):
        if self.id == 2:
            self.x += x_change
            self.y += y_change