'''
	PACKAGE DEVELOPED BY : SUBHAM GHOSH
	ROLL NO. : 20CS10065
	SECOND YEAR UNDERGRADUATE STUDENT CSE
	IIT KGP
'''

#if flip type argument is wrong then the image is by default flipped horizontally
#Imports
from PIL import Image

supported_image_types = ["<class 'PIL.JpegImagePlugin.JpegImageFile'>", "<class 'PIL.PngImagePlugin.PngImageFile'>", "<class 'PIL.Image.Image'>"]

class FlipImage(object):
    '''
        Flips the image.
    '''

    def __init__(self, flip_type='horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''

        # Write your code here
        if(flip_type=='vertical'):
            self.flip_type = Image.FLIP_LEFT_RIGHT
        else:
            self.flip_type = Image.FLIP_TOP_BOTTOM

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        if (str(type(image)) in supported_image_types):
            return image.transpose(method=self.flip_type)
        elif (str(type(image)) == "<class 'numpy.ndarray'>"):
            return Image.fromarray(image).transpose(method=self.flip_type)
        else:
            print("\n<> Exception : Image Argument must be of Type PIL IMAGE/JPEG IMAGE/PNG IMAGE or NUMPY ARRAY!\n")
            return None

#testing code for debugging purpose ->
#img = Image.open(r"C:\Users\mezartine\Downloads\CS29006_SW_Lab_Spr2022-master\Python_DS_Assignment\data\imgs\5.jpg").convert('RGBA')
#FlipImage()(img).show()
