from math import radians
from pathlib import Path
import sys

import bpy
import mathutils

sys.path.append(".")

from image import image_to_np
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


def load_env(p_json, novel_blocks):
    # get prefab references
    norm_agent = bpy.data.objects["NormalAgent"].data
    norm_cube = bpy.data.objects["NormalCube"].data
    norm_tree = bpy.data.objects["NormalTree"].data
    novel_cube = bpy.data.objects["NovelCube"].data
    # add prefab agents to the scene
    pts = polycraft_json.get_p_json_agents(p_json)
    for pt in pts:
        create_prefab(norm_agent, pt)
    # add prefab blocks to the scene
    pts, names = polycraft_json.get_p_json_pts(p_json)
    for pt, name in zip(pts, names):
        if name in novel_blocks:
            create_prefab(novel_cube, pt)
        elif name == "minecraft:log":
            create_prefab(norm_tree, pt)
        elif name != "minecraft:air":
            create_prefab(norm_cube, pt)


def load_cam(p_json, fov_degrees=71.2666, player_y_offset=1.1066):
    # import camera parameters
    player_pos, yaw, pitch = polycraft_json.get_p_json_cam(p_json)
    player_pos[1] += player_y_offset
    # get camera reference and update settings
    cam = bpy.context.scene.camera
    cam.location = player_pos
    cam.rotation_euler = mathutils.Euler((radians(pitch), radians(180 - yaw), 0), "ZYX")
    cam.data.angle = radians(fov_degrees)


def render_to_np():
    # render image and save temporarily
    render_path = "temp.png"
    render_to_file(render_path)
    np_render = image_to_np(render_path)
    # remove temp file
    Path(render_path).unlink()
    return np_render


def render_to_file(fname):
    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(fname)


def render_from_json(p_json, novel_blocks):
    load_scene()
    load_env(p_json, novel_blocks)
    load_cam(p_json)
    return render_to_np()
