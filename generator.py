import os
import sys

import cv2
import numpy as np
from sklearn.cluster import KMeans


class DominantColors():
    def __init__(self):
        self.IMAGE_PATH = None
        self.IMAGE = None
        self.CLUSTERS = 5
        self.LABELS = None
        self.MODE = "gradient" # gradient or frequency

    def get_dominant_colors(self):
        img = self.IMAGE = cv2.imread(self.IMAGE_PATH)
        # reshape to a list of pixels
        pixels = img.reshape((img.shape[0] * img.shape[1], 3))
        # use k-means to cluster pixels
        clt = KMeans(n_clusters=self.CLUSTERS, n_init=10)
        clt.fit(pixels)
        # save labels for calculating frequency count later
        self.LABELS = clt.labels_
        # dominant colors are cluster centers
        return clt.cluster_centers_

    def create_bar(self, width, color):
        bar = np.zeros((width, width, 3), np.uint8)
        bar[:] = color
        return bar

    def create_output_image(self, colors):
        bars = []
        height, width = self.IMAGE.shape[0], self.IMAGE.shape[1]
        bar_width = width // self.CLUSTERS

        for color in colors:
            # create a square bar for each color
            bar = self.create_bar(bar_width, color)
            bars.append(bar)

        # stack all squares together
        palette = np.hstack(bars)
        # stack the img and its palette together
        resized_img = cv2.resize(self.IMAGE, (bar_width * self.CLUSTERS, height))
        return np.vstack([resized_img, palette])

    def bgr_to_rgb(self, colors):
        for color in colors:
            color[0], color[1], color[2] = color[2], color[1], color[0]

    def generate_color_palette(self):
        print("Running color palette generator...")
        colors = np.uint8(self.get_dominant_colors())

        # sort colors based on the current mode
        if self.MODE == "gradient":
            colors = sorted(colors, key=lambda x: sum(x))
        if self.MODE == "frequency":
            label_counts = np.unique(self.LABELS, return_counts=True)[1]
            sorted_indices = np.argsort(label_counts)[::-1]
            colors = colors[sorted_indices]

        # generate output image
        output = self.create_output_image(colors)
        cv2.imwrite("output.jpg", output)
        print(f"Output image is saved to: {os.getcwd()}/")

        print("The dominant colors are:")
        # OpenCV uses BGR instead of RGB
        self.bgr_to_rgb(colors)
        # print rgb values based on the current mode
        if self.MODE== "gradient":
            for i, color in enumerate(colors):
                print(f"{i + 1}. {tuple(color)}")
        if self.MODE == "frequency":
            num_pixels = sum(label_counts)
            for i, color in enumerate(colors):
                size = label_counts[sorted_indices[i]]
                frequency = round(size / num_pixels, 2)
                print(f"{i + 1}: {tuple(color)} Frequency: {frequency}")

        cv2.imshow("output", output)
        cv2.waitKey(0)


def main():
    args = sys.argv
    if len(args) == 1:
        print("Error: Please specify the path to your input image")
        sys.exit(1)
    generator = DominantColors()
    generator.IMAGE_PATH = args[1]
    generator.generate_color_palette()


if __name__ == '__main__':
    main()
