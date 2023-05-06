---
title: Prime Failure 1 Year in the Making
date: 2010-08-11 07:49:58
tags: ["python", "old"]
---

# Prime Failure 1 Year in the Making

__My expression is completely flat right now.__ I simply cannot believe I'm about to say what I'm preparing to say. I spent nearly a year cracking large prime numbers. In short, I took-on a project I called [_The Flowering N'th Prime Project_](http://swharden.dyndns.org:8081/), where I used my [SheevaPlug](http://en.wikipedia.org/wiki/SheevaPlug) to generate a list of every \[every millionth\] prime number. The current "golden standard" is [this page](http://primes.utm.edu/nthprime/) where one can look-up the N'th prime up to 1 trillion. My goal was to reach over 1 trillion, which I did just this morning! I was planning on being the only source on the web to allow lookups of prime numbers greater than 1 trillion.

<div class="text-center img-border">

[![](https://swharden.com/static/2010/08/11/flowering_primes_thumb.jpg)](https://swharden.com/static/2010/08/11/flowering_primes.png)

</div>

__However, when I went to look at the logs,__ I realized that the software had a small, fatal bug in it. Apparently every time the program restarted (which happened a few times over the months), although it resumed at its most recent prime number, it erased the previous entries. As a result, I have no logs below N=95 billion. In other words, although I reached my target this morning, it's completely irrelevant since I don't have all the previous data to prove it. I'm completely beside myself, and have no idea what I'm going to do. I can start from the beginning again, but that would take another YEAR. \[sigh\]

__So here's the screw-up.__ Apparently I coded everything correctly on paper, but due to my lack of experience I overlooked the potential for multiple appends to occur simultaneously. I can only assume that's what screwed it up, but I cannot be confident. Honestly, I still don't know specifically what the problem is. All in all, it looks good to me. Here is the relevant Python code.

```python
def add2log(c,v):
 f=open(logfile,'a')
 f.write("%d,%dn"%(c,v))
 f.close()

def resumeFromLog():
 f=open('log.txt')
 raw=f.readlines()[-1]
 f.close()
 return eval("["+raw+"]")
```

__For what it's worth,__ this is what remains of the log file:

```python
953238,28546251136703
953239,28546282140203
953240,28546313129849
...
1000772,30020181524029
1000773,30020212566353
1000774,30020243594723
```

