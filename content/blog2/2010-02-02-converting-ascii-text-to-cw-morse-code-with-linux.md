---
title: Convert Text to CW Morse Code with Linux
date: 2010-02-02 10:58:54
tags: ["amateur radio", "python", "old"]
---

# Convert Text to CW Morse Code with Linux

__I wanted a way to have a bunch of Morse code mp3s on my mp3 player (with a WPM/speed that I decide__ and I found an easy way to do it with Linux. Rather than downloading existing mp3s of boring text, I wanted to be able to turn ANY text into Morse code, so I could copy something interesting (perhaps the news? hackaday? bash.org?). It's a little devious, but my plan is to practice copying Morse code during class when lectures become monotonous. \[The guy who teaches about infectious diseases is the most boring person I ever met, I learn nothing from class, and on top of that he doesn't allow laptops to be out!\] So, here's what I did in case it helps anyone else out there...

### Step 1: Get the Required Programs

Make sure you have installed [Python](http://www.Python.org), [cwtext](http://cwtext.sourceforge.net/), and [lame](http://lame.sourceforge.net/). Now you're ready to roll!

### Step 2: Prepare the Text to Encode

I went to Wikipedia and copy/pasted an ENTIRE article into a text file called in.txt. Don't worry about special characters (such as " and \* and \#), we'll fix them with the following python script.

```python
import os
import time
f = open("out.txt")
raw = f.read()
f.close()

cmd = """echo "TEST" | cwpcm -w 7 | """
cmd += """lame -r -m m -b 8 --resample 8 -q9 - - > text.mp3"""

i = 0
for chunk in raw.split("n")[5:]:
    if chunk.count(" ") > 50:
        i += 1
        print "nnfile", i, chunk.count(" "), "wordsn"
        do = cmd.replace("TEST", chunk).replace("text", "%02d" % i)
        print "running:", do,
        time.sleep(1)
        print "nnSTART ...",
        os.system(do)
        print "DONE"
```

### Step 3: Generate Morse Code Audio

There should be a new file, out.txt, which is cleaned-up nicely. Run the following script to turn every paragraph of text with more than 50 words into an mp3 file...

```python
import os
f = open("out.txt")
raw = f.read()
f.close()
cmd = """echo "TEST" | cwpcm -w 13 | sox -r 44k -u -b 8 -t raw - text.wav"""
cmd += """; lame --preset phone text.wav text.mp3; rm text.wav"""
i = 0
for chunk in raw.split("n")[5:]:
    if chunk.count(" ") > 50:
        i += 1
        print i, chunk.count(" "), "words"
        os.system(cmd.replace("TEST", chunk).replace("text", "%02d" % i))
```

Now you should have a directory filled with mp3 files which you can skip through (or shuffle!) using your handy dandy mp3 player. Note that "-w 13" means 13 WPM (words per minute). Simply change that number to change the speed.

Good luck with your CW practice!

