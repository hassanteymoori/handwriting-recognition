import os
import gdown
import zipfile

ids= ['1KGpmejUbouzWqvoJjY71iuSp4KfnMJfg',
'1KPPRUlm8X6hDHVLmRhZ5VNFr686qCqcb',
'1KLpaix9VUAiLOqm0BiiUdgmIfQAhvsDy'] 
dests = ['ascii.zip',
'forms.zip',
'XML.zip']
for id,dest in zip(ids,dests):
    # if not os.path.exists(dest):
    #     os.mkdir(dest) 
    gdown.download(id=id,output=dest,quiet=False)

project_dir ='/Users/shahramshabani/Documents/biometric/projectGit/handwriting-recognition/'

dir_name = os.path.join(project_dir)
extension = ".zip"

os.chdir(dir_name) # change directory from working dir to dir with files

for item in os.listdir(dir_name): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        if not os.path.exists(os.path.join(project_dir,'raw_data')):
            os.mkdir(os.path.join(dir_name, 'raw_data'))
        zip_ref.extractall(os.path.join(dir_name, 'raw_data')) # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file
