import math as m
import time
import pygame
import numpy as np

from src.utils.math_tools import liangbarsky, get_distance
from src.common.constants import GameSettings

class Agent:
    """
    This class defines the intelligent agent for this project and handles it's
    primary functions such as movment, visual updates, interfacing with sensors
    fitness evalutation and dying.
    """
    death_count = 0

    def __init__(self, x, y, size, field_of_view, nb_sensors, max_range, manager, brain):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.size = size
        self.colour = (255, 255, 255)
        self.max_range = max_range
        self.sensors = []
        self.angle = 0  # agent's orientation
        self.manager = manager
        self.base_speed = 5
        self.alive = True
        self.brain = brain
        self.fitness = 0
        self.time_alive = time.time()
        self.considered = False
        self.hit_target = False
        self._attach_sensors(field_of_view, nb_sensors, max_range)

    def move(self, x_change, y_change):
        """
        Handles the movement of the agent based on the output of the neural network.
        The neural network outputs two values based on the sensor reading inputs.
        One output controls the speed and the other controls the direction.
        """
        if self.alive:
            brain_output = self.brain.forward(
                [(sensor.reading / self.max_range) for sensor in self.sensors])
            speed = brain_output[0]
            angle = brain_output[1]
            self.angle = np.interp(angle, [-1, 1], [-60, 60])
            self.x += self.base_speed * speed * (m.cos(m.radians(self.angle)))
            self.y += self.base_speed * speed * (m.sin(m.radians(self.angle)))

    def update(self, screen, obstacles):
        """
        Responsible for drawing the agent onto the screen after it's position
        has been updated by the move function. Also check's if the agent has been
        alive longer than a specified threshold and kills it if it has.
        """
        if self.alive:
            pygame.draw.circle(screen, self.colour,
                               (int(self.x), int(self.y)), self.size, 0)
            for sensor in self.sensors:
                sensor.update()
                sensor.draw(screen)
                for obstacle in obstacles:
                    self._collide(obstacle)
                    if sensor.in_range(obstacle):
                        sensor.detect(screen, obstacle)
                    else:
                        if sensor.activated and sensor.current_obstacle == obstacle.id:
                            sensor.handle_obstacle_exit()
        # if time.time() - self.time_alive > 4:
        #     self.alive = False

    def _collide(self, obstacle):
        """
        Checks for collision between the agent and the obstacle, or
        between agent and map boundary. If there is a collision, the agent is killed.
        """
        if self.alive:
            if self.x <= 10 or self.y <= 10 or self.y >= GameSettings.HEIGHT - 20 \
                or self.x >= GameSettings.WIDTH - 20:
                self.alive = False
                Agent.death_count += 1
            delta_x = self.x - max(obstacle.x, min(self.x, obstacle.x + obstacle.width))
            delta_y = self.y - max(obstacle.y, min(self.y, obstacle.y + obstacle.height))
            if ((delta_x**2) + (delta_y**2)) < self.size**2:
                self.alive = False
                Agent.death_count += 1

    def evaluate_fitness(self):
        """
        Scores the agent based on how well it performed on the task.
        """
        pass

    def _attach_sensors(self, field_of_view, nb_sensors, max_range):
        interval = field_of_view / nb_sensors
        angle = 0
        for i in range(nb_sensors):
            self.sensors.append(Sensor(self, angle, max_range, i))
            angle += interval


class Sensor:
    """
    This class defines the sensors that the agent uses to detect distance
    to nearby obstacles. It is the readings from these sensors that are then passed
    in as the input the neural network controlling the agent. The sensors in this project
    are represented as straight line segments with origin and end coordinates of
    (x0, y0) and (x1, y1) respectively. In order to detect distance we then use some simple
    mathematics to check for intersection between this line segment and other shapes (obstacles).
    """

    def __init__(self, agent, angle, max_range, tag):
        self.agent = agent
        self.angle = angle
        self.max_range = max_range
        self.reading = self.max_range
        self.tag = tag
        self.x0 = self.x1 = self.y0 = self.y1 = 0
        self.activated = False
        self.current_obstacle = None
        self.engaged_obstacles = []

    def update(self):
        """
        Updates the position of the sensor in accordance with the position of the agent, 
        such that the sensor is always 'attached' to the body of the agent.
        """
        self.x0 = self.agent.x + self.agent.size * \
            m.cos(m.radians(self.angle + self.agent.angle))
        self.y0 = self.agent.y + self.agent.size * \
            m.sin(m.radians(self.angle + self.agent.angle))
        self.x1 = self.agent.x + (self.agent.size + self.max_range) * \
            m.cos(m.radians(self.angle + self.agent.angle))
        self.y1 = self.agent.y + (self.agent.size + self.max_range) * \
            m.sin(m.radians(self.angle + self.agent.angle))

    def draw(self, screen):
        """
        Draws the actual sensor onto the screen
        """
        if self.tag == 0:
            # draws a black line to help identify the orientation of the robot
            pygame.draw.line(screen, (0, 0, 0), (self.agent.x, self.agent.y), (self.x0, self.y0))
        if not self.activated:
            pygame.draw.circle(screen, (0, 255, 0), (int(self.x1), int(self.y1)), 1, 0)
            # pygame.draw.line(screen, (0, 255, 0), (self.x0, self.y0), (self.x1, self.y1))

    def detect(self, screen, obstacle):
        """
        Implementation of Liang-Barsky line clipping algorithm to
        detect whether a line segment (the sensor) has intersected with an
        obstacle, in this case a rectangle.
        """
        collision_pts = self._detect_rectangle(obstacle)
        if self.current_obstacle and self.current_obstacle != obstacle.id:
            self._handle_additional_obstacle(obstacle, collision_pts)
        else:
            x_coll, y_coll, _, _ = collision_pts
            self.reading = get_distance((self.x0, self.y0), (x_coll, y_coll))
            pygame.draw.line(screen, (255, 0, 0), (self.x0, self.y0), (x_coll, y_coll))
            pygame.draw.circle(screen, (255, 0, 0), (int(x_coll), int(y_coll)), 1, 0)
            self.activated = True
            self.current_obstacle = obstacle.id

    def _handle_additional_obstacle(self, obstacle, collision_pts):
        """
        When an obstacle intersects a sesnor that is already activated (by another obstacle)
        this function checks to determine which obstacle is closer to the sensor and updates
        the sensor reading and current obstacle variable accordingly.
        """
        x_coll, y_coll, _, _ = collision_pts
        new_reading = get_distance((self.x0, self.y0), (x_coll, y_coll))
        if new_reading < self.reading:
            self.current_obstacle = obstacle.id
            self.reading = new_reading

    def handle_obstacle_exit(self):
        """
        Resets sensor and the current obstacle variable
        when the obstacle that initially activated the sensor has disengaged.
        """
        if len(self.engaged_obstacles) > 1:
            readings = []
            for obstacle in self.engaged_obstacles:
                # find closest, set reading to that one
                coll = self._detect_rectangle(obstacle)
                if coll:
                    x_coll, y_coll, _, _ = coll
                    distance = get_distance((self.x0, self.y0), (x_coll, y_coll))
                    readings.append(distance)
                    lowest_reading_idx = readings.index(min(readings))
                    self.reading = readings[lowest_reading_idx]
                    self.current_obstacle = None
        elif len(self.engaged_obstacles) == 1:
            # get distance of only obstacle set reading to that
            coll = self._detect_rectangle(self.engaged_obstacles[0])
            if coll:
                x_coll, y_coll, _, _ = coll
                distance = get_distance((self.x0, self.y0), (x_coll, y_coll))
                self.reading = distance
                self.current_obstacle = None
        else:
            self.activated = False
            self.reading = self.max_range
            self.current_obstacle = None

    def in_range(self, obstacle):
        """
        Return true if the obstacle intersects with the sensor
        and false otherwise.
        """
        collision = self._detect_rectangle(obstacle)
        if collision:
            if obstacle not in self.engaged_obstacles:
                self.engaged_obstacles.append(obstacle)
            return True
        else:
            if obstacle in self.engaged_obstacles:
                self.engaged_obstacles.remove(obstacle)
            return False

    def _detect_rectangle(self, rectangle):
        """
        Uses the Liang-Barsky line clipping algorithm to
        detect intersections between a line segment (the sensor) and an
        obstacle, in this case a rectangle. Returns the coordinates of the intersction.
        """
        x_min = rectangle.x
        x_max = rectangle.x + rectangle.width
        y_min = rectangle.y
        y_max = rectangle.y + rectangle.height
        collision_pts = liangbarsky(x_min, y_max, x_max, y_min, self.x0, self.y0, self.x1, self.y1)
        return collision_pts
