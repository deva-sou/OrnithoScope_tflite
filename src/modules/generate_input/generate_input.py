"""
@Authors: SOU Deva, CARLIER Axel
"""

# Imports
import toolbox_generate_input as toolbox
import variables_generate_input as v

# Main
toolbox.create_input_as_csv(v.tasks_dir,
                            v.list_object,
                            v.path_input_csv)
