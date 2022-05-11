import math
import config
import os
import cv2
import xml.etree.ElementTree as ET
from tqdm import tqdm



class ParagraphExtractor:
    """
    A class to extract the paragraph from the forms which is
    related to the handwritten part only
    """

    def __init__(self, path=config.path.get('preprocessed_data'), offset=10):
        """
        initialize the class

        :param path: the location in which the extracted paragraph will be stored
        :param offset: act like padding
        """
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
        self._offset = offset

    def extractParagraph(self, img_path, xml_path, filename):
        """
        extract paragraph given an image and corresponding xml file

        :param img_path: path to the image to be loaded
        :param xml_path: path to the xml file corresponding to the image
        :param filename: final image will be stored under this filename
        """
        img = cv2.imread(img_path)
        root = ET.parse(xml_path).getroot()
        # extract height information
        y1 = int(root[1][0].attrib['asy'])
        y2 = int(root[1][len(root[1])-1].attrib['dsy'])

        # extract width information
        x1 = math.inf
        x2 = -math.inf
        for line in root[1]:
            for word in line.findall('word'):
                if len(word):
                    lower_bound = int(word[0].attrib['x'])
                    width_of_char = int(word[len(word)-1].attrib['width'])
                    upper_bound = int(word[len(word)-1].attrib['x']) + width_of_char
                    if lower_bound < x1: x1 = lower_bound
                    if upper_bound > x2: x2 = upper_bound


        cropped_img = img[
            self.__addOffset(y1):self.__addOffset(y2, False),
            self.__addOffset(x1):self.__addOffset(x2, False)
            ]

        cv2.imwrite(os.path.join(self.path, filename), cropped_img)
        return


    def extractAll(self, img_dir, xml_dir):
        """
        extract paragraph given an directory and corresponding xml directory

        :param img_dir: path to the image directory to be extracted at one shot
        :param xml_dir: path to the xml directory corresponding to the images
        """
        for filename in tqdm(os.listdir(img_dir)):
            if not filename.startswith('.'):
                form_id = filename.split('.')[0]
                self.extractParagraph(
                    os.path.join(img_dir, filename),
                    os.path.join(xml_dir, f'{form_id}.xml'),
                    filename
                )

    def __addOffset(self, pixel, lower_bound=True):
        return pixel-self._offset  if lower_bound else pixel + self._offset
