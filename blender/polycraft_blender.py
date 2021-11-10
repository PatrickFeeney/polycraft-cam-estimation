from math import radians
from pathlib import Path
import sys

import bpy
import mathutils

import numpy as np

sys.path.append(".")

from image import image_to_np, image_error
import polycraft_json


def load_scene(filepath="base_scene.blend"):
    # load base scene
    bpy.ops.wm.open_mainfile(filepath=filepath)


def create_prefab(prefab, pt):
    x, y, z = pt
    name = "%i, %i, %i" % (x, y, z)
    obj = bpy.data.objects.new(name=name, object_data=prefab)
    obj.location = pt
    # get layer used for rendering and link object
    view_layer = bpy.context.view_layer
    view_layer.active_layer_collection.collection.objects.link(obj)


def load_env(json_name, include_blocks):
    # get prefab references
    norm_cube = bpy.data.objects["NormalCube"].data
    # add prefab cubes to the scene
    pts = polycraft_json.get_p_json_pts(json_name, include_blocks)
    for pt in pts.T:
        create_prefab(norm_cube, pt)


def load_cam(json_name, fov_degrees=70.8, player_y_offset=1.1):
    # import camera parameters
    player_pos, yaw, pitch = polycraft_json.get_p_json_cam(json_name)
    player_pos[1] += player_y_offset
    # get camera reference and update settings
    cam = bpy.context.scene.camera
    cam.location = player_pos
    cam.rotation_euler = mathutils.Euler((radians(pitch), radians(180 - yaw), 0), "ZYX")
    cam.data.angle = radians(fov_degrees)


def render_to_np():
    # render image and save temporarily
    render_path = "temp.png"
    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(render_path)
    np_render = image_to_np(render_path)
    # remove temp file
    Path(render_path).unlink()
    return np_render


# search space for parameters
n_fov = 10
n_y_offset = 10
fov_grid, y_offset_grid = np.meshgrid(
    np.linspace(65, 80, num=n_fov),
    np.linspace(1, 1.2, num=n_y_offset),
    indexing="ij",
)
# data to use
data_nums = [1, 7, 50, 52, 90]

for data_num in data_nums:
    # get file paths and load label
    unlabeled_data = Path("../unlabeled_data")
    json_name = unlabeled_data / ("%i.json" % (data_num, ))
    labeled_data = Path("../manual_segments/crafting_table")
    label_img = image_to_np(labeled_data / ("%i.png" % (data_num, )))
    # load Polycraft data into Blender scene
    load_scene()
    load_env(json_name, ["minecraft:crafting_table"])
    for i in range(n_fov):
        for j in range(n_y_offset):
            load_cam(json_name, fov_grid[i, j], y_offset_grid[i, j])
            # render and compare to label
            np_render = render_to_np()
            print(image_error(label_img, np_render))
