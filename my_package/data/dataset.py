#Imports
import json
from os import path
from .model import InstanceSegmentationModel
from PIL import Image
import numpy as np

class Dataset(object):
    '''
        A class for the dataset that will return data items as per the given index
    '''

    def __init__(self, annotation_file, transforms = None, usePreData=False):
        '''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''
        self.transforms = transforms
        self.usePreData = usePreData
        if(path.exists(annotation_file)): # check if file exits
            self.annotation_file = annotation_file.replace('/','\\')
            self.data_list = list(open(annotation_file)) # load and read .jsonl file
        else:
            print("\n<> Exception : The path to annotation file is erroneous!\n")
            self.annotation_file = None
            self.data_list = None

    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        if(self.data_list==None):
            return 0
        else:
            return self.data_list.__len__()

    def __getitem__(self, idx):
        '''
            return the dataset element for the index: "idx"
            Arguments:
                idx: index of the data element.

            Returns: A dictionary with:
                image: image (in the form of a numpy array) (shape: (3, H, W))
                gt_png_ann: the segmentation annotation image (in the form of a numpy array) (shape: (1, H, W))
                gt_bboxes: N X 5 array where N is the number of bounding boxes, each
                            consisting of [class, x1, y1, x2, y2]
                            x1 and x2 lie between 0 and width of the image,
                            y1 and y2 lie between 0 and height of the image.

            The following things are done,
            1. Extracted the correct annotation using the idx provided.
            2. Read the image, png segmentation and converted it into a numpy array. The shape of the arrays would be (3, H, W) and (1, H, W), respectively.
            3. Scaled the values in the arrays to be with [0, 1].
            4. Performed the desired transformations on the image.
            5. Returned the dictionary of the transformed image and annotations as specified.
        '''
        if(self.data_list==None):
            print("\n<> Exception : The dataset is empty")
            return None
        else:
            # the function does additional work for the programmer
            # instead of leaving the work of calling the segmentor on the image the function internally does so to ease out the tasks of a programmer
            element = json.loads(self.data_list[idx])
            token = self.annotation_file.rsplit('\\').pop()
            parent_path = self.annotation_file.rstrip(token)
            image_path = parent_path + element["img_fn"].replace('/','\\')
            img_file = Image.open(image_path)
            dictL = {}
            img_file = np.uint8(img_file)
            if(self.transforms!=None): # transform images through rotation, flipping, etc as provided
                for iter in self.transforms:
                    img_file = iter(img_file)
                segmentation = InstanceSegmentationModel()((np.uint8(img_file) / 255).transpose(2, 0, 1)[0:3])
                dictL["image"] = img_file
                dictL["gt_png_ann"] = segmentation[1]
                dictL["gt_bboxes"] = segmentation[0]
                dictL["category"] = segmentation[2]
                dictL["confidence"] = segmentation[3]
            elif(self.transforms==None): # no transforms
                if(self.usePreData): # use pre computed data from annotations file
                    dictL["image"] = img_file
                    dictL["gt_png_ann"] = None # annotations file does not have masks
                    dictL["confidence"] = None # annotations file does not have scores
                    dictL["gt_bboxes"] = []
                    dictL["category"] = []
                    for iter in element["bboxes"]:
                        dictL["gt_bboxes"] = dictL["gt_bboxes"] + [iter["bbox"]]
                        dictL["category"] = dictL["category"] + [iter["category"]]

                else: # call the segmentor and get information
                    segmentation = InstanceSegmentationModel()((np.uint8(img_file) / 255).transpose(2, 0, 1)[0:3])
                    dictL["image"] = img_file
                    dictL["gt_png_ann"] = segmentation[1]
                    dictL["gt_bboxes"] = segmentation[0]
                    dictL["category"] = segmentation[2]
                    dictL["confidence"] = segmentation[3]
            return dictL
