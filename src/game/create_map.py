from src.game.obstacle import Rectangle, Circle

def create_map():
    """
    Returns an array of randomly placed and sized obstacles (shapes)
    that will serve as map/obstacle course for the agents to traverse through
    wihtou any collisions.
    """
    obstacles = []
    obstacles.append(Rectangle(280, 125, 100, 50, (0, 0, 255), 1))
    obstacles.append(Rectangle(280, 425, 100, 50, (0, 0, 255), 1))
    obstacles.append(Rectangle(280, 210, 50, 150, (0, 0, 255), 1))
    return obstacles
