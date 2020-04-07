#!/bin/bash

while read row; do
    name=`echo ${row} | cut -d , -f 1`
    prec_no=`echo ${row} | cut -d , -f 2`
    block_no=`echo ${row} | cut -d , -f 3`
    date=`echo ${row} | cut -d , -f 4`
    days=`echo ${row} | cut -d , -f 5`
    
    python3 ground_scraping.py ${name} ${prec_no} ${block_no} ${date} ${days}

done < ./csv/ground_scraping.csv
