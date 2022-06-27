'''
	PACKAGE DEVELOPED BY : SUBHAM GHOSH
	ROLL NO. : 20CS10065
	SECOND YEAR UNDERGRADUATE STUDENT CSE
	IIT KGP
'''

#if shape argument is wrongly given then the function prints an exception and the image is not cropped
#if crop_type argument is wrongly given then the function by default does centre cropping
#Imports
from PIL import Image
from random import randint

supported_image_types = ["<class 'PIL.JpegImagePlugin.JpegImageFile'>", "<class 'PIL.PngImagePlugin.PngImageFile'>", "<class 'PIL.Image.Image'>"]

class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''

        # Write your code here
        if(type(shape)==tuple and shape.__len__()>=2):
            self.shape = shape
        else:
            self.shape = None
            print("\n<> Exception : Shape Argument must be a TUPLE OF INT with atleast two elements! The image won't be cropped\n")

        if(type(crop_type)==str):
            if(crop_type!='center'):
                self.crop_type = 'random'
            else:
                self.crop_type = 'center'
        else:
            self.crop_type = 'random'

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        if (str(type(image)) in supported_image_types):
            if(self.shape==None):
                return image
            if(self.crop_type=='center'):
                h = self.shape[0]
                w = self.shape[1]
                wi = image.size[0]
                hi = image.size[1]
                l_corner = (wi-w)//2
                t_corner = (hi-h)//2
                r_corner = l_corner + w
                b_corner = t_corner + h
            else:
                h = self.shape[0]
                w = self.shape[1]
                wi = image.size[0]
                hi = image.size[1]
                l_corner = randint(0,wi)
                t_corner = randint(0,hi)
                r_corner = l_corner + w
                b_corner = t_corner + h
            return image.crop((l_corner,t_corner,r_corner,b_corner))
        elif (str(type(image)) == "<class 'numpy.ndarray'>"):
            sample = Image.fromarray(image)
            if (self.shape == None):
                return sample
            if (self.crop_type == 'center'):
                h = self.shape[0]
                w = self.shape[1]
                wi = sample.size[0]
                hi = sample.size[1]
                l_corner = (wi - w) // 2
                t_corner = (hi - h) // 2
                r_corner = l_corner + w
                b_corner = t_corner + h
            else:
                h = self.shape[0]
                w = self.shape[1]
                wi = sample.size[0]
                hi = sample.size[1]
                l_corner = randint(0, wi)
                t_corner = randint(0, hi)
                r_corner = l_corner + w
                b_corner = t_corner + h
            return sample.crop((l_corner, t_corner, r_corner, b_corner))
        else:
            print("\n<> Exception : Image Argument must be of Type PIL IMAGE/JPEG IMAGE/PNG IMAGE or NUMPY ARRAY!\n")
            return None

#testing code for debugging purpose ->
#img = Image.open(r"C:\Users\mezartine\Downloads\CS29006_SW_Lab_Spr2022-master\Python_DS_Assignment\data\imgs\5.jpg").convert('RGBA')
#CropImage((2000,2000))(img).show()
