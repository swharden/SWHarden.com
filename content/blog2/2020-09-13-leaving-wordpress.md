---
title: Leaving WordPress
date: 2020-09-13 18:15:00
tags: ["php"]
---



**After fifteen years using WordPress, I'm leaving it for a simpler alternative: flat markdown files.** There were several reasons behind why I made the change. First, I was disappointed with how frequently I had to update WordPress (and upgrade my database) to stay current with security updates. Second, I didn't like how abstract post content was. The text of posts was stored in SQL tables and references to image URLs weren't easily accessible (posts point to content IDs, the URLs of which were stored in another table), and images and media were scattered all over the filesystem because the default image placement changed several times over the years. Finally I found that logging in to a web front-end just to write a post was a bit of a barrier that prevented me from writing more frequently. 

<div class="text-center">

![](https://swharden.com/static/2020/09/13/github.png)

</div>

**I have been [very active on GitHub](https://github.com/swharden) over the last few years** and used their platform to share my code instead of this website. Lots of code and notes belong in repositories there, yes, but sometimes I create neat things which would be better represented as one-off posts on my personal website. Some of my repositories have collected notes like these, so I look forward to migrating a lot of that content here. My hope is that the new system I put together will make it easier to share content by writing it in Markdown using the editors I'm already working in every day.

## Dynamic Markdown Parsing with PHP

**The system I'm using now is pretty simple.** Every post is a folder, and each folder contains a markdown file along with all of the images and files that post references. At the top of the markdown file is a little header which has information like title, date, and categories (tags). I use a PHP script route HTTP requests and if a requested folder lacks index.html but has index.md, I serve that using [Parsedown](https://github.com/erusev/parsedown) to convert it to HTML. I also add a few tweaks to do things like convert YouTube links to embedded videos and add syntax highlighting to code blocks. Backups are easy (I just zip the folder), and the website could be committed to source control. I'm leaning away from this because it's about 1GB (lots of images), but I'll consider it. Also, the URL is just the path to the folder.

**There's a clear path toward generating a static site.** If a folder lacks index.html, index.md is parsed and served. Switching to and from a static site can be achieved just by pre-converting all the markdown files to html and deleting them. I'll probably keep working on refining the PHP script until the conversions are reliably processing like I desire, then convert most of the old pages to static files. The cool thing about this method is that it lets me serve some posts statically but others dynamically.

<div class="text-center">

Wordpress (slow) | Markdown (fast)
---|---
<img src="https://swharden.com/static/2020/09/13/benchmark-slow.png"> | <img src="https://swharden.com/static/2020/09/13/benchmark-fast.png">

</div>

## Performing the Conversion

The conversion from WordPress to Markdown was semi-automated, but still labor-intensive. 

* I first dumped the database to a SQL file, parsed-out the content and metadata (url, title, date, and privacy status), then created the filesystem and markdown files. 

* I then had to manually inspect every markdown file and reformat it, converting inline HTML to markdown (mostly images, galleries, and divs for alignment formatting). In many cases code formatting was damaged over the years, so lots of my old code was run through an autoformatter.

* I also had to hunt-down the media (images, MP3s, ZIP files, etc.) for every post, copy it to the same folder, and update the URLs to be relative. This was especially hard for galleries which only point to meta content IDs (stored in a separate database table), and my database had gotten damaged somewhere along the way over the years so I really struggled to find the right content sometimes. 

* I also added tags to indicate categories, carefully reviewing content and code and marking posts as "old" if they contained out of date examples (lots of Python 2 code) or code that I deemed today to be of very poor quality. Part of me wanted to delete (hide) old posts with bad code, but I decided to leave them up. It's a reminder of how long I've worked in improving my craft, and my revulsion to code I wrote in the past is an indication of how much I've learned since.

* This process took me about 10 hours a day for 3 days in a row.

Along the way I had a few laughs at the ridiculousness of some of my old content. I think it's probably a good thing to encourage teenagers to have personal websites, but I also encourage professionals and employers not to give too much credence to ramblings written by a person decades ago that Google happens to remember. I didn't delete any content, but I marked most of the posts I made as a teenager as private and only exposed the ones that discuss this website.

## History of this Blog

After reviewing all of my posts I now have a really good understanding of the evolution of the technologies I used to serve my website over the years. Here's a summary of the major events:

* It started as a blog on GeoCities, with the [oldest surviving post](https://swharden.com/blog/2001-06-16-geocities-hardentechnologies-1) dating to June 2001. Back then adding content meant editing HTML files and using FTP to upload changes. 

* In 2002 I started hosting my website from a server at my house. Initially it was served with Windows/IIS using ASP for comments pages. On October 19, 2002 I switched to FreeBSD/Apache using PHP for comments pages.

* I started using the [Movable Type](https://en.wikipedia.org/wiki/Movable_Type) (a flat-file PHP-based CMS) on Aug 25, 2003.

* I migrated to [WordPress](https://en.wikipedia.org/wiki/WordPress) (a CMS that stored posts in a database) in 2005.

* In 2020 I converted all my posts to [Markdown](https://en.wikipedia.org/wiki/Markdown) using PHP to dynamically generate HTML (with an avenue to generate flat-file output).
