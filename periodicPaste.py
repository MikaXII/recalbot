#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import settings
import os
import codecs
from zpaste import ZPaste
import time

class PPaste():
    def __init__(self):
        self.read_all_file("./mega","mega.txt")
        self.read_all_file("./wiki","wiki.txt")        


    def read_all_file(self, folder, file):

        data = {}
        for dir_entry in os.listdir(folder):
            dir_entry_path = os.path.join(folder, dir_entry)
            if os.path.isfile(dir_entry_path):
                with codecs.open(dir_entry_path, 'r', encoding='utf8') as my_file:
                    data[dir_entry] = my_file.read()
        self.paste_info(data, file);

    def paste_info(self, info, file):
        a = ZPaste(info)
        with codecs.open("./links/"+file,'w','utf-8',errors="replace") as myFile:
            myFile.writelines(a.link)
        del a
        

if __name__ == "__main__":
    PPaste()
