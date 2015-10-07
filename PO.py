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

# TODO:
# Verschiedene Darstellungsmodi implementieren:
# palarm(STRheadline, STRcontent)
# psql(STRexception, STRsqlstatement)
# 
# Start und Stop sollte noch eingebaut werden... am besten in dem eine Prozess-
# Nummer zurückgegeben wird, anhand derer man Zeitunterschiede messen kann.


class pp():

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



    def __print__(self, STRcontent, INTcolor=0, INTborder=0):

        # border:
        # 0 = kein Rand
        # 1 = Rand mit - Linie
        # 2 = Rand mit + Linie
        # 3 = Rand mit * Linie
        # 4 = Rand mit # Linie

        self.__INTprocesscounter__ += 1
        
        # STRoutc ist die Zeile, mit der die Prozessnummer und die Uhrzeit
        # ausgegeben werden: xxxx - hh:mm:ss: Ausgabeinhalt
        
        # STRoutb ist die Zeile ohne Prozessnummer und Zeit
        
        STRoutc=""
        STRoutc += "%.5d" % self.__INTprocesscounter__
        STRoutc += " - "
        STRoutc += "%s" % time.strftime("%X")
        STRoutc += ": "

        STRoutb = " " * len(STRoutc)

        LSTout = self.__linewrap__(STRcontent, len(STRoutb), INTborder)

        for INTline in range(len(LSTout)):

            if INTline == 0:
                LSTout[INTline] = self.__parse__(LSTout[INTline], INTcolor)
                STRtmp = "%s%s%s%s%s" % (self.__LSTfcolor__[0], STRoutc, self.__LSTfcolor__[INTcolor], LSTout[INTline],self.__LSTfcolorend__)
                print STRtmp
            else:
                STRtmp = "%s%s%s%s" % (self.__LSTfcolor__[INTcolor],STRoutb, LSTout[INTline],self.__LSTfcolorend__)
                print self.__parse__(STRtmp,INTcolor)


    def __linewrap__(self, STRcontent, INTwidthreducer, INTborder):
        
        # __linewrap__ bricht Zeilen um
        # STRcontent:       Inhalt der ggf umgebrochen wird
        # INTwidthreducer:  Gibt an, wie breit der rechte, leere Rand ist
        # INTborder:        Rahmenart (0=ohne Rahmen)
        LSTreturn = []
        
        INTborderborder = 6*len(self.__LSTborder__[INTborder])

        if INTborder > 0:

            LSTreturn.append(self.__LSTborder__[INTborder] * (self.__width__ - INTwidthreducer))
            LSTreturn.append("%s%s%s" %(self.__LSTborder__[INTborder], " " * (self.__width__ - INTwidthreducer - 2),self.__LSTborder__[INTborder]))

        INTmax = self.__width__ - INTwidthreducer - INTborderborder

        if INTmax < 0:
            return LSTreturn

        if len(STRcontent) > INTmax:
            LSTsplit = string.split(STRcontent,' ')
            INTsplit = len(LSTsplit)

            if INTsplit > 1:
                INTsum = 0
                STRtmp = ""

                for INTi in range(INTsplit):

                    if len(LSTsplit[INTi]) > INTmax:

                        if len(STRtmp)>0:
                            LSTreturn += self.__ssplit__("%s %s" % (STRtmp, LSTsplit[INTi]), INTmax)

                        if INTi < len(LSTsplit)-1:
                            STRtmp = LSTreturn[len(LSTreturn)-1]
                            STRnotused=LSTreturn.pop()

                        else:
                            STRtmp=""

                    else:

                        if STRtmp == "":
                            STRtmp = LSTsplit[INTi]

                        else:

                            if len(STRtmp) + 1 + len(LSTsplit[INTi]) < INTmax:
                                STRtmp = "%s %s" % (STRtmp, LSTsplit[INTi])

                            else:
                                LSTreturn.append(STRtmp)
                                STRtmp = LSTsplit[INTi]

                if STRtmp <> "":
                    LSTreturn.append(STRtmp)

                if INTborder > 0:
                    LSTreturn.append("%s%s%s" %(self.__LSTborder__[INTborder], " " * (self.__width__ - INTwidthreducer - 2),self.__LSTborder__[INTborder]))
                    LSTreturn.append(self.__LSTborder__[INTborder] * (self.__width__ - INTwidthreducer))
                return LSTreturn

            else:
                return self.__ssplit__(STRcontent, INTmax)

        else:

            if INTborder > 0:
                    LSTreturn.append("%s  %s%s  %s" % (self.__LSTborder__[INTborder], STRcontent, " " * (INTmax-len(STRcontent)), self.__LSTborder__[INTborder]))
                    LSTreturn.append("%s%s%s" %(self.__LSTborder__[INTborder], " " * (self.__width__ - INTwidthreducer - 2),self.__LSTborder__[INTborder]))
                    LSTreturn.append(self.__LSTborder__[INTborder] * (self.__width__ - INTwidthreducer))

            else:
                LSTreturn.append(STRcontent)
            return LSTreturn


    def __ssplit__(self, STRcontent, INTmaxwidth):

        LSTreturn = []

        if len(STRcontent)<INTmaxwidth:
            LSTreturn.append(STRcontent)
            return LSTreturn
        else:
            INTmax = len(STRcontent) / INTmaxwidth
            for INTi in range(INTmax):
                LSTreturn.append(STRcontent[INTi*INTmaxwidth:(INTi+1)*INTmaxwidth])

            if len(STRcontent) % INTmaxwidth <> 0:
                LSTreturn.append(STRcontent[INTmax*INTmaxwidth:len(STRcontent)])

            return LSTreturn


    def __parse__(self, STRcontent, INTcolor=0):

        LSTunderline = ['PPRINT']
        LSTmysql = ['ACTION', 'ADD', 'AFTER', 'AGAINST', 'AGGREGATE', 'ALGORITHM', 
                    'ALL', 'ALTER', 'ANALYZE', 'AND', 'ANY', 'AS', 'ASC', 'ASCII', 
                    'ASENSITIVE', 'AUTO_INCREMENT', 'AVG', 'AVG_ROW_LENGTH', 
                    'BACKUP', 'BDB', 'BEFORE', 'BEGIN', 'BERKELEYDB', 'BETWEEN', 
                    'BIGINT', 'BINARY', 'BINLOG', 'BIT', 'BLOB', 'BLOCK', 'BOOL', 
                    'BOOLEAN', 'BOTH', 'BTREE', 'BY', 'BYTE', 'CACHE', 'CALL', 
                    'CASCADE', 'CASCADED', 'CASE', 'CHAIN', 'CHANGE', 'CHANGED', 
                    'CHAR', 'CHARACTER', 'CHARSET', 'CHECK', 'CHECKSUM', 'CIPHER', 
                    'CLIENT', 'CLOSE', 'CODE', 'COLLATE', 'COLLATION', 'COLUMN', 
                    'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 
                    'COMPRESSED', 'CONCURRENT', 'CONDITION', 'CONNECTION', 
                    'CONSISTENT', 'CONSTRAINT', 'CONTAINS', 'CONTEXT', 'CONTINUE', 
                    'CONVERT', 'CPU', 'CREATE', 'CROSS', 'CUBE', 'CURRENT_DATE', 
                    'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'CURSOR', 
                    'DATA', 'DATABASE', 'DATABASES', 'DATE', 'DATETIME', 'DAY', 
                    'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 
                    'DEALLOCATE', 'DEC', 'DECIMAL', 'DECLARE', 'DEFAULT', 'DEFINER', 
                    'DELAYED', 'DELAY_KEY_WRITE', 'DELETE', 'DESC', 'DESCRIBE', 
                    'DES_KEY_FILE', 'DETERMINISTIC', 'DIRECTORY', 'DISABLE', 
                    'DISCARD', 'DISTINCT', 'DISTINCTROW', 'DIV', 'DO', 'DOUBLE', 
                    'DROP', 'DUAL', 'DUMPFILE', 'DUPLICATE', 'DYNAMIC', 'EACH', 
                    'ELSE', 'ELSEIF', 'ENABLE', 'ENCLOSED', 'END', 'ENGINE', 
                    'ENGINES', 'ENUM', 'ERRORS', 'ESCAPE', 'ESCAPED', 'EVENTS', 
                    'EXECUTE', 'EXISTS', 'EXIT', 'EXPANSION', 'EXPLAIN', 
                    'EXTENDED', 'FALSE', 'FAST', 'FAULTS', 'FETCH', 'FIELDS', 
                    'FILE', 'FIRST', 'FIXED', 'FLOAT', 'FLOAT4', 'FLOAT8', 'FLUSH', 
                    'FOR', 'FORCE', 'FOREIGN', 'FOUND', 'FRAC_SECOND', 'FROM', 
                    'FULL', 'FULLTEXT', 'FUNCTION', 'GEOMETRY', 'GEOMETRYCOLLECTION', 
                    'GET_FORMAT', 'GLOBAL', 'GRANT', 'GRANTS', 'GROUP', 'HANDLER', 
                    'HASH', 'HAVING', 'HELP', 'HIGH_PRIORITY', 'HOSTS', 'HOUR', 
                    'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'IDENTIFIED', 
                    'IF', 'IGNORE', 'IMPORT', 'IN', 'INDEX', 'INDEXES', 'INFILE', 
                    'INNER', 'INNOBASE', 'INNODB', 'INOUT', 'INSENSITIVE', 'INSERT', 
                    'INSERT_METHOD', 'INT', 'INT1', 'INT2', 'INT3', 'INT4', 'INT8', 
                    'INTEGER', 'INTERVAL', 'INTO', 'INVOKER', 'IO', 'IO_THREAD', 
                    'IPC', 'IS', 'ISOLATION', 'ISSUER', 'ITERATE', 'JOIN', 'KEY', 
                    'KEYS', 'KILL', 'LANGUAGE', 'LAST', 'LEADING', 'LEAVE', 'LEAVES', 
                    'LEFT', 'LEVEL', 'LIKE', 'LIMIT', 'LINES', 'LINESTRING', 'LOAD', 
                    'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCK', 'LOCKS', 'LOGS', 
                    'LONG', 'LONGBLOB', 'LONGTEXT', 'LOOP', 'LOW_PRIORITY', 'MASTER', 
                    'MASTER_CONNECT_RETRY', 'MASTER_HOST', 'MASTER_LOG_FILE', 
                    'MASTER_LOG_POS', 'MASTER_PASSWORD', 'MASTER_PORT', 
                    'MASTER_SERVER_ID', 'MASTER_SSL', 'MASTER_SSL_CA', 
                    'MASTER_SSL_CAPATH', 'MASTER_SSL_CERT', 'MASTER_SSL_CIPHER', 
                    'MASTER_SSL_KEY', 'MASTER_USER', 'MATCH', 
                    'MAX_CONNECTIONS_PER_HOUR', 'MAX_QUERIES_PER_HOUR', 'MAX_ROWS', 
                    'MAX_UPDATES_PER_HOUR', 'MAX_USER_CONNECTIONS', 'MEDIUM', 
                    'MEDIUMBLOB', 'MEDIUMINT', 'MEDIUMTEXT', 'MEMORY', 'MERGE', 
                    'MICROSECOND', 'MIDDLEINT', 'MIGRATE', 'MINUTE', 
                    'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MIN_ROWS', 'MOD', 'MODE', 
                    'MODIFIES', 'MODIFY', 'MONTH', 'MULTILINESTRING', 'MULTIPOINT', 
                    'MULTIPOLYGON', 'MUTEX', 'NAME', 'NAMES', 'NATIONAL', 'NATURAL', 
                    'NCHAR', 'NDB', 'NDBCLUSTER', 'NEW', 'NEXT', 'NO', 'NONE', 
                    'NOT', 'NO_WRITE_TO_BINLOG', 'NULL', 'NUMERIC', 'NVARCHAR', 
                    'OFFSET', 'OLD_PASSWORD', 'ON', 'ONE', 'ONE_SHOT', 'OPEN', 
                    'OPTIMIZE', 'OPTION', 'OPTIONALLY', 'OR', 'ORDER', 'OUT', 
                    'OUTER', 'OUTFILE', 'PACK_KEYS', 'PAGE', 'PARTIAL', 'PASSWORD', 
                    'PHASE', 'POINT', 'POLYGON', 'PRECISION', 'PREPARE', 'PREV', 
                    'PRIMARY', 'PRIVILEGES', 'PROCEDURE', 'PROCESSLIST', 'PROFILE', 
                    'PROFILES', 'PURGE', 'QUARTER', 'QUERY', 'QUICK', 'RAID0', 
                    'RAID_CHUNKS', 'RAID_CHUNKSIZE', 'RAID_TYPE', 'READ', 'READS', 
                    'REAL', 'RECOVER', 'REDUNDANT', 'REFERENCES', 'REGEXP', 
                    'RELAY_LOG_FILE', 'RELAY_LOG_POS', 'RELAY_THREAD', 'RELEASE', 
                    'RELOAD', 'RENAME', 'REPAIR', 'REPEAT', 'REPEATABLE', 'REPLACE', 
                    'REPLICATION', 'REQUIRE', 'RESET', 'RESTORE', 'RESTRICT', 
                    'RESUME', 'RETURN', 'RETURNS', 'REVOKE', 'RIGHT', 'RLIKE', 
                    'ROLLBACK', 'ROLLUP', 'ROUTINE', 'ROW', 'ROWS', 'ROW_FORMAT', 
                    'RTREE', 'SAVEPOINT', 'SCHEMA', 'SCHEMAS', 'SECOND', 
                    'SECOND_MICROSECOND', 'SECURITY', 'SELECT', 'SENSITIVE', 
                    'SEPARATOR', 'SERIAL', 'SERIALIZABLE', 'SESSION', 'SET', 
                    'SHARE', 'SHOW', 'SHUTDOWN', 'SIGNED', 'SIMPLE', 'SLAVE', 
                    'SMALLINT', 'SNAPSHOT', 'SOME', 'SONAME', 'SOUNDS', 'SOURCE', 
                    'SPATIAL', 'SPECIFIC', 'SQL', 'SQLEXCEPTION', 'SQLSTATE', 
                    'SQLWARNING', 'SQL_BIG_RESULT', 'SQL_BUFFER_RESULT', 'SQL_CACHE', 
                    'SQL_CALC_FOUND_ROWS', 'SQL_NO_CACHE', 'SQL_SMALL_RESULT', 
                    'SQL_THREAD', 'SQL_TSI_DAY', 'SQL_TSI_FRAC_SECOND', 
                    'SQL_TSI_HOUR', 'SQL_TSI_MINUTE', 'SQL_TSI_MONTH', 
                    'SQL_TSI_QUARTER', 'SQL_TSI_SECOND', 'SQL_TSI_WEEK', 
                    'SQL_TSI_YEAR', 'SSL', 'START', 'STARTING', 'STATUS', 'STOP', 
                    'STORAGE', 'STRAIGHT_JOIN', 'STRING', 'STRIPED', 'SUBJECT', 
                    'SUPER', 'SUSPEND', 'SWAPS', 'SWITCHES', 'TABLE', 'TABLES', 
                    'TABLESPACE', 'TEMPORARY', 'TEMPTABLE', 'TERMINATED', 'TEXT', 
                    'THEN', 'TIME', 'TIMESTAMP', 'TIMESTAMPADD', 'TIMESTAMPDIFF', 
                    'TINYBLOB', 'TINYINT', 'TINYTEXT', 'TO', 'TRAILING', 
                    'TRANSACTION', 'TRIGGER', 'TRIGGERS', 'TRUE', 'TRUNCATE', 
                    'TYPE', 'TYPES', 'UNCOMMITTED', 'UNDEFINED', 'UNDO', 'UNICODE', 
                    'UNION', 'UNIQUE', 'UNKNOWN', 'UNLOCK', 'UNSIGNED', 'UNTIL', 
                    'UPDATE', 'UPGRADE', 'USAGE', 'USE', 'USER', 'USER_RESOURCES', 
                    'USE_FRM', 'USING', 'UTC_DATE', 'UTC_TIME', 'UTC_TIMESTAMP', 
                    'VALUE', 'VALUES', 'VARBINARY', 'VARCHAR', 'VARCHARACTER', 
                    'VARIABLES', 'VARYING', 'VIEW', 'WARNINGS', 'WEEK', 'WHEN', 
                    'WHERE', 'WHILE', 'WITH', 'WORK', 'WRITE', 'X509', 'XA', 'XOR']
        
        LSTsplitsign = [' ', '\'', ',', '.', ';', ':', '(', ')', '[', ']', '{', '}', '<', '>', '=', '!']
        LSTsplitcontent = []
        
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
        
        INTcount = 0        
        for STRtmp in LSTsplitcontent:
            # UNDERLINE            
            if string.upper(STRtmp) in LSTunderline:
                LSTsplitcontent[INTcount]="%s%s%s%s" % ("\033[4m",STRtmp,"\033[0m",self.__LSTfcolor__[INTcolor])
            
            #MySQL
            elif string.upper(STRtmp) in LSTmysql:
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
        self.__print__(STRcontent, INTcolor, INTborder)

    def pinfo(self):
        STRinfo = "Das Fenster hat eine Hoehe von %s Zeilen " % self.__height__
        STRinfo += "und eine Breite von %s Spalten" % self.__width__
        self.pprint(STRinfo)

if __name__ == '__main__':
    P=pp()
    P.pprint("Dies ist ein 'Test', der zeigen soll, wie bei PPrint das=das sein kann:soll")
    P.pprint("SELECT PDID, PAID FROM 0000_00_main where PAID=1 ORdeR BY PDID")
    P.pprint("Willkommen in der PPRINT-DEMO!",10,3)
    STRtext = ""
    STRtext += "PPRINT soll die Bildschirmausgabe von Console-Programmen verbessern. "
    STRtext += "Das bedeutet, dass Sie nur noch Ihre Ausgabe an PPRINT uebergeben muessen, "
    STRtext += "den Rest erledigt PPrint. Ihre Ausgabe wird an die Console angepasst, "
    STRtext += "auf der PPrint Ihre Meldungen ausgibt. Dabei bricht PPrint automatisch um, "
    STRtext += "sobald das Zeilenende erreicht ist."
    P.pprint(STRtext)
    STRtext = ""
    STRtext += "Der folgende Text ist ein langer Text, der sowohl sehr lange Zeichenketten, "
    STRtext += "als auch ganz normale Woerter enthaelt. Durch diesen Text soll "
    STRtext += "geziegt werden, dass der Umbruch sauber funktioniert."
    P.pprint(STRtext)
    STRtext = ""
    STRtext += "Auto Haus AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ist BBBBBBBBBBBBBBBBBBBBBBBBBBB "
    STRtext += "kann Dach soll gerne CCCCCCCCCCCCCCCCCCCCCCCCCCC mit DDDDDDDDDDDDDDDDDDDDDDDDD "
    STRtext += "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE "
    STRtext += "eins zwei drei FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF vier "
    STRtext += "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
    P.pprint(STRtext)
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
    P.pprint("Dies ist ein Text mit Border 1", 2, 1)
    P.pprint("Dies ist ein Text mit Border 2", 2, 2)
    P.pprint("Dies ist ein Text mit Border 3", 2, 3)
    P.pprint("Dies ist ein Text mit Border 4", 2, 4)
