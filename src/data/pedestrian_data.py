import pickle
import matplotlib.pyplot as plt
import pandas as pd

COLUMN_NAMES = ['time', 'person id', 'x', 'y', 'z', 'velocity', 'angle of motion', 'facing angle']
DATA = pd.read_csv('pedestrian-data.csv', header=None, names=COLUMN_NAMES)

def get_trajectories(data):
    """
    Returns a dictionary with the key being the
    person id and the value being a list of lists
    containing the (x, y) coordinates of each person
    in a format as such {person id: [[x_coords], [y_coords]]}
    """
    trajectories = {}
    all_people = data['person id']
    people_array = all_people.unique()
    people_list = list(set(all_people.values))
    for person in people_array:
        trajectory = data.loc[all_people == person]
        print(trajectory.head)
        # convert from mm to cm, negative for y because pygame defines downards y as positve
        x_coords = trajectory['x'].values / 100.0
        y_coords = -trajectory['y'].values / 100.0
        coordinates = [x_coords, y_coords]
        trajectories[person] = coordinates
    return trajectories

def visiualise_trajectories(trajectories):
    """
    Plots trajectory path of all people to show the
    path they took whilst in the mall.
    """
    for coords in trajectories.values():
        x = coords[0]
        y = coords[1]
        plt.plot(x, y)
    plt.show()

def main():
    trajectories = get_trajectories(DATA)
    pickle.dump(trajectories, open("trajectories.p", "wb"))
    visiualise_trajectories(trajectories)

if __name__ == "__main__":
    main()
