from pathlib import Path
import sys

import numpy as np
import pandas as pd

sys.path.append(".")

from image import image_to_np, image_error
import polycraft_json
import polycraft_blender


if __name__ == "__main__":
    # search space for parameters
    n_fov = 10
    n_y_offset = 10
    fovs = np.linspace(71, 71.6, num=n_fov)
    y_offsets = np.linspace(1.10, 1.13, num=n_y_offset)
    # data to use
    data_nums = [1, 7, 50, 52, 90]
    # store output in array
    im_errors = np.empty((n_fov * n_y_offset, len(data_nums) + 2))

    for i, data_num in enumerate(data_nums):
        # get file paths and load label
        unlabeled_data = Path("../unlabeled_data")
        json_name = unlabeled_data / ("%i.json" % (data_num, ))
        p_json = polycraft_json.load_json(json_name)
        labeled_data = Path("../manual_segments/crafting_table")
        label_img = image_to_np(labeled_data / ("%i.png" % (data_num, )))
        # load Polycraft data into Blender scene
        polycraft_blender.load_scene()
        polycraft_blender.load_env(p_json, ["minecraft:crafting_table"])
        for j, fov in enumerate(fovs):
            for k, y_offset in enumerate(y_offsets):
                polycraft_blender.load_cam(p_json, fov, y_offset)
                # render and compare to label
                np_render = polycraft_blender.render_to_np()
                im_error = image_error(label_img, np_render)
                # store output
                row = j * n_y_offset + k
                im_errors[row, 0] = fov
                im_errors[row, 1] = y_offset
                im_errors[row, i + 2] = im_error
    # calculate means
    im_error_means = np.mean(im_errors[:, 2:], axis=1)
    im_errors = np.insert(im_errors, [2], im_error_means[:, np.newaxis], axis=1)
    # save output
    data_nums_str = [str(num) for num in data_nums]
    im_errors_df = pd.DataFrame(im_errors, columns=["FoV", "Y-Offset", "Mean IoU", *data_nums_str])
    im_errors_df.to_csv("cam_param_search.csv", index=False)
