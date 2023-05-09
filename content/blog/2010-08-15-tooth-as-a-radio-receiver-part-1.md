---
title: Tooth as a Radio Receiver?
date: 2010-08-15 12:13:39
tags: ["obsolete"]
---



__We've all heard the urban legend where someone's tooth filling picks up radio signals__, some versions claim AM radio stations' music is heard, others that wartime Morse code is heard. Is this really possible? Well, as a dental student and an electrical engineering / RF engineering enthusiast, I can think of no one better prepared to put this myth to the test! Yeah, __I'm going to put my money where my mouth is.__ (zing!) [Myth Busters attempted to replicate this](http://www.youtube.com/watch?v=OwfAyo4twqg), but they concluded it was "busted", however I think they were going about it the wrong way. Let's back up! Here's a quote from Lucille Ball who is often accredited for originating this urban legend:

<blockquote class="wp-block-quote"><p>One night I came into the Valley over Coldwater Canyon, and I heard music. I reached down to turn the radio off, and it wasn't on. The music kept getting louder and louder, and then I realized it was coming from my mouth. I even recognized the tune. My mouth was humming and thumping with the drumbeat, and I thought I was losing my mind. I thought, What the hell is this? Then it started to subside. I got home and went to bed, not sure if I should tell anybody what had happened because they would think I was crazy.<br/>--Lucille Ball</p></blockquote>

__It was noted that Lucy recently had several temporary lead fillings__ installed in her teeth which caused this unique phenomenon. Let's assume this isn't a made-up story. If this were possible, what would cause it? Without going into detail as to how (whether by [galvanic corrosion](http://en.wikipedia.org/wiki/Galvanic_corrosion) or other means), we'd have to assume that RF could be absorbed by the filling (whatever type it was), and turned into electrical activity. This electrical activity was either transferred directly to the nerves (felt as tingly electric shocks, which I feel isn't likely) or converted into mechanical energy (creating vibrations which would be hears as sound waves). The [piezoelectric effect](http://en.wikipedia.org/wiki/Piezoelectricity) may be one method where an electrical signal could produce these vibrations. Many small speakers are called [piezoelectric speakers](http://en.wikipedia.org/wiki/Loudspeaker#Piezoelectric_speakers), because they have a small crystal in them (usually quartz) which changes its dimension as electricity is applied to the crystal, creating mechanical vibrations (turned into sound waves). [Tooth enamel](http://en.wikipedia.org/wiki/Tooth_enamel) is 98% hydroxyapatite crystal - I wonder if it could be coaxed to vibrate similarly to quartz? There's only one way to find out!

<div class="text-center img-border">

![](https://swharden.com/static/2010/08/15/IMG_5554.jpg)

</div>

__First, I start with a jar of teeth.__ Yeah, this is mine. Don't ask how I got it! They're all nasty as heck, and require sterilization before I will touch them without gloves. There are many advantages of spending every day in a medical setting, one of which is easy access to an autoclave! After picking a tooth which I think will have a lot of enamel I can isolate, I sterilized it.

<div class="text-center img-border">

![](https://swharden.com/static/2010/08/15/IMG_5562.jpg)

</div>

__I started by sectioning the tooth mesio-distally__ using a slow-speed air-driven handpiece and a \#2 round burr. As I cut through the enamel, you can see the darker, yellowish dentin layer showing through.

<div class="text-center img-border">

![](https://swharden.com/static/2010/08/15/IMG_5563.jpg)

</div>

__This is my test subject.__ It's a maxillary left first premolar. My goal is to isolate only enamel from this tooth, take it home and experiment with it.

<div class="text-center img-border">

![](https://swharden.com/static/2010/08/15/IMG_5567.jpg)

</div>

__Although dentin is crystal too, it's about half organic matter and I feel it's less likely to exhibit significant piezoelectric effect.__ Therefore, I'm going to try to eliminate all the dentin attached to the enamel. The image above shows some yellow dentin remaining near the center of the enamel. The lingual surface of the tooth has already been removed, leaving a thin shell of the facial surface. I'll try to be more aggressive taking out more dentin...

__Oops!__ Enamel is strong, but brittle. This brittleness is exacerbated by the process of autoclaving. While trying to drill away dentin, a large amount of the enamel chipped off, but I think it's enough to use for my experiment.

__Here's what I have to work with.__ It's pretty thick - I imagine if I make it thinner still, it will have a better chance of vibrating. Either way, it's a start! The view above shows the facial aspect of the tooth - just think, this was probably on someone's mouth for 50 years, viewed by thousands of people. Now it's in my hands, and I'm about to turn it into a radio. I love my life.

__From the other side, you can see enamel gets thicker toward one side of the tooth.__ My plan once I go home tonight (after I spend the afternoon in oral surgery, possibly extracting some teeth) is to gator-clip leads onto different sections of this tooth and run current through it. I'm thinking half a watt of 28MHz (since I have that transmitter I made yesterday still on my workbench), amplitude-modulated to produce a 300Hz tone. If my piezoelectric tooth enamel theory holds water, the tooth will vibrate at 300Hz when I do this. I can't wait to try it out!

<div class="text-center img-border">

![](https://swharden.com/static/2010/08/15/IMG_5570.jpg)

![](https://swharden.com/static/2010/08/15/IMG_5573.jpg)

![](https://swharden.com/static/2010/08/15/IMG_5577.jpg)

![](https://swharden.com/static/2010/08/15/IMG_5578.jpg)

![](https://swharden.com/static/2010/08/15/IMG_5583.jpg)

</div>

### Update - 3pm 8/15/2011

__We had a cancellation in the student oral surgery clinic__, so with my unexpected free time I decided to prepare another tooth and attempt to isolate a larger, thinner selection of enamel. I chose a maxillary left lateral incisor this time, and carefully drilled it down until it was only enamel, and pretty thin at that. Take a look!

__I don't have my calipers on me,__ so I can only estimate its thickness to be between 500 and 1000 microns. It's likely still too thick to vibrate extremely well, but it will be a good starting point. We'll see how it fairs when I apply some RF current through it tonight at home!

__To add credibility to this story,__ here is the official description of an episode from the [Gilligan's Island Episode List](http://en.wikipedia.org/wiki/List_of_Gilligan's_Island_episodes) wikipedia page:

<blockquote class="wp-block-quote"><p>Gilligan's mouth becomes a radio when a filling in a tooth is knocked loose. Just in time too, as the regular radio is broken and a monster typhoon is on its way.<br/><i>"Hi-Fi Gilligan", Season 2, Episode 10, November 25, 1965</i></p></blockquote>

### Update - 9:50 pm 8/15/2011

__I'm starting to feel like I might have been played.__ I tried sending different types of current through flakes of enamel and nothing I did seemed to make it vibrate measurably. I tried audio level 5V square waves, audio level modulated RF 30PPV sine waves, and a few other things at all locations on the enamel, but I couldn't get it to produce sound. I think it's either (a) not thin enough to vibrate freely, (b) not highly piezoelectric, (c) not fed the correct frequency, for which I really need a RF sweep generator, or (d) simply not possible and I'm chasing a ghost on this one... If someone has any ideas of what to try, I'd appreciate it. If I can't make it vibrate from electrical current, I'll never make progress toward proving the "tooth radio" story, so I guess it ends here for now. If you have any ideas, feel free to share them with me! I'll probably move on to bigger, better things now...

__Second wind: I'm starting to think that I'm beginning this project too complexly.__ I know a quartz peizoelectric speaker works. I should probably start by replicating this, using a fragment of enamel rather than quartz. Also, most of the volume from a peizo speaker comes from its resonant chamber. Technically, _this could be vibrating in front of me right now and I wouldn't be able to hear or see it!_ I should find a crystal peizo speaker, replace the quartz with enamel, and start from there...

### Update - 10:35 pm 8/15/2011

__SUCCESS!__ I can't believe I gave up that easily! I'd actually started moving onto another project, when I had an idea and revisited this one. So what if the piezoelectric vibration experiment didn't work? Is it possible that RF could be turned into electrical signals that could be sensed by the mouth? Two dissimilar metals in contact may form a [P-N junction](http://en.wikipedia.org/wiki/P-n_junction), the fundamental unit of semiconductors. A simple diode would take audio-level amplitude modulated radio frequency signal and act as an envelope detector, producing electrical output corresponding to the audio used to modulate the carrier signal. A simple diode should do the same thing. Therefore, if a diode in my mouth produces a tingle of electricity upon RF exposure, and if I can figure out which dental materials are [P-type](http://en.wikipedia.org/wiki/P-type_semiconductor) and [N-type](http://en.wikipedia.org/wiki/N-type_semiconductor), I can replicate this! First test, diode.

<div class="text-center img-border">

![](https://swharden.com/static/2010/08/15/DSCN1732.jpg)

</div>

__There's a simple [1N914 diode](http://www.fairchildsemi.com/ds/1N/1N914.pdf) with a tooth beside it for scale reference.__ A diode, when exposed to RF, acts a bit like a half-wave rectifier, the body acts as a lowpass filter, and the result is a small electrical current delivered upon RF exposure. The black stripe indicates the + side of the diode. I place this on my tongue, touch the other end with my hand and and let's try keying up a transmitter...

<div class="text-center img-border">

![](https://swharden.com/static/2010/08/15/DSCN1733.jpg)

</div>

__ZAP!__ Even though I'm not holding the radio (as evidenced by a black/Mexican hand with nail polish), every time my wife presses the transmit button I feel a slight tingle in my mouth. This is a 5W radio a few feet away. I couldn't even imagine what a 50,000 watt AM radio station would feel like! Now, if I can just figure out which dental materials would act like a diode, I can construct this dental device in a human tooth and measure the current produced! If I'm confident it's sterilized, I guess I can put it in my mouth and see if I can feel it tingle. eww! I'll cross that bridge when I come to it. Time for more research!

#### _TO BE CONTINUED..._

