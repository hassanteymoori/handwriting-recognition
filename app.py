import os
import config
import modules.getdata as getdata
from modules.preprocessing import ParagraphExtractor
################ Step 1 of the pipeline: download the raw data  ################
'''
    To get the data from the google drive. The data includes the information
    about authors, handwriting forms and an xml file per each form which
    consist of the meta date of the documents
'''
# downloder = getdata.Downloader()
# downloder.download(config.google_ids.get('ascii') , 'ascii.zip').extract()
# downloder.download(config.google_ids.get('xml') , 'xml.zip').extract()
# downloder.download(config.google_ids.get('forms') , 'forms.zip').extract()


################ Step 2 of the pipeline" extract the paragraph   ################
'''
    To extract the handwritten part from the form.
'''

# preprocessor = ParagraphExtractor(offset=10)
# preprocessor.extractAll(
#     config.path.get('forms'),
#     config.path.get('xml'),
# )

################ Step 3 of the pipeline" extract the paragraph   ################
'''
    paragraph preprocessing step
'''
