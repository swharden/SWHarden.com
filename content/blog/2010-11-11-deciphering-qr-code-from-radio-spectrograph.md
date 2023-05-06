---
title: Deciphering QR Code from Radio Spectrogram
date: 2010-11-11 15:13:29
tags: ["qrss", "amateur radio"]
---

# Deciphering QR Code from Radio Spectrogram

__Although I've been ridiculously busy the last few weeks,__ I've been eying some posts circulating around the [Knights QRSS mailing list](http://cnts.be/mailman/listinfo/knightsqrss_cnts.be) regarding mysterious signals in the 40m band.  They recognized it as a [QR Code](http://en.wikipedia.org/wiki/QR_Code) and tried decoding it with phones and such, but the signal wasn't strong enough above the noise to be automatically deciphered.

<dev class="center border medium">

![](https://swharden.com/static/2010/11/11/on5ex-odd.jpg)

</dev>

__That's the original spectrograph__ as captured by ON5EX in Belgium. It's a pretty good capture, it's just not great enough to be automatically decoded.  The first thing I did was pop it open in ImageJ, separate the channels, and use the most useful one (red, I believe).  When adjusted for brightness and contrast, I was already at a pretty good starting point.

<dev class="center border medium">

![](https://swharden.com/static/2010/11/11/better.jpg)

</dev>

__I tried using an automated decoder__ at this point (<http://zxing.org/w/decode.jspx>) but it wasn't able to recognize the QR code. I don't blame it! It was pretty rough.  I decided to manually recreate one, so I slapped the image into [InkScape](http://inkscape.org/), add a grid, and align the image with the grid.  From there, it was as easy as drawing a single grid-square-sized rectangle and copy/pasting it in all the right places.

<dev class="center border medium">

![](https://swharden.com/static/2010/11/11/building.jpg)

</dev>

__However problems came__ when working on those last few rows.  The static was pretty serious, so I tried a lot of different filters / adjustments.  One of the greatest benefits was when I stretched the image super-wide and performed a "rolling ball" background subtraction, then revered it to its original size. That greatly helped reduce the effect of the vertical striping, and let me visually determine where to place the last few squares by squinting a bit.

<dev class="center border medium">

![](https://swharden.com/static/2010/11/11/building3.jpg)

</dev>

__Once it was all done,__ I saved the output as orange, then later converted it to black and white for web-detection via [the ZXing Decoder](http://zxing.org/w/decode.jspx).

<dev class="center border medium">

![](https://swharden.com/static/2010/11/11/building2.jpg)

</dev>

__The final result:__

<dev class="center">

![](https://swharden.com/static/2010/11/11/finished.jpg)

</dev>

__which when decoded reads:__

`WELL DONE / F4GKA QSL PSE 73`

__Yay!__ I did it.  Although my call sign is AJ4VD, I'm spending the afternoon at the University of Florida Gator Amateur Radio Club station and am using their computers, so I might QSL as W4DFU.  Also, there's a lot to be said for ON5EX for capturing/reporting the QR code in the first place. After a bit of research, it turns out that F4GKA is one of the Knights! I should have known it =o)

Thanks for the fun challenge!