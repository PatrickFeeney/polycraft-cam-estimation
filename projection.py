import numpy as np
from scipy.spatial.transform import Rotation


def get_proj_matrix(f, cam_y, player_pos, yaw, pitch):
    # camera intrinsics
    cam_matrix = np.array([
        [f, 0, 128],
        [0, f, 128],
        [0, 0, 1],
    ])
    # camera extrinsics
    rot_matrix = Rotation.from_euler("zyx", [yaw, pitch, 0]).as_matrix()
    ext_matrix = np.array([
        [0, 0, 0, player_pos[0]],
        [0, 0, 0, cam_y],
        [0, 0, 0, player_pos[2]],
    ])
    ext_matrix[:3, :3] = rot_matrix
    # projection matrix
    return cam_matrix @ ext_matrix


def proj_pts(proj_matrix, pts):
    _, num_pts = pts.shape
    pts = np.concatenate((pts, np.ones_like(pts, shape=(1, num_pts))), axis=0)
    proj_pts = proj_matrix @ pts
    proj_pts = proj_pts[:2] / proj_pts[2]
    return proj_pts
