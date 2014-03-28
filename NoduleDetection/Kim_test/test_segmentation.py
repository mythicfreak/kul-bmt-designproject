'''
Created on 27-mrt.-2014

@author: Eigenaar
'''
import dicom
import pylab

# get image slice
ds=dicom.read_file("../data/LIDC-IDRI/LIDC-IDRI-0001/1.3.6.1.4.1.14519.5.2.1.6279.6001.298806137288633453246975630178/000000/000000.dcm")
#print(ds)
# get pixel values
data=ds.pixel_array
#print(data)
#show image
#pylab.imshow(ds.pixel_array, cmap=pylab.gray())
#pylab.show()

# apply a mask to the image to exclude the pixels outside the thorax in the image
#transform the pixel grey values to HU units: HU = pixel_value*slope - intercept
intercept = ds.RescaleIntercept # found in dicom header at (0028,1052)
slope = ds.RescaleSlope # found in dicom header at (0028,1053)
HU=data*slope - intercept
maxI=int(HU.max())
minI=int(HU.min())
# kom max waarde 3195 uit en min 0??? long zou normaal -500 moeten zijn

assert minI==0
datavector=HU.reshape(512*512,1)
print(datavector.shape)
(p, bins, patches)=pylab.hist(datavector,maxI)
# #pylab.show()
print(p)

## step 1: calculate T and M for every grey value

Mhigh={}
Thigh={}
Mlow={}
Tlow={}
for i in range(minI, maxI):
    Mhigh[i]=0
    Mlow[i]=0
    
    Thigh[i]=0
    Tlow[i]=0
        
    for k in range(i,maxI):
        Mhigh[i]=k*p[k]+Mhigh[i]
        Thigh[i]=p[k]+Thigh[i]
            
    for k in range(minI,i):
        Mlow[i]=k*p[k]+Mlow[i]
        Tlow[i]=p[k]+Tlow[i]
        
print("Mhigh = {0}".format(Mhigh))
print("Mlow = {0}".format(Mlow))
print("Thigh = {0}".format(Thigh))
print("Tlow = {0}".format(Tlow))

# step 2: calculate the mean values of both regions

mulow={}
muhigh={}

for i in range(minI, maxI):
    if Tlow[i] == 0:
        mulow[i]=0
    else:
        mulow[i]=Mlow[i]/Tlow[i]
    
    if Thigh[i] == 0:
        muhigh[i]=0
    else:
        muhigh[i]=Mhigh[i]/Thigh[i]
    
# step 3: membership measurement
def distance(t, muHigh_i, muLow_i, i):
    if t <= i:
        return abs(t-muLow_i)
    else:
        return abs(t-muHigh_i)

member={}
for i in range(minI, maxI):
    for t in range(minI, maxI):
        member[t]=0
        member[t]= 1/(1 + distance(t, muhigh[i], mulow[i], i) / (maxI - 1))
   



