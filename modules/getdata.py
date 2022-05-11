import os
import gdown
import zipfile
import config


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
