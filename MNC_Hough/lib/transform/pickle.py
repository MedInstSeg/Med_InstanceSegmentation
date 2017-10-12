import os
import ntpath
import pickle
import glob
import pdb

output=[]
os.chdir("/data/Workspace/MNC/lib/transform/anchors/")
for file in glob.glob("*.txt"):
    midpoint=[]
    imname=[]
    with open(file,'r') as f:
        for line in f:
            filename, xmid, ymid=line.partition(' ')
            lenline=len(line)-3
            lin= line[61:lenline]
            imgname=ntpath.basename(filename).split('GroundTruthPng')[0]
            lengh=len(imgname)+1
            xmidymid=lin[lengh:]
            midpoint.append(xmidymid)
            img=ntpath.basename(filename).split('.png')[0]
        imname=imgname
        output.append((imname,midpoint))
        #pdb.set_trace()
        print output

destPath='/data/Workspace/MNC/lib/transform/anchors1.pkl'
pickle.dump(output,open(destPath,"wb"))


