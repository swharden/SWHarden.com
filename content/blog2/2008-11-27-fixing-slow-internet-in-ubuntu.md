---
title: Fixing Slow Internet in Ubuntu
date: 2008-11-27 00:22:18
---



 __I recently swapped my two main PCs in my house.__  The "headless" (no monitor) media PC (whose job consists of downloading, storing, and playing movies) connected directly to my TV, and our standard desktop PC which my wife uses most of the time.  I decided to do the swap because the media PC was way nicer than our desktop PC, and since the media PC is just playing movies and downloading torrents, I figured the extra processing power / ram / video acceleration could be put to better use.  Anyhow, I decided (in both cases) to completely start fresh by wiping hard drives clean and reinstalling Ubuntu linux (I'm using 8.10 currently).  However, after the installation I noticed a peculiar problem.  I'll quote it to emphasize it...

>  Browsing the internet was very slow. When I'd click a link on a website, it would take several seconds before it seemed to even try to go to the next page. The same thing would happen if I manually typed-in a new website. I tried disabling IPv6 in firefox's about:config and in the /etc/init.d/aliases file, but it didn't help!

__The solution for me was simple, and since__ I spent a lot of time searching forums I know I'm not the only one with this problem.  Disabling IPv6 was suggested in 99% of similar posts.  My solution took a while to uncover, so I figured I'd write it here.  The basic problem is that my DHCP (auto-configured IP address) settings were screwed up, and my manually setting them I fixed the problem.  Here's what I did...

<div class="text-center img-border">

![](https://swharden.com/static/2008/11/27/dnsfix1.png)

</div>


 Start by right-clicking your network icon (wireless in my case) and selecting __connection information__

<div class="text-center img-border">

![](https://swharden.com/static/2008/11/27/dnsfix4.png)

</div>

Check out your current configuration.  __Is a local address (192.168.\*.\*) set for the primary DNS server?__  If so, that's your problem!  Note your secondary server.  We'll set it as your primary...

<div class="text-center img-border">

![](https://swharden.com/static/2008/11/27/dnsfix1.png)

</div>

Continue by right-clicking your network icon (wireless in my case) and selecting __edit connections\*. Open the tab corresponding to your internet connection (wired or wireless - wireless in my case), select your connection, and click ____Edit__

<div class="text-center img-border">

![](https://swharden.com/static/2008/11/27/dnsfix3.png)

</div>

Use this screen to __manually enter the information from the information screen you saw earlier, but making sure not to list any local IP addresses as the DNS servers.__  Save your settings, close the windows, and the problem should be immediately corrected.  Leave "search domains" blank, that's important too. Good luck!!!