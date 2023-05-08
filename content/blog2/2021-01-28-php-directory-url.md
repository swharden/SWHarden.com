---
Title: Get URL of a Directory with PHP
Description: This page describes how to determine the URL for a given folder using PHP
Date: 2021-01-28 18:15:00
tags: ["php"]
---



**My website went down for a few hours today** when my hosting company unexpectedly changed Apache's root http folder to a new one containing a symbolic link. This change broke some of my PHP scripts because `__DIR__` suddenly had a base path that was different than `DOCUMENT_ROOT`, and the `str_replace` method I was using to determine the directory URL assumed they would always be the same. If you Google "how to get the URL of the current directory with PHP", you'll probably find recommendations to use code like this:

```php
// WARNING: DON'T USE THIS CODE!
$folderUrl = 'http://'.$_SERVER['HTTP_HOST'].str_replace($_SERVER['DOCUMENT_ROOT'], '', __DIR__); 
```

Let's look at what these variables resolve to on my site:

Variable | Value
---|---
`$_SERVER['HTTP_HOST']`|`swharden.com`
`__DIR__`|`/home/customer/www/swharden.com/public_html/tmp/test`
`realpath(__DIR__)`|`/home/customer/www/swharden.com/public_html/tmp/test`
`$_SERVER['DOCUMENT_ROOT']`|`/home/u123-bsasdfas7hj/www/swharden.com/public_html`
`realpath($_SERVER['DOCUMENT_ROOT'])`|`/home/customer/www/swharden.com/public_html`

Comparing `__DIR__` with `DOCUMENT_ROOT`, notice that without real path resolution the base paths are different! This caused the string replace method to abruptly fail on my website, taking several sites down for a few hours. I'll accept it as a rookie mistake on my part, and I'm sharing what I learned here in case it helps others in the future.

**The Solution is to ensure all paths** are converted to canonicalized absolute paths using `realpath()`. This will protect you from unexpected symbolic links. Notice this code also adds the appropriate HTTP or HTTPS prefix.

```php
// This script displays the URL of the current folder
$realDocRoot = realpath($_SERVER['DOCUMENT_ROOT']);
$realDirPath = realpath(__DIR__);
$suffix = str_replace($realDocRoot, '', $realDirPath);
$prefix = isset($_SERVER['HTTPS']) ? 'https://' : 'http://';
$folderUrl = $prefix . $_SERVER['HTTP_HOST'] . $suffix;
echo $folderUrl;
```