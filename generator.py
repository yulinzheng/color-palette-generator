import sys

import cv2
import numpy as np
from sklearn.cluster import KMeans


class DominantColors():
    def __init__(self):
        self.IMAGE = None
        self.CLUSTERS = 5
        self.MODE = "gradient"

    def create_bar(self, width, color):
        bar = np.zeros((width, width, 3), np.uint8)
        bar[:] = color
        # OpenCV uses BGR instead of RGB
        r, g, b = color[2], color[1], color[0]
        return bar, (r, g, b)

    def generate_color_palette(self):
        print("Running color palette generator...")
        # read image
        img = cv2.imread(self.IMAGE)
        height, width = img.shape[0], img.shape[1]
        # reshape to a list of pixels
        pixels = img.reshape((img.shape[0] * img.shape[1], 3))
        # use k-means to cluster pixels
        clt = KMeans(n_clusters=self.CLUSTERS, n_init=10)
        clt.fit(pixels)
        # dominant colors are cluster centers
        colors = clt.cluster_centers_

        bars = []
        rgb_values = []
        bar_width = width // self.CLUSTERS

        for color in colors:
            # create a square bar for each color
            bar, rgb = self.create_bar(bar_width, color)
            bars.append(bar)
            rgb_values.append(rgb)

        # stack all squares together
        palette = np.hstack(bars)
        # stack the img and its palette together
        resized_img = cv2.resize(img, (bar_width * self.CLUSTERS, height))
        output = np.vstack([resized_img, palette])

        cv2.imshow("output", output)
        cv2.waitKey(0)


def main():
    args = sys.argv

    if len(args) == 1:
        print("Error: Please specify the path to your input image")
        sys.exit(1)

    generator = DominantColors()
    generator.IMAGE = args[1]
    if len(args) == 3:
        generator.CLUSTERS = int(args[2])

    generator.generate_color_palette()


if __name__ == '__main__':
    main()
