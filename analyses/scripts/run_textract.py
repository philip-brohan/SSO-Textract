#!/usr/bin/env python

# Run Textract on the selected image

import argparse
import pickle
import boto3

parser = argparse.ArgumentParser()
parser.add_argument("--source", help="Image file name",
                    type=str,default='modified.jpg')
parser.add_argument("--opfile", help="Output file name",
                    default="detection.pkl",
                    type=str,required=False)
args = parser.parse_args()

# Load the jpeg
with open(args.source,'rb') as jf:
    ie=jf.read()

# Analyze the document
client = boto3.client('textract')
response = client.detect_document_text(Document={'Bytes': ie})

# Save the resulting JSON
pickle.dump(response, open( args.opfile, "wb" ) )
