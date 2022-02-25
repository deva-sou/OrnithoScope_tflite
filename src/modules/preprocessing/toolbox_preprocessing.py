"""
@Authors: SOU Deva, CARLIER Axel
"""

# Imports
import os
import pandas as pd
from xml.dom import minidom
import matplotlib.pyplot as plt

import variables_preprocessing as v


################################################################################################
# Toolbox for getting img number
################################################################################################


def get_info_from_one_xml_minidom(xml_path):
    my_doc = minidom.parse(xml_path)
    items = my_doc.getElementsByTagName('object')
    nb_obj = len(items)
    nb_obj_real = 0
    birds = []
    for k in range(nb_obj):
        bird = items[k].childNodes[7].childNodes[1].childNodes[3].childNodes[0].data
        if bird not in V.unwanted_list:
            birds.append(bird)
            nb_obj_real += 1
        if bird == '1L':
            print(xml_path)
    return nb_obj_real, birds


def import_images_as_df(path):
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


################################################################################################
# Toolbox for adding information on raw images about location and dates
################################################################################################


def add_site_and_day(df):
    df_task = pd.read_csv(v.path_ornithoTasks)
    df_task = df_task.rename(columns={"Task name": "task_name"})
    df_difference = df.merge(df_task, how='outer', indicator=False)
    return df_difference


def import_raw_data_split_as_df(path):
    df_images = import_images_as_df(path)
    df_images_site_day = add_site_and_day(df_images)
    return df_images_site_day


################################################################################################
# Toolbox for split data
################################################################################################


def extract_split_value(df, column_value_selected, column_split_value, split_value):
    df_split_value = df.loc[df[column_split_value] == split_value]
    values_selected = df_split_value[column_value_selected]
    return values_selected


def get_percentage_split_value(df, column_value_selected, column_split_value):
    test = extract_split_value(df, 'obj_detected_number', 'Split', 'TEST')
    train = extract_split_value(df, 'obj_detected_number', 'Split', 'TRAIN')
    count_test = 0
    count_train = 0

    for value in test:
        if isinstance(value, int):
            count_test += value
    for value in train:
        if isinstance(value, int):
            count_train += value
    print(f"Train: {count_train} Test: {count_test}")
    total_value_selected = count_train + count_test
    percentage_train = round(count_train / total_value_selected, 2)
    percentage_test = round(count_test / total_value_selected, 2)
    # get_percentage_split_value(df_difference, 'obj_detected_number', 'Split')
    return percentage_train, percentage_test


def random_split_train_in_validation(df_input, column_split):
    df = df_input.copy()
    df_train = df.loc[df[column_split] == 'TRAIN']
    df_train_lenght = df_train.shape[0]
    df_validation = df_train.sample(round(df_train_lenght / 10))
    df_validation['Split'] = df_validation['Split'].replace('TRAIN', 'VALIDATION')
    print('Indexes of validation tasks', list(df_validation.index))
    df.loc[df_validation.index] = df.loc[df_validation.index].replace('TRAIN', 'VALIDATION')
    # df_split = random_split_train_in_validation(df_difference,'Split')
    return df


def clean_nan_df(df):
    df['Split'] = df['Split'].replace(np.nan, 'TRAIN')
    cols = ["img_number","usable_img","obj_detected_number"]
    df[cols] = df[cols].replace({np.nan:0})
    # df['detected_ojects_number'] = df['detected_ojects_number'].replace(np.nan, {})
    return df


def get_number_object_depending_on_split_value(df):
    df = clean_nan_df(df)
    dict_birds = {}
    df_clean = df[['Split','detected_ojects_number']]
    # list_split_value_type = [x for x in df_clean['Split'].unique() if pd.isnull(x) == False]
    # print('l',list_split_value_type)
    list_split_value_type = []
    # _ = pd.DataFrame(df_clean['detected_ojects_number'])
    # print('_',_)
    counter = 0
    for col_name, infos in df_clean.items():
        for data in infos:
            if type(data) is dict:
                # print('Scanning data')
                # print('\t0- initial data', data)
                for specie, value in data.items():
                    # if specie == 'PINARB':
                        # print(specie,value)
                    # print('1- data to add: ',specie, value)
                    if specie not in dict_birds.keys():
                        dict_birds[specie]={}
                    split_value_type = df_clean['Split'].iloc[counter]
                    # print('2- Split value: ',split_value_type)
                    if split_value_type not in dict_birds[specie].keys():
                        # print('Current birds dictionnary',dict_birds)
                        # print('in?: ',specie, dict_birds[specie].keys())
                        # print('not in.')
                        dict_birds[specie][split_value_type] = value
                        # print(specie, dict_birds[specie].keys())
                    elif split_value_type in dict_birds[specie].keys():
                        # print('Current birds dictionnary',dict_birds)
                        # print('in?: ',specie, dict_birds[specie].keys())
                        # print('in.')
                        dict_birds[specie][split_value_type] += value
                        # print(specie, dict_birds[specie].keys())
                # print('Results: ', dict_birds)
                counter +=1
                # print('COUTER: ',counter)
    # dict_birds = get_number_object_depending_on_split_value(df_difference)
    # df_birds_distribution_split = pd.DataFrame(dict_birds)
    # df_birds_distribution_split
    return dict_birds


def generate_split_df():
    pass
