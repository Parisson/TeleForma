#!/usr/bin/python

import os, sys

class FixCheckMedia(object):

    def __init__(self, dir):
        self.dir = dir
        self.tmp_dir = '/home/telecaster/tmp/'
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

    def process(self):
        for root, dirs, files in os.walk(self.dir):
            for filename in files:
                path = root + os.sep + filename
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]
                dir_files = os.listdir(root)

                fix_log = 'webm.fixed'
                if ext == 'webm' and not fix_log in dir_files:
                    print path
                    self.fix_webm(path)
                    os.system('touch ' + root + os.sep + fix_log)

                fix_log = 'mp3.tofix'
                if ext == 'mp3' and fix_log in dir_files:
                    print path
                    for file in dir_files:
                        ext = os.path.splitext(file)[1][1:]
                        if ext == 'webm':
                            break
                    source = root + os.sep + file
                    self.fix_mp3(source, path)
                    os.system('rm ' + root + os.sep + fix_log)


    def fix_webm(self, path):
        command = 'ffmpeg -i '+ path + ' -vcodec copy -acodec copy -f webm -y ' + self.tmp_dir + 'out.webm'
        print command
        os.system(command)
        command = 'mv '  + self.tmp_dir + 'out.webm ' + path
        print command
        os.system(command)


    def fix_mp3(self, source, path):
        command = 'ffmpeg -i '+ source + ' -aq 9 -y ' + path
        print command
        os.system(command)




dir = sys.argv[-1]
f = FixCheckMedia(dir)
f.process()
