#!/usr/bin/python3

import os
import sys
from pypdf import PdfReader

dir = sys.argv[-1]

for f in os.listdir(dir):
    filename = f.split(os.sep)[-1]
    reader = PdfReader(dir + os.sep + f)
    meta = reader.metadata
    print(filename, ":", meta['/Downloader'])
