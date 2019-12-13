import random
import pygame
from src.game.obstacle import Circle
from src.common.constants import GameSettings

class Pedestrian(Circle):
    """
    a class to serve as a Pedestrian and include a move method which
    moves the pedestrian according to a predefined trajectory based on real
    data.
    """
    def __init__(self, trajectory, id):
        self.x_coords = trajectory[0]
        self.y_coords = trajectory[1]
        self.destination = 0
        self.x = self.x_coords[self.destination] + (GameSettings.WIDTH / 2)
        self.y = self.y_coords[self.destination] + (GameSettings.HEIGHT / 2)
        self.radius = 10
        self.colour = (random.randint(20, 255), random.randint(20, 255), random.randint(20, 255))
        self.id = id
        self.finished = False

    def move(self):
        """
        Responsible for making the pedestrian move based on their
        trajectory (a list of x,y coordinates).
        """
        if self.destination == len(self.x_coords) - 1:
            self.finished = True
        else:
            self.x = self.x_coords[self.destination] + (GameSettings.WIDTH / 2)
            self.y = self.y_coords[self.destination] + (GameSettings.HEIGHT / 2)
            self.destination += 1

    def draw(self, screen):
        """
        Draws the pedestrian provided they have not finished their trajectory.
        """
        if not self.finished:
            super().draw(screen)

class PedestrianManager:
    """
    A class to manage an array of pedestrians which will serve as the current obstacles,
    once a pedestrian has finished its trajectory, it will be removed from the array and a new
    pedestrian will be introudced.
    """
    def __init__(self, all_pedestrians, limit):
        self.all_pedestrians = all_pedestrians
        self.limit = limit
        self.current_pedestrians = all_pedestrians[:limit]
        self.next_pedestrian_idx = limit

    def _add(self):
        if self.next_pedestrian_idx != len(self.all_pedestrians) - 1:
            next_pedestrian = self.all_pedestrians[self.next_pedestrian_idx]
            self.current_pedestrians.append(next_pedestrian)
            self.next_pedestrian_idx += 1

    def _remove(self, pedestrian):
        self.current_pedestrians.remove(pedestrian)

    def update(self, pedestrian):
        if pedestrian.finished:
            self._remove(pedestrian)
            self._add()
