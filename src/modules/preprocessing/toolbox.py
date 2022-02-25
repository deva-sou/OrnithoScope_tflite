'''
@Authors: SOU Deva, CARLIER Axel
'''

def get_info_from_one_xml(xml_path):
    mydoc = minidom.parse(xml_path)
    items = mydoc.getElementsByTagName('object')
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