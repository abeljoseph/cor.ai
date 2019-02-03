# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 01:45:45 2019

@author: james
"""
from random import shuffle 
total = 10800
trainRatio = int(total*.70)
validRatio = (total - trainRatio)//2
testRatio = total - trainRatio - validRatio

bits = [0]*trainRatio
bits += [1]*validRatio
bits +=[2]*testRatio
shuffle(bits)

output = ''
for i in bits:
    output+=str(i)

file = open('randomOrder.txt','w')
file.write(output)
file.close()