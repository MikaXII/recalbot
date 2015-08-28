#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import irclib
import ircbot
import settings
import os
import codecs
from zpaste import ZPaste

class Recalbot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(settings.SRV, settings.PORT, settings.PWD)], settings.NAME,
                                           settings.DESC)
        self.availableCmd = ["!mega", "!wiki", "!help","!histo"]

    def on_welcome(self, serv, ev):
        serv.join("#test-recalbot")

    def on_pubmsg(self, serv, ev):
        self.auteur = irclib.nm_to_n(ev.source())
        self.canal = ev.target()
        self.message = ev.arguments()[0].decode('utf-8', errors='replace')
        self.serv = serv
        if self.find_cmd_on_string(self.message) == False:
            self.write_file("./histo","histo.txt",self.message)

    def find_cmd_on_string(self, string_with_cmd):
        for cmd in self.availableCmd:
            if cmd in string_with_cmd:
                self.execute_cmd(cmd)
                return True
        return False

    def execute_cmd(self, cmd):
        if cmd == "!mega":
            self.read_all_file("./mega")
        
        elif cmd=="!histo":
            self.read_all_file("./histo")
        """
        elif cmd=="!wiki":
            self.read_all_file("./wiki")
      
        """

    def read_all_file(self, folder):

        data = {}
        for dir_entry in os.listdir(folder):
            dir_entry_path = os.path.join(folder, dir_entry)
            if os.path.isfile(dir_entry_path):
                with codecs.open(dir_entry_path, 'r', encoding='utf8') as my_file:
                    data[dir_entry] = my_file.read()
        self.paste_info(data);

    def paste_info(self, info):
        self.serv.privmsg(self.auteur, "Please wait I'm working for you :*")
        a = ZPaste(info)
        self.serv.privmsg(self.auteur, a.link)

    def write_file(self, folder, file, info):
        #with open(folder+'/'+file, 'r' as fin:
            #data = fi
        print(folder, file, info)

if __name__ == "__main__":
    Recalbot().start()
