'''
	PACKAGE DEVELOPED BY : SUBHAM GHOSH
	ROLL NO. : 20CS10065
	SECOND YEAR UNDERGRADUATE STUDENT CSE
	IIT KGP
'''

#if output_size argument is given wrong then the image is not rescaled
#Imports
from PIL import Image
from math import floor

supported_image_types = ["<class 'PIL.JpegImagePlugin.JpegImageFile'>", "<class 'PIL.PngImagePlugin.PngImageFile'>", "<class 'PIL.Image.Image'>"]

class RescaleImage(object):
    '''
        Rescales the image to a given size.
    '''

    def __init__(self, output_size, scale=None):
        '''
            Arguments:
            output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
        '''

        # Write your code here
        self.scale = scale;
        self.output_size = output_size
        if(type(self.output_size)==tuple):
            if (output_size.__len__() < 2):
                print("\n<> Exception : Output_Size tuple must have atleast two elements! Setting default output_size = 0 (The Image won't be rescaled)\n")
                self.output_size = 0

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''

        # Write your code here
        if(type(self.output_size)==tuple and type(self.output_size[0])==int):
            if (str(type(image)) in supported_image_types):
                return image.resize(self.output_size)
            elif (str(type(image)) == "<class 'numpy.ndarray'>"):
                return Image.fromarray(image).resize(self.output_size)
            else:
                print("\n<> Exception : Image Argument must be of Type PIL IMAGE/JPEG IMAGE/PNG IMAGE or NUMPY ARRAY!\n")
                return None
        elif(type(self.output_size) == int):
            if (str(type(image)) in supported_image_types):
                if(self.output_size==0):
                    return image
                a = image.size[0]
                b = image.size[1]
                if(a<b):
                    b = b * self.output_size // a
                    a = self.output_size
                else:
                    a = a * self.output_size // b
                    b = self.output_size
                return image.resize((a,b))
            elif (str(type(image)) == "<class 'numpy.ndarray'>"):
                sample = Image.fromarray(image)
                if (self.output_size == 0):
                    return sample
                a = sample.size[0]
                b = sample.size[1]
                if (a < b):
                    b = b * self.output_size / a
                    a = self.output_size
                else:
                    a = a * self.output_size / b
                    b = self.output_size
                return sample.resize((a, b))
            else:
                print("\n<> Exception : Image Argument must be of Type PIL IMAGE/JPEG IMAGE/PNG IMAGE or NUMPY ARRAY!\n")
                return None
        elif(type(self.scale)==float or type(self.scale)==int):
            if (str(type(image)) in supported_image_types):
                a = floor(image.size[0]*self.scale)
                b = floor(image.size[1]*self.scale)
                return image.resize((a,b))
            elif (str(type(image)) == "<class 'numpy.ndarray'>"):
                sample = Image.fromarray(image)
                a = floor(sample.size[0]*self.scale)
                b = floor(sample.size[1]*self.scale)
                return sample.resize((a,b))
            else:
                print("\n<> Exception : Image Argument must be of Type PIL IMAGE/JPEG IMAGE/PNG IMAGE or NUMPY ARRAY!\n")
                return None
        else:
            print("\n<> Exception : Output_Size/Scale Argument must be of Type INT or a TUPLE OF INT!\n")

#testing code for debugging purpose ->
#img = Image.open(r"C:\Users\mezartine\Downloads\CS29006_SW_Lab_Spr2022-master\Python_DS_Assignment\data\imgs\5.jpg").convert('RGBA')
#RescaleImage(())(img).show()
