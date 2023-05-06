---
title: Generate LUTs with Python
date: 2010-05-10 22:31:46
tags: ["python", "old"]
---

# Generate LUTs with Python

__I wrote a script to generate and display LUTs with Python.__ There has been a lot of heated discussion in the [QRSS Knights mailing list](http://cnts.be/mailman/listinfo/knightsqrss_cnts.be) as to the use of color maps when representing QRSS data. I'll make a separate post (perhaps later?) documenting why it's so critical to use particular mathematically-generated color maps rather than empirical "looks good to me" color selections. Anyway, this is what I came up with:

<div class="text-center img-border">

[![](Blin_Glin_Rlin_scale_thumb.jpg)](Blin_Glin_Rlin_scale.png)

</div>

__For my QRSS needs,__ I desire a colormap which is aesthetically pleasing but can also be quickly reverted to its original (gray-scale) data. I accomplished this by choosing a channel (green in this case) and applying its intensity linearly with respect to the value it represents. Thus, any "final" image can be imported into an editor, split by RGB, and the green channel represents the original data. This allows adjustment of contrast/brightness and even the reassignment of a different colormap, all without losing any data!

<div class="text-center img-border">

![](Blin_Glin_Rlin.jpg-green.jpg)

</div>

__ORIGINAL DATA:__
(that's the "flying W" and the FSK signal below it is WA5DJJ)

<div class="text-center img-border">

[![](Blin_Glin_Rlin_graph_thumb.jpg)](Blin_Glin_Rlin_graph.png)
![](Blin_Glin_Rlin.jpg)

</div>

Note that it looks nice, shows weak signals, doesn't get blown-out by strong signals, and it fully includes the noise floor (utilizing all available data).

<div class="text-center img-border">

![](Blin_Glin_Rlin.jpg-blue.jpg)
![](Blin_Glin_Rlin.jpg-red.jpg)
![](Blin_Glin_Rlin.jpg-green.jpg)
[![](Bsin_Glin_Rsin_graph_thumb.jpg)](Bsin_Glin_Rsin_graph.png)
![](Bsin_Glin_Rsin.jpg)

</div>

__This is the Python script__ I wrote to generate the downloadable LUTs, graphs, and scale bars / keys / legends which are not posted. It requires python, matplotlib, and PIL.

```python
import math
import pylab
from PIL import Image

####################### GENERATE RGB VALUES #######################

r,g,b=[],[],[]
name="Blin_Glin_Rlin"
for i in range(256):
    if i>128: #LOW HALF
        j=128
        k=i
    else: #HIGH HALF
        k=128
        j=i
    #b.append((math.sin(3.1415926535*j/128.0/2))*256)
    #r.append((1+math.sin(3.1415926535*(k-128*2)/128.0/2))*256)
    r.append(k*2-255)
    g.append(i)
    b.append(j*2-1)

    if r[-1]<0:r[-1]=0
    if g[-1]<0:g[-1]=0
    if b[-1]<0:b[-1]=0

    if r[-1]>255:b[-1]=255
    if g[-1]>255:g[-1]=255
    if b[-1]>255:b[-1]=255

####################### SAVE LUT FILE #######################
im = Image.new("RGB",(256*2,10*4))
pix = im.load()
for x in range(256):
    for y in range(10):
        pix[x,y] = (r[x],g[x],b[x])
        pix[x,y+10] = (r[x],0,0)
        pix[x,y+20] = (0,g[x],0)
        pix[x,y+30] = (0,0,b[x])
        a=(g[x]+g[x]+g[x])/3
        pix[256+x,y] = (a,a,a)
        pix[256+x,y+10] = (r[x],r[x],r[x])
        pix[256+x,y+20] = (g[x],g[x],g[x])
        pix[256+x,y+30] = (b[x],b[x],b[x])
#im=im.resize((256/2,40),Image.ANTIALIAS)
im.save(name+"_scale.png")

####################### PLOT IT #######################
pylab.figure(figsize=(8,4))
pylab.grid(alpha=.3)
pylab.title(name)
pylab.xlabel("Data Value")
pylab.ylabel("Color Intensity")
pylab.plot(g,'g-')
pylab.plot(r,'r-')
pylab.plot(b,'b-')
pylab.axis([-10,266,-10,266])
pylab.subplots_adjust(top=0.90, bottom=0.14, left=0.1, right=0.97)
pylab.savefig(name+"_graph.png",dpi=60)
#pylab.show()

####################### SAVE LUT FILE #######################
f=open(name+".lut",'w')
out="IndextRedtGreentBluen"
for i in range(256):
    out+=("t%dt%dt%dt%dn"%(i,r[i],g[i],b[i]))
f.write(out)
f.close()
```

