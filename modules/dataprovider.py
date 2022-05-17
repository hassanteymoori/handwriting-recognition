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
        self.df = pd.read_csv(
            filepath_or_buffer=self.path,
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

        return self


    def get_df(self):
        self._is_loaded()

        return self.df

    def filter_by_top_writers(self, number_of_forms=8):
        self._is_loaded()
        return self.df.groupby("writer_id").filter(lambda x: len(x) > number_of_forms)

    def number_of_top_writers(self):
        return len(self.filter_by_top_writers(8)['writer_id'].unique())

    def number_of_top_writers_forms(self):
        return len(self.filter_by_top_writers())

    def _is_loaded(self):
        if self.df is None:
            raise Exception('dataframe has not been loaded! first call the `load_into_df` method')
        return self

class Dataset:
    def __init__(
        self,
        train_set = config.path.get('train_set'),
        test_set = config.path.get('test_set')
    ):
        if not os.path.exists(train_set):
            os.makedirs(train_set)
        if not os.path.exists(test_set):
            os.makedirs(test_set)
        self.train_set = train_set
        self.test_set = test_set

    def form_to_writer_directory(self, )
