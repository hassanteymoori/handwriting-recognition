from logging import root
import os

####################### Path constants #######################
root = os.path.dirname(__file__)
path = {
    'project_path'      : root,
    'raw_data'          : os.path.join(root, 'raw_data'),
    'forms'             : os.path.join(root, 'raw_data' , 'forms'),
    'xml'               : os.path.join(root, 'raw_data' , 'xml'),
    'ascii'             : os.path.join(root, 'raw_data' , 'ascii'),
    'paragraphs'        : os.path.join(root, 'preprocessed_data', 'paragraphs'),
    'paragraphs_edged'  : os.path.join(root, 'preprocessed_data', 'paragraphs_edged'),
    'cropped_images'    : os.path.join(root, 'preprocessed_data', 'cropped_images' )
 
}


####################### google drive #######################
google_ids = {
    'ascii' : '1KGpmejUbouzWqvoJjY71iuSp4KfnMJfg',
    'forms' : '1KPPRUlm8X6hDHVLmRhZ5VNFr686qCqcb',
    'xml'   : '1BXbzmfk8NWxzqOKQXVgiXGlCRGczqNwT'
}
