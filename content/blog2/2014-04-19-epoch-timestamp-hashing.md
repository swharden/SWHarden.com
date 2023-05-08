---
title: Epoch Timestamp Hashing
date: 2014-04-19 08:31:53
tags: ["python", "obsolete"]
---

# Epoch Timestamp Hashing

__I was recently presented with the need to rename a folder of images based on a timestamp.__ This way, I can keep saving new files in that folder with overlapping filenames (i.e., <span style="color: #339966;">01.jpg</span>, <span style="color: #339966;">02.jpg</span>, <span style="color: #339966;">03.jpg</span>, etc.), and every time I run this script all images are prepended with a timestamp. I still want the files to be sorted alphabetically, which is why an alphabetical timestamp (rather than a random hash) is preferred.

*   At first I considered a long date such as <span style="color: #339966;">2014-04-19-01.jpg</span>, but that adds so much text!...also, it doesn't include time of day.
*   If I include time of day, it becomes <span style="color: #339966;">2014-04-19-09-16-23-01.jpg</span>
*   If I eliminate dashes to shorten it, it becomes hard to read, but might work <span style="color: #339966;">140419091623-01.jpg</span>
*   If I use [Unix Epoch](http://en.wikipedia.org/wiki/Unix_time) time, it becomes <span style="color: #339966;">1397912944-01.jpg</span>

__The result I came up with uses base conversion and a string table of numbers and letters (in alphabetical order) to create a second-respecting timestamp hash using an arbitrary number of characters.__ For simplicity, I used 36 characters: 0-9, and a-z. I then wrote two functions to perform arbitrary base conversion, pulling characters from the hash. Although I could have nearly doubled my available characters by including the full ASCII table, respecting capitalization, I decided to keep it simple. The scheme goes like this:

*   Determine the date / time: <span style="color: #339966;">19-Apr-2014 13:08:55</span>
*   Create an integer of [Unix Epoch](http://en.wikipedia.org/wiki/Unix_time) time (seconds past Jan 1, 1970):  <span style="color: #339966;">1397912935</span>
*   Do a base conversion from a character list: <span style="color: #339966;">n4a4iv</span>
*   My file name now becomes <span style="color: #888888;">n4a4iv-01.jpg</span> - I can accept this!_and when I sort the folder alphabetically, they're in order by the timestamp_

__I can now represent any modern time, down to the second, with 6 characters.__ Here's some example output:

```python
19-Apr-2014 13:08:55 <-> 1397912935 <-> n4a4iv
19-Apr-2014 13:08:56 <-> 1397912936 <-> n4a4iw
19-Apr-2014 13:08:57 <-> 1397912937 <-> n4a4ix
19-Apr-2014 13:08:58 <-> 1397912938 <-> n4a4iy
19-Apr-2014 13:08:59 <-> 1397912939 <-> n4a4iz
19-Apr-2014 13:09:00 <-> 1397912940 <-> n4a4j0
19-Apr-2014 13:09:01 <-> 1397912941 <-> n4a4j1
19-Apr-2014 13:09:02 <-> 1397912942 <-> n4a4j2
19-Apr-2014 13:09:03 <-> 1397912943 <-> n4a4j3
19-Apr-2014 13:09:04 <-> 1397912944 <-> n4a4j4
```

__Interestingly, if I change my hash characters away from the list of 36 alphanumerics and replace it with just 0 and 1, I can encode/decode the date in binary:__

```python
19-Apr-2014 13:27:28 <-> 1397914048 <-> 1010011010100100111100111000000
19-Apr-2014 13:27:29 <-> 1397914049 <-> 1010011010100100111100111000001
19-Apr-2014 13:27:30 <-> 1397914050 <-> 1010011010100100111100111000010
19-Apr-2014 13:27:31 <-> 1397914051 <-> 1010011010100100111100111000011
19-Apr-2014 13:27:32 <-> 1397914052 <-> 1010011010100100111100111000100
19-Apr-2014 13:27:33 <-> 1397914053 <-> 1010011010100100111100111000101
19-Apr-2014 13:27:34 <-> 1397914054 <-> 1010011010100100111100111000110
19-Apr-2014 13:27:35 <-> 1397914055 <-> 1010011010100100111100111000111
19-Apr-2014 13:27:36 <-> 1397914056 <-> 1010011010100100111100111001000
19-Apr-2014 13:27:37 <-> 1397914057 <-> 1010011010100100111100111001001
```

__Here's the code to generate / decode Unix epoch timestamps in Python:__

```python
hashchars='0123456789abcdefghijklmnopqrstuvwxyz'
#hashchars='01' #for binary

def epochToHash(n):
  hash=''
  while n>0:
    hash = hashchars[int(n % len(hashchars))] + hash
    n = int(n / len(hashchars))
  return hash

def epochFromHash(s):
  s=s[::-1]
  epoch=0
  for pos in range(len(s)):
    epoch+=hashchars.find(s[pos])*(len(hashchars)**pos)
  return epoch

import time
t=int(time.time())
for i in range(10):
  t=t+1
  print(time.strftime("%d-%b-%Y %H:%M:%S", time.gmtime(t)),
              "<->", t,"<->",epochToHash(t))
```
