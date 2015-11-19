#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import irclib
import ircbot
import settings
import os
import codecs
from zpaste import ZPaste
import time, threading

class Recalbot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(settings.SRV, settings.PORT, settings.PWD)], settings.NAME,
                                           settings.DESC)
        self.availableCmd = ["!mega", "!wiki", "!help","!histo","!op"]
        self.megaLink = ""
        self.wikiLink = ""

    def on_welcome(self, serv, ev):
        serv.join(settings.CHAN)


    def on_kick(self, serv, ev):
        serv.join(settings.CHAN)
        #serv.action(settings.CHAN, "se sent bien ici")

    def on_pubmsg(self, serv, ev):
        self.auteur = irclib.nm_to_n(ev.source())
        self.canal = ev.target()
        self.message = ev.arguments()[0].decode('utf-8', errors='replace')
        self.serv = serv
        self.find_cmd_on_string(self.message)
        info = '<'+time.strftime('%H:%M',time.localtime()) +"> "+self.auteur + ' : ' + self.message + '\n'
        self.write_file(settings.HISTOF,"histo.txt", info)
        
    def on_privmsg(self, serv, ev):
        self.auteur = irclib.nm_to_n(ev.source())
        self.canal = ev.target()
        self.message = ev.arguments()[0].decode('utf-8', errors='replace')
        self.serv = serv
        #self.serv.mode("#test-recalbot", "+o MikaXII")
        self.find_cmd_on_string(self.message)
        self.find_godmode_on_string(self.message)
        
    def find_cmd_on_string(self, string_with_cmd):
        for cmd in self.availableCmd:
            if cmd in string_with_cmd:
                self.execute_cmd(cmd)
                return True
        return False
    
    def on_join(self,serv,ev):
        self.auteur = irclib.nm_to_n(ev.source())
        self.canal = ev.target()
        self.serv = serv
        for user in settings.OP:
            if user == self.auteur:
                self.serv.mode("#recalbox", "+o "+self.auteur)

    def find_godmode_on_string(self, string_with_cmd):
        cmd = string_with_cmd.split(' ')
        if(len(cmd) > 1):
            if settings.GOD in cmd:
                self.serv.kick(settings.CHAN,cmd[1],self.auteur + " activate god mode")
                return True
        return False

    def execute_cmd(self, cmd):
        if cmd == "!mega":
            self.read_file("./links/mega.txt")
        elif cmd=="!histo":
            self.serv.privmsg(self.auteur, settings.HISTO)
        elif cmd=="!wiki":
            self.read_file("./links/wiki.txt")
        elif cmd == "!help":
            self.serv.privmsg(self.auteur, "If you want mega link say !mega, wiki pages say !wiki, channel history say !histo")
        elif cmd == "!op":
            for user in settings.OP:
                if user in self.auteur:
                    self.serv.mode("#recalbox", "+o "+self.auteur)

    def read_all_file(self, folder):

        data = {}
        for dir_entry in os.listdir(folder):
            dir_entry_path = os.path.join(folder, dir_entry)
            if os.path.isfile(dir_entry_path):
                with codecs.open(dir_entry_path, 'r', encoding='utf8') as my_file:
                    data[dir_entry] = my_file.read()
        self.paste_info(data);
    
    def read_file(self,fileToRead):
        data = ""
        with codecs.open(fileToRead, 'r', encoding='utf8') as my_file:
            data = my_file.read()
        self.serv.privmsg(self.auteur,data)

    def paste_info(self, info):
        self.serv.privmsg(self.auteur, "Please wait I'm working for you :*")
        a = ZPaste(info)
        self.serv.privmsg(self.auteur, a.link)
        del a
        
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

    def periodicPast(self):
        a = ZPaste

if __name__ == "__main__":
    Recalbot().start()
