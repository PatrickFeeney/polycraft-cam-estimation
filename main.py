from pathlib import Path

import plot
import polycraft_json
import projection


data_folder = Path("unlabeled_data")
data_num = 1
json_name = data_folder / ("%i.json" % (data_num, ))
image_name = data_folder / ("%i.png" % (data_num, ))

f = 10
cam_y = 4

player_pos, yaw, pitch = polycraft_json.get_p_json_cam(json_name)
pts = polycraft_json.get_p_json_pts(json_name)
proj_matrix = projection.get_proj_matrix(f, cam_y, player_pos, yaw, pitch)
proj_pts = projection.proj_pts(proj_matrix, pts)
plot.plot_projection(image_name, proj_pts)
