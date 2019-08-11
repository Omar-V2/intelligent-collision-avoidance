from src.game.obstacle import Rectangle, Circle

def create_map():
    """
    Returns an array of randomly placed and sized obstacles (shapes)
    that will serve as map/obstacle course for the agents to traverse through
    wihtou any collisions.
    """
    obstacles = []
    # make sure id (last argument of obstacle) is unique
    # obstacles.append(Rectangle(280, 125, 300, 50, (0, 0, 255), 1)) # two long ones side
    # obstacles.append(Rectangle(280, 475, 300, 50, (0, 0, 255), 2)) # two long ones side
    # obstacles.append(Rectangle(380, 260, 50, 120, (0, 0, 255), 3))
    # obstacles.append(Rectangle(280, 200, 50, 80, (0, 0, 255), 4))
    # obstacles.append(Rectangle(280, 320, 50, 130, (0, 0, 255), 5))
    # obstacles.append(Rectangle(580, 200, 50, 80, (0, 0, 255), 6))
    # obstacles.append(Rectangle(580, 320, 50, 130, (0, 0, 255), 7))
    # obstacles.append(Rectangle(400, 150, 50, 200, (0, 0, 255), 1))
    obstacles.append(Circle(300, 300, 65, (0, 0, 255), 1))
    obstacles.append(Circle(500, 300, 85, (0, 0, 255), 2))
    return obstacles
