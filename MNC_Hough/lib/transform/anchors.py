# --------------------------------------------------------
# Multitask Network Cascade
# Modified from py-faster-rcnn (https://github.com/rbgirshick/py-faster-rcnn)
# Copyright (c) 2016, Haozhi Qi
# Licensed under The MIT License [see LICENSE for details]
#This code modified by Author to get Anchors based on Hough_Transform features
# --------------------------------------------------------

import numpy as np
import pickle
import pdb
import os
from random import sample


def generate_anchors(base_size=16, ratios=[0.5, 1, 2],
                     scales=2**np.arange(3, 6)):
   
    base_anchor = np.array([1, 1, base_size, base_size]) - 1
    ratio_anchors = _ratio_enum(base_anchor, ratios)
    anchors = np.vstack([_scale_enum(ratio_anchors[i, :], scales)
                         for i in xrange(ratio_anchors.shape[0])])
    print anchors
    return anchors

def _get_center(batch_name):
    path = '/data/Workspace/MNC/lib/transform/anchors.pkl'  
    #with open(anchors_file, 'rb') as fid:
    #pickle.load(fid, obj)
    #batch_name = ['VSD.Brain.XX.O.MR_Flair_501.nz.58.png','VSD.Brain.XX.O.MR_Flair_501.nz.48.png','VSD.Brain.XX.O.MR_Flair_501.nz.52.png','VSD.Brain.XX.O.MR_Flair_501.nz.37.png','VSD.Brain.XX.O.MR_Flair_501.nz.36.png','VSD.Brain.XX.O.MR_Flair_501.nz.44.png','VSD.Brain.XX.O.MR_Flair_501.nz.45.png','VSD.Brain.XX.O.MR_Flair_501.nz.47.png']
    files=open(path, 'rb')
    obj=pickle.load(files)
    for line in obj:
        Points=[]
        imname=line[0]
        midpoints=line[1]
        count_ctr=len(midpoints)
        #for imname in batch_name:
        for pairs in midpoints:
                pair=pairs.split()
                a_ctr = int(pair[0])
                b_ctr = int(pair[1])
                Points.append((a_ctr,b_ctr))
                #print Points            
        return line, count_ctr, Points

def _findmaxmin(Points):
    global xmin, ymin, xmax, ymax
    xmin, ymin, xmax, ymax = 240, 240, 0 ,0

    for pairs in Points:
                x_ = int(pairs[0])
                y_ = int(pairs[1])
                if x_ <xmin :
                    xmin=x_
                if y_ <ymin :
                    ymin=y_
                if x_ >xmax :
                    xmax=x_
                if y_ >ymax :
                    ymax=y_

    #print xmin,ymin,xmax,ymax
    return xmin,ymin,xmax,ymax

def _generate27(count_ctr,xmin,ymin,xmax,ymax):
   
    global gtr_points 
    gtr_points= []
    num_gntr= 27-count_ctr
    X=sample(xrange(xmin, xmax),num_gntr)
    Y=sample(xrange(ymin, ymax),num_gntr)
    gtr_points=list(zip(X, Y))

    return gtr_points


def _whctrs(anchor):
    """
    Return width, height, x center, and y center for an anchor (window).
    """
    global imname, anchor_dict
    anchor_dict=[]
    imname="VSD.Brain.XX.O.MR_Flair_501.nz.58.png"
    batch_name=['VSD.Brain.XX.O.MR_Flair_501.nz.58.png', 'VSD.Brain.XX.O.MR_Flair_501.nz.48.png', 'VSD.Brain.XX.O.MR_Flair_501.nz.52.png', 'VSD.Brain.XX.O.MR_Flair_501.nz.37.png', 'VSD.Brain.XX.O.MR_Flair_501.nz.36.png', 'VSD.Brain.XX.O.MR_Flair_501.nz.44.png', 'VSD.Brain.XX.O.MR_Flair_501.nz.45.png', 'VSD.Brain.XX.O.MR_Flair_501.nz.47.png']
    #pdb.set_trace()
    anchors_file = '/data/Workspace/MNC/lib/transform/anchors.pkl'
    if os.path.exists(anchors_file):
        
        line, count_ctr, Points=_get_center(batch_name)
        if count_ctr < 27:
            print 'find some point between min and max'
            
            _findmaxmin(Points)
            _generate27(count_ctr,xmin,ymin,xmax,ymax)            
            
            hough_anchor= Points+gtr_points
            imagename=line[0]
            anchor_dict.append((imagename,hough_anchor))
            #hough_anchor.append( imname )
            w = anchor[2] - anchor[0] + 1
            h = anchor[3] - anchor[1] + 1
          
        elif count_ctr > 30:
           print 'Just select top 30'

        elif count_ctr == 30:
            print 'every thing is right and return values '
             
    return w, h, hough_anchor


def _mkanchors(ws, hs, x_ctr, y_ctr):
    """
    Given a vector of widths (ws) and heights (hs) around a centeanchorr
    (x_ctr, y_ctr), output a set of anchors (windows).
    """
    ws = ws[:, np.newaxis]
    hs = hs[:, np.newaxis]
    print 'x-ctr is y_ctr is '
    print x_ctr,y_ctr
    anchors = np.hstack((x_ctr - 0.5 * (ws - 1),
                         y_ctr - 0.5 * (hs - 1),
                         x_ctr + 0.5 * (ws - 1),
                         y_ctr + 0.5 * (hs - 1)))
    print anchors.shape
    return anchors


def _ratio_enum(anchor, ratios):
    """
    Enumerate a set of anchors for each aspect ratio wrt an anchor.
    """
    w, h, hough_anchor = _whctrs(anchor)
    size = w * h
    size_ratios = size / ratios
    ws = np.round(np.sqrt(size_ratios))
    hs = np.round(ws * ratios)
    for center in hough_anchor:
        #hough_ctr=center.split()
        x_ctr = int(center[0])
        y_ctr = int(center[1])
        anchors = _mkanchors(ws, hs, x_ctr, y_ctr)
        print anchors
    return anchors


def _scale_enum(anchor, scales):
    """
    Enumerate a set of anchors for each scale wrt an anchor.
    """
    w, h, hough_anchor = _whctrs(anchor)
    ws = w * scales
    hs = h * scales
    for center in hough_anchor:
        x_ctr = int(center[0])
        y_ctr = int(center[1])
        anchors = _mkanchors(ws, hs, x_ctr, y_ctr)
        
    pdb.set_trace()

    print anchors
    return anchors


def generate_shifted_anchors(anchors, height, width, feat_stride):
    # Enumerate all shifted anchors:
    #
    # add A anchors (1, A, 4) to
    # cell K shifts (K, 1, 4) to get
    # shift anchors (K, A, 4)
    # reshape to (K*A, 4) shifted anchors
    shift_x = np.arange(0, width) * feat_stride
    shift_y = np.arange(0, height) * feat_stride
    shift_x, shift_y = np.meshgrid(shift_x, shift_y)
    shifts = np.vstack((shift_x.ravel(), shift_y.ravel(),
                       shift_x.ravel(), shift_y.ravel())).transpose()
    A = anchors.shape[0]
    K = shifts.shape[0]
    anchors = anchors.reshape((1, A, 4)) + \
              shifts.reshape((1, K, 4)).transpose((1, 0, 2))
    anchors = anchors.reshape((K * A, 4))
    return anchors

def generate_all_anchors_per_img (base_size=16, ratios=[0.5, 1, 2],
                     scales=2**np.arange(3, 6)):
   
    base_anchor = np.array([1, 1, base_size, base_size]) - 1
    ratio_anchors = _ratio_enum(base_anchor, ratios)
    anchors = np.vstack([_scale_enum(ratio_anchors[i, :], scales)
                         for i in xrange(ratio_anchors.shape[0])])
    print anchors
    return anchors

if __name__ == '__main__':
    import time
    t = time.time()
    #a = generate_anchors()
    a = hough_voting_anchors()
    pdb.set_trace()
    print time.time() - t
    print a
    from IPython import embed
    embed()
