import math as m
import numpy as np
import pygame

from src.utils.math_tools import liangbarsky

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

    def collide(self, agent):
        pass

    def intersect(self, sensor):
        pass


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

    def collide(self, agent):
        """
        Returns True if the agent has collided with the rectangle
        and False otherwise.
        """
        delta_x = agent.x - max(self.x, min(agent.x, self.x + self.width))
        delta_y = agent.y - max(self.y, min(agent.y, self.y + self.height))
        if ((delta_x**2) + (delta_y**2)) < agent.size**2:
            return True
        return False

    def intersect(self, sensor):
        """
        Uses the Liang-Barsky line clipping algorithm to
        detect intersections between a line segment (the sensor) and an
        obstacle, in this case a rectangle. Returns the coordinates of the intersction.
        """
        x_min = self.x
        x_max = self.x + self.width
        y_min = self.y
        y_max = self.y + self.height
        intersection_pts = liangbarsky(x_min, y_max, x_max, y_min, sensor.x0, sensor.y0, sensor.x1, sensor.y1)
        return intersection_pts

    def move(self, x_change, y_change):
        if self.id == 2:
            self.x += x_change
            self.y += y_change