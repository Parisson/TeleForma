# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Authors: Guillaume Pellerin <yomguy@parisson.com>


import time
from .xmltodict2 import *
import json
from collections import defaultdict
import pprint

ENCODING = 'utf-8'

def parse_timecode(value, fps):
    """
    Parse a timestamp, either new HH:MM:SS.mmm format or old frames format
    """
    if ':' in value:
        if '.' in value:
            value, decimal = value.split('.')
        comps = value.split(':')
        comps = [ int(c) for c in comps ]
        res = 0
        for comp in comps:
            res = res * 60 + comp
        res += float(decimal) / 10**len(decimal)
    else:
        res = float(value)  / fps
    return res
    

class KDEnLiveSession(object):

    def __init__(self, path):
        self.session = xmltodict(path)

    def entries(self):
        entries = []
        for attr in self.session['children']:
            if 'playlist' in self.get_name(attr) and 'children' in attr:
                for att in attr['children']:
                    if 'entry' in self.get_name(att) and att['attributes']['producer'] != 'black':
                        entries.append(att['attributes'])
        return entries

    def video_entries(self):
        entries = []
        for attr in self.session['children']:
            if 'playlist' in self.get_name(attr) and 'children' in attr:
                plid = attr['attributes'].get('id', '')
                if 'main_bin' in plid or 'main bin' in plid:
                    continue
                for att in attr['children']:                    
                    if 'entry' in self.get_name(att) and att['attributes']['producer'] != 'black' \
                            and not 'audio' in att['attributes']['producer']:
                        entries.append(att['attributes'])
        return entries

    def entries_sorted(self):
        return sorted(self.entries(), key=lambda k: int(k['in']), reverse=False)

    def get_fps(self):
        profile = self.profile()
        fps = float(profile['frame_rate_num'])/float(profile['frame_rate_den'])
        return fps
    
    def entries_video_seconds(self):
        fps = self.get_fps()
        res = []
        start = 0
        entries = self.video_entries()

        for entry in entries:
            id = entry['producer'].split('_')[0]
            t_in = parse_timecode(entry['in'], fps)
            t_out = parse_timecode(entry['out'], fps)
            t_len = t_out - t_in
            end = start + t_len
            res.append({ 'id': str(id), 't': start, 'in': t_in, 'out': t_out })
            start = end
        return res

    def cuts(self, entries):
        i = 0
        cuts = [0, ]
        for entry in entries:
            if i > 0:
                cuts.append(cuts[i-1] + int(entries[i]['in'])-int(entries[i-1]['out']))
            i += 1
        return cuts

    def first_video_frame(self):
        return int(self.entries_sorted()[0]['in'])

    def get_name(self, attr):
        """
        Get the name of an attibute, handling encoding issues
        """
        name = attr['name']
        if isinstance(name, bytes):
            name = name.decode(ENCODING)
        return name
    
    def profile(self):
        for attr in self.session['children']:
            if 'profile' in self.get_name(attr):
                return attr['attributes']

    def fix_text(self, text):
        try:
            s = text.split(' ')
            i = int(s[1])
            s.insert(2, ':')
            return ' '.join(s)
        except:
            return text

    def get_producer_altids(self):
        """
        Get the alternate ids of producers if any
        """
        by_names = defaultdict(list)
        for attr in self.session['children']:
            if 'producer' in self.get_name(attr) and 'children' in attr:
                if "id" in attr['attributes']:
                    entry_id = attr['attributes']['id']
                    for att in attr['children']:
                        name = self.get_name(att['attributes'])
                        if 'resource' in name and 'cdata' in att:
                            by_names[att['cdata']].append(entry_id)

        alt_ids = {}
        for vals in by_names.values():
            if len(vals) > 1:
                vals = set(vals)
                for val in vals:
                    alt_ids[val] = vals

        return alt_ids
        
        
    def markers(self, offset=0, from_first_marker=False):
        """ by default return a dict of markers with timecodes relative to an origin

            if from_first_marker=False: the origin is the first entry timecode
            if from_first_marker=True: the origin is the first entry timecode before the first marker

            offset: general origin offset
        """
        markers = []
        entries = self.entries_video_seconds()
        #print("=> Video entries")
        #pprint.pprint(entries)
        title = ''
        fps = self.get_fps()
        alternate_ids = self.get_producer_altids()
        #print("=> Alternate ids")
        #pprint.pprint(alternate_ids)

        def add_marker(rel_time, comment):
            """
            Add a marker to the list from it's id, timestamp and comment
            """
            marker = {}
            marker['time'] = rel_time
            if ":" in comment:
                pre, post = comment.split(':', 1)
                if pre.isdigit():
                    comment = post
            marker['comment'] = comment
            markers.append(marker)

        def get_reltime(entry_id, marker_time, alt_ids = []):
            """
            Get the relative time of a marker linked to an entry
            """
            rel_time = 0

            for entry in entries:
                #print(entry_id, entry['id'], entry['in'], entry['out'], entry['t'], marker_time)
                if entry['in'] <= marker_time <= entry['out'] and (entry_id == entry['id'] or entry['id'] in alt_ids):
                    rel_time = entry['t'] + (marker_time - entry['in']) + offset
                    return rel_time            

        for attr in self.session['children']:
            if 'playlist' in self.get_name(attr) and 'children' in attr:
                # Old v 6.4 file format, markers in playlist
                for att in attr['children']:
                    if 'name' in att['attributes']:
                        name = self.get_name(att['attributes'])
                        if 'docmetadata.meta.attr.title.markup' in name:
                            title = att['cdata']
                        if 'marker' in name:
                            marker_time = float(name.split(':')[-1].replace(',','.').replace(' ', ''))
                            entry_id = str(name.split(':')[-2].split('.')[-1])
                            comment = self.fix_text(att['cdata'])
                            rel_time = get_reltime(entry_id, marker_time)
                            if rel_time is not None:
                                #print(comment, entry_id, marker_time, rel_time)
                                add_marker(rel_time, comment)
            elif 'producer' in self.get_name(attr) and 'children' in attr:
                # New v 6.24 file format, markers in producers
                if "id" in attr['attributes']:
                    entry_id = attr['attributes']['id']
                    alt_ids = alternate_ids.get(entry_id, [])
                    for att in attr['children']:
                        name = self.get_name(att['attributes'])
                        if 'markers' in name:
                            items = json.loads(self.fix_text(att['cdata']))
                            #print("=> Marker items")
                            #pprint.pprint(items)                            
                            for marker in items:
                                marker_time = float(marker['pos'] / fps)
                                rel_time = get_reltime(entry_id, marker_time,
                                                       alt_ids)
                                #print(marker['comment'], entry_id, marker_time, rel_time)
                                if rel_time is not None:
                                    add_marker(rel_time, marker['comment'])


        if markers and from_first_marker:
            delta = min([ marker['time'] for marker in markers ])
            for marker in markers:
                marker['time'] -= delta
        if markers:
            for marker in markers:
                rel_time = marker['time']
                marker['session_timecode'] = time.strftime('%H:%M:%S', time.gmtime(rel_time))

        return title, markers

