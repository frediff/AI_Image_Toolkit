'''
	PACKAGE DEVELOPED BY : SUBHAM GHOSH
	ROLL NO. : 20CS10065
	SECOND YEAR UNDERGRADUATE STUDENT CSE
	IIT KGP
'''

#if blur radius argument is given wrong then the image is not blurred
#Imports
from PIL import Image, ImageFilter

supported_image_types = ["<class 'PIL.JpegImagePlugin.JpegImageFile'>", "<class 'PIL.PngImagePlugin.PngImageFile'>", "<class 'PIL.Image.Image'>"]

class BlurImage(object):
    '''
        Applies Gaussian Blur on the image.
    '''

    def __init__(self, radius):
        '''
            Arguments:
            radius (int): radius to blur
        '''

        # Write your code here

        if (type(radius) == int or type(radius) == float):
            self.radius = radius
        else:
            print("\n<> Exception : Radius Argument must be of Type INT or FLOAT! Setting radius = 0\n")
            self.radius = 0

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL Image)

            Returns:
            image (numpy array or PIL Image)
        '''

        # Write your code here
        if(str(type(image)) in supported_image_types):
            return image.filter(ImageFilter.GaussianBlur(self.radius))
        elif(str(type(image))=="<class 'numpy.ndarray'>"):
            return Image.fromarray(image).filter(ImageFilter.GaussianBlur(self.radius))
        else:
            print("\n<> Exception : Image Argument must be of Type PIL IMAGE/JPEG IMAGE/PNG IMAGE or NUMPY ARRAY!\n")
            return None

#testing code for debugging purpose ->
#import numpy as np
#obj1 = BlurImage(10)
#img = Image.open(r"C:\Users\mezartine\Documents\snake.jpeg").convert('RGBA')
#obj1.__call__(img).show()
