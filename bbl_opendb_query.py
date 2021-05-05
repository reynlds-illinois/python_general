import cx_Oracle, os, sys, urllib3, time, csv
from datetime import datetime
sys.path.append('/path/to/external/functions/bin')
from icFunctions import *

# configure outFile for query results
dateFormat = '%Y-%m-%d_%H:%M:%S'
now = datetime.now()
tempNow = now.strftime(dateFormat)
outFile = '/my/directory/tmp/opendb_results_' + tempNow + '.csv'

# connect to OpenDb
def connect2Sql(dbUser, dbPass, dbHost, dbPort, dbSid):
    import cx_Oracle, sys
    oraConn = cx_Oracle.connect('%s/%s@%s:%s/%s' % (dbUser, dbPass, dbHost, dbPort, dbSid))
    cursor = oraConn.cursor()
    return cursor

# prompt for SQL input
def sqlInput():
    '''prompt for multi-line input to query an Oracle DB'''
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z (Windows) to save it:")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    print('Starting query...')
    strJoin = " ".join(contents)
    return str(strJoin)

# parse environment file for variables
envDict = getEnv()

# connect to OpenDb cursor
try:
    #cursor = connect2Sql(dbUser, dbPass, dbHost, dbPort, dbSid)
    cursor = connect2Sql(envDict['ic2gprod.db.opendb.user'],
                         envDict['ic2gprod.db.opendb.pass'],
                         envDict['ic2gprod.db.opendb.sys'],
                         envDict['ic2gprod.db.opendb.port'],
                         envDict['ic2gprod.db.opendb.sid'])
    print('Connected to Bb OpenDB')
except:
    print('NOT connected to Bb OpenDB')

# prompt for SQL input
tmpSql = sqlInput()

# execute SQL query
print('SQL Query starting')
cursor.execute(tmpSql)

# retrieve column headers
headers = [i[0] for i in cursor.description]

# retrieve all results
print('SQL Query complete - fetching rows')
r = cursor.fetchall()

# count results
records = len(r)

print('#####')
print('##### Query has found ', records, ' results.')
print('##### Press a <ENTER> to export to file or <CTRL-C> to exit.')
input('#####')

# output results to CSV while reporting to screen
try:
    csvFile = csv.writer(open(outFile, 'w', newline=''),
                         delimiter='|', lineterminator='\r\n',
                         quoting=csv.QUOTE_ALL, escapechar='\\')
    csvFile.writerow(headers)
    csvFile.writerows(r)
    print('##### Results saved to this file:')
    print('#####', outFile)
    print('#####')
except:
    print('>>>>> Something went wrong...try it again.')

cursor.close()
