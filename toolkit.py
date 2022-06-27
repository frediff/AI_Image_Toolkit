"""
Code written by Subham Ghosh
2nd Year CSE Undergraduate
IIT KGP
"""

from my_package.model import InstanceSegmentationModel
from my_package.data import Dataset
from my_package.analysis import plot_visualization
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage
import PIL.Image
import PIL.ImageTk
import numpy as np
from tkinter import *
import os
from functools import partial
from tkinter import filedialog
import matplotlib.pyplot as plt

# Defining the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor, e):
	##############
	# This function will pop-up a dialog for the user to select an input image file.
	# Once the image is selected by the user, it will automatically get the corresponding outputs from the segmentor.
	# Called the segmentor from here, then computde the output images from using the `plot_visualization` function and saved it as an image.
	# Once the output is computed it will be shown automatically based on choice the dropdown button is at.

	try:
		os.mkdir("./tmp")
	except OSError:
		1

	path_selected = filedialog.askopenfilename()
	e.config(text="  "+path_selected+"  ")
	img_file = PIL.Image.open(path_selected)
	fig = plt.figure(figsize=(20, 20))
	t_plot = fig.add_subplot(111)
	plt.axis('off')
	plt.imshow(img_file)
	fig.savefig("./tmp/org.jpg",bbox_inches='tight', transparent="True",pad_inches=1)
	plt.close(fig)
	segmentation = segmentor((np.uint8(img_file) / 255).transpose(2, 0, 1)[0:3])

	dictL = {}
	dictL["image"] = img_file
	dictL["gt_png_ann"] = segmentation[1]
	dictL["gt_bboxes"] = segmentation[0]
	dictL["category"] = segmentation[2]
	dictL["confidence"] = segmentation[3]

	plot_visualization("CompleteSegmentation",dictL, "./tmp/seg.jpg")
	plot_visualization("OnlyBoundingBox",dictL, "./tmp/bbx.jpg")

	img_file.close()

# `process` function definition starts from here.
# will process the output when clicked.
def process(clicked):
	##############
	# Will show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
	# Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
	# Note: Handled the case if the user clicks on the `Process` button without selecting any image file.
	w = Toplevel()

	try:
		w.title("Final Output")
		f = 3

		img_org = PIL.Image.open("./tmp/org.jpg")
		img_seg = PIL.Image.open("./tmp/seg.jpg")
		img_bbx = PIL.Image.open("./tmp/bbx.jpg")
		img_orgL = PIL.ImageTk.PhotoImage(img_org.resize((img_org.size[0]//f,img_org.size[1]//f)))
		img_segL = PIL.ImageTk.PhotoImage(img_seg.resize((img_org.size[0]//f,img_org.size[1]//f)))
		img_bbxL = PIL.ImageTk.PhotoImage(img_bbx.resize((img_org.size[0]//f,img_org.size[1]//f)))

		Label(w,text='ORIGINAL IMAGE',font=("Bahnschrift", "12"),bg='#00ff1e').grid(row=0,column=0,sticky = N+E+S+W)
		orgl = Label(w, image = img_orgL, bg='#4b4be3')
		orgl.grid(row=1,column=0, sticky=N+E+S+W)

		if(clicked.get() == "Segmentation"):
			Label(w,text='SEGMENTATION',font=("Bahnschrift", "12"),bg='#00ff1e').grid(row=0,column=1,sticky = N+E+S+W)
			segl = Label(w, image = img_segL, bg='#4b4be3')
			segl.grid(row=1,column=1,sticky=N+E+S+W)
		else:
			Label(w,text='BOUNDING BOXES',font=("Bahnschrift", "12"),bg='#00ff1e',).grid(row=0,column=1,sticky = N+E+S+W)
			bbxl = Label(w, image = img_bbxL, bg='#4b4be3')
			bbxl.grid(row=1,column=1, sticky=N+E+S+W)

		img_org.close()
		img_seg.close()
		img_bbx.close()
	except FileNotFoundError:
		w.title("Error")
		msg = Message(w, text = "First Select a Image!",width=200)
		msg.config(bg='#fc4949', font=("Bahnschrift", "12"), borderwidth=8)
		msg.pack(fill=BOTH,ipadx=20,expand=True)

	w.mainloop()
	##############

if __name__ == '__main__':

	##############
	# Instantiating the root window.
	# Providing a title to the root window.
	root = Tk(className=" Image Segmentation and Bounding Box | Python GUI | SUBHAM GHOSH")
	##############

	# Setting up the segmentor model.
	annotation_file = './data/annotations.jsonl'
	transforms = []

	# Instantiating the segmentor model.
	segmentor = InstanceSegmentationModel()

	# Instantiating the dataset.
	dataset = Dataset(annotation_file, transforms=transforms)

	# Declaring the options.
	options = ["Segmentation", "Bounding-box"]
	clicked = StringVar()
	clicked.set(options[0])
	path_selected = StringVar()
	e = Label(root,text="\t\t\t\t\t\t\t\t",font=("Bahnschrift", "12"), relief=FLAT, fg="#0000ff")
	e.grid(row=0, column=0, columnspan=2, sticky=N+E+S+W)

	##############
	# Declaring the file browsing button
	image_browse_button = Button(root, text="Browse Image", command=partial(fileClick,clicked,dataset,segmentor,e))
	image_browse_button.config(font=("Bahnschrift", "12"), relief=FLAT, bg="#1c7305", fg="white")
	image_browse_button.grid(row=0,column=2,sticky=N+E+S+W)
	##############

	##############
	# Declaring the drop-down button
	drop_down_button = OptionMenu( root , clicked , *options )
	drop_down_button.config(bg="light blue",relief=FLAT, font =("Bahnschrift", "12"))
	drop_down_button.grid(row=0,column=3, sticky=N+E+S+W)
	##############

	# This is the `Process` button
	myButton = Button(root, text="Process", font=("Bahnschrift", "12"), bg="#ff9d00",relief=FLAT, command=partial(process, clicked)).grid(row=0, column=4, sticky=N+E+S+W)

	##############
	# Executing with mainloop()
	root.mainloop()
	for file in os.scandir('./tmp'):
		os.remove(file.path)
	##############
