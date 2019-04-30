#!/usr/bin/env python

# Tweak the brightness, contrast, colour and sharpness of an image

from PIL import Image, ImageEnhance, ImageOps
import argparse
import tempfile
from subprocess import call
import os

parser = argparse.ArgumentParser()
parser.add_argument("--source", help="Image file name",
                    type=str,required=True)
parser.add_argument("--colour", help="Colour scale factor",
                    type=float,default=1.0)
parser.add_argument("--contrast", help="Contrast scale factor",
                    type=float,default=1.0)
parser.add_argument("--brightness", help="Brightness scale factor",
                    type=float,default=1.0)
parser.add_argument("--sharpness", help="Sharpness scale factor",
                    type=float,default=1.0)
parser.add_argument("--equalize", help="Equalize the image",
                    action='store_true')
parser.add_argument("--autocontrast", help="Scale contrast 0-1",
                    action='store_true')
parser.add_argument("--greyscale", help="Convert to greyscale",
                    action='store_true')
parser.add_argument("--bw", help="Convert to black and white",
                    action='store_true')
parser.add_argument("--unpaper", help="Deskew with unpaper?",
                    action='store_true')
parser.add_argument("--opfile", help="Output file name",
                    default="modified.jpg",
                    type=str,required=False)
args = parser.parse_args()

if args.unpaper:
   f1=tempfile.mktemp('.pbm')
   f2=tempfile.mktemp('.pbm')
   f3=tempfile.mktemp('.jpg')
   call("convert %s %s" % (args.source,f1),shell=True)
   call("unpaper %s %s" % (f1,f2),shell=True)
   call("convert %s %s" % (f2,f3),shell=True)
   args.source=f3
   os.remove(f1)
   os.remove(f2)

im = Image.open(args.source)

if args.greyscale:
   im=im.convert('L')

if args.bw:
   im=im.convert('1')
   
if args.autocontrast:
   im=ImageOps.autocontrast(im,cutoff=5)
   
if args.equalize:
   im=ImageOps.equalize(im)

if args.colour != 1.0:
   enhancer = ImageEnhance.Color(im)
   im = enhancer.enhance(args.colour)

if args.contrast != 1.0:
   enhancer = ImageEnhance.Contrast(im)
   im = enhancer.enhance(args.contrast)

if args.brightness != 1.0:
   enhancer = ImageEnhance.Brightness(im)
   im = enhancer.enhance(args.brightness)

if args.sharpness != 1.0:
   enhancer = ImageEnhance.Sharpness(im)
   im = enhancer.enhance(args.sharpness)
      
im.save(args.opfile)

if args.unpaper:
    os.remove(f3)

