<?php
/* rss2csv.php - convert RSS feed to CSV format

   Created by Brian Cantoni <brian AT cantoni.org>
   http://scooterlabs.com/hacks/rss2csv.php
*/
if ($_SERVER['REQUEST_METHOD'] != 'GET') {
    header ('Allow: GET');
    header ('HTTP/1.0 405 Method Not Allowed');
    exit();
}
?>
<!DOCTYPE HTML>
<html lang="en">
<head>
    <title>RSS to CSV Converter - Scooter Labs</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name=viewport content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?2.8.0r4/build/reset-fonts-grids/reset-fonts-grids.css&amp;2.8.0r4/build/base/base-min.css">
    <style>
        h1 { font-size: 2em; margin: 0.5em 0.5em 0.5em 0; }
        body { overflow: auto; }
    </style>
</head>
<body>
<div id="doc3" class="yui-t7">
<div id="hd"><h1>RSS to CSV Converter</h1></div>
<div id="bd">
<div class="yui-g">
<p>This is a simple script to convert RSS feeds into CSV format, suitable for importing into Excel.</p>
<form id="search-form" action="https://gatos-jabra-buster.azurewebsites.net/api/RssToCsv" method="get">
  <fieldset>
    <label for="query">Enter URL of RSS feed:</label>
    <input type="text" id="query" name="url" size="50" />
    <button type="submit">Submit</button>
  </fieldset>
</form>

<p>Notes:</p>
<ul>
<li><strong>Feb 2020 update:</strong> To fix some issues with my old host, I've changed the backend from PHP to Python which is now running on Azure Functions. Everything should still work as before.</li>
<li>Excel does not properly handle UTF-8 CSV files, so you may see some corruption if the RSS feed contains international characters</li>
<li>Fields output are: title, link, description, pubDate, guid</li>
<li>Only RSS feeds are supported - not Atom; if interested in Atom support, let me know</li>
<li>Original blog post: <a href="http://www.cantoni.org/2009/12/22/rss-to-csv-converter" title="RSS to CSV converter">RSS to CSV Converter</a></li>
<li>Source code available on Github: <a href="https://github.com/bcantoni/rss-to-csv">https://github.com/bcantoni/rss-to-csv</a></li>
</ul>

<div id="ft"><hr><p>Feedback/suggestions to Brian Cantoni (<span class="hideEmail">brian AT cantoni.org</span>).</p></div>

</div>
</div>
</div>
<script src="/javascript/scooterlabs-min.js"></script>
</body>
</html>
