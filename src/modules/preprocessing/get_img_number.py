"""
@Authors: SOU Deva, CARLIER Axel
"""

# Imports
import os
import os.path

import pandas as pd
import matplotlib.pyplot as plt

import toolbox as t
import variables as v


def get_img_number(path):
    df = pd.DataFrame(columns=v.columns_names)
    tasks_dir = sorted(os.listdir(v.path_annotations))
    total_img = 0
    total_obj = 0
    total_obj_dict = {}
    for i in range(len(tasks_dir)):
        # For each task
        task_name = tasks_dir[i]
        task_dict = {}
        complete_path = path + task_name + '/Annotations/bird/' + task_name + '/'
        # Get all images of a task
        image_paths = sorted(os.listdir(complete_path))
        nb_img_real = 0
        nb_obj_real = 0
        for img in range(len(image_paths)):
            # For each image
            nb_obj, birds = t.get_info_from_one_xml_minidom(complete_path + image_paths[img])
            if nb_obj > 0:
                nb_img_real += 1
                nb_obj_real += len(birds)
                for bird in birds:
                    if bird in task_dict:
                        task_dict[bird] += 1
                    else:
                        task_dict[bird] = 1

                    if bird in total_obj_dict:
                        total_obj_dict[bird] += 1
                    else:
                        total_obj_dict[bird] = 1

        total_img += nb_img_real
        total_obj += nb_obj_real
        df = df.append({'task_name': task_name, 'img_number': len(image_paths),
                        'usable_img': nb_img_real, 'obj_detected_number': nb_obj_real,
                        'detected_objects_number': task_dict}, ignore_index=True)
        print('Parsing done')
        print('Total images ', total_img, total_obj, total_obj_dict)
        return df


def plot_stats_img_raw_data(df):
    plt.figure(figsize=(14, 14))
    df.plot()


def main():
    df = get_img_number(v.path)
    plot_stats_img_raw_data(df)
