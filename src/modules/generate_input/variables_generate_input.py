import os
import pandas as pd

# PATHS
path_annotation = '/home/deva/code/data_ornitho/annotations/'
path_raw_data = '/home/deva/code/data_ornitho/raw_data/'
path_input_csv = '/home/deva/code/OrnithoScope/data/input.csv'
path_ornithoTasks = '/home/deva/code/OrnithoScope/data/Ornithotasks - CVAT_task.csv'
tasks_dir = sorted(os.listdir(path_annotation))

#
unwanted_labels_list = ['unknown', 'human', 'noBird']
columns_input_data = ["split_value", "file_path", "label",
                      "x_min", "y_min", "empty_1", "empty_2",
                      "x_max", "y_max", "empty_3"]
list_object = []
df_input = pd.DataFrame(columns=columns_input_data)
