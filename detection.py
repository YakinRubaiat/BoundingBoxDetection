import os
import sys
import time
import json
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

import warnings
warnings.filterwarnings('ignore')


from util import get_detection_from_file,draw,nms

from keras_retinanet import models

# from tensorflow import keras

graph = tf.get_default_graph()

class detectp:


    def __init__(self):   
        with open('settings.json') as json_data_file:
            json_data = json.load(json_data_file)


        self.model2_path = json_data["MODEL_101"]
        self.model2 = models.load_model(self.model2_path, backbone_name='resnet101', convert=True, nms=False)

    def detect(self,fpath): 
        im = cv2.imread(fpath)

        sz = 224

        # threshold for non-max-suppresion for each model
        nms_threshold = 0

        # shrink bounding box dimensions by this factor, improves test set performance
        shrink_factor = 0.17

        # threshold for judging overlap of bounding boxes between different networks (for weighted average)
        wt_overlap = 0

        # threshold for including boxes from model 1
        score_threshold1 = 0.04

        # threshold for including boxes from model 2
        score_threshold2 = 0.03

        # threshold for including isolated boxes from either model
        solo_min = 0.15




        #boxes_pred1, scores1 = util.get_detection_from_file(fpath, model1, sz)
        global graph
        with graph.as_default():
            boxes_pred2, scores2 = get_detection_from_file(fpath, self.model2, sz)


        # indices1 = np.where(scores1 > score_threshold1)[0]
        # scores1 = scores1[indices1]
        # boxes_pred1 = boxes_pred1[indices1]
        # boxes_pred1, scores1 = util.nms(boxes_pred1, scores1, nms_threshold)

        indices2 = np.where(scores2 > score_threshold2)[0]
        scores2 = scores2[indices2]
        boxes_pred2 = boxes_pred2[indices2]
        boxes_pred2, scores2 = nms(boxes_pred2, scores2, nms_threshold)

        boxes_pred = boxes_pred2
        scores = scores2

       

        boxx = []
        #print(boxes_pred,scores)

        for i, bb in enumerate(boxes_pred):
            x1 = int(bb[0])
            y1 = int(bb[1])
            w = int(bb[2]-x1+1)
            h = int(bb[3]-y1+1)
            
            boxx.append([x1,y1,w,h])

        
        draw(im,boxx)
        
        if scores.size == 0:
            return 0
        else:
            return np.max(scores)