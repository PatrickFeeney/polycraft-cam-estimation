import numpy as np
from PIL import Image


def image_to_np(img_path):
    # create numpy array with grayscale image data
    img = np.asarray(Image.open(img_path), dtype=np.int32).copy()
    while len(img.shape) > 2:
        img = img[:, :, 0]
    # threshold values
    img[img < 128] = 0
    img[img >= 128] = 255
    return img


def image_error(img1, img2):
    # intersection over union
    intersect = img1
    intersect[img2 < 1] = 0
    union = img1
    union[img2 > 0] = 1
    if np.sum(union) == 0:
        return 1
    return np.sum(intersect)/np.sum(union)
