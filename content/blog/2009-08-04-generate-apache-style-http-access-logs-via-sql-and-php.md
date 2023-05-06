---
title: Generate Apache-Style HTTP Access Logs via SQL and PHP
date: 2009-08-04 00:11:18
tags: ["old"]
---

# Generate Apache-Style HTTP Access Logs via SQL and PHP

__Does your web hosting company block access to access.log, the text file containing raw website log files?__  If so, you're like me, and it sucks.  There's a plethora of gorgeous and extremely insightful website traffic analyzers, but all of them require access to raw HTTP access logs.  Today I propose a semi-efficient way to generate such logs utilizing PHP to determine page load data (time, user IP, requested page, referring page, user client, etc) and SQL to save such data for easy retrieval later.  Note that this method is a HUGE improvement of my previous project which [used PHP scripts to store HTTP access logs as flat files](http://www.swharden.com/blog/2009-01-22-using-php-to-create-apache-style-accesslog/).  Although it worked in theory, in all practicality the process of opening, writing to, and closing a text file (which grew a few MB a week) was too cumbersome for my server to comfortable handle.  The method described on this page utilizes [SQL](http://en.wikipedia.org/wiki/SQL), a database engine well-suited to meet these exact demands.  When we're done, you'll be able to use a web interface to view your access log (pictured, converting long, complicated search queries to web search and image search strings automatically), or have the option to export it directly to an access.log text file in a standard Apache-style format.

<div class="text-center img-border">

[![](sql_php_http_log_viewer_thumb.jpg)](sql_php_http_log_viewer.jpg)

</div>

__First, make sure your database is structured appropriately.__  This page is written for those with a working knowledge of PHP and SQL, but if you're new to the field I encourage you to learn!  [W3Schools.com](http://www.w3schools.com/) is an awesome resource to rapidly learn new languages.  Also, when starting-out with SQL (like me), [phpMyAdmin](http://www.phpmyadmin.net/home_page/index.php) is a awesome. The code, as it's currently written (below) is designed to store data in the "nibjb" database under the "logs" table.  Briefly, it uses PHP to determine user data (time, ip, requested page, etc.) and injects this information into the SQL database.  In fact, it's doing it to you right now!  Don't believe me?  View the source of this web page and scroll to the bottom.  BAM!  There you are.

```php
// logme.php
<?php

if ( !isset($wp_did_header) ) {
    $wp_did_header = true;
    require_once( '/home/content/n/i/b/nibjb/html/blog/wp-load.php' );
    //wp();
    //require_once( '/home/content/n/i/b/nibjb/html/blog/wp-includes/template-loader.php' );
}

function logwriter_handlevar($varname,$defaultvalue){
    $tempvar = getenv($varname);
    if(!empty($tempvar)) {
        return $tempvar;
    } else {
        return $defaultvalue;
    }
}

if (!empty($REMOTE_HOST)) {
$logwriter_remote_vistor = $REMOTE_HOST;
}else{
$logwriter_remote_vistor = logwriter_handlevar("REMOTE_ADDR","-");
}

$logwriter_remote_ident = logwriter_handlevar("REMOTE_IDENT","-");
$logwriter_remote_user = logwriter_handlevar("REMOTE_USER","-");
$logwriter_date = date("d/M/Y:H:i:s");
$logwriter_request_method = logwriter_handlevar("REQUEST_METHOD","GET");
$logwriter_request_uri = logwriter_handlevar("REQUEST_URI","");
$logwriter_server_protocol = logwriter_handlevar("SERVER_PROTOCOL","HTTP/1.1");
$logwriter_http_referer = logwriter_handlevar("HTTP_REFERER","-");
$logwriter_http_user_agent = logwriter_handlevar("HTTP_USER_AGENT","");
$logwriter_logstring = "$logwriter_remote_vistor $logwriter_remote_ident $logwriter_remote_user [$logwriter_date $logwriter_timezone] "$logwriter_request_method $logwriter_request_uri $logwriter_server_protocol" 200 - "$logwriter_http_referer" "$logwriter_http_user_agent"n";
?>

<?php
$username="YOUR_USERNAME";
$password="YOUR_PASSWORD";
$database="nibjb";
mysql_connect('mysql157.secureserver.net',$username,$password);
//mysql_connect(localhost,$username,$password);

$query = "INSERT INTO logs VALUES ('','$logwriter_date','$logwriter_remote_vistor','$logwriter_request_method','$logwriter_request_uri','$logwriter_server_protocol','$logwriter_http_referer','$logwriter_http_user_agent')";
mysql_query($query);
mysql_close();
?>

<!--
LOG DETAILS:
time: <?php echo($logwriter_date); ?>
vistor: <?php echo($logwriter_remote_vistor); ?>
method: <?php echo($logwriter_request_method); ?>
request: <?php echo($logwriter_request_uri); ?>
protocol: <?php echo($logwriter_server_protocol); ?>
referrer: <?php echo($logwriter_http_referer); ?>
agent: <?php echo($logwriter_http_user_agent); ?>
HTML LOG LINE:
<?php echo($logwriter_logstring); ?>
-->
```

__All right, that was easy.__ Every time we load logme.php, it adds the data to the SQL database. To add data every time you go to a particular web page, you could use a PHP include() statement in each webpage, or you could take advantage of the PHP's auto_append_file feature!  Simply insert the following line into your php.ini file if you have access to yours:

```
auto_append_file = "/path/to/html/logme.php"
```

__How do we access this data once it's been loaded into the database?__ There are many different ways, but I've chosen to get a little creative with a sleek, yet minimalistic web-based fronted.  It basically just shows the last [x] number of entries in the access log.  You can adjust the number of entries displayed by slapping on some arguments to the URL, transforming viewLast.php into viewLast.php?limit=123 or something (see the screenshot above).  I won't discuss the details of this script.  It's self-explanatory.

```php
// viewLast.php
<html>
<head>
<style type="text/css">
td {
font-family: verdana, arial;
font-size:10px;
}
</style>
</head>
<body>
<?php

$limit = (int)$_GET['limit'];
if ($limit===0) {$limit=25;}

$username="YOUR_USERNAME";
$password="YOUR_PASSWORD";
$database="nibjb";
mysql_connect('mysql157.secureserver.net',$username,$password);
mysql_select_db($database) or die( "Unable to select database");
$query="
SELECT * FROM logs WHERE
request NOT LIKE "%testlog.php%"
AND request NOT LIKE  "%/logs/%"
AND request NOT LIKE "%/wp-admin/%"
ORDER BY ID DESC LIMIT 0,$limit
";
//$query="SELECT * FROM logs WHERE referrer LIKE "%&q=%" or referrer LIKE "%&prev=%" ";
$result=mysql_query($query);
$num=mysql_numrows($result);
mysql_close();
?>

<b><?php echo($query); ?></b>
<table border="1">
<tr>
<td>id</td>
<td>time</td>
<td>visitor</td>
<td>request</td>
<td>referrer</td>
</tr>

<?php
$i=1;
while ($i<$num) {
$id=mysql_result($result,$i,"id");
$time=mysql_result($result,$i,"time");
$visitor=mysql_result($result,$i,"visitor");
$method=mysql_result($result,$i,"method");
$request=mysql_result($result,$i,"request");
$protocol=mysql_result($result,$i,"protocol");
$referrer=mysql_result($result,$i,"referrer");
$referrer2=str_replace("&", "& ", $referrer);
$agent=mysql_result($result,$i,"agent");
$searchWords="";
$searchEngine="";
if (strpos($referrer, "q=")>0 and strpos($referrer, "google")>0) {$searchEngine="Google Web Search: ";}
if (strpos($referrer, "prev=/images")>0 and strpos($referrer, "google")>0) {$searchEngine="Google Image Search: ";}

// SEARCH EXTRACTION //
$j=0;
$rTemp=str_replace("prev=/images%3Fq%3D", "q=", $referrer);
$rTemp=str_replace("?q=","&q=", $rTemp);
$rTemp=str_replace("%2B"," ", $rTemp);
$rTemp=str_replace("%26"," ", $rTemp);
$rTemp=str_replace("%3D"," ", $rTemp);
$rTemp=str_replace("+"," ", $rTemp);
$wvars=split("&",$rTemp);
while ($j<count($wvars)){
    if (substr($wvars[$j],0,2) === "q=") {
        $searchWords = $searchWords . $wvars[$j] . " ";
        }
    $j++;
}

$searchWords=substr($searchWords,strpos($searchWords, "q=")+2);
if (strlen($searchWords)<3) {$searchWords=$referrer;}

echo "
<tr>
<td>$id</td>
<td>$time</td>
<td>$visitor</td>
<td><a href='$request'>$request</a></td>
<td>$searchEngine <a href='$referrer'>$searchWords</a></td>
</td>
";
$i++;
}
?>
</table>
</body>
</html>
```

__And you're done!__  This example is a simplified, bare bones example.  You can take this a long way if you'd like.  My goal is lite & flexible.  A quick query from [Python](http://www.python.org) and [Matplotlib](matplotlib.sourceforge.net/) (for example) yields gorgeous visual representations of otherwise-convoluted data!
<a href="http://www.SWHarden.com/blog/images/graph_time.png" onclick="javascript:urchinTracker ('/outbound/article/www.SWHarden.com');">

<div class="text-center">

[![](graph_time_thumb.jpg)](graph_time.png)

</div>

__If you have any questions, or end-up developing something awesome with this code, shoot me an email!__  It's not luxurious, but this code works for me, and I share it with the best of intentions.