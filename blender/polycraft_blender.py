from math import radians
from pathlib import Path
import sys

import bpy
import mathutils

from image import image_to_np

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


def load_env(json_name, ignore_blocks=["air"]):
    # add prefab cubes to the scene
    pts = polycraft_json.get_p_json_pts(json_name)
    for pt in pts.T:
        create_prefab(norm_cube, pt)


def load_cam(json_name, player_y_offset=1.1):
    # import camera parameters
    player_pos, yaw, pitch = polycraft_json.get_p_json_cam(json_name)
    player_pos[1] += player_y_offset
    cam.location = player_pos
    cam.rotation_euler = mathutils.Euler((radians(pitch), radians(180 - yaw), 0), "ZYX")


def render_to_np():
    # render image and save temporarily
    render_path = Path("temp.png")
    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(render_path)
    np_render = image_to_np(render_path)
    # remove temp file
    render_path.unlink()
    return np_render


# get file paths
data_num = 1
data_folder = Path("../unlabeled_data")
json_name = data_folder / ("%i.json" % (data_num, ))
image_name = data_folder / ("%i.png" % (data_num, ))
# load Polycraft data
load_env(json_name)
load_cam(json_name)
