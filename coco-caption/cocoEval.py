#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
import matplotlib.pyplot as plt
import skimage.io as io
import pylab
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

import argparse, os
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')

parser = argparse.ArgumentParser(description='Generate captions.')
parser.add_argument('infile')
args = parser.parse_args()

pwd = os.getcwd()+"/"


# set up file names and pathes
dataDir='.'
dataType='val2014'
algName = 'fakecap'
annFile='%s/annotations/captions_%s.json'%(dataDir,dataType)
subtypes=['results', 'evalImgs', 'eval']
[resFile, evalImgsFile, evalFile]= ['%s/results/captions_%s_%s_%s.json'%(dataDir,dataType,algName,subtype) for subtype in subtypes]

resFile = args.infile
imgDir=  '../im2txt/data/mscoco/raw-data'

# In[3]:


# create coco object and cocoRes object
coco = COCO(annFile)
cocoRes = coco.loadRes(resFile)


# In[4]:


# create cocoEval object by taking coco and cocoRes
cocoEval = COCOEvalCap(coco, cocoRes)

# evaluate on a subset of images by setting
# cocoEval.params['image_id'] = cocoRes.getImgIds()
# please remove this line when evaluating the full validation set
cocoEval.params['image_id'] = cocoRes.getImgIds()

# evaluate results
# SPICE will take a few minutes the first time, but speeds up due to caching
cocoEval.evaluate()


# In[5]:

# print output evaluation scores
for metric, score in cocoEval.eval.items():
    print '%s: %.3f'%(metric, score)


# In[6]:


# demo how to use evalImgs to retrieve low score result
evals = [eva for eva in cocoEval.evalImgs if eva['CIDEr']<30]
sorted_evals = sorted(evals, key=lambda x: x['CIDEr'])
def printImg(idx):
    imgId = sorted_evals[idx]['image_id']
    annIds = coco.getAnnIds(imgIds=imgId)
    anns = coco.loadAnns(annIds)

    print 'image_id: %d' %imgId
    print 'score:'
    print '   CIDEr:  %0.4f'%(sorted_evals[idx]['CIDEr'])
    print '   METEOR: %0.4f'%(sorted_evals[idx]['METEOR'])
    print '   BLEU1:  %0.4f'%(sorted_evals[idx]['Bleu_1'])
    print '   BLEU4:  %0.4f'%(sorted_evals[idx]['Bleu_4'])

    print 'ground truth captions'
    coco.showAnns(anns)
    print 'generated caption:'
    annIds = cocoRes.getAnnIds(imgIds=imgId)
    anns = cocoRes.loadAnns(annIds)
    coco.showAnns(anns)
    #img = coco.loadImgs(imgId)[0]
    #I = io.imread('%s/%s/%s'%(imgDir,dataType,img['file_name']))
    #plt.imshow(I)
    #plt.axis('off')
    #plt.show()


#print '[all]'
#for idx in range(len(sorted_evals)):
#    printImg(idx)
# In[7]:


# plot score histogram
#ciderScores = [eva['CIDEr'] for eva in cocoEval.evalImgs]
#plt.hist(ciderScores)
#plt.title('Histogram of CIDEr Scores', fontsize=20)
#plt.xlabel('CIDEr score', fontsize=20)
#plt.ylabel('result counts', fontsize=20)
#plt.show()


# In[8]:


# save evaluation results to ./results folder
json.dump(cocoEval.evalImgs, open(evalImgsFile, 'w'))
json.dump(cocoEval.eval,     open(evalFile, 'w'))

