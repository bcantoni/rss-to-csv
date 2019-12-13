<?php
/* rss2csv.inc - utilities for RSS->CSV conversion script

   Created by Brian Cantoni <brian AT cantoni.org>
   scooterlabs.com/hacks/rss2csv.php
*/

// max cell size for benefit of MS Excel
// ref: https://support.office.com/en-us/article/Excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3
define ('MAX_CELL_SIZE', 32000);

// given RSS feed URL, fetch it using YQL, then output as CSV
function fetchRSSandOutputCSV ($url) {
    if(@simplexml_load_file($url)) {
        $feeds = simplexml_load_file($url);
    } else {
        print "No data returned for RSS feed\n";
        return;
    }

    /*
    foreach ($feeds->channel->item as $item) {
        foreach ($item as $key => $value) {
            print "$key => $value\n";
        }
        print "-----------------\n";
    }
    */

    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="export.csv"');
    header('Pragma: no-cache');
    header('Expires: 0');

    // save values from first items (to use as column headers)
    $headers = array();
    foreach ($feeds->channel->item[0] as $k => $v) {
        // todo: properly handle >1 category problem
        if (!preg_match('/category/', $k)) {
            $headers[] = $k;
        }
    }

    // open stdout and write headers, then data, as CSV
    $fp = fopen('php://output', 'w');
    if ($fp) {
        fputcsv($fp, $headers);
        foreach ($feeds->channel->item as $item) {
            $values = Array();
            foreach ($item as $k => $v) {
                // todo: properly handle >1 category problem
                if (!preg_match('/category/', $k)) {
                    $values[] = substr($v, 0, MAX_CELL_SIZE);
                }
            }
            fputcsv($fp, $values);
        }
    }

    return;
}

