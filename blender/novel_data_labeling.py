from pathlib import Path
import sys

import numpy as np
import pandas as pd

sys.path.append(".")

from image import percent_novel
import polycraft_json
import polycraft_blender


if __name__ == "__main__":
    fov, y_offset = 71.26666666666667, 1.1066666666666667
    data_dir = Path("../../polycraft-dataset")
    ids = []
    percents = []
    for task_dir in data_dir.iterdir():
        if task_dir.stem == "normal" or not task_dir.is_dir():
            continue
        task_id = task_dir.stem
        run_dir_count = 0
        for run_dir in task_dir.iterdir():
            run_dir_count += 1
            print("Task %s run %i" % (task_id, run_dir_count))
            run_id = run_dir.stem
            for file in run_dir.iterdir():
                if file.suffix != ".json":
                    continue
                file_id = file.stem
                # get file paths and load label
                p_json = polycraft_json.load_json(file)
                # load Polycraft data into Blender scene
                polycraft_blender.load_scene()
                polycraft_blender.load_env(p_json, ["minecraft:fence"])
                polycraft_blender.load_cam(p_json, fov, y_offset)
                # render and determine if novel
                np_render = polycraft_blender.render_to_np()
                percent = percent_novel(np_render)
                # store output
                ids.append(task_id + "/" + run_id + "/" + file_id)
                percents.append(percent)
    # sort output
    ids = np.array(ids)
    percents = np.array(percents)
    order = np.argsort(ids)
    ids = ids[order]
    percents = percents[order]
    # save output
    label_df = pd.DataFrame({
        "id": ids,
        "novel_percent": percents,
    })
    label_df.to_csv("targets.csv", index=False)
