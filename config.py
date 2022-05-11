import os

####################### Path constants #######################
path = {
    'project_path'      : os.path.dirname(__file__),
    'raw_data'          : os.path.join(os.path.dirname(__file__), 'raw_data'),
    'forms'             : os.path.join(os.path.dirname(__file__), 'raw_data' , 'forms'),
    'xml'               : os.path.join(os.path.dirname(__file__), 'raw_data' , 'xml'),
    'ascii'             : os.path.join(os.path.dirname(__file__), 'raw_data' , 'ascii'),
    'preprocessed_data' : os.path.join(os.path.dirname(__file__), 'preprocessed_data')
}


####################### google drive #######################
google_ids = {
    'ascii' : '1KGpmejUbouzWqvoJjY71iuSp4KfnMJfg',
    'forms' : '1KPPRUlm8X6hDHVLmRhZ5VNFr686qCqcb',
    'xml'   : '1BXbzmfk8NWxzqOKQXVgiXGlCRGczqNwT'
}
