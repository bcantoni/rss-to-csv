# RSS to CSV Converter

This is a simple script to convert RSS feeds into CSV format, suitable
for importing into Excel.

**Update Feb 2020:** I've updated the core process part of this script
from PHP running on my shared web host to Python running in the cloud
via Azure Functions.

See this original blog post for the historical background:
<http://www.cantoni.org/2009/12/22/rss-to-csv-converter>

## Usage

1. Browse to <http://scooterlabs.com/hacks/rss2csv.php>
2. Enter the URL of an RSS feed and submit
3. The results will automatically download to a file named `export.csv`

## Limitations

1. The script can handle UTF-8 in the source file, but Excel cannot
   (CSV files don't technically support Unicode)
2. Data fields are limited (truncated) to 32,000 characters to avoid
   hitting Excel's cell size limitation

## License

Licensed under the MIT License.
