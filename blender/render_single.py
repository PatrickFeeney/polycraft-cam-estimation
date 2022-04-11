from pathlib import Path
import sys

sys.path.append(".")

import polycraft_json
import polycraft_blender


if __name__ == "__main__":
    # details of render
    json_path = Path("item_quartz_block/6/6.json")
    novel_block = "minecraft:quartz_block"
    # constants
    fov, y_offset = 71.26666666666667, 1.1066666666666667
    data_dir = Path("../../polycraft-dataset")
    # get file paths and load label
    p_json = polycraft_json.load_json(data_dir / json_path)
    print(polycraft_json.get_p_json_pts(p_json)[1])
    # load Polycraft data into Blender scene
    polycraft_blender.load_scene()
    polycraft_blender.load_env(p_json, [novel_block])
    polycraft_blender.load_cam(p_json, fov, y_offset)
    polycraft_blender.render_to_file("temp.png")
