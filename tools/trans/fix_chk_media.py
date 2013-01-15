#!/usr/bin/python

import os, sys, psutil
import datetime
from ebml.utils.ebml_data import *

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

                fixed_log = 'mp3.fixed'
                tofix_log = 'mp3.tofix'

                if ext == 'mp3' and tofix_log in dir_files and not fixed_log in dir_files:
                    print path
                    for file in dir_files:
                        source_ext = os.path.splitext(file)[1][1:]
                        if source_ext == 'webm':
                            source = root + os.sep + file
                            if os.path.getsize(source):
                                self.fix_mp3(source, path)
                                os.system('touch ' + root + os.sep + fixed_log)
                                os.system('rm ' + root + os.sep + tofix_log)
                            break
                            #pass

                fixed_log = 'webm.fixed'
                tofix_log = 'webm.tofix'

                if ext == 'webm' and not fixed_log in dir_files:
                    print path
                    if os.path.getsize(path):
                        self.fix_webm(path)
                        os.system('touch ' + root + os.sep + fixed_log)
                        #pass

                if ext == 'webm' and tofix_log in dir_files and not fixed_log in dir_files:
                    print path
                    if os.path.getsize(path):
                        self.fix_webm(path)
                        os.system('touch ' + root + os.sep + fixed_log)
                        os.system('rm ' + root + os.sep + tofix_log)
                        #pass


    def hard_fix_webm(self, path):
        try:
            tmp_file = self.tmp_dir + 'out.webm '
            command = 'ffmpeg -loglevel 0 -i '+ path + ' -vcodec libvpx -vb 500k -acodec libvorbis -aq 7 -f webm -y ' + tmp_file + ' > /dev/null'
            print command
            os.system(command)
            command = 'mv '  + tmp_file + path
            os.system(command)
        except:
            pass


    def fix_webm(self, path):
        try:
            tmp_file = self.tmp_dir + 'out.webm'
            command = 'ffmpeg -loglevel 0 -i ' + path + ' -vcodec copy -acodec copy -f webm -y ' + tmp_file + ' > /dev/null'
            print command
            os.system(command)
            ebml_obj = EBMLData(tmp_file)
            offset = ebml_obj.get_first_cluster_timecode()
            command = 'ffmpeg -loglevel 0 -ss ' + str(offset) + ' -i ' + tmp_file + ' -vcodec copy -acodec copy -f webm -y ' + path + ' > /dev/null'
            print command
            os.system(command)
        except:
            pass

    def fix_mp3(self, source, path):
        try:
            command = 'ffmpeg -loglevel 0 -i '+ source + ' -aq 6 -y ' + path + ' > /dev/null'
            print command
            os.system(command)
        except:
            pass

def get_pids(name, args=None):
    """Get a process pid filtered by arguments and uid"""
    pids = []
    for proc in psutil.process_iter():
        if proc.cmdline:
            if name == proc.name:
                if args:
                    if args in proc.cmdline:
                        pids.append(proc.pid)
                else:
                    pids.append(proc.pid)
    return pids

dir = sys.argv[-1]

path =  os.path.abspath(__file__)
pids = get_pids('python2.6',args=path)

print datetime.datetime.now()
if len(pids) <= 1:
    print 'starting process...'
    f = FixCheckMedia(dir)
    f.process()
    print 'process finished.\n'
else:
    print 'already started !\n'
