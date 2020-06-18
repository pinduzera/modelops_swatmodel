# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:01:52 2020

@author: edhell
"""

###
import swat
import sys

conn = swat.CAS(#'pdcesx06128.exnet.sas.com', port=8777, protocol = 'http',
             'localhost', port = 5570, ## bug on swat 1.6.0
            caslib = 'public', username = 'sasdemo',
            password = 'Orion123')

session_id = list(conn.session.sessionId().values())[0]

conn.sessionProp.setSessOpt(
                           casLib="public", 
                           timeOut=3600)

tablenames = ['hmeq', 
                'hmeqpr_1_1q', 'hmeqpr_2_2q',
                'hmeqpr_3_3q', 'hmeqpr_4_4q']

tablenames[0]

tables = dict()

for i in tablenames:
    tables[i] =  conn.table.tableExists(caslib= 'public',
                        name= i)['exists']

for key in tables: 
    if(tables[key] == 2):   
        tables[key] = True
    else:
        tables[key] = False
tables

if (all(value == True for value in tables.values())):

  with open("session_id.txt", "w") as f:
      f.write(session_id)
      f.close()
  
  conn.close()
  
  print('All tables exists in session with id:' + session_id)
  print(tables)

## what to do if fails
else:

  with open("session_id.txt", "w") as f:
      f.write(session_id)
      f.close()
 
  conn.close()
  print(tables)
  print('Not all tables exists in session with id:' + session_id)
  sys.exit(1)
