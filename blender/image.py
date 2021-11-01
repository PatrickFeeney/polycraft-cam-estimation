import numpy as np
from PIL import Image


def image_to_np(img_path):
    # create numpy array with grayscale image data
    render_img = np.asarray(Image.open(img_path)).copy()
    # threshold values
    render_img[render_img < 128] = 0
    render_img[render_img >= 128] = 255
    return render_img


def image_error(img1, img2):
    return (np.abs(img1 - img2) / 255).sum()
