#!/usr/bin/env python

# Split the NMLA pfd of the 1916 second order stations book into
#  1 jpeg per station-month.

import subprocess
import os

source_file="../../originals/1916.pdf"
if not os.path.isfile(source_file):
    raise FileNotFoundError("Original pdf not found")

image_dir="../../images/1916"
if not os.path.isdir(image_dir):
    os.makedirs(image_dir)

# Split the PDF into pages
proc = subprocess.Popen("pdfseparate %s %s/page_%%04d.pdf" % 
                            (source_file,image_dir),
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       shell=True)
(out, err) = proc.communicate()
