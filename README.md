
# What is the Task and Motivation?
* Automatic handwriting recognition and writer verification system help in determining the valid writer of a particular handwritten text image among the  number of writers whose handwriting has been already trained. Many research scholars had shown interest in this domain because of its large number of applications like security and criminological analysis, antique documents , literature analysis, and etc. The traditional approaches extract features from handwriting using hand-designed and manual calculations or from image processing techniques. They used techniques such as scale-invariant feature transforms, local binary patterns (LBP), wavelet transforms, etc, where the final feature vectors are extracted from local patches of handwriting images and constructed models like a bag of words, etc. With the advent of deep learning algorithms like CNNs, ANNs, etc, the feature extraction work has become much easier. Since the convolutional neural networks and their state of art architectures like AlexNet, VGG, GoogleNet are very powerful in extracting deep features and their huge success in the fields of computer vision made several research scholars employ CNN techniques for writer identification.


## Prerequisites:
- Python 3.5
- [OpenCV3](https://opencv.org/)
- tensorflow
- keras
- Numpy
- Deep learning techniques

# Dataset
Providing appropriate training datasets and testing datasets is the main objective for any machine learning task. There are several important dataset on the internet for specific kind of tasks.

2.1. Raw DataSet:  
In this project, we used the IAM Handwriting Database contains forms of handwritten English text.  
The be able to download the dataset into our local machine, we implemented a `dataprovider` module which is able to download the dataset using the Downloader class.
The database contains forms of unconstrained handwritten text, which were scanned at a resolution of 300dpi and saved as PNG images with 256 gray levels. The figure below provides a sample of a complete form with the specific writer’s ID and Name. The IAM Handwriting Database has 657 writers who contributed samples of their handwriting.

# Paragraph Extraction modules
All forms are provided as PNG files and the corresponding form label files, including segmentation information and a variety of estimated parameters, are included in the image files as meta-information in XML format which is described in XML file and XML file format.
The XML files as well as the other annotation information are downloaded using the same Downloader class from `dataprovider` modules.
As you can observe in the above figure and mentioned in the previous section, the raw image consists of some information that we don’t need, so by using the corresponding XML files, we extracted only handwritten paragraphs with respect to the given coordinates.

# Image Preprocessing
In this stage, the main objective is to remove the noise and variations in background lighting, since the images are differently captured by every writer. This is done using a Gaussian blur filter and finally extracting the edges alone from the handwriting image. This is done using Canny Edge Detector.
Gaussian Blur filtering is an operation in which a Gaussian filter instead of a box filter is convolved over an image. It is a low-pass filter that eliminates the high-frequency components and reduces the unwanted noise in the image.
The Canny edge detector is an edge detection operation that uses a multi-stage algorithm to detect an extensive range of edges in images.

All the preprocessing processes ,which have been mentioned above, implemented by using the open-cv library. We created an interface over the open-cv related functions and bring the functionality into our own modules so called Preprocessing.

# Split Data
One of the most important parts of data processing would be this stage. Since it is a biometric task (not a Machine Learning one), we need to define some important specific criteria:
- Each writer must have at least one sample in the test set to be testified.
- There should be a sufficient number of training samples due to the nature of the problem.
- There should be a good number of testing samples as well.
- Since the task does not depend on the image itself or text but is to identify the writer, thus we could crop the samples into multiple smaller ones in order to increase the number of the training and testing samples.
- For the training, the overlap between the smaller samples (after cropping) is allowed while for the testing samples overlap is not allowed at all.
We considered 4 forms out of at least 9 per each writer, for the testing set. On the other hand, the remaining which would be at least 5 samples have been considered as the training set. Later on, once we want to prevent having an unbalanced train set, we take only the minimum number of the samples for training which is 5 samples.
For increasing the Dataset samples, we enhanced cropping edged images into several images with sizes of 500 x 500.

As mentioned above, we considered no overlap between the cropped images but for the train set we considered a little overlap with a specific threshold to have a larger training set. For each sample of the training set, we cropped the edged image into 8 different  smaller images. Similarly, for each of the test samples, we cropped the edged image into  just 3 different smaller images (to avoid having any overlap). 
Overall, we finally have 1240 images belonging to 31 different writers for the training set, and 372 images for the testing set.
These numbers are without considering any augmentation process.

# Training Phase:
Now we have everything to start the training phase. Let's define some constants for our deep architecture.
```
BATCH_SIZE = 32
IMAGE_SIZE = 500
IMAGE_SHAPE = (IMAGE_SIZE, IMAGE_SIZE) 
N_CLASSES = 31
```

# Evaluation
What we are going to do before starting a biometric evaluation task, is to remove the last layer of our models which is the classification layer in order to access the feature layer. Then once we have the feature extractor models, we will perform an all-against-all method in order to stress the system evaluation.

<br>

# Results
Look at docs
