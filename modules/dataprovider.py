import os
import gdown
import zipfile
import config
import pandas as pd


class Downloader:
    """ A class used to retrieve the raw data from google drive """

    def __init__(self, path=config.path.get('raw_data')):
        """
        initialize the class

        :param path: the location in which the downloded file will be stored
        :param file_name: the name of downloded file, e.g: test.zip
        """
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path
        self.file_name = None

    def download(self, google_id, file_name):
        """
        an interface over gdown library

        :param google_id: g_id reference
        :param file_name: name of the file to be saved
        :return: self -> chaining
        """
        os.chdir(self.path)
        gdown.download(id=google_id, output=file_name)
        self.file_name = file_name
        return self

    def extract(self, auto_delete=True):
        """
        extract the downloded file into the self.path

        :param auto_delete: set false if you want to keep the file
        :return: __clean the directory from any other stuff
        """

        # create zipfile object
        zip_ref = zipfile.ZipFile(os.path.join(self.path, self.file_name))
        # extract zip file to the given directory
        zip_ref.extractall(self.path)
        # close file
        zip_ref.close()
        if auto_delete:
            os.remove(os.path.join(self.path, self.file_name))
        return self.__cleaning()

    def __cleaning(self):
        junk = os.path.join(self.path, '__MACOSX', self.file_name.split('.')[0])
        if os.path.exists(junk):
            os.removedirs(junk)

class Annotation:

    def __init__(self, path=os.path.join(config.path.get('ascii'), 'forms.txt')):
        """
        initialize the class

        :param path: the location of the annotation file
        """
        if not os.path.exists(path):
            raise Exception('The annotation file is not exists, neet to be downloaded first!')
        self.path = path
        self.df = None

    def load_into_df(self):
