---
title: QRSS VD Image Assembler
date: 2010-06-07 23:20:18
tags: ["qrss", "obsolete", "python"]
---

# QRSS VD Image Assembler

This minimal Python script will convert a directory filled with tiny image captures such as [this](http://www.swharden.com/blog/images/mass-W1BW_2jpg.jpg) into gorgeous montages as seen below! I whipped-up this script tonight because I wanted to assess the regularity of my transmitter's embarrassing drift. I hope you find it useful.

<div class="text-center img-border">

![](https://swharden.com/static/2010/06/07/assembled-squished.jpg)

</div>

```python
import os
from PIL import Image

x1,y1,x2,y2=[0,0,800,534] #crop from (x,y) 0,0 to 800x534
squish=10 #how much to squish it horizontally

### LOAD LIST OF FILES ###
workwith=[]
for fname in os.listdir('./'):
    if ".jpg" in fname and not "assembled" in fname:
        workwith.append(fname)
workwith.sort()

### MAKE NEW IMAGE ###
im=Image.new("RGB",(x2*len(workwith),y2))
for i in range(len(workwith)):
    print "Loading",workwith[i]
    im2=Image.open(workwith[i])
    im2=im2.crop((x1,y1,x2,y2))
    im.paste(im2,(i*x2,0))
print "saving BIG image"
im.save("assembled.jpg")
print "saving SQUISHED image"
im=im.resize((im.size[0]/10,im.size[1]),Image.ANTIALIAS)
im.save("assembled-squished.jpg")
print "DONE"
```

__Script to download every image linked to from a webpage__:

```python
import urllib2
import os

suckFrom="http://w1bw.org/grabber/archive/2010-06-08/"

f=urllib2.urlopen(suckFrom)
s=f.read().split("'")
f.close()
download=[]

for line in s:
    if ".jpg" in line and not line in download and not "thumb" in line:
        download.append(line)

for url in download:
    fname = url.split("/")[-1].replace(":","-")
    if fname in os.listdir('./'):
        print "I already downloaded",fname
    else:
        print "downloading",fname
        output=open(fname,'wb')
        output.write(urllib2.urlopen(url).read())
        output.close()
```

