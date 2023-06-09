---
title: PHP-Generated Apache-Style Access Logs
date: 2009-05-14 13:33:22
---



__A few months ago__ I wrote about a way [I use PHP to generate apache-style access.log files](https://swharden.com/blog/2009-05-14-php-generated-accesslog-is-a-success/) since my web host blocks access to them.  Since then I've forgotten it was even running!  I now have some pretty cool-looking graphs generated by [Python](http://www.python.org) and [Matplotlib](http://matplotlib.sourceforge.net/).  For details (and the messy script) check the original posting.

![](https://swharden.com/static/2009/05/14/graph_time.png)

__This image represents__ the number of requests (php pages) made per hour since I implemented the script.  It might be a good idea to perform some [linear data smoothing techniques](https://swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/) (which I love writing about), but for now I'll leave it as it is so it most accurately reflects the actual data.

This code has been updated:
[2009-08-04-generate-apache-style-http-access-logs-via-sql-and-php](https://swharden.com/blog/2009-08-04-generate-apache-style-http-access-logs-via-sql-and-php/)
