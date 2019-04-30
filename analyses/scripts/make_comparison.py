#!/usr/bin/env python

# Make a comparison figure showing Textract performance against a 
# station-month image from the SSO book.

import os
import argparse
import sys
import subprocess
from shutil import copyfile


parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year to compare",
                    type=int,required=True)
parser.add_argument("--image", help="page in year",
                    type=str,required=True)
parser.add_argument("--colour", help="Colour scale factor",
                    type=float,default=1.0)
parser.add_argument("--contrast", help="Contrast scale factor",
                    type=float,default=1.0)
parser.add_argument("--brightness", help="Brightness scale factor",
                    type=float,default=1.0)
parser.add_argument("--sharpness", help="Sharpness scale factor",
                    type=float,default=1.0)
parser.add_argument("--opimg", help="Image output file name",
                    default="oplot_text.png",
                    type=str,required=False)
parser.add_argument("--unpaper", help="Deskew with unpaper?",
                    action='store_true')
args = parser.parse_args()

source="../images/%04d/%s.jpg" % (args.year,args.image)

# Deskew the image
opfile=("../images.processed/%04d/%s/unpaper.jpg" % 
                              (args.year,args.image))
if not os.path.isdir(os.path.dirname(opfile)):
    os.makedirs(os.path.dirname(opfile))
if args.unpaper:
    proc = subprocess.Popen("./scripts/modify.py " +
                            "--source=%s "     % source +
                            "--unpaper " +
                            "--opfile=%s" % opfile,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(err)
else:
    opfile=("../images.processed/%04d/%s/copy.jpg" % 
                              (args.year,args.image))
    copyfile(source,opfile)
   
# Make the modified image
imfile=opfile
opfile=("../images.processed/%04d/%s/modified.jpg" % 
                              (args.year,args.image))
proc = subprocess.Popen("./scripts/modify.py " +
                        "--source=%s "     % imfile +
                        "--colour=%f "     % args.colour +
                        "--contrast=%f "   % args.contrast +
                        "--brightness=%f " % args.brightness +
                        "--sharpness=%f "  % args.sharpness +
                        "--opfile=%s" % opfile,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
if len(err)>0: 
    print(err)
    sys.exit(0)

# Run Textract
infile=opfile
opfile=("../images.processed/%04d/%s/textract.pkl" % 
                              (args.year,args.image))
proc = subprocess.Popen("./scripts/run_textract.py " +
                        "--source=%s "     % infile +                    
                        "--opfile=%s" % opfile,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
if len(err)>0: 
    print(err)
    sys.exit(0)

# Make the validation plot
infile=opfile
opfile=("../images.processed/%04d/%s/oplot_text.png" % 
                              (args.year,args.image))
proc = subprocess.Popen("./scripts/oplot_text.py " +
                        "--source=%s "     % imfile +
                        "--pickle=%s "     % infile +
                        "--opfile=%s "     % opfile,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
if len(err)>0: 
    print(err)
    sys.exit(0)
