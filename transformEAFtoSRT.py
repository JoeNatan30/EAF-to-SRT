import pympi
import numpy as np
import argparse
import pysrt
import nltk
import os
import matplotlib.pyplot as plt
from collections import Counter

#from os import listdir, mkdir
#from os.path import isfile, join, exists

parser = argparse.ArgumentParser(description='The Embedded Topic Model')
parser.add_argument('--srtPath', type=str, default='EAF_input/', help='Path where per-line files are located')
parser.add_argument('--inputName', type=str, default='', help='Input File Name')
parser.add_argument('--outputPath', type=str, default='SRT_output/', help='Path where per-line files are located')

args = parser.parse_args()

srtPath = args.srtPath
inputName = args.inputName
outputPath = args.outputPath

if inputName == '':
    listFile = [ file for file in os.listdir(srtPath) if os.path.isfile(srtPath+file) and file[-3:]=='eaf' ]
else:
    listFile = [inputName]


print(listFile)
vocab = {}

for eafFile in listFile:

    newIndex = 0
    #open EAF file
    aEAFfile = pympi.Elan.Eaf(os.path.join(srtPath,eafFile))

    #create SRT file
    srtFile = pysrt.SubRipFile() #.open(srtPath+eafFile[:-4]+'.srt', encoding='utf-8')#, encoding='iso-8859-1'

    print(aEAFfile.tiers.keys())
    #print(aEAFfile.timeslots)

    ## Reading gloss tier (this are the different levels of annotations in ELAN)

    if 'GLOSA' in aEAFfile.tiers.keys():
        dictGloss = aEAFfile.tiers['GLOSA']
    elif  'GLOSADO' in aEAFfile.tiers.keys():
        dictGloss = aEAFfile.tiers['GLOSADO']
    elif 'GLOSAS' in aEAFfile.tiers.keys():
        dictGloss = aEAFfile.tiers['GLOSAS']

    print(len(dictGloss[0]))
    for key in dictGloss[0]:
    
    	# Read al the annotations in an specific tier. In Australian case should be FreeTransl or LitTransl
        start = dictGloss[0][key][0] # get the TIME_SLOT_REF1 that is the start
        end = dictGloss[0][key][1] # get TIME_SLOT_REF2 that is the end
        gloss = dictGloss[0][key][2] # get the ANNOTATION_VALUE which is the text or sentence annotation

	# this is to count the vocab, when the tier or annotation is per word or sign, it can be ignored
        if gloss in vocab:
            vocab[gloss] +=1
        else:
            vocab[gloss] = 1
            
        #print(key, "start ", start, aEAFfile.timeslots[start], " end ", end, aEAFfile.timeslots[end] )
        
        # With the key for the start and end, look in the previous xml level to get the actual time and write it in an SRT file
        newLine = pysrt.SubRipItem(index=newIndex, start= aEAFfile.timeslots[start], end=aEAFfile.timeslots[end], text=gloss)
        srtFile.append(newLine)
        newIndex +=1

    srtSave = outputPath+eafFile[:-4]+'.srt'
    print("path:",srtSave)
    srtFile.save(srtSave, encoding='utf-8')

print(len(vocab))

vocab = dict(sorted(vocab.items(), key=lambda x: x[0].lower()))
with open('glosas.csv', 'w') as f:
    for key in vocab.keys():
        f.write("%s,%d\n"%(key,vocab[key]))

    '''
    print(aEAFfile.get_controlled_vocabulary_names())
    print(aEAFfile.get_child_tiers_for('GLOSADO')) # GLOSA o GLOSADO o GLOSAS
    print(aEAFfile.get_child_tiers_for('CLASIFICADORES'))
    '''
