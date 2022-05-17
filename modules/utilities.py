from fileinput import filename
import os
import sys
sys.path.append('')
import config
import cv2
import Augmentor
import shutil
import matplotlib as plt
import numpy as np




class Utility:

    '''
    A class contains some utility functions to handle the images
    for creating folders, renaming, moving, zipping, downloading etc
    Image Augmentation is performed by using a python package called 'Augmentor'

    '''

    def __init__(self, path=config.path.get('cropped_images')):
        """
        initialize the class

        :param path: the location in which the cropped images will be stored
        """
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path


    def view_image(self,path):
        print("path=",path)
        img = cv2.imread(path)
        img_cvt=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_cvt)
        plt.show()







    def rotate(self, image_path, no_of_images=9, lr=10, rr=10):
        for foldername in os.listdir(image_path):
            self.p = Augmentor.Pipeline(os.path.join(image_path, foldername))
            self.p.rotate(probability=0.9, max_left_rotation=lr, max_right_rotation=rr)
            self.p.sample(no_of_images)
        return self



    def random_distortion(self, image_path, no_of_images=9, gridwdth=4, gridht=4, mag=15):
        for foldername in os.listdir(image_path):
            p = Augmentor.Pipeline(os.path.join(image_path, foldername))
            self.p.random_distortion(probability=1, grid_width=gridwdth, grid_height=gridht, magnitude=mag)
            self.p.sample(no_of_images)

        return self


    #RANDOM SILCES OF 224*224
    def get_random_crop(image, crop_height, crop_width):
        max_x = image.shape[1] - crop_width
        max_y = image.shape[0] - crop_height
        x = np.random.randint(0, max_x)
        y = np.random.randint(0, max_y)
        crop = image[y: y + crop_height, x: x + crop_width]
        return crop

    def sliding_window(no_of_crops, image_path, foldername, htsize=224,wdsize=224):
        cnt=1
        for imagename in os.listdir(os.path.join(image_path, foldername, 'output')):
            image = os.path.join(image_path, foldername, 'output',imagename)
            image = cv2.imread(image)
            for i in range(no_of_crops):
                image_cropped = get_random_crop(image, htsize, wdsize)

                cv2.imwrite(
                    os.path.join(config.path.get('cropped_images'), f'{str(cnt)}.jpeg'), image_cropped
                )
                cnt += 1
        return


    def save(self, filename):
        cv2.imwrite(os.path.join(self.path, filename), self.image)

        return True



    def apply_to_directory(self, image_path):
        self.rotate(image_path,20,14,12).rotate(image_path,20,8,10
        ).random_distortion(image_path,20, 10, 10, 12
        ).random_distortion(image_path,20, 4, 4, 18)

        # for foldername in os.listdir(image_path):
        #     sliding_window(5, foldername).save(filename)

        return
