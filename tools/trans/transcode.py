#!/usr/bin/python

import os, sys, string

root_dir = sys.argv[-1]
source_format = 'webm'
ffmpeg_args = {'mp3' : ' -vn -acodec libmp3lame -aq 6',
               'ogg' : ' -vn -acodec copy '
               'mp4' : ' -vcodec libx264 -vb 512k -acodec libfaac -ab 96k ' 
              }

done = []
log_file = 'transmeta.log'
f = open(log_file, 'r')
for line in f.readlines():
    done.append(line)


for root, dirs, files in os.walk(root_dir):
    for file in files:
        path = root + os.sep + file
        name, ext = os.path.splitext(file)
        if ext == source_format:
            for format in ffmpeg_args.keys():
                dest = root + os.sep + name + format
                if not dest in done:
                    command = 'ffmpeg -i ' + path + ffmpeg_args[format] + ' -y ' + dest
                    os.system(command)
                    logger.info(dest)

                

