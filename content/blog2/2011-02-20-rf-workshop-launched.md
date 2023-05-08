---
title: RF Workshop Launched
date: 2011-02-20 00:13:37
tags: ["circuit", "amateur radio", "obsolete"]
---

# RF Workshop Launched

__The _Radio Active Workshop_ kicked off a couple weeks ago__ in the engineering department of the University of Florida led by yours truly! Jimmy Lin (an aerospace engineering graduate student) set up the group, and together we're trying to provide an open environment for engineering students (or anyone who's interested) to meet, share ideas, and get some practical hands-on experience building stuff. We made gave it a radio theme so it meshes nicely with the [Gator Amateur Radio Club](http://www.GatorRadio.org). I brought a lot of my equipment from home (components, o-scope, tools, etc) and we all started building right away!


<div class="text-center img-border">

![](https://swharden.com/static/2011/02/20/rag1.jpg)

</div>

__This was the first time__ many students worked on copper boards, as most of them spend their time working with breadboards and/or computer simulations. For a couple it was the first time picking up a soldering iron (how exciting!). My goal is to start everybody off building the same thing (an ultra-simple multi band radio receiver) with a modular design, then turn everyone loose to modify it to their liking. There are a lot of possibilities, from computer control, micro-controller interaction, frequency measurement, stability testing and compensation, audio processing, and of course making it transmit (which should be trivial!). I'm very excited, but still a bit cautious - I think it's too early to tell whether or not this will be a worthwhile success, or misdirected enthusiasm! I'll give it my all and see where it goes...

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/20/rag2.jpg)

</div>

__One thing that struck me as a challenge__ is the difference in levels of experience of the group. We have everything from undergraduate freshmen to experienced graduate students all working on the same project. You can imagine how each of us look at the same circuit differently! I hope that some of the more experienced students can help those less experienced (I fit in that group!) gain some knowledge and come up with some ideas to improve the project.

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/20/rag3.jpg)

</div>

__There are many other projects__ which would be fun to work on! A cheap and simple frequency counter would be a fun project, especially for the micro-controller gurus out there. Then there's the enclosure problem - I hope to get a mechanical engineering student to help me out in that department. It would be nice to have a design for an inexpensive HF receiver that can be produced in a small quantity and made available for check out from school radio clubs to let new hams (or those interested in radio) the ability to listen to HF, learn CW, or decode some digital signals!  When I got home my wife and I were talking about it and she gave me a hard time for my devices looking so sloppy, specifically commenting on my soldering. Can you believe it? A nursing student ripping on a dental student's soldering skills -- what a funny life I stumbled into =o)  Anyhow, I challenged her to make a circuit (switch-controlled LED with filtering capacitor for smooth fade-off) look pretty, and she did! Although it's not pictured, I got a snapshot of her building it...


<div class="text-center img-border">

![](https://swharden.com/static/2011/02/20/angelina_harden_2.jpg)

</div>

__Details of the board__ won't be published quite yet. I wish to improve it and finalize the design. A PCB would be nice, but I'm very very very hesitant to
go in that direction. PCBs imply "finished" circuits, and I don't want to give the impression that any circuit I design shouldn't be tinkered with to try to improve it! We'll figure that out as it goes. Here are a couple photos of the modules I'm providing as a starting point for the students to make. So far they've only made the center board, and next week I imagine we'll start on (maybe even complete) the rest...


<div class="text-center img-border">

![](https://swharden.com/static/2011/02/20/DSCN1256.jpg)
![](https://swharden.com/static/2011/02/20/DSCN1251.jpg)

</div>

__And of course a video__ - it's a bit on the long and redundant side, but it clearly demonstrates what we're working on at the workshop. Again, note that this board is purely for educational purposes, and the amount of exposed copper in the critical sections (antenna/oscillator) obviously needs to be minimized in more finalized designs.

{{<youtube 6rSC0JMR0fs>}}

__Here's my most recent schematic:__

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/20/sa612_rx.jpg)

</div>

WARNING: This schematic has a couple problems. First and foremost, pins 2 and 3 are *ACTUALLY* pins 1 and 2 (antenna). Pin 3 should be GROUDNED.  Also, the series capacitor between the two ICs was replaced by a 22uF capacitor.