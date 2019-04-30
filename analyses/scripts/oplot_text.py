#!/usr/bin/env python

# Overplot transcription results on the original image.

import argparse
import pickle
from PIL import Image

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches
import numpy

parser = argparse.ArgumentParser()
parser.add_argument("--source", help="Image file name",
                    type=str,default='modified.jpg')
parser.add_argument("--pickle", help="Pickled Textract results file name",
                    type=str,default='detection.pkl')
parser.add_argument("--opfile", help="Output file name",
                    default="oplot.png",
                    type=str,required=False)
args = parser.parse_args()

# We're going to need the original image
im = Image.open(args.source)

fig=Figure(figsize=((1*im.size[0]/100)*1.04,
                    (1*im.size[1]/100)*1.04),
       dpi=100,
       facecolor=(0.88,0.88,0.88,1),
       edgecolor=None,
       linewidth=0.0,
       frameon=False,
       subplotpars=None,
       tight_layout=None)
ax_original=fig.add_axes([0.02,0.02,0.96,0.96],label='original')
ax_result=fig.add_axes([0.02,0.02,0.96,0.96],label='result')
# Matplotlib magic
canvas=FigureCanvas(fig)
# Turn off the axis tics
ax_original.set_axis_off()
ax_result.set_axis_off()

# Show the original image
ax_original.imshow(im)

# Load the JSON from Textract for this image
textract=pickle.load( open( args.pickle, "rb" ) )
# Convert block polygon dictionary to numpy array for matplotlib
def d2p(dct):
    result=numpy.zeros((len(dct),2))
    for idx in range(len(dct)):
        result[idx,0]=dct[idx]['X']
        result[idx,1]=1.0-dct[idx]['Y']
    return result
# Get bounding box centroid for text
def b2t(dct):
    result=[0,0]
    result[0]=dct['Left']+dct['Width']/2
    result[1]=1.0-dct['Top']-dct['Height']/2
    return result
   
# Draw all the blocks
zorder=0
for block in textract['Blocks']:
    if 'Text' in block and block['BlockType']=='WORD':
       # Polygon
        pp=matplotlib.patches.Polygon(d2p(block['Geometry']['Polygon']),
                                      closed=True,
                                      edgecolor=(0.5,0.5,1,1),
                                      facecolor=(0.5,0.5,1,0.2),
                                      fill=True,
                                      linewidth=0.2,
                                      alpha=0.9,
                                      zorder=10)
        ax_result.add_patch(pp)
       # Text
        txt_centroid=b2t(block['Geometry']['BoundingBox'])
        angle=0
        if (block['Geometry']['BoundingBox']['Height'] >
            block['Geometry']['BoundingBox']['Width']*3):
            angle=90
        ax_result.text(txt_centroid[0],txt_centroid[1],
                       block['Text'],
                       fontsize=18,
                       verticalalignment='center',
                       horizontalalignment='center',
                       rotation=angle,
                       zorder=zorder+10)
    zorder=zorder+10
    

# Draw the image
fig.savefig(args.opfile)
