---
title: Dynamic Logo Generation with Python
date: 2010-03-07 18:47:00
tags: ["python", "old"]
---

# Dynamic Logo Generation with Python

__I'm working on a software project and I'd love the startup screen to be unique.__ I want the splash image to be generated programmatically. I have to generate it from the script, but how can I reliably print text on an image with fonts vary across operating systems? Keep in mind many OS's don't have "arial.ttf", or no truetype fonts at all!

__First, I created a 2D binary array to represent the alphabet__ using pixel fonts [such as this](http://img.nattawat.org/images/yus3i81of22r503eyjtw.png) as a reference. The word I'm trying to create is "QRSS VD" (the name of my program). I store the data in strings, as seen below. I use 1's to mark pixels, and spaces to mark empty spaces.

```python
data="""
1111 1111 1111 1111   1  1 111
1  1 1  1 1    1      1  1 1  1
1  1 1111 1111 1111   1  1 1  1
1 11 1 1     1    1   1 1  1  1
1111 1 11 1111 1111    1   111
"""
```

__Once I think it looks nice__, I replace the spaces with zeros to make it take up a lot of visual space...

```python
data2="""
1111011110111101111000100101110
1001010010100001000000100101001
1001011110111101111000100101001
1011010100000100001000101001001
1111010110111101111000010001110
"""
```

__Then I further obscure it__ by replacing linebreaks with a different symbol, such as the number 2, then break the lines so they're not lined up...

```python
b="1111011110111101111000100101110210010100101000010000001001010012"
b+="1001011110111101111000100101001210110101000001000010001010010012"
b+="1111010110111101111000010001110"
```

__The result is a pretty cool way__ to obscure the text. I don't know why you'd want to, but if you want to make sure that no one goes in and changes the letters around (at least without making them think pretty hard about it) you could look at ways to further encrypt this data stream. From here, I create an image using the Python Imaging Library, setting pixel values to 255\*b\[x,y\] (so 0 stays 0 and 1 becomes 255, perfect for an 8-bit image). After enlarging, here's the result:

<div class="text-center img-border">

![](https://swharden.com/static/2010/03/07/nearest.png)

</div>

Now let's make it a little bit less pixelated. It's not a cure-all method, but blurring it up a little with a bilinear filter helps a lot...

<div class="text-center img-border">

![](https://swharden.com/static/2010/03/07/bilinear.png)

</div>

Then I apply the code below which applies a cool colormap to the pixel values. I'll provide cleaner code for this later (I have a really cool way of generating colormaps and saving them as arrays of RGB tuples). Then I go through and plot some random sin wavs on top of it. Sweet! Here are 6 images generated from the program run 6 times. Notice the randomness of the sine wavs!

<div class="text-center img-border img-micro">

![](https://swharden.com/static/2010/03/07/qrss-vd-logo-0.png)
![](https://swharden.com/static/2010/03/07/qrss-vd-logo-1.png)
![](https://swharden.com/static/2010/03/07/qrss-vd-logo-2.png)
![](https://swharden.com/static/2010/03/07/qrss-vd-logo-3.png)
![](https://swharden.com/static/2010/03/07/qrss-vd-logo-4.png)
![](https://swharden.com/static/2010/03/07/qrss-vd-logo-5.png)

</div>

__A different image is generated every time the script runs, __and it requires no external files (bitmaps or fonts) and should work well on all operating systems.

```python
from PIL import Image
from PIL import ImageOps
from PIL import ImageFilter
from random import randint
import scipy


def genLogo():
    colormap = [(0, 0, 129), (0, 0, 134), (0, 0, 139), (0, 0, 143), (0, 0, 148), (0, 0, 152), (0, 0, 157), (0, 0, 161), (0, 0, 166), (0, 0, 170), (0, 0, 175), (0, 0, 180), (0, 0, 184), (0, 0, 189), (0, 0, 193), (0, 0, 198), (0, 0, 202), (0, 0, 207), (0, 0, 211), (0, 0, 216), (0, 0, 220), (0, 0, 225), (0, 0, 230), (0, 0, 234), (0, 0, 239), (0, 0, 243), (0, 0, 248), (0, 0, 252), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 2, 255), (0, 7, 255), (0, 11, 255), (0, 14, 255), (0, 18, 255), (0, 23, 255), (0, 27, 255), (0, 31, 255), (0, 34, 255), (0, 39, 255), (0, 43, 255), (0, 47, 255), (0, 51, 255), (0, 54, 255), (0, 59, 255), (0, 63, 255), (0, 67, 255), (0, 71, 255), (0, 75, 255), (0, 79, 255), (0, 83, 255), (0, 87, 255), (0, 91, 255), (0, 95, 255), (0, 99, 255), (0, 103, 255), (0, 107, 255), (0, 111, 255), (0, 115, 255), (0, 119, 255), (0, 123, 255), (0, 127, 255), (0, 131, 255), (0, 135, 255), (0, 139, 255), (0, 143, 255), (0, 147, 255), (0, 151, 255), (0, 155, 255), (0, 159, 255), (0, 163, 255), (0, 167, 255), (0, 171, 255), (0, 175, 255), (0, 179, 255), (0, 183, 255), (0, 187, 255), (0, 191, 255), (0, 195, 255), (0, 199, 255), (0, 203, 255), (0, 207, 255), (0, 211, 255), (0, 215, 255), (0, 219, 254), (0, 223, 251), (0, 227, 248), (2, 231, 245), (5, 235, 241), (7, 239, 238), (11, 243, 235), (14, 247, 232), (18, 251, 228), (21, 255, 225), (23, 255, 222), (27, 255, 219), (31, 255, 215), (34, 255, 212), (37, 255, 208), (40, 255, 205), (44, 255, 203), (47, 255, 199), (50, 255, 195), (54, 255, 192), (57, 255, 189), (60, 255, 186), (63, 255, 183), (66, 255, 179), (70, 255, 176), (73, 255, 173), (76, 255, 170), (79, 255, 166), (83, 255, 163), (86, 255, 160), (89, 255, 157), (92, 255, 154), (95, 255, 150), (99, 255, 147), (102, 255, 144), (105, 255, 141), (108, 255, 137), (112, 255, 134), (115, 255, 131), (118, 255, 128), (121, 255, 125), (124, 255, 121),
                (128, 255, 118), (131, 255, 115), (134, 255, 112), (137, 255, 108), (141, 255, 105), (144, 255, 102), (147, 255, 99), (150, 255, 95), (154, 255, 92), (157, 255, 89), (160, 255, 86), (163, 255, 83), (166, 255, 79), (170, 255, 76), (173, 255, 73), (176, 255, 70), (179, 255, 66), (183, 255, 63), (186, 255, 60), (189, 255, 57), (192, 255, 54), (195, 255, 50), (199, 255, 47), (202, 255, 44), (205, 255, 41), (208, 255, 37), (212, 255, 34), (215, 255, 31), (218, 255, 28), (221, 255, 24), (224, 255, 21), (228, 255, 18), (231, 255, 15), (234, 255, 12), (238, 255, 8), (241, 252, 5), (244, 248, 2), (247, 244, 0), (250, 240, 0), (254, 236, 0), (255, 233, 0), (255, 229, 0), (255, 226, 0), (255, 221, 0), (255, 218, 0), (255, 215, 0), (255, 211, 0), (255, 207, 0), (255, 203, 0), (255, 199, 0), (255, 196, 0), (255, 192, 0), (255, 188, 0), (255, 184, 0), (255, 180, 0), (255, 177, 0), (255, 173, 0), (255, 169, 0), (255, 165, 0), (255, 162, 0), (255, 159, 0), (255, 155, 0), (255, 151, 0), (255, 147, 0), (255, 143, 0), (255, 140, 0), (255, 136, 0), (255, 132, 0), (255, 128, 0), (255, 125, 0), (255, 121, 0), (255, 117, 0), (255, 114, 0), (255, 110, 0), (255, 106, 0), (255, 102, 0), (255, 99, 0), (255, 95, 0), (255, 91, 0), (255, 88, 0), (255, 84, 0), (255, 80, 0), (255, 76, 0), (255, 73, 0), (255, 69, 0), (255, 65, 0), (255, 62, 0), (255, 58, 0), (255, 54, 0), (255, 51, 0), (255, 47, 0), (255, 43, 0), (255, 39, 0), (255, 36, 0), (255, 32, 0), (255, 28, 0), (255, 25, 0), (255, 21, 0), (253, 17, 0), (248, 14, 0), (244, 10, 0), (240, 6, 0), (235, 2, 0), (230, 0, 0), (225, 0, 0), (221, 0, 0), (217, 0, 0), (212, 0, 0), (207, 0, 0), (203, 0, 0), (198, 0, 0), (194, 0, 0), (189, 0, 0), (185, 0, 0), (180, 0, 0), (175, 0, 0), (171, 0, 0), (166, 0, 0), (162, 0, 0), (157, 0, 0), (152, 0, 0), (148, 0, 0), (144, 0, 0), (139, 0, 0), (134, 0, 0), (130, 0, 0), (134, 0, 0), (130, 0, 0)]

    def red(val):
        return colormap[val][0]

    def green(val):
        return colormap[val][1]

    def blue(val):
        return colormap[val][2]

    def colorize(im):
        r = Image.eval(im, red)
        g = Image.eval(im, green)
        b = Image.eval(im, blue)
        im = Image.merge("RGB", (r, g, b))
        return im
    b = "1111011110111101111000100101110210010100101000010000001001010012"
    b += "1001011110111101111000100101001210110101000001000010001010010012"
    b += "1111010110111101111000010001110"
    b = b.split("2")
    im = Image.new("L", (33+15, 7+13))
    data = im.load()
    for y in range(len(b)):
        for x in range(len(b[y])):
            data[x+6, y+6] = int(b[y][x])*255
    scale = 15
    im = im.resize((im.size[0]*scale, im.size[1]*scale))
    data = im.load()

    def drawSin(width, height, vertoffset, horizoffset, thickness, darkness):
        for x in range(im.size[0]):
            y = scipy.sin((x-horizoffset)/float(width))*height+vertoffset
            for i in range(thickness):
                if 0 <= y+i < im.size[1] and 0 <= x < im.size[0]:
                    # print x,im.size[0],y+i,im.size[1]
                    data[x, y+i] = data[x, y+i]+darkness

    for i in range(5):
        print "line", i
        drawSin(randint(5, 75), randint(-100, 200), randint(0, im.size[1]),
                randint(0, im.size[0]), randint(3, 15), 70)
    for i in range(10):
        im = im.filter(ImageFilter.SMOOTH_MORE)
    im = colorize(im)
    return im


im = genLogo()
im.save('logo.png', "PNG")
```