import os

PROJECT_PATH = '/Users/shahramshabani/Documents/biometric/projectGit/handwriting-recognition/'
DATASET_PATH = os.path.join(PROJECT_PATH, 'raw_data' , 'forms')
ANNOTATION_PATH = os.path.join(PROJECT_PATH, 'raw_data' , 'ascii')
IMAGE_PATH = os.path.join(PROJECT_PATH,'raw_data' , 'XML')

import pandas as pd

df = pd.read_csv(
    filepath_or_buffer=os.path.join(ANNOTATION_PATH, 'forms.txt'), 
    comment="#", 
    sep=' ',
    index_col=False, 
    header=0, 
    names=[
             'form_id',
             'writer_id',
             'number_of_sentences',
             'word_segmentation',
             'lines',
             'line_correctly_segmented',
             'words',
             'word_correctly_segmented'
    ])

# print(len(df.groupby("writer_id").filter(lambda x: len(x) > 8)['writer_id'].unique())) # Number of the total writers

