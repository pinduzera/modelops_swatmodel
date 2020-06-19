# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 19:25:33 2020

@author: edhell
"""

################################################
######### FIT STATISTICS #######################
gb_score = conn.CASTable("gb_score")
gb_score.head()
outs =conn.percentile.assess(casOut={"name":"gb_assess", "replace":True},
                               nbins=10,
                               cutStep = 0.01,
                               table = {'name':'gb_score',
                                        'groupBy': '_PartInd_'},
                               inputs=['P_BAD1'],
                               response='BAD',
                               event='1',
                               pVar=['P_BAD0'],
                               pEvent='0')
gb_asses = conn.CASTable("gb_assess_FITSTAT")

print('\nFIT STATISTICS')

print('\nTRAIN FIT')
print("\n".join("{}\t{}".format(k, v) for k, v in gb_asses.head(1).to_dict().items()))

print('\nVALIDATION FIT')
print("\n".join("{}\t{}".format(k, v) for k, v in gb_asses.tail(1).to_dict().items()))

