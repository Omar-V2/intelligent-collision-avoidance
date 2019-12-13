import random
import time
import pickle
import pygame
from src.game.obstacle import Rectangle, Circle
from src.game.pedestrian import Pedestrian

def create_map():
    """
    Returns an array of obstacles (shapes)
    that will serve as map/obstacle course for the agents to traverse through
    wihtout any collisions.
    """
    obstacles = []
    # make sure id (last argument of obstacle) is unique
    obstacles.append(Circle(300, 300, 65, (0, 0, 255), 1))
    obstacles.append(Circle(500, 300, 85, (0, 0, 255), 2))
    return obstacles

def create_pedestrians():
    """
    Creates pedestrian objects and provides them with their
    correct trajectory
    """
    # CHANGE THIS, work out how to make path relative
    path = "/Users/omardiab/Code/collision-avoidance/src/game/trajectories.p"
    trajectories = pickle.load(open(path, "rb"))
    pedestrians = []
    for pedestrian, trajectory in trajectories.items():
        pedestrians.append(Pedestrian(trajectory, pedestrian))
    return pedestrians

def update_target():
    """
    Generates a new location for the target
    """
    x_pos = random.randint(100, 900)
    y_pos = random.randint(100, 500)
    return x_pos, y_pos
