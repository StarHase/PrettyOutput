# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:00:27 2015

@author: lars
"""


#import threading
import time
import sys
import termios
import os
import fcntl, termios, struct, string
import syntax

# TODO:
# Verschiedene Darstellungsmodi implementieren:
# palarm(STRheadline, STRcontent)
# psql(STRexception, STRsqlstatement)
# 
# Start und Stop sollte noch eingebaut werden... am besten in dem eine Prozess-
# Nummer zurückgegeben wird, anhand derer man Zeitunterschiede messen kann.


class PO():

    def __init__(self):
        self.__DICprocessestimes__  = {}
        self.__INTlastprocess__     = 0
        self.__INTprocesscounter__  = 0
        COLwh                       = self.__getTerminalSize__()
        self.__width__              = COLwh[0]
        self.__height__             = COLwh[1]
        self.__LSTfcolor__          = []
        self.__LSTfcolorend__       ='\033[0m'
        self.__LSTftype__           = []
        self.__LSTborder__          = ['','-','+','*','#']

        self.__LSTfcolor__.append('\033[97m')   # bright white
        self.__LSTfcolor__.append('\033[37m')   # grey
        self.__LSTfcolor__.append('\033[93m')   # bright yellow
        self.__LSTfcolor__.append('\033[33m')   # dark yellow (orange)
        self.__LSTfcolor__.append('\033[92m')   # bright green
        self.__LSTfcolor__.append('\033[32m')   # dark green
        self.__LSTfcolor__.append('\033[91m')   # bright red
        self.__LSTfcolor__.append('\033[31m')   # dark red
        self.__LSTfcolor__.append('\033[95m')   # bright pink
        self.__LSTfcolor__.append('\033[35m')   # dark pink
        self.__LSTfcolor__.append('\033[94m')   # bright blue
        self.__LSTfcolor__.append('\033[34m')   # dark blue
        self.__LSTfcolor__.append('\033[96m')   # bright bright blue
        self.__LSTfcolor__.append('\033[36m')   # dark bright blue

        self.__LSTftype__.append('\033[1m')
        self.__LSTftype__.append('\033[4m')



    def __print__(self, STRcontent, INTcolor=0, INTborder=0, STRsyntaxtype="none"):

        # border:
        # 0 = kein Rand
        # 1 = Rand mit - Linie
        # 2 = Rand mit + Linie
        # 3 = Rand mit * Linie
        # 4 = Rand mit # Linie

        # syntaxtype:
        # none = kein Syntaxhighlighting (Standard)
        # mysql = MySQL-Highlighting

        self.__INTprocesscounter__ += 1
        
        # STRoutc ist die Zeile, mit der die Prozessnummer und die Uhrzeit
        # ausgegeben werden: xxxx - hh:mm:ss: Ausgabeinhalt. Das c steht fuer count
        
        # STRoutb ist die Zeile ohne Prozessnummer und Zeit. Das b steht fuer blank
        
        STRoutc=""
        STRoutc += "%.5d" % self.__INTprocesscounter__
        STRoutc += " - "
        STRoutc += "%s" % time.strftime("%X")
        STRoutc += ": "

        STRoutb = " " * len(STRoutc)

        LSTout = self.__linewrap__(STRcontent, len(STRoutb), INTborder)

        for INTline in range(len(LSTout)):
            
            if INTborder > 0:
                # Header                
                if INTline == 0:
                    LSTout[INTline] = self.__parse__(LSTout[INTline], INTcolor, STRsyntaxtype)
                    STRtmp = "%s%s%s%s%s" % (self.__LSTfcolor__[0], STRoutc, self.__LSTfcolor__[INTcolor], LSTout[INTline],self.__LSTfcolorend__)
                    print STRtmp
                # Content
                elif INTline not in [1, len(LSTout)-2, len(LSTout)-1]:
                    STRtmp = "%s%s%s  %s  %s%s" % (self.__LSTfcolor__[INTcolor], STRoutb, self.__LSTborder__[INTborder], LSTout[INTline], self.__LSTborder__[INTborder], self.__LSTfcolorend__)
                    print self.__parse__(STRtmp, INTcolor, STRsyntaxtype)
                # Border
                else:
                    STRtmp = "%s%s%s%s" % (self.__LSTfcolor__[INTcolor],STRoutb, LSTout[INTline],self.__LSTfcolorend__)
                    print self.__parse__(STRtmp, INTcolor, STRsyntaxtype)
            else:
                if INTline == 0:
                    LSTout[INTline] = self.__parse__(LSTout[INTline], INTcolor, STRsyntaxtype)
                    STRtmp = "%s%s%s%s%s" % (self.__LSTfcolor__[0], STRoutc, self.__LSTfcolor__[INTcolor], LSTout[INTline],self.__LSTfcolorend__)
                    print STRtmp
                else:
                    STRtmp = "%s%s%s%s" % (self.__LSTfcolor__[INTcolor],STRoutb, LSTout[INTline],self.__LSTfcolorend__)
                    print self.__parse__(STRtmp, INTcolor, STRsyntaxtype)


    def __linewrap__(self, STRcontent, INTwidthreducer, INTborder):
        
        # __linewrap__ bricht Zeilen um
        # STRcontent:       Inhalt der ggf umgebrochen wird
        # INTwidthreducer:  Gibt an, wie breit der rechte, leere Rand ist
        # INTborder:        Rahmenart (0=ohne Rahmen)
        
        LSTreturn = []
        
        
        # INTborderborder = innerer Abstand bei Rahmen: 
        # <Rahmen><Leer><Leer><Content><Leer><Leer><Rahmen>
        # also 3 Zeichen vor- und 3 Zeichen nach Inhalt = 6 Zeichen
        INTborderborder = 6*len(self.__LSTborder__[INTborder])

        
        # Wenn Rahmen, dann sind die ersten beiden Ausgabezeilen nur Rahmen        
        if INTborder > 0:

            LSTreturn.append(self.__LSTborder__[INTborder] * (self.__width__ - INTwidthreducer))
            LSTreturn.append("%s%s%s" %(self.__LSTborder__[INTborder], " " * (self.__width__ - INTwidthreducer - 2),self.__LSTborder__[INTborder]))

        # Maximale Inhaltsbreite ermitteln        
        INTmax = self.__width__ - INTwidthreducer - INTborderborder

        # Wenn Maximale Inhaltsbreite weniger als ein Zeichen, dann raus hier
        if INTmax < 1:
            return LSTreturn

        # ist der Inhalt so lang, dass die Zeile umgebrochen werden muss?        
        if len(STRcontent) > INTmax:
            
            # STRcontent zerlegen            
            LSTsplit = string.split(STRcontent,' ')
        
            # Besteht STRcontent aus mehr als einem Wort?            
            if len(LSTsplit) > 1:
                
                STRtmp = ""  # temporaere Rueckgabezeile (TRZ)

                for INTi in range(len(LSTsplit)):

                    # Ist das aktuelle Wort laenger als INTmax                    
                    if len(LSTsplit[INTi]) > INTmax:

                        
                        # Enthaelt die TRZ schon Inhalt                        
                        if len(STRtmp)>0:
                            # Da das Wort sowieso schon laenger als eine Zeile ist, 
                            # haenge es an TRZ an und brich mitten im Wort um.
                            LSTreturn += self.__ssplit__("%s %s" % (STRtmp, LSTsplit[INTi]), INTmax)

                        # Nachdem mitten im Wort umgebrochen wurde (durchaus 
                        # auch mehrfach), ueberschreibe TRZ mit dem Wortrest des
                        # Ueberlangen Wortes, also mit dem Inhalt des letzten                        
                        if INTi < len(LSTsplit)-1:
                            STRtmp = LSTreturn.pop()
                            
                        else:
                            STRtmp=""
                            
                    # Das aktuelle Wort ist nicht laenger als INTmax
                    else:

                        if STRtmp == "":
                            STRtmp = LSTsplit[INTi]

                        else:

                            if len(STRtmp) + 1 + len(LSTsplit[INTi]) < INTmax:
                                STRtmp = "%s %s" % (STRtmp, LSTsplit[INTi])

                            else:
                                LSTreturn.append("%s%s" % (STRtmp, (INTmax-len(STRtmp))*' '))
                                STRtmp = LSTsplit[INTi]

                if STRtmp <> "":
                    LSTreturn.append("%s%s" % (STRtmp, (INTmax-len(STRtmp))*' '))

                if INTborder > 0:
                    LSTreturn.append("%s%s%s" %(self.__LSTborder__[INTborder], " " * (self.__width__ - INTwidthreducer - 2),self.__LSTborder__[INTborder]))
                    LSTreturn.append(self.__LSTborder__[INTborder] * (self.__width__ - INTwidthreducer))
                return LSTreturn

            # STRcontent besteht nur aus einem Wort            
            else:
                return self.__ssplit__(STRcontent, INTmax)

        else:

            if INTborder > 0:
                    LSTreturn.append("%s%s" % (STRcontent, (INTmax-len(STRcontent))*' '))
                    LSTreturn.append("%s%s%s" %(self.__LSTborder__[INTborder], " " * (self.__width__ - INTwidthreducer - 2),self.__LSTborder__[INTborder]))
                    LSTreturn.append(self.__LSTborder__[INTborder] * (self.__width__ - INTwidthreducer))

            else:
                LSTreturn.append(STRcontent)
            return LSTreturn


    def __ssplit__(self, STRcontent, INTmaxwidth):

        LSTreturn = []

        if len(STRcontent)<INTmaxwidth:
            LSTreturn.append("%s%s" % (STRcontent, (INTmaxwidth - len(STRcontent))*' '))
            return LSTreturn
        else:
            for INTi in range(len(STRcontent) / INTmaxwidth):
                LSTreturn.append(STRcontent[INTi*INTmaxwidth:(INTi+1)*INTmaxwidth])

            if len(STRcontent) % INTmaxwidth <> 0:
                LSTreturn.append(STRcontent[INTmax*INTmaxwidth:len(STRcontent)])

            return LSTreturn


    def __parse__(self, STRcontent, INTcolor=0, STRsyntaxtype="none"):

        LSTunderline = ['PRETTYOUTPUT']
        LSTmysql = syntax.MySQL
        LSTsplitsign = [' ', '\'', ',', '.', ';', ':', '(', ')', '[', ']', '{', '}', '<', '>', '=', '!', '+', '-', '*', '/']
        LSTsplitcontent = []
        
        
        # zunaechst wird der uebergebene String komplett zerlegt: alle Zeichen
        # der LSTsplitsign dienen als moegliche Trennzeichen. Die einzelnen
        # Stringteile werden inklusive der Trennzeichen in der Liste
        # LSTsplitcontent abgelegt
        # Bsp: Das ist toll! Oder?
        # ['Das', ' ', 'ist', ' ', 'toll', '!', ' ', 'Oder', '?']
        
        for STRsign in LSTsplitsign:
            LSTtmp = []
            LSTtmptmp = []
    
            if len(LSTsplitcontent)==0:    
                LSTtmp = string.split(STRcontent, STRsign)  
                for STRtmp in LSTtmp:
                    LSTsplitcontent.append(STRtmp)
                    LSTsplitcontent.append(' ')
                LSTsplitcontent = LSTsplitcontent[:-1]
            else:
                for STRtmpcontent in LSTsplitcontent:
                    
                    LSTtmp=string.split(STRtmpcontent, STRsign)
                    if len(LSTtmp)>1:
                        for STRtmp in LSTtmp:
                            LSTtmptmp.append(STRtmp)
                            LSTtmptmp.append(STRsign)
                        LSTtmptmp = LSTtmptmp[:-1]
                    else:
                        LSTtmptmp.append(STRtmpcontent)
                    
                LSTsplitcontent = LSTtmptmp
        
        # danach wird LSTsplitcontent durchlaufen und eingefaerbt
        INTcount = 0        
        for STRtmp in LSTsplitcontent:
            
            # UNDERLINE gilt immer... Werbung :-)
            if string.upper(STRtmp) in LSTunderline:
                LSTsplitcontent[INTcount]="%s%s%s%s" % ("\033[4m",STRtmp,"\033[0m",self.__LSTfcolor__[INTcolor])
            
            #MySQL
            elif string.upper(STRtmp) in LSTmysql and STRsyntaxtype == "mysql":
                LSTsplitcontent[INTcount]="%s%s%s%s" % ("\033[96m",STRtmp,"\033[0m",self.__LSTfcolor__[INTcolor])
                
            INTcount += 1
                
        STRcontent = string.join(LSTsplitcontent, '')

        return STRcontent



    def __getTerminalSize__(self):

        # This Code was copied from the Internet. The author is unknown

        env = os.environ
        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct, os
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
            '1234'))
            except:
                return
            return cr
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        return int(cr[1]), int(cr[0])

    def pprint(self, STRcontent, INTcolor=0, INTborder=0):
        self.__print__(STRcontent, INTcolor, INTborder, "none")
        
    def sqlprint(self, STRcontent, INTcolor=0, INTborder=0):
        self.__print__(STRcontent, INTcolor, INTborder, "mysql")

    def pinfo(self):
        STRinfo = "Das Fenster hat eine Hoehe von %s Zeilen " % self.__height__
        STRinfo += "und eine Breite von %s Spalten" % self.__width__
        self.pprint(STRinfo)

if __name__ == '__main__':
    P=PO()
    P.pprint("Use Sample.py to see how it works",4,2)
