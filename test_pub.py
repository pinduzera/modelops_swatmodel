# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:27:02 2020

@author: edhell
"""

from sasctl import Session
from sasctl.services import microanalytic_score as mas

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

s = Session(host, user, password,
            verify_ssl = False) 

module = mas.get_module(modelname)


module = mas.define_steps(module)
steps = mas.list_module_steps(module)

steps[0]['id']

steps[0]['links']

print(help(module.score))

res = module.score(clage=94.3, clno=9.0, debtinc=34.8, delinq=0,
             derog=0, loan=1100, mortdue=25860, ninq=1, 
             value=39025, yoj=10.5, 
             job="Other", reason="HomeImp")


"""
DATA SAMPLE
{'_PartInd_': {0: 0.0},
 'BAD': {0: 1.0},
 'CLAGE': {0: 94.3666666666667},
 'CLNO': {0: 9.0},
 'DEBTINC': {0: 34.818261818587},
 'DELINQ': {0: 0.0},
 'DEROG': {0: 0.0},
 'LOAN': {0: 1100.0},
 'MORTDUE': {0: 25860.0},
 'NINQ': {0: 1.0},
 'VALUE': {0: 39025.0},
 'YOJ': {0: 10.5},
 'JOB': {0: 'Other'},
 'REASON': {0: 'HomeImp'}}
"""
