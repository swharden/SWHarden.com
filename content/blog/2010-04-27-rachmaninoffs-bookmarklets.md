---
title: Rachmaninoff's Bookmarklets
date: 2010-04-27 22:09:04
---

# Rachmaninoff's Bookmarklets

__What a hodgepodge of topics my life has become.__ Yeah, dental school has been rough lately (finals week was last week), but I'm hanging in there and trying to be creative nonetheless. I've been dabbling in video motion tracking last week, and am contemplating attacking a project involving a lot of video shooting/editing and possibly some 3D work. It must have been almost 10 years since I last used 3D modeling software! I think it was 3D Studio Max back in the day they required a parallel port dongle and I had to spoof the hardware interface with a script so I could use a hacked version \[rolls eyes\]. I don't want to give anything away, so I'll leave it at that.

__I unknowingly stumbled into a new realm of web scripting__ when I searched for a way to skimp on my teacher evaluations. At the end of each course, many of our professors provide a point of extra credit for completing course evaluations. These things are lengthy, as you have to bubble choices (1-5) on about 30 topics per teacher, and some courses have 15+ teachers. It can take half an hour to click every bubble even for a single course, so I wrote a script to do it for me. [Tom Hayward](http://tomh.us) mentioned to me after-the-fact that such a script is called a [Bookmarklet](http://en.wikipedia.org/wiki/Bookmarklet). It's basically some fancy JavaScript with all the line breaks removed so it's a single line, and with all spaces replaced by %20 such that it's formatted as a URL. This JavaScript can be bookmarked as a URL, and when it's clicked the script is run. While it seems to me like a blatantly obvious security risk and a terrible idea, it seems to work on most browsers on most OSes. So, in the hope that this script inspires someone else to be creative, I'll post the source:

```js
javascript: var auto = {
    fillerup: function () {
        var all_inputs = document.getElementsByTagName('input');
        var all_selects = document.getElementsByTagName('select');
        var all_textareas = document.getElementsByTagName('textarea');

        for (var i = 0, max = all_selects.length; i < max; i++) {
            var sel = all_selects[i];
            if (sel.selectedIndex != -1 && sel.options[sel.selectedIndex].value) { continue; }
            var howmany = 1;
            if (sel.type == 'select-multiple') {
                var howmany = 1 + this.getRand(sel.options.length - 1);
            }
            for (var j = 0; j < howmany; j++) {
                var index = this.getRand(sel.options.length - 1);
                sel.options[index].selected = 'selected';
            }
        }

        for (var i = 0, max = all_inputs.length; i < max; i++) {
            var inp = all_inputs[i];
            var type = inp.getAttribute('type');
            if (!type) { type = 'text'; }
            if (type == 'radio') {
                var to_update = true;
                var name = inp.name;
                var input_array = inp.form.elements[inp.name];
                for (var j = 0; j < input_array.length; j++) {
                    if (input_array[j].checked) {
                        to_update = false; continue;
                    }
                }
                if (to_update) {
                    var index = this.getRand(input_array.length - 1);
                    input_array[index].setAttribute('checked', 'checked');
                }
            }
        }
    }
    , getRand: function (count) { return count * Math.random()); }
}; auto.fillerup()
```

__My microchips arrived in the mail!__ I'm so excited. It's just in time too, I'm about to build my first \[hopefully\] functional non-bread-boarded single-chip transmitter (with a single-chip preamplifier) QRSS radio beacon -err, manned experimental propagation transmitter. These chips are smaller than the ATTiny2313's I'm used to working with, and will be so awesome to work with surface-mount size. I wonder if I trust myself to hand-drill a circuit board for such a SMT microchip using copper-plated PC board? Perhaps with a dental drill? ha! Finally a use for that blasted thing.

<div class="text-center img-small">

![](https://swharden.com/static/2010/04/27/attiny44a.jpg)

</div>

__Work on my single-chip radio transmitter has stalled.__ On one hand I have almost all the equipment I need at my apartment (boxes of components, a dremel, a drill press, an excellent soldering station, copious amounts of work space, boxes of tools, and many different types of wire), but I have no high-quality radio to receive any transmissions my device makes at the target frequency (10.140 MHz). However, a radio shack filled with many gorgeous radios exists on the other side of town at the top of Shands hospital! Yeah, I could work on the project using a frequency I could measure with my Century 21 direct-conversion radio (14 MHz or 7 MHz), but it doesn't seem as exciting doing it this way. I fear I'll build a beautiful 7 MHz transmitter which doesn't perform at 10 MHz. Tonight I realized I left my prototype transmitter bread-boarded at the station, and here I sit with nothing to work on (hence my writing). I've been dabbling in non-productive projects over the last few weeks - I think it's time for me to wake up, shape up, and get back to working on something significant! With that, I'm outta here. Time to read some datasheets.

