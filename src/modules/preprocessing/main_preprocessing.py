"""
@Authors: SOU Deva, CARLIER Axel
"""


# Module imports
import get_img_number
import split_data

# Main
df_images = get_img_number.main()
df_split = split_data.main(df_images)
