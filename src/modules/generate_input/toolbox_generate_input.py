import os
import os.path
import pandas as pd
from xml.etree import ElementTree as ET

import variables_generate_input as v


def get_info_from_one_xml(xml_path, list_object):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    df_tasks = import_tasks_as_df()
    # Filename Extraction and local path creation
    filename = root.find("./filename").text
    local_img_path = f"{v.path_raw_data}{filename.split('/', 1)[1]}"
    # Width and height extraction
    width = int(root.find("./size/width").text)
    height = int(root.find("./size/height").text)
    task_name_xml = filename.split('/')[1]
    # print('task_name', task_name_xml)

    for object in root.findall("./object"):
        # Extract specie name
        for attributes in object.findall("./attributes/"):
            if attributes.find('name').text == 'species':
                specie = attributes.find('value').text
                # Data creation
                data = {}
                data['split_value'] = check_split_value(pd.read_csv(v.path_ornithoTasks), task_name_xml)
                data['file_path'] = local_img_path
                data['label'] = specie
                # Extract bndbx
                bndbox = object.find('./bndbox')
                x_min = round(float(bndbox.find("xmin").text) / width, 4)
                y_min = round(float(bndbox.find("ymin").text) / height, 4)
                x_max = round(float(bndbox.find("xmax").text) / width, 4)
                y_max = round(float(bndbox.find("ymax").text) / height, 4)
                data['x_min'] = x_min
                data['y_min'] = y_min
                data["empty_1"] = ""
                data["empty_2"] = ""
                data['x_max'] = x_max
                data['y_max'] = y_max
                data["empty_3"] = ""
                list_object.append(data)
    return list_object


def get_info_from_all_xml(tasks_dir, list_object):
    for i in range(len(tasks_dir)):
        # For each task
        task_name = tasks_dir[i]
        complete_path = v.path_annotation + task_name + '/Annotations/bird/' + task_name + '/'
        # Get all images of a task
        image_paths = sorted(os.listdir(complete_path))
        for img in range(len(image_paths)):
            xml_path = complete_path + image_paths[img]
            get_info_from_one_xml(xml_path, list_object)
            # print(xml_path, 'done')
    return list_object


def import_tasks_as_df():
    df_task = pd.read_csv(v.path_ornithoTasks)
    df_task = df_task.rename(columns={"Task name": "task_name"})
    return df_task


def check_split_value(df, task_name):
    row_specific_task = df[df['task_name'] == task_name]
    # print('spe task ', row_specific_task)
    val = row_specific_task['Split'].values[0]
    # print('val ', val)
    if val == 'TRAIN':
        return 'TRAINING'
    elif val == 'TEST':
        return 'TEST'
    elif val == 'VALIDATE':
        return 'VALIDATION'


def add_validation_split_value(df):
    print(df[df['Split'] == 'TRAINING'])
    return df

def df_to_csv(df, path_and_name_csv):
    return df.to_csv(path_and_name_csv, encoding='utf-8', index=False, header=False)


def csv_to_df(csv_path):
    return pd.DataFrame.to_csv(csv_path)


def generate_validation_split_value(df_for_input):
    df = df_for_input.reset_index(drop=True)
    j = 0
    for index, row in df.iterrows():
        if row['split_value'] == 'TRAINING':
            j += 1
            # print('j current', j)
            # print('split value before ', row['split_value'])
            if j == 10:
                # print(_.split_value.iloc[index])
                # _.split_value.iloc[index] = _.split_value.iloc[index].replace('VALIDATION')
                df.iloc[index, df.columns.get_loc('split_value')] = 'VALIDATION'
                # print('split value after ', row['split_value'])
                j = 0
    print('TRAIN ', df[df.split_value == 'TRAINING'].shape[0])
    print('VALIDATION ', df[df.split_value == 'VALIDATION'].shape[0])
    print('TEST ', df[df.split_value == 'TEST'].shape[0])
    return df


def create_df_for_input(list_of_object):
    count = 0
    list_df = []
    for object in list_of_object:
        count += 1
        content = pd.DataFrame(object, index=[count])
        list_df.append(content)
    df_input = pd.concat(list_df)
    for label in v.unwanted_labels_list:
        df_input = df_input[(df_input.label != label)]
    return df_input


def create_input_as_df(task_dir, list_object):
    print('Import data ...')
    get_info_from_all_xml(task_dir, list_object)
    print('Done!')
    print('Create dataframe ...')
    df_raw = create_df_for_input(list_object)
    print('Done!')
    print('Create validation set ...')
    df_input = generate_validation_split_value(df_raw)
    print('Done!')
    return df_input


def create_input_as_csv(tasks_dir, list_object, path_input_csv):
    df_input = create_input_as_df(tasks_dir, list_object)
    print('Export to csv ...')
    df_to_csv(df_input, path_input_csv)
    print('Done!')
