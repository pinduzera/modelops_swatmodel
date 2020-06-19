# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:22:46 2020

@author: edhell
"""

from sasctl import Session
from sasctl import register_model, publish_model
from sasctl.services import model_repository
from pathlib import Path
import swat

###################################
####### Variables #################

host = 'localhost'
#host = 'pdcesx12091.exnet.sas.com'

publishdestination = 'maslocal'

modelname = 'gb_jk_swat'

project = 'hmeq_os'

user = 'sasdemo'

password = 'Orion123'

astore_table = 'gb_astore'
#astore_caslib = 'public'

###################################
####### Getting astore table ######

with open("session_id.txt", "r") as f:
    session_id = f.read()
    f.close()

conn = swat.CAS(#'pdcesx12091.exnet.sas.com', port=8777, protocol = 'http',
            host, port = 5570, ## bug on swat 1.6.0
            #caslib = 'public',
            username = 'sasdemo',
            password = 'Orion123')#, session = session_id)


astore = conn.CASTable(astore_table)

#### coneccting from SASCTL
s = Session(host, user, password,
            verify_ssl = False) 


model_exists = model_repository.get_model(modelname, refresh=False)

#model_repository.delete_model(modelname)
if model_exists == None:
    print('Creating new model')
    model = register_model(astore, 
                           modelname, 
                           project,
                           force = True,
                           version = 'latest')
    
else:
    print('Model exists, creting new version')
    model_repository.delete_model(modelname)
    register_model(model = astore, 
                   name= modelname, 
                   project= project,
                   force=True,
                   version = 'latest')

path = Path.cwd()

############################## 
######## adding files ########

#3THIS SESSION IS BUGGED, CANNOT REPLACE FILE

filenames = {'file':['training_code.py'],
            'role':['train']}
            
#### uploading files
model_repository.get_model_contents(modelname)
for i in range(len(filenames['file'])):

    with open(path / filenames['file'][i], "rb") as _file:

        model_repository.add_model_content(
                      model = modelname, 
                      file = _file, 
                      name = filenames['file'][i], 
                      role= filenames['role'][i],
                         )
        
        print('uploaded ' + filenames['file'][i] + ' as ' + filenames['role'][i])
        _file.close()

#### Publish model
publish_model(modelname, publishdestination,
                  replace = True)

conn.close()
#### 