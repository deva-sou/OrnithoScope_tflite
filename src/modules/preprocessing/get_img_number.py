"""
@Authors: SOU Deva, CARLIER Axel
"""

# Imports

import toolbox_preprocessing as t
import variables_preprocessing as v


def main():
    df = t.import_images_as_df(v.path_annotations)
    return df
