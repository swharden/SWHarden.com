---
title: Compress and Store Files in Python
date: 2008-11-24 17:48:16
tags: ["python", "obsolete"]
---



 __While writing code for my graduate research thesis__ I came across the need to lightly compress a huge and complex variable (a massive 3D data array) and store it in a text file for later retrieval.  I decided to use the [zlib](http://en.wikipedia.org/wiki/Zlib) compression library because it's open source and works pretty much on every platform.  I ran into a snag for a while though, because whenever I loaded data from a text file it wouldn't properly decompress.  I fixed this problem by adding the "rb" to the open line, forcing python to read the text file as binary data rather than ascii data.  Below is my code, written in two functions to save/load compressed string data to/from files in Python.

```python
import zlib  
  
def saveIt(data,fname):  
    data=str(data)  
    data=zlib.compress(data)  
    f=open(fname,'wb')  
    f.write(data)  
    f.close()  
    return  
  
def openIt(fname,evaluate=True):  
    f=open(fname,'rb')  
    data=f.read()  
    f.close()  
    data=zlib.decompress(data)  
    if evaluate: data=eval(data)  
    return data  
```

__Oh yeah, don't forget__ the evaluate option in the openIt function.  If set to True (default), the returned variable will be an evaluated object.  For example, `[[1,2],[3,4]]` will be returned as an actual 2D list, not just a string.  How convenient is that?