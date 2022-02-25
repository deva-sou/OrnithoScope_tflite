'''
@Authors: SOU Deva, CARLIER Axel
'''

# Imports
import os, os.path
import pandas as pd
from xml.dom import minidom
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import variables as V
import toolbox

def annotations_parse(path):
    df = pd.DataFrame(columns = V.columns_names)
    tasks_dir = sorted(os.listdir(V.path_annotations))
    total_img = 0
    total_obj = 0
    total_obj_dict = {}
    for i in range(len(tasks_dir)):
    # For each task
        task_name = tasks_dir[i]
        task_dict = {}
        complete_path = path + task_name + '/Annotations/bird/' + task_name + '/'
        # Lister toutes les images de la tâche
        image_paths = sorted(os.listdir(complete_path))

        nb_img_real = 0
        nb_obj_real = 0
        for img in range(len(image_paths)):
            nb_obj, birds = toolbox.get_info_from_xml(complete_path + image_paths[img])
            
            if nb_obj > 0:
                nb_img_real += 1
                nb_obj_real += len(birds)
                
                for b in birds:
                    if b in task_dict:
                        task_dict[b] += 1
                    else:
                        task_dict[b] = 1
                        
                    if b in total_obj_dict:
                        total_obj_dict[b] += 1
                    else:
                        total_obj_dict[b] = 1
        
        total_img += nb_img_real
        total_obj += nb_obj_real        
        #print(task_name, len(image_paths), nb_img_real, nb_obj_real, task_dict)
        df = df.append({'task_name': task_name, 'img_number':len(image_paths),
                       'usable_img':nb_img_real,'obj_detected_number':nb_obj_real,'detected_ojects_number':task_dict},ignore_index=True)
        print('Total images ', total_img, total_obj, total_obj_dict)
        return df

def main():
    df = annotations_parse(V.path)
    
