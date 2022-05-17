import os

import config
import modules.dataprovider as dataprovider
from modules.preprocessing import ParagraphExtractor
from modules.preprocessing import Preprocessing

################ Step 1 of the pipeline: download the raw data  ################

# downloder = dataprovider.Downloader()
# downloder.download(config.google_ids.get('ascii') , 'ascii.zip').extract()
# downloder.download(config.google_ids.get('xml') , 'xml.zip').extract()
# downloder.download(config.google_ids.get('forms') , 'forms.zip').extract()


################ Step 2 of the pipeline: extract the paragraph   ################

# paragraph = ParagraphExtractor(offset=10)
# paragraph.extractAll(
#     config.path.get('forms'),
#     config.path.get('xml'),
# )

############### Step 3 of the pipeline: extract the paragraph   ################

# preprocessor = Preprocessing()
# preprocessor.apply_to_directory(
#     config.path.get('paragraphs')
# )


############### Step 4 of the pipeline: Annotations & top writers    ################

annotations = dataprovider.Annotation()

top_writers_df = annotations.load_into_df().filter_by_top_writers()

dataset = dataprovider.Dataset()
dataset.form_to_writer_directory(top_writers_df)
