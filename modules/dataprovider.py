
import os
import gdown
import zipfile
import config
import pandas as pd
import shutil
from tqdm import tqdm
import cv2


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
    """ A class used to retrieve and manipulate the annotation information  """

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
        """
        Load the annotation txt file into the pandas dataframe
        """
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
        """
        getter for the dataframe object
        """
        self._is_loaded()

        return self.df

    def filter_by_top_writers(self, number_of_forms=8):
        """
        returns the dataframe which has been filtered by the top writers who have been participated more than others
        :param number_of_forms: number of the forms in which we want to filter by as lower limit
        """
        self._is_loaded()
        return self.df.groupby("writer_id").filter(lambda x: len(x) > number_of_forms)

    def number_of_top_writers(self):
        """
        returns the number of the top writer based on the participation limit
        """
        return len(self.filter_by_top_writers(8)['writer_id'].unique())

    def number_of_top_writers_forms(self):
        """
        total number of the forms written by  the top writer
        """
        return len(self.filter_by_top_writers())

    def _is_loaded(self):
        """
        Private method, check to see whether the dataframe has been loaded successfully
        """
        if self.df is None:
            raise Exception('dataframe has not been loaded! first call the `load_into_df` method')
        return self

class Dataset:
    """
        database provider based on the given paragraphs and dataframe
    """
    def __init__(
        self,
        dataset = config.path.get('dataset'),
        train_set = config.path.get('train_set'),
        test_set = config.path.get('test_set'),
        number_of_test_sample = 4,
        number_of_train_sample = 5,
        split_train_set = 8,
        split_test_set = 3,
        crop_height = 224,
        crop_width = 224,
        padding_threshold = 50
    ):
        """
            Initialize the class object
            :param dataset : the location for the dataset
            :param train_set : the location for the train_set
            :param test_set : the location for the test_set
            :param number_of_test_sample: the number of the test sample for to be splitted
            :param crop_width width of the new image after crop functionality
            :param crop_height height of the new image after crop functionality
            :param padding_threshold a threshold in which we ignore to split an image during test
        """
        if not os.path.exists(train_set):
            os.makedirs(train_set)
        if not os.path.exists(test_set):
            os.makedirs(test_set)
        self.train_set = train_set
        self.test_set = test_set
        self.dataset = dataset
        self.number_of_test_sample = number_of_test_sample
        self.number_of_train_sample = number_of_train_sample
        self.crop_width = crop_width
        self.crop_height = crop_height
        self.padding_threshold = padding_threshold
        self.split_train_set = split_train_set
        self.split_test_set = split_test_set

    def form_to_writer_directory(self, dataframe ):
        """
            move each form to the corresponding writer directory in the given test and train path
            :param dataframe : the annotation information dataframe
        """
        for _, row in tqdm(dataframe.iterrows()):
            train_folder_writer = os.path.join(self.train_set, str(row['writer_id']))
            test_folder_writer = os.path.join(self.test_set, str(row['writer_id']))
            if not os.path.exists(train_folder_writer):
                os.mkdir(train_folder_writer)
            if not os.path.exists(test_folder_writer):
                os.mkdir(test_folder_writer)

            form_path = os.path.join(config.path.get('paragraphs_edged'), f"{row['form_id']}.png")

            upper_test_bound = len(os.listdir(test_folder_writer))
            upper_train_bound = len(os.listdir(train_folder_writer))
            if upper_test_bound < self.number_of_test_sample:
                shutil.copy(form_path, os.path.join(self.test_set, test_folder_writer))
            elif upper_train_bound < self.number_of_train_sample:
                shutil.copy(form_path, os.path.join(self.train_set, train_folder_writer))


        return self

    #RANDOM SILCES OF crop_width*crop_height
    def crop_train_set(self):
        """
            crop each sample of the training set to smaller samples of the given crop_width and crop_height
        """
        for folder in tqdm(os.listdir(self.train_set)):
            for image in os.listdir(os.path.join(self.train_set, folder)):
                image_path = os.path.join(self.train_set, folder, image)
                img = cv2.imread(image_path)
                filename = image.split('.')[0]
                self._crop_image(img, folder ,filename)
                os.remove(image_path)
        return self


    def crop_test_set(self):
        """
            crop each sample of the test set to smaller samples of the given crop_width and crop_height
        """
        for folder in tqdm(os.listdir(self.test_set)):
            for image in os.listdir(os.path.join(self.test_set, folder)):
                image_path = os.path.join(self.test_set, folder, image)
                img = cv2.imread(image_path)
                filename = image.split('.')[0]
                self._crop_image(img, folder ,filename, train_set=False, apply_threshold=True)
                os.remove(image_path)

        return self

    def _crop_image(self, image, folder ,filename, train_set=True, apply_threshold=False):
        """
            @private method
            crop the given image based on crop_width and crop_height and save in the folder
            :param image a numpy array of the loaded image
            :param folder a writer folder name
            :param name of file
            :apply_threshold a threshold in which we decide to continue spliting
        """
        count = 0
        for row in range(0, image.shape[1], self.crop_width):
            step_row = row + self.crop_width
            if (step_row) > image.shape[1]:
                if apply_threshold:
                    if (step_row - image.shape[1]) > self.padding_threshold:
                        break
                row = row - ((step_row) - image.shape[1])
            for column in range(0, image.shape[0], self.crop_height):
                split_number = self.split_train_set if train_set else self.split_test_set
                if count == split_number:
                    break
                step_column = column + self.crop_height
                if (step_column) > image.shape[0]:
                    if apply_threshold:
                        if (step_column - image.shape[0]) > self.padding_threshold:
                            break
                    column = column - ((step_column) - image.shape[0])
                if apply_threshold:
                    dest_path = os.path.join(self.test_set, folder ,f'{filename}-{str(count)}.png')
                else:
                    dest_path = os.path.join(self.train_set, folder ,f'{filename}-{str(count)}.png')
                cv2.imwrite(dest_path,image[column: step_column, row: step_row])
                count +=1

    def make_zipfolder(self, zipfoldername='dataset'):
        """
            create a zip folder from the dataset for training
        """
        shutil.make_archive(zipfoldername, 'zip', self.dataset)
        return self
