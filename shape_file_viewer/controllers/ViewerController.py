import json

import matplotlib

from shape_file_viewer.repositories.ShapeFileRepository import ShapeFileRepository

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


class ViewerController:
    """
    Loads and displays the shape file in matplotlib.
    """

    def __init__(self, path):
        self.fig, self.axs = plt.subplots(1, 1)
        self.fig.canvas.set_window_title('Shapefile Viewer')
        self.repo = ShapeFileRepository(path)

    def run(self):
        features = self.repo.read()
        for points in features:
            self.axs.plot(points[:, 0], points[:, 1])
            self.axs.scatter(points[:, 0], points[:, 1])
        plt.show()
