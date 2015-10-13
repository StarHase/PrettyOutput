# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:01:45 2015

@author: lhoeger
"""

MySQL = ['ACTION', 'ADD', 'AFTER', 'AGAINST', 'AGGREGATE', 'ALGORITHM', 
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