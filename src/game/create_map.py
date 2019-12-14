from src.game.obstacle import Rectangle, Circle

def create_map():
    """
    Returns an array of randomly placed and sized obstacles (shapes)
    that will serve as map/obstacle course for the agents to traverse through
    wihtou any collisions.
    """
    obstacles = []
    # make sure id (last argument of obstacle) is unique
    # obstacles.append(Circle(300, 300, 65, (0, 0, 255), 1))
    obstacles.append(Circle(500, 300, 85, (0, 0, 255), 2))
    return obstacles
