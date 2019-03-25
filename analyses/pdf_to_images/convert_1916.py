#!/usr/bin/env python

# Split the NMLA pfd of the 1916 second order stations book into
#  1 jpeg per station-month.

import subprocess
import os
import glob
from PIL import Image

source_file="../../originals/1916.pdf"
if not os.path.isfile(source_file):
    raise FileNotFoundError("Original pdf not found")

image_dir="../../images/1916"
if not os.path.isdir(image_dir):
    os.makedirs(image_dir)

# Split the PDF into pages
proc = subprocess.Popen("convert -density 300 %s %s/page_%%04d.jpg" % 
                            (source_file,image_dir),
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       shell=True)
(out, err) = proc.communicate()
print(err)

# Split the pages into quarters
pages=glob.glob("%s/page_????.jpg" % image_dir)

for page in pages:
    pn=int(page[-8:-4])
    if pn<5 or pn>29: continue
    im=Image.open(page)
    w, h = im.size
    area = (w/10, 0, w/2*1.03, h/2*1.1)
    sub_im=im.crop(area)
    sub_im.save("%s_tl.jpg" % page[:-4])
    area = (w/2*1.03, 0, w, h/2*1.1)
    sub_im=im.crop(area)
    sub_im.save("%s_tr.jpg" % page[:-4])
    area = (w/10, h/2*1.1, w/2*1.03, h)
    sub_im=im.crop(area)
    sub_im.save("%s_bl.jpg" % page[:-4])
    area = (w/2*1.03, h/2*1.1, w, h)
    sub_im=im.crop(area)
    sub_im.save("%s_br.jpg" % page[:-4])
   
