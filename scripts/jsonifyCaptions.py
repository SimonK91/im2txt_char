#!/usr/bin/env python3


import os, sys
import argparse
import json
from parseCaptions import parseCaptions

parser = argparse.ArgumentParser(description='Generate captions.')
parser.add_argument('-i', '--infile', required=True)
args = parser.parse_args()

pwd = os.getcwd()+"/"

if args.infile[0] == "/":
    pwd = ""
captions = parseCaptions(pwd+args.infile)

jsonified = [{"image_id": int(cpt[0][13:-4]), "caption": cpt[1]} \
        for cpt in captions]

print(json.dumps(jsonified, indent=4))
