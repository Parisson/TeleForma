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

		fixed_log = 'mp3_fixed'
                tofix_log = 'mp3.tofix'
                if ext == 'mp3' and tofix_log in dir_files and not fixed_log in dir_files:
                    print path
                    for file in dir_files:
                        ext = os.path.splitext(file)[1][1:]
                        if ext == 'webm':
                            break
                    source = root + os.sep + file
                    os.system('touch ' + root + os.sep + fixed_log)
                    os.system('rm ' + root + os.sep + tofix_log)
                    if os.path.getsize(source):
                        self.fix_mp3(source, path)
                        #pass

                fixed_log = 'webm.fixed'
                tofix_log = 'webm.tofix'

                if ext == 'webm' and not fixed_log in dir_files:
                    print path
                    os.system('touch ' + root + os.sep + fixed_log)
                    if os.path.getsize(path):
                        self.fix_webm(path)
                        #pass

                if ext == 'webm' and tofix_log in dir_files:
                    print path
                    os.system('touch ' + root + os.sep + fixed_log)
                    os.system('rm ' + root + os.sep + tofix_log)
                    if os.path.getsize(path):
                        self.hard_fix_webm(path):
                        #pass


    def hard_fix_webm(self, path):
        try:
            tmp_file = self.tmp_dir + 'out.webm '
            command = 'ffmpeg -loglevel 0 -i '+ path + ' -vcodec libvpx -vb 500k -acodec libvorbis -ab 96k -f webm -y ' + tmp_file + ' > /dev/null'
            print command
            os.system(command)
            command = 'mv '  + tmp_file + path
            os.system(command)
        except:
            pass


    def fix_webm(self, path):
        try:
            tmp_file = self.tmp_dir + 'out.webm '
            command = 'ffmpeg -loglevel quiet -i '+ path + ' -vcodec copy -acodec copy -f webm -y ' + tmp_file + ' > /dev/null'
            print command
            os.system(command)
            command = 'mv '  + tmp_file + path
            os.system(command)
        except:
            pass

    def fix_mp3(self, source, path):
        try:
            command = 'ffmpeg -loglevel quiet -i '+ source + ' -ab 96k -y ' + path + ' > /dev/null'
            print command
            os.system(command)
        except:
            pass




dir = sys.argv[-1]
f = FixCheckMedia(dir)
f.process()
