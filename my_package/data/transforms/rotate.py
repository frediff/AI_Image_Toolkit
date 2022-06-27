'''
	PACKAGE DEVELOPED BY : SUBHAM GHOSH
	ROLL NO. : 20CS10065
	SECOND YEAR UNDERGRADUATE STUDENT CSE
	IIT KGP
'''

#if degree argument is given wrong then the image is not rotated at all
#Imports
from PIL import Image

supported_image_types = ["<class 'PIL.JpegImagePlugin.JpegImageFile'>", "<class 'PIL.PngImagePlugin.PngImageFile'>", "<class 'PIL.Image.Image'>"]

class RotateImage(object):
    '''
        Rotates the image about the centre of the image.
    '''

    def __init__(self, degrees, doNotClipAtEdges=True):
        '''
            Arguments:
            degrees: rotation degree.
        '''

        # Write your code here
        self.doNotClipAtEdges = doNotClipAtEdges
        if(type(degrees)==int or type(degrees)==float):
            self.degrees = degrees
        else:
            print("\n<> Exception : Degree Argument must be of Type INT or FLOAT! Setting degrees = 0\n")
            self.degrees = 0

    def __call__(self, sample):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        if (str(type(sample)) in supported_image_types):
            return sample.rotate(self.degrees,expand=self.doNotClipAtEdges)
        elif (str(type(sample)) == "<class 'numpy.ndarray'>"):
            return Image.fromarray(sample).rotate(self.degrees,expand=self.doNotClipAtEdges)
        else:
            print("\n<> Exception : Image Argument must be of Type PIL IMAGE/JPEG IMAGE/PNG IMAGE or NUMPY ARRAY!\n")
            return None


#testing code for debugging purpose ->
#obj1 = RotateImage(30);
#img = Image.open(r"C:\Users\mezartine\Downloads\CS29006_SW_Lab_Spr2022-master\Python_DS_Assignment\data\imgs\5.jpg").convert('RGBA')
#RotateImage(30)(img,False).show()
#img = RotateImage("s")(6)
