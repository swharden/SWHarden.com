---
title: Fixing Slow Matplotlib in Python(x,y)
date: 2013-04-15 11:55:27
tags: ["python", "old"]
---

# Fixing Slow Matplotlib in Python(x,y)

__I recently migrated to [Python(x,y)](https://code.google.com/p/pythonxy/) and noticed my matplotlib graphs are resizing unacceptably slowly when I use the pan/zoom button.__ I'm quite a fan of [numpy](http://www.scipy.org/Download), [scipy](http://www.scipy.org/Download), [matplotlib](http://matplotlib.org), the [python imaging library (PIL)](http://www.pythonware.com/products/pil/), and GUI platforms like [Tk/TkInter](http://wiki.python.org/moin/TkInter), [pyGTK](http://www.pygtk.org/), and [pyQT](http://www.riverbankcomputing.com/software/pyqt/intro), but getting them all to play nicely is a sometimes pain. I'm considering migrating entirely to [Python(x,y)](https://code.google.com/p/pythonxy/) because, as a single distribution, it's designed to install all [these libraries (and many more)](https://code.google.com/p/pythonxy/wiki/StandardPlugins) in a compatible way out of the box. However, when I did, I noticed matplotlib graphs would resize, rescale, and drag around the axes very slowly. After a lot of digging on the interweb, I figured out what was going wrong. I'll show you by plotting 20 random data points the slow way (left) then the fast way (right).

<div class="text-center img-small">

[![](matplotlib-qt4agg_thumb.jpg)](matplotlib-qt4agg.jpg)
[![](matplotlib-tkagg_thumb.jpg)](matplotlib-tkagg.jpg)

</div>

__THE PROBLEM:__ See the difference between the two plots? The one on the left (SLOW!) uses the Qt4Agg backend, which renders the matplotlib plot on a QT4 canvas. This is slower than the one on the right, which uses the more traditional TkAgg backend to draw the plot on a Tk canvas with tkinter (FASTER!).  Check out [matplotlib's official description of what a backend is](http://matplotlib.org/faq/usage_faq.html#what-is-a-backend) and which ones you can use. When you just install Python and matplotlib, Tk is used by default.

```python
import numpy
import matplotlib
matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import pylab
pylab.plot(numpy.random.random_integers(0,100,20))
pylab.title("USING: "+matplotlib.get_backend())
pylab.show()
```

__THE FIX:__ Tell matplotlib to stop using QT to draw the plot, and let it plot with Tk. This can be done immediately after importing matplotlib, but must be done before importing pylab using the line `` matplotlib.use('TkAgg') ``. Here's the full example I used to generate the demonstration plots above. Change TkAgg to Qt4Agg (or comment-out the 'use' line if you're using PythonXY) and you will see performance go down the tube. Alternatively, [make a change to the matplotlib rc file](http://matplotlib.org/users/customizing.html) to customize default behavior when the package is loaded.