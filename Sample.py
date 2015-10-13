# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:42:18 2015

@author: lhoeger
"""

import PO

P=PO.PO()
P.pprint("Willkommen in der PrettyOutput-DEMO!",10,3)

STRtext = ""
STRtext += "PrettyOutput soll die Bildschirmausgabe von Console-Programmen verbessern. "
STRtext += "Der Text wird automatisch umgebrochen und eingerueckt, so dass die Ausgabe "
STRtext += "immer gut lesbar sein sollte. "
P.pprint(STRtext,0,0)

STRtext = ""
STRtext += "Natuerlich kann auch Text innerhalb von Rahmen umgebrochen werden. "
STRtext += "Welche Rahmenarten es gibt, wird weiter unten aufgefuehrt."
P.pprint(STRtext,0,2)

P.pprint("Bunte Texte sind kein Problem:",1,0)
P.pprint("Dieser Text ist weiss............:  [0] -> pprint(\"Dieser Text ist [...]\",0)", 0)
P.pprint("Dieser Text ist hellgrau.........:  [1] -> pprint(\"Dieser Text ist [...]\",1)", 1)
P.pprint("Dieser Text ist gelb.............:  [2] -> pprint(\"Dieser Text ist [...]\",2)", 2)
P.pprint("Dieser Text ist orange...........:  [3] -> pprint(\"Dieser Text ist [...]\",3)", 3)
P.pprint("Dieser Text ist hellgruen........:  [4] -> pprint(\"Dieser Text ist [...]\",4)", 4)
P.pprint("Dieser Text ist dunkelgruen......:  [5] -> pprint(\"Dieser Text ist [...]\",5)", 5)
P.pprint("Dieser Text ist hellrot..........:  [6] -> pprint(\"Dieser Text ist [...]\",6)", 6)
P.pprint("Dieser Text ist dunkelrot........:  [7] -> pprint(\"Dieser Text ist [...]\",7)", 7)
P.pprint("Dieser Text ist rosa.............:  [8] -> pprint(\"Dieser Text ist [...]\",8)", 8)
P.pprint("Dieser Text ist lila.............:  [9] -> pprint(\"Dieser Text ist [...]\",9)", 9)
P.pprint("Dieser Text ist hellblau.........: [10] -> pprint(\"Dieser Text ist [...]\",10)", 10)
P.pprint("Dieser Text ist dunkelblau.......: [11] -> pprint(\"Dieser Text ist [...]\",11)", 11)
P.pprint("Dieser Text ist hell hellblau....: [12] -> pprint(\"Dieser Text ist [...]\",12)", 12)
P.pprint("Dieser Text ist dunkel hellblau..: [13] -> pprint(\"Dieser Text ist [...]\",13)", 13)

P.pprint("Rahmen sind kein Problem:",1,0)
P.pprint("Dies ist ein Text mit Border 1", 0, 1)
P.pprint("Dies ist ein Text mit Border 2", 0, 2)
P.pprint("Dies ist ein Text mit Border 3", 0, 3)
P.pprint("Dies ist ein Text mit Border 4", 0, 4)
