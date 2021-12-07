import json

import numpy as np


def get_p_json_cam(p_json):
    player_pos = np.array(p_json["player"]["pos"], dtype=float)
    yaw = p_json["player"]["yaw"]
    pitch = p_json["player"]["pitch"]
    return player_pos, yaw, pitch


def get_p_json_pts(p_json):
    pts = np.empty((0, 3))
    names = []
    if "map" in p_json:
        for pos, data in p_json["map"].items():
            pts = np.concatenate(
                (pts, np.fromstring(pos, sep=",")[np.newaxis]), axis=0)
            names.append(data["name"])
    return pts, names


def get_p_json_agents(p_json):
    pts = np.empty((0, 3))
    if "entities" in p_json:
        for id, data in p_json["entities"].items():
            pts = np.concatenate((pts, np.array(data["pos"])[np.newaxis]), axis=0)
    return pts


def load_json(p_json_name):
    with open(p_json_name, "r") as f:
        p_json = json.load(f)
        return p_json
