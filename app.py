import os
import config
import modules.getdata as getdata

downloder = getdata.Downloader()

# After downloding, comment the section below
downloder.download(config.google_ids['ascii'] , 'ascii.zip').extract()
downloder.download(config.google_ids['xml'] , 'xml.zip').extract()
downloder.download(config.google_ids['forms'] , 'forms.zip').extract()
