---
title: Analyzing my Writings with Python
date: 2009-01-29 18:46:22
tags: ["python", "obsolete"]
---



__I had some free time in lab today__ (between steps while of an immunohistochemistry experiment) so I decided to further investigate the field of bioinformatics. I was curious if it may be worth seeking a PhD in bioinformatics if I don't get into dental school. UCF offers a PhD in bioinformatics but it's a new and small department (I think there are only 4 faculty). A degree in bioinformatics combines molecular biology (DNA, proteins, etc), computer science (programming), and statistics.

__I came across a paper today__: [Structural Alignment of Pseudoknotted RNA](http://cseweb.ucsd.edu/users/shzhang/app/RECOMB2005_pseudoknot.pdf) which is a good example of the practice of bioinformatics. Think about what goes on in a cell... the sequence of a gene (a short region of DNA) is copied (letter-by-letter) onto an RNA molecule. The RNA molecule is later read by an enzyme (called a ribosome) and converted into a protein based on its sequence. (This process is the central dogma of molecular biology) Traditionally, it was believed that RNA molecules' only function was to copy gene sequences from DNA to ribosomes, but recently (the last several years) it was discovered that some small RNA molecules are never read and turned into proteins, but rather serve their own unique functions! For example, some RNA molecules (siRNAs) can actually turn genes on and off, and have been associated with cancer development and other immune diseases. Given the human genome (the ~3 billion letter long sequence all of our DNA), how can we determine what regions form these functional RNA molecules which don't get converted into proteins? The paper I mentioned earlier addresses this. An algorithm was developed and used to test regions of DNA and predict its probability of forming small RNA molecules. Spikes in this trace (figure 7 of the paper) represent areas of the DNA which are likely to form these RNA molecules. (Is this useful? What if you were to compare these results between normal person and someone with cancer?)

__After reading the article__ I considered how similar my current programming projects are with this one (e.g., my recent DIY ECG projects). The paper shows a trace of score (likelihood that a region of DNA forms an RNA molecule) where peaks represent likely locations of RNA formation. Just generate the trace, determine the positions of the peaks, and you're golden. How similar is this to the work I've been doing with my homemade ECG machine, where I perform signal analysis to eliminate electrical noise and then analyze the resulting trace to isolate and identify peaks corresponding to heartbeats?

__I got the itch to write my own string-analysis program.__ It reads the content of my website (exported from a SQL query), splits it up by date, and analyzes it. Ultimately I want to track the usage of certain words, but for now I wrote a script which plots the number of words I wrote.

<div class="text-center">

![](https://swharden.com/static/2009/01/29/blog_words.png)

</div>

__Pretty cool huh? __Check out all those spikes between 2004 and 2005! Not only are they numerous (meaning many posts), but they're also high (meaning many words per post). As you can see by the top trace, the most significant contribution to my site occurred during this time. So, let's zoom in on it.

<div class="text-center">

![](https://swharden.com/static/2009/01/29/blog_words_zoom.png)

</div>

__Here is the code__ I used to produce this image.

```python
"""Convert SQL backups of my WordPress blog into charts"""

import datetime, pylab, numpy

class blogChrono():
    baseUrl="https://swharden.com/blog"
    posts=[]
    dates=[]
    def __init__(self,fname):
        self.fname=fname
        self.load()
    def load(self):
        print "loading [%s]..."%self.fname,
        f=open(self.fname)
        raw=f.readlines()
        f.close()
        for line in raw:
            if "INSERT INTO" in line
            and';' in line[-2:-1]
            and " 'post'," in line[-20:-1]:
                post={}
                line=line.split("VALUES(",1)[1][:-3]
                line=line.replace(', NULL',', None')
                line=line.replace(", '',",", None,")
                line=line.replace("''","")
                c= line.split(',',4)[4][::-1]
                c= c.split(" ,",21)
                text=c[-1]
                text=text[::-1]
                text=text[2:-1]
                text=text.replace('"""','###')
                line=line.replace(text,'blogtext')
                line=line.replace(', ,',', None,')
                line=eval("["+line+"]")
                if len(line[4])&gt;len('blogtext'):
                    x=str(line[4].split(', '))[2:-2]
                    raw=str(line)
                    raw=raw.replace(line[4],x)
                    line=eval(raw)
                post["id"]=int(line[0])
                post["date"]=datetime.datetime.strptime(line[2],
                                                        "%Y-%m-%d %H:%M:%S")
                post["text"]=eval('"""'+text+' """')
                post["title"]=line[5]
                post["url"]=line[21]
                post["comm"]=int(line[25])
                post["words"]=post["text"].count(" ")
                self.dates.append(post["date"])
                self.posts.append(post)
        self.dates.sort()
        d=self.dates[:]
        i,newposts=0,[]
        while len(self.posts)&gt;0:
            die=min(self.dates)
            for post in self.posts:
                if post["date"]==die:
                    self.dates.remove(die)
                    newposts.append(post)
                    self.posts.remove(post)
        self.posts,self.dates=newposts,d
        print "read %d posts!n"%len(self.posts)

#d=blogChrono('sml.sql')
d=blogChrono('test.sql')

fig=pylab.figure(figsize=(7,5))
dates,lengths,words,ltot,wtot=[],[],[],[0],[0]
for post in d.posts:
    dates.append(post["date"])
    lengths.append(len(post["text"]))
    ltot.append(ltot[-1]+lengths[-1])
    words.append(post["words"])
    wtot.append(wtot[-1]+words[-1])
ltot,wtot=ltot[1:],wtot[1:]

pylab.subplot(211)
#pylab.plot(dates,numpy.array(ltot)/(10.0**6),label="letters")
pylab.plot(dates,numpy.array(wtot)/(10.0**3),label="words")
pylab.ylabel("Thousand")
pylab.title("Total Blogged Words")
pylab.grid(alpha=.2)
#pylab.legend()
fig.autofmt_xdate()
pylab.subplot(212,sharex=pylab.subplot(211))
pylab.bar(dates,numpy.array(words)/(10.0**3))
pylab.title("Words Per Entry")
pylab.ylabel("Thousand")
pylab.xlabel("Date")
pylab.grid(alpha=.2)
#pylab.axis([min(d.dates),max(d.dates),None,20])
fig.autofmt_xdate()
pylab.subplots_adjust(left=.1,bottom=.13,right=.98,top=.92,hspace=.25)
width=675
pylab.savefig('out.png',dpi=675/7)
pylab.show()

print "DONE"
```

__I wrote a Python script to analyze the word frequency __of the blogs in my website (extracted from an SQL query WordPress backup file) for frequency, then I took the list to [Wordie](http://www.wordle.net/) and created a word jumble. Neat, huh?

```python
import datetime, pylab, numpy
f=open('dump.txt')
body=f.read()
f.close()
body=body.lower()
body=body.split(" ")
tot=float(len(body))
words={}
for word in body:
    for i in word:
        if 65&lt; =ord(i)&lt;=90 or 97&lt;=ord(i)&lt;=122: pass
        else: word=None
    if word:
        if not word in words:words[word]=0
        words[word]=words[word]+1
data=[]
for word in words: data.append([words[word],word])
data.sort()
data.reverse()
out= "&lt;b&gt;Out of %d words...n"%tot
xs=[]
for i in range(1000):
    d=data[i]
    out += '&lt;b&gt;"%s"&lt;/b&gt; ranks #%d used &lt;b&gt;%d&lt;/b&gt; times (%.05f%%)
n'%
                (d[1],i+1,d[0],d[0]/tot)
f=open("dump.html",'w')
f.write(out)
f.close()
print "DONE"&lt;/b&gt;
```

<div class="text-center">

![](https://swharden.com/static/2009/01/29/wordie2.png)

</div>

