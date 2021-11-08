from math import radians
from pathlib import Path
import sys

import bpy
import mathutils

sys.path.append(".")

from image import image_to_np, image_error

sys.path.append("..")

import polycraft_json


# load base scene
bpy.ops.wm.open_mainfile(filepath="base_scene.blend")
# get layer used for rendering
view_layer = bpy.context.view_layer
# get camera reference
cam = bpy.context.scene.camera
# get prefab references
norm_cube = bpy.data.objects["NormalCube"].data


def create_prefab(prefab, pt):
    x, y, z = pt
    name = "%i, %i, %i" % (x, y, z)
    obj = bpy.data.objects.new(name=name, object_data=prefab)
    obj.location = pt
    view_layer.active_layer_collection.collection.objects.link(obj)


def load_env(json_name, include_blocks):
    # add prefab cubes to the scene
    pts = polycraft_json.get_p_json_pts(json_name, include_blocks)
    for pt in pts.T:
        create_prefab(norm_cube, pt)


def load_cam(json_name, fov_degrees=70.8, player_y_offset=1.1):
    # import camera parameters
    player_pos, yaw, pitch = polycraft_json.get_p_json_cam(json_name)
    player_pos[1] += player_y_offset
    cam.location = player_pos
    cam.rotation_euler = mathutils.Euler((radians(pitch), radians(180 - yaw), 0), "ZYX")
    cam.angle = radians(fov_degrees)


def render_to_np():
    # render image and save temporarily
    render_path = "temp.png"
    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(render_path)
    np_render = image_to_np(render_path)
    # remove temp file
    Path(render_path).unlink()
    return np_render


# get file paths and load label
data_num = 1
unlabeled_data = Path("../unlabeled_data")
json_name = unlabeled_data / ("%i.json" % (data_num, ))
labeled_data = Path("../manual_segments/crafting_table")
label_img = image_to_np(labeled_data / ("%i.png" % (data_num, )))
# load Polycraft data
load_env(json_name, ["minecraft:crafting_table"])
load_cam(json_name)
# render and compare to label
np_render = render_to_np()
print(image_error(label_img, np_render))
