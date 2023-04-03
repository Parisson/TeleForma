#!/usr/bin/python3.5

import os    
from chardet import detect
from pyutil import filereplace
srcfile = "./var/backup/mariadb.dump"
trgfile = "./var/backup/mariadb2.dump"

# get file encoding type
def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

from_codec = get_encoding_type(srcfile)

# add try: except block for reliability
try: 
    with open(srcfile, 'r', encoding=from_codec) as f, open(trgfile, 'w', encoding='utf-8') as e:
        text = f.read() # for small files, for big use chunks
        e.write(text)

    os.remove(srcfile) # remove old encoding file
    os.rename(trgfile, srcfile) # rename new encoding
except UnicodeDecodeError:
    print('Decode Error')
except UnicodeEncodeError:
    print('Encode Error')

# replace charset latin1 to ut8
filereplace(srcfile,"CHARSET=latin1","CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")