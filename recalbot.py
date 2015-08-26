#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot
import settings
from zpaste import ZPaste


class Recalbot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(settings.SRV, settings.PORT, settings.PWD)],settings.NAME, settings.DESC)

    def on_welcome(self, serv, ev):
	serv.join("#test-recalbot")

    def on_pubmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0].lower() 
        a = ZPaste(message)
	serv.privmsg("#test-recalbot", a.link)
		        

if __name__ == "__main__":
    Recalbot().start()

