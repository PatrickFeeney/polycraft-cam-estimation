import matplotlib.pyplot as plt


def plot_projection(image_name, proj_points):
    im = plt.imread(image_name)
    plt.imshow(im)
    plt.scatter(proj_points[0], proj_points[1], color=[1, 0, 0, .5])
    plt.show()
