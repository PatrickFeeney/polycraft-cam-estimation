import pandas as pd


if __name__ == "__main__":
    targets = pd.read_csv("blender/targets.csv")
    type_to_max_novel = {}

    for i in range(targets.shape[0]):
        type = targets.iloc[i, 0]
        type = type[:type.find("/")]
        type_to_max_novel[type] = max(type_to_max_novel.get(type, 0), targets.iloc[i, 1])
    for type, max_novel in type_to_max_novel.items():
        print("%s: %f" % (type, max_novel))
