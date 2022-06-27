#Imports
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math

def plot_visualization(query,dictL,dest_path,upperBound=0.95,title_p=None): # Write the required arguments
  # This function has some arguments to control the plotting of bounding boxes and masks and optionally add titles if provided
  # The function will plot the predicted segmentation maps and the bounding boxes on the images and save them.

    if(query=='OnlyBoundingBox'): # plots only bounding boxes formed from passing the image to the model and labels them for boxes with scores greater than upperBound
        image_file = dictL['image']
        fig = plt.figure(figsize=(20, 20))
        t_plot = fig.add_subplot(111)
        plt.axis('off')
        idx = dictL["category"].__len__()
        if(type(title_p)==str):
            plt.title(title_p,family="serif",weight='bold',va='top',color='green',fontsize=30, pad=50)
        plt.imshow(image_file)
        for iter in range(idx):
            bbox = dictL["gt_bboxes"][iter]
            xy = bbox[0]
            w = bbox[1][0] - bbox[0][0]
            h = bbox[1][1] - bbox[0][1]
            t_plot.add_patch(plt.Rectangle((xy[0], xy[1]), w, h, ec='r', fc=(0, 0, 0, 0), lw=4))
            if(dictL["confidence"][iter]>upperBound):
                t_plot.annotate(dictL["category"][iter] + " " + str(dictL["confidence"][iter]), [xy[0],xy[1]-5], color='b',weight='bold', va='bottom', ha='left', fontsize=22, family='monospace')
        fig.savefig(dest_path,bbox_inches='tight', transparent="True",pad_inches=1)
        plt.close(fig)

    elif(query=='OnlyBoundingBox_PreData'): # plots only the bounding boxes using the pre-computed json file
        image_file = dictL['image']
        fig = plt.figure(figsize=(20, 20))
        t_plot = fig.add_subplot(111)
        plt.axis('off')
        idx = dictL["category"].__len__()
        if(type(title_p)==str):
            plt.title(title_p,family="serif",weight='bold',va='top',color='green',fontsize=30, pad=50)
        plt.imshow(image_file)
        for iter in range(idx):
            left = dictL["gt_bboxes"][iter][0]
            top = dictL["gt_bboxes"][iter][1]
            w = dictL["gt_bboxes"][iter][2]
            h = dictL["gt_bboxes"][iter][3]
            t_plot.add_patch(plt.Rectangle((left,top), w, h, ec='r', fc=(0, 0, 0, 0), lw=4))
        fig.savefig(dest_path,bbox_inches='tight', transparent="True",pad_inches=1)
        plt.close(fig)

    elif(query=="CompleteSegmentation"): # plots the masks and bounding boxes for the top-3 scores predicted by the model applied on the image
        if(dictL["category"].__len__()>3): # plotting top_3
            s1 = 0
            s2 = 0
            s3 = 0
            i1 = 0
            i2 = 0
            i3 = 0
            marks = dictL["confidence"]
            for idx in range(marks.__len__()):
                score = marks[idx]
                if (score > s1):
                    s3 = s2
                    i3 = i2
                    s2 = s1
                    i2 = i1
                    s1 = score
                    i1 = idx
                elif (score > s2):
                    s3 = s2
                    i3 = i2
                    s2 = score
                    i2 = idx
                elif (score > s3):
                    s3 = score
                    i3 = idx
                else:
                    continue

            top_3 = [i1, i2, i3]
            image_file = dictL['image']
            fig = plt.figure(figsize=(20, 20))
            t_plot = fig.add_subplot(111)
            plt.yticks(fontsize=16, weight='bold')
            plt.xticks(fontsize=16, weight='bold')
            if(type(title_p)==str):
                plt.title(title_p,family="serif",weight='bold',va='top',color='green',fontsize=30, pad=50)
            plt.imshow(image_file)
            for iter in top_3:
                pred_masks = dictL["gt_png_ann"][iter]
                img = Image.fromarray(np.uint8(255 - pred_masks[0] * 255), 'P')
                img = img.convert('RGBA')
                width = img.size[0]
                height = img.size[1]
                colorM = tuple(np.random.choice(range(256), size=3))
                colorM = colorM + (240,)
                for x in range(0, width):  # process all pixels
                    for y in range(0, height):
                        data = img.getpixel((x, y))
                        if (data[0] <= 200 and data[1] <= 200 and data[2] <= 200):
                            img.putpixel((x, y), colorM)
                        else:
                            img.putpixel((x, y), (255, 255, 255, 0))
                plt.imshow(img)
                bbox = dictL["gt_bboxes"][iter]
                xy = bbox[0]
                w = bbox[1][0] - bbox[0][0]
                h = bbox[1][1] - bbox[0][1]
                t_plot.add_patch(plt.Rectangle((xy[0], xy[1]), w, h, ec='r', fc=(0, 0, 0, 0), lw=4))
                t_plot.annotate(dictL["category"][iter] + " " + str(dictL["confidence"][iter]), [xy[0],xy[1]-5], color='b', weight='bold', va='bottom',ha='left', fontsize=22, family='monospace')
            fig.savefig(dest_path,bbox_inches='tight', transparent="True",pad_inches=1)
            plt.close(fig)

        else: # plotting all boxes if less than 3 boxes are predicted
            image_file = dictL['image']
            fig = plt.figure(figsize=(20, 20))
            t_plot = fig.add_subplot(111)
            plt.yticks(fontsize=16, weight='bold')
            plt.xticks(fontsize=16, weight='bold')
            idx = dictL["category"].__len__()
            if(type(title_p)==str):
                plt.title(title_p,family="serif",weight='bold',va='top',color='green',fontsize=30, pad=50)
            plt.imshow(image_file)
            for iter in range(idx):
                pred_masks = dictL["gt_png_ann"][iter]
                img = Image.fromarray(np.uint8(255 - pred_masks[0] * 255), 'P')
                img = img.convert('RGBA')
                width = img.size[0]
                height = img.size[1]
                colorM = tuple(np.random.choice(range(256), size=3))
                colorM = colorM + (240,)
                for x in range(0, width):  # process all pixels
                    for y in range(0, height):
                        data = img.getpixel((x, y))
                        if (data[0] <= 200 and data[1] <= 200 and data[2] <= 200):
                            img.putpixel((x, y), colorM)
                        else:
                            img.putpixel((x, y), (255, 255, 255, 0))
                plt.imshow(img)
                bbox = dictL["gt_bboxes"][iter]
                xy = bbox[0]
                w = bbox[1][0] - bbox[0][0]
                h = bbox[1][1] - bbox[0][1]
                t_plot.add_patch(plt.Rectangle((xy[0], xy[1]), w, h, ec='r', fc=(0, 0, 0, 0), lw=4))
                t_plot.annotate(dictL["category"][iter] + " " + str(dictL["confidence"][iter]), [xy[0],xy[1]-5], color='b', weight='bold', va='bottom',ha='left', fontsize=22, family='monospace')
            fig.savefig(dest_path,bbox_inches='tight', transparent="True",pad_inches=1)
            plt.close(fig)

def multi_plot_visualization(dictList,dest_path,box_w=40,box_h=40,title_list=[]): # does a subplot of the list of images and their segmentations provided in the dictionary list
    count = 0
    plot_size = math.sqrt(dictList.__len__())
    plot_size = math.floor(plot_size)
    hh = plot_size
    ww = math.ceil(dictList.__len__() / hh)
    # the above code auto adjusts and finds the best fit way to arrange the images in the subplot in hh*ww matrix
    fig = plt.figure(figsize=(box_w, box_h))
    for dictL in dictList:
        count = count + 1
        t_plot = fig.add_subplot(hh, ww, count)
        if(count <= title_list.__len__()): # optionally add titles
            plt.title(title_list[count-1],family="serif",weight='bold',va='top',color='green',fontsize=30,pad=50)
        if (dictL["category"].__len__() > 3): # for images with more than 3 masks predicted plot top 3
            s1 = 0
            s2 = 0
            s3 = 0
            i1 = 0
            i2 = 0
            i3 = 0
            marks = dictL["confidence"]
            for idx in range(marks.__len__()):
                score = marks[idx]
                if (score > s1):
                    s3 = s2
                    i3 = i2
                    s2 = s1
                    i2 = i1
                    s1 = score
                    i1 = idx
                elif (score > s2):
                    s3 = s2
                    i3 = i2
                    s2 = score
                    i2 = idx
                elif (score > s3):
                    s3 = score
                    i3 = idx
                else:
                    continue

            top_3 = [i1, i2, i3]
            image_file = dictL['image']
            plt.yticks(fontsize=16, weight='bold')
            plt.xticks(fontsize=16, weight='bold')
            plt.imshow(image_file)
            for iter in top_3:
                pred_masks = dictL["gt_png_ann"][iter]
                img = Image.fromarray(np.uint8(255 - pred_masks[0] * 255), 'P')
                img = img.convert('RGBA')
                width = img.size[0]
                height = img.size[1]
                colorM = tuple(np.random.choice(range(256), size=3))
                colorM = colorM + (240,)
                for x in range(0, width):  # process all pixels
                    for y in range(0, height):
                        data = img.getpixel((x, y))
                        if (data[0] <= 200 and data[1] <= 200 and data[2] <= 200):
                            img.putpixel((x, y), colorM)
                        else:
                            img.putpixel((x, y), (255, 255, 255, 0))
                plt.imshow(img)
                bbox = dictL["gt_bboxes"][iter]
                xy = bbox[0]
                w = bbox[1][0] - bbox[0][0]
                h = bbox[1][1] - bbox[0][1]
                t_plot.add_patch(plt.Rectangle((xy[0], xy[1]), w, h, ec='r', fc=(0, 0, 0, 0), lw=4))
                t_plot.annotate(dictL["category"][iter] + " " + str(dictL["confidence"][iter]), [xy[0], xy[1] - 5],
                                color='b', weight='bold', va='bottom', ha='left', fontsize=22, family='monospace')
        else: # plotting all boxes if less than 3 boxes are predicted
            image_file = dictL['image']
            plt.yticks(fontsize=16, weight='bold')
            plt.xticks(fontsize=16, weight='bold')
            idx = dictL["category"].__len__()
            plt.imshow(image_file)
            for iter in range(idx):
                pred_masks = dictL["gt_png_ann"][iter]
                img = Image.fromarray(np.uint8(255 - pred_masks[0] * 255), 'P')
                img = img.convert('RGBA')
                width = img.size[0]
                height = img.size[1]
                colorM = tuple(np.random.choice(range(256), size=3))
                colorM = colorM + (240,)
                for x in range(0, width):  # process all pixels
                    for y in range(0, height):
                        data = img.getpixel((x, y))
                        if (data[0] <= 200 and data[1] <= 200 and data[2] <= 200):
                            img.putpixel((x, y), colorM)
                        else:
                            img.putpixel((x, y), (255, 255, 255, 0))
                plt.imshow(img)
                bbox = dictL["gt_bboxes"][iter]
                xy = bbox[0]
                w = bbox[1][0] - bbox[0][0]
                h = bbox[1][1] - bbox[0][1]
                t_plot.add_patch(plt.Rectangle((xy[0], xy[1]), w, h, ec='r', fc=(0, 0, 0, 0), lw=4))
                t_plot.annotate(dictL["category"][iter] + " " + str(dictL["confidence"][iter]), [xy[0], xy[1] - 5],
                                color='b', weight='bold', va='bottom', ha='left', fontsize=22, family='monospace')

    fig.savefig(dest_path,bbox_inches='tight', transparent="True",pad_inches=1)
    plt.close(fig)
