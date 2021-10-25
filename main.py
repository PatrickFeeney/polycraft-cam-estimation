from pathlib import Path

import plot
import polycraft_json
import projection


f = 1
cam_y = 4


def project(data_num):
    data_folder = Path("unlabeled_data")
    json_name = data_folder / ("%i.json" % (data_num, ))
    image_name = data_folder / ("%i.png" % (data_num, ))

    player_pos, yaw, pitch = polycraft_json.get_p_json_cam(json_name)
    pts = polycraft_json.get_p_json_pts(json_name)
    proj_matrix = projection.get_proj_matrix(f, cam_y, player_pos, yaw, pitch)
    proj_pts = projection.proj_pts(proj_matrix, pts)
    plot.plot_projection(image_name, proj_pts)


project(1)
project(8)
project(92)
