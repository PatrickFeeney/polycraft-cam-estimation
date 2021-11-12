import pandas as pd


mean_iou = pd.read_csv("cam_param_search.csv").to_numpy()[:, 2]
mean_iou = mean_iou.reshape((10, 10))
print("Max IoU")
print(mean_iou.max())
print("\nMax IoU by Y-Offset")
print(mean_iou.max(axis=0))
print("\nMax IoU by FoV")
print(mean_iou.max(axis=1))
