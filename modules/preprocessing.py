import math
import config
import os
import cv2
import xml.etree.ElementTree as ET


class ParagraphExtractor:
    def __init__(self, path=config.path.get('preprocessed_data')):
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path

    def extractParagraph(self, img_path, xml_path):
        img = cv2.imread(img_path)
        root = ET.parse(xml_path).getroot()
        y1 = int(root[1][0].attrib['asy'])
        y2 = int(root[1][len(root[1])-1].attrib['dsy'])

        x1 = math.inf
        x2 = -math.inf
        for line in root[1]:
            for word in line.findall('word'):
                lower_bound = int(word[0].attrib['x'])
                upper_bound = int(word[len(word)-1].attrib['x']) + int(word[len(word)-1].attrib['width'])
                if lower_bound < x1:
                    x1 = lower_bound
                if upper_bound > x2:
                    x2 = upper_bound
        color = (0, 0, 255)


    def extractAll(self):
        pass
