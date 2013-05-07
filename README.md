# RSS to CSV Converter

This is a simple script to convert RSS feeds into CSV format,
suitable for importing into Excel.

See this original blog post for more background and instructions:
http://www.cantoni.org/2009/12/22/rss-to-csv-converter

# Usage

1. Browse to http://scooterlabs.com/hacks/rss2csv.php
2. Enter the URL of an RSS feed and submit
2. Save the resulting file (named `export.csv` by default)

# Installation

To run your own copy of this script:

1. Download and locate rss2csv.php and rss2csv.inc in a suitable location
2. Create a subdirectory `logs` that is writeable by the webserver process (e.g., `mkdir logs; chmod 777 logs`)
3. Browse to rss2csv.php and give it a try!

# Limitations

1. The script can handle UTF-8 in the source file, but Excel cannot (CSV files don't technically support Unicode)
2. Only RSS feeds are supported; it won't work with an Atom feed

# License

Licensed under the MIT License.

