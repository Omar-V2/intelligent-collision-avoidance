import math as m
import time
import pygame
import numpy as np

from src.utils.math_tools import liangbarsky, get_distance


class Agent:
    """
    This class defines the intelligent agent for this project and handles it's
    primary functions such as movment, visual updates, interfacing with sensors
    fitness evalutation and dying.
    """

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
        One input controlles the speed and the other controlles the direction.
        """
        if self.alive:
            self.x += x_change
            self.y += y_change
            # brain_output = self.brain.forward(
            #     [(sensor.reading / self.max_range) for sensor in self.sensors])
            # speed = brain_output[0]
            # angle = brain_output[1]
            # self.angle = np.interp(angle, [-1, 1], [-60, 60])
            # self.x += self.base_speed * speed * (m.cos(m.radians(self.angle)))
            # self.y += self.base_speed * speed * (m.sin(m.radians(self.angle)))

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
                    if sensor.in_range(obstacle):
                        sensor.detect(screen, obstacle)
                    else:
                        if sensor.activated and sensor.current_obstacle == obstacle.id:
                            sensor.reading = sensor.max_range
                            sensor.activated = False
                print(f"Sensor {sensor.tag} is: {sensor.reading}")
        # if time.time() - self.time_alive > 4:
        #     self.alive = False

    def collide(self):
        pass

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
        if collision_pts:
            self.activated = True
            self.current_obstacle = obstacle.id
            x_coll, y_coll, _, _ = collision_pts
            self.reading = get_distance((self.x0, self.y0), (x_coll, y_coll))
            pygame.draw.circle(screen, (0, 255, 0), (int(x_coll), int(y_coll)), 1, 0)
        else:
            print("here")*20
            # pass
            self.activated = False
            self.reading = self.max_range
    
    def in_range(self, obstacle):
        collision = self._detect_rectangle(obstacle)
        if collision:
            return True
        return False

    def _detect_rectangle(self, rectangle):
        """
        Implementation of Liang-Barsky line clipping algorithm to
        detect whether a line segment (the sensor) has intersected with an
        obstacle, in this case a rectangle.
        """
        # rectangle in pygame defined (start_x, start_y, width, height)
        # origin is y_max left corner of screen, left ---> x_max is positive x
        # and y_max to y_min is positve y.
        x_min = rectangle.x
        x_max = rectangle.x + rectangle.width
        y_min = rectangle.y
        y_max = rectangle.y + rectangle.height
        collision_pts = liangbarsky(x_min, y_max, x_max, y_min, self.x0, self.y0, self.x1, self.y1)
        return collision_pts





if __name__ == "__main__":
    line = [-5, 3, 15, 9]
    rectangle = [0, 0, 10, 10]
    # print(detect_rectangle(rectangle, line))
    # print(liangbarsky(0, 10, 10, 0, -5, 3, 15, 9))
    # print(liangbarsky(5, 9, 9, 5, 4, 12, 8, 8))
    print(liangbarsky(230, 400, 430, 200, 185, 300, 260, 300))