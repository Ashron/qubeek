"""
Created on Tue Jun 13 10:30:55 2017

@author: KAA
"""

from sharehelper import ShareHelper

sh = ShareHelper()
#m =sh.get_code('mosenrg')
l =sh.get_code('tmk-ao')
#print(len(l))
#print(l[0][0])
#print(l[0][1])
#
#print(l[1][0])

list_code = sh.get_listcode()
print(list_code[0][0])
print(list_code[1][0])