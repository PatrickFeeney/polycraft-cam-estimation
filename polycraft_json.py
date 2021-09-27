import json

import numpy as np


def get_p_json_cam(p_json_name):
    with open(p_json_name, "r") as f:
        p_json = json.load(f)
        player_pos = p_json["player"]["pos"]
        yaw = p_json["player"]["yaw"]
        pitch = p_json["player"]["pitch"]
        return player_pos, yaw, pitch


def get_p_json_pts(p_json_name):
    with open(p_json_name, "r") as f:
        p_json = json.load(f)
        pts = np.empty((0, 3))
        for pos, _ in p_json["map"].items():
            pts = np.concatenate((pts, np.fromstring(pos, sep=",")[np.newaxis]), axis=0)
        return pts.T
