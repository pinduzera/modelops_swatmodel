# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:08:00 2020

@author: edhell
"""
###
import swat
#####

with open("session_id.txt", "r") as f:
    session_id = f.read()
    f.close()

conn = swat.CAS(#'hostname.com', port=8777, protocol = 'http',
            'localhost', port = 5570, ## bug on swat 1.6.0
            #caslib = 'public', 
            username = 'username',
            password = 's3cr3t!')#, session = session_id)

conn.loadactionset("sampling")
conn.loadactionset("decisionTree")
conn.loadactionset("autotune")

# Tables in memory
# conn.tableinfo(caslib="public")

### sampling 

conn.sampling.stratified(
    table={"name":"HMEQ", "groupBy":"BAD", "caslib": "public"},
    output={"casOut":{"name":"hmeq_part", 
                      #"caslib":"public",
                      "replace": True}, 
            "copyVars":"ALL"},
    samppct=70,
    partind=True
)


# Value imputation
db_var_imp = conn.datapreprocess.impute(
                          table={"name": "hmeq_part"},
                                 #"caslib": "public"},
                          methodnominal = "mode",  
                          methodinterval ="median",
                          casout={"name":"hmeq_treated",
                                  "replace":1},
                           outvarsnameprefix='')

# Promoting table
db_treated = conn.CASTable("hmeq_treated")
#conn.table.promote(db_treated)

# Separacao de Colunas
columns_info = conn.columninfo(table=db_treated).ColumnInfo

target = "BAD"
columns_char = list(columns_info["Column"][columns_info["Type"]=="varchar"])
columns_double = list( columns_info["Column"][ columns_info["Type"]=="double" ])
columns_double.remove("BAD")
columns_double.remove("_PartInd_")

print("Varchar columns:")
print(columns_char)

print("Double columns:")
print(columns_double)

droptables = ['gb_score', 'gb_astore']

for tb in droptables:
    exists = conn.table.tableExists(tb)
    
    if exists['exists'] == 2:
        print("Dropping:" + tb)
        conn.table.dropTable(tb)

exists = conn.table.tableExists('gb_astore')

if exists['exists'] == 2:
    conn.table.dropTable('gb_score')
# Treinamento e Scoragem - Gradient Boosting
result = conn.autotune.tuneGradientBoostTree(
    trainOptions = {
        "table"   : {"name":"hmeq_part", 
                     #"caslib":"public",
                     "where": "_PartInd_=0"},
        "inputs"  : columns_double+columns_char,
        "target"  : target,
        "nominal" : columns_char+[target],
        "casout"  : {"name":"gb_train"},
        "saveState": {"name": "gb_astore"}  ### THIS IS THE ASTORE
                                            ### USED FOR PUBLICATION
                                            ### OR exported for ESP
    },
    tunerOptions={
         "maxIters": 5,
         "maxTime": 60,
         "searchMethod": "GA",
         "objective": "KS",
         "userDefinedPartition": True,
         "targetEvent" : "1"
    },
    scoreOptions= {
        "table" : {"name":"hmeq_part"}, 
                   #"caslib": "public",
                   #"where": "_PartInd_=1"},
        "modeltable": {"name":"gb_train"},
        "casout":{"name":"gb_score", 
                  "replace":1}, 
        "copyvars":["BAD", "_PartInd_"]
   }
)

conn.table.promote('gb_score')

conn.table.promote('gb_astore')

#gb_score = conn.CASTable("gb_score")
#gb_score.head()


######

conn.close()

