---
title: Removing Textile Markup From Wordpress Entries
date: 2009-05-15 17:56:32
tags: ["old"]
---

# Removing Textile Markup From Wordpress Entries

__I realized that the C code from yesterday wasn't showing-up properly__ because of [textile](http://wordpress.org/tags/textile), a rapid, inline, tag-based formatting system.  While it's fun and convenient to use, it's not always practical.  The problem I was having was that in C code, variable names (such as _delay_) were becoming irrevocably italicized, and nothing I did could prevent textile from ignoring code while styling text.  The kicker is that I couldn't disable it easily, because I've been writing in this style for __over four years!__  I decided that the time was now to put my mad Python skills to the test and write code to handle the conversion from textile-format to raw HTML.
__I accomplished this feat__ in a number of steps.  Yeah, I could have done hours of research to find a "faster way", but it simply wouldn't have been as creative.  In a nutshell, I backed-up the SQL database using [PHPMyAdmin](http://en.wikipedia.org/wiki/PhpMyAdmin) to a single "x.sql" file.  I then wrote a pythons script to parse this [massive] file and output "o.sql", the same data but with all of the textile tags I commonly used replaced by their HTML equivalent.  It's not 100% perfect, but it's 99.999% perfect.  I'll accept that.  The output?  You're viewing it!  Here's the code I used to do it:

```python
## This Python script removes *SOME* textile formatting from Wordpress
## backups in plain text SQL format (dumped from PHP MyAdmin). Specifically,
## it corrects bold and itallic fonts and corrects links. It should be easy
## to expand if you need to do something else with it.

infile = 'x.sql'

replacements=   ["r"," "],["n"," n "],["*:","* :"],["_:","_ :"],
                ["n","&lt;br&gt;n"],["&gt;*","&gt; *"],["*&lt; ","* &lt;"],
                ["&gt;_","&gt; _"],["_&lt; ","_ &lt;"],
                [" *"," &lt;b&gt;"],["* "," "],[" _"," &lt;i&gt;"],["_ ","&lt;/i&gt; "]
                #These are the easy replacements

def fixLinks(line):
    ## replace ["links":URL] with [&lt;a href="https://swharden.com/static/2009/05/15/URL"&gt;links&lt;/a&gt;]. ##
    words = line.split(" ")
    for i in range(len(words)):
        word = words[i]
        if '":' in word:
            upto=1
            while (word.count('"')&amp;lt;2):
                word = words[i-upto]+" "+word
                upto+=1
            word_orig = word
            extra=""
            word = word.split('":')
            word[0]=word[0][1:]
            for char in ".),'":
                if word[1][-1]==char: extra=char
            if len(extra)&gt;0: word[1]=word[1][:-1]
            word_new='&lt;a href="https://swharden.com/static/2009/05/15/%s"&gt;%s&lt;/a&gt;'%(word[1],word[0])+extra
            line=line.replace(word_orig,word_new)
    return line

def stripTextile(orig):
    ## Handle the replacements and link fixing for each line. ##
    if not orig.count("', '") == 13: return orig #non-normal post
    line=orig
    temp = line.split
    line = line.split("', '",5)[2]
    if len(line)&amp;lt;10:return orig #non-normal post
    origline = line
    line = " "+line
    for replacement in replacements:
        line = line.replace(replacement[0],replacement[1])
    line=fixLinks(line)
    line = orig.replace(origline,line)
    return line

f=open(infile)
raw=f.readlines()
f.close
posts=0
for raw_i in range(len(raw)):
    if raw[raw_i][:11]=="INSERT INTO":
        if "wp_posts" in raw[raw_i]: #if it's a post, handle it!
            posts+=1
            print "on post",posts
            raw[raw_i]=stripTextile(raw[raw_i])

print "WRITING..."
out = ""
for line in raw:
    out+=line
f=open('o.sql','w')
f.write(out)
f.close()

```

__I certainly held my breath while the thing ran.__  As I previously mentioned, this thing modified SQL tables.  Therefore, when I uploaded the "corrected" versions, I kept breaking the site until  I got all the bugs worked out.  Here's an image from earlier today when my site was totally dead (0 blog posts)

<div class="text-center img-border">

[![](https://swharden.com/static/2009/05/15/hostingwork_thumb.jpg)](https://swharden.com/static/2009/05/15/hostingwork.jpg)

</div>