#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import irclib
import ircbot
import settings
import os
import codecs
from zpaste import ZPaste
import time

class Recalbot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(settings.SRV, settings.PORT, settings.PWD)], settings.NAME,
                                           settings.DESC)
        self.availableCmd = ["!mega", "!wiki", "!help","!histo"]

    def on_welcome(self, serv, ev):
        serv.join(settings.CHAN)


    def on_kick(self, serv, ev):
        serv.join(settings.CHAN)

    def on_pubmsg(self, serv, ev):
        self.auteur = irclib.nm_to_n(ev.source())
        self.canal = ev.target()
        self.message = ev.arguments()[0].decode('utf-8', errors='replace')
        self.serv = serv
        if self.find_cmd_on_string(self.message) == False:
            info = '<'+time.strftime('%H:%M',time.localtime()) +"> "+self.auteur + ' : ' + self.message + '\n'
            self.write_file("/usr/share/webapps/histo","histo.txt", info)

    def on_privmsg(self, serv, ev):
        self.auteur = irclib.nm_to_n(ev.source())
        self.canal = ev.target()
        self.message = ev.arguments()[0].decode('utf-8', errors='replace')
        self.serv = serv
        #self.serv.mode("#test-recalbot", "+o MikaXII")
        self.find_cmd_on_string(self.message)
        self.find_godmode_on_string(self.message)
        """
        if self.find_cmd_on_string(self.message) == False:
            info = self.auteur + ' ' + self.message + '\n'
            self.write_file("./histo","histo.txt", info)
        """

    def find_cmd_on_string(self, string_with_cmd):
        for cmd in self.availableCmd:
            if cmd in string_with_cmd:
                self.execute_cmd(cmd)
                return True
        return False

    def find_godmode_on_string(self, string_with_cmd):
        cmd = string_with_cmd.split(' ')
        if(len(cmd) > 1):
            if settings.GOD in cmd:
                self.serv.kick(settings.CHAN,cmd[1],self.auteur + " activate god mode")
                return True
        return False

    def execute_cmd(self, cmd):
        if cmd == "!mega":
            self.read_all_file("./mega")
        elif cmd=="!histo":
            self.serv.privmsg(self.auteur, settings.HISTO)
        elif cmd=="!wiki":
            self.read_all_file("./wiki")
        elif cmd == "!help":
            self.serv.privmsg(self.auteur, "If you want mega link say !mega, wiki pages say !wiki, channel history say !histo")



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
        with codecs.open(folder+'/'+file, 'r','utf-8',errors="replace") as fin:
            data = fin.read().splitlines(True)
        if len(data) >= 5000:
            with codecs.open(folder+'/'+file, 'w', 'utf-8',errors="replace") as fout:
                fout.writelines(data[1:])
                fout.writelines(info)
        else:
            with codecs.open(folder+'/'+file, 'w', 'utf-8',errors="replace") as fout:
                fout.writelines(data)
                fout.writelines(info)

if __name__ == "__main__":
    Recalbot().start()
