import os
import os.path
import pandas as pd
from xml.etree import ElementTree as ET

import variables_model_creation as v


def get_info_from_one_xml(xml_path, list_object):
    i = 0
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # Filename Extraction and local path creation
    filename = root.find("./filename").text
    local_img_path = f"{v.path_raw_data}{filename.split('/', 1)[1]}"
    # Width and height extraction
    width = int(root.find("./size/width").text)
    height = int(root.find("./size/height").text)

    for object in root.findall("./object"):
        # Extract specie name
        for attributes in object.findall("./attributes/"):
            if attributes.find('name').text == 'species':
                specie = attributes.find('value').text
        # Data creation
        data = {}
        data['split_value'] = 'TRAINING'
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
            list_of_data = get_info_from_one_xml(xml_path, list_object)
        return list_object


def df_to_csv(df, path_and_name_csv):
    df.to_csv(path_and_name_csv, encoding='utf-8', index=False, header=False)


def create_df_for_input(list_of_object):
    count = 0
    list_df = []
    for object in list_of_object:
        print(object)
        count += 1
        content = pd.DataFrame(object, index=[count])
        list_df.append(content)
    df_input = pd.concat(list_df)
    for label in v.unwanted_labels_list:
        df_input = df_input[(df_input.label != label)]
    return df_input


def create_input_as_df(tasks_dir, list_object):
    input_for_model = get_info_from_all_xml(tasks_dir, list_object)
    df = create_df_for_input(input_for_model)
    return df


def create_input_as_csv():
    df = create_input_as_df(v.tasks_dir, v.list_object)
    df_to_csv(df, v.path_and_name_csv)
